import logging
import os

import mysql.connector

from src.config.config_loader import load_config, load_local_config, load_connection_config
from src.database.sqlite_connection import get_sqlite_connection

TABLAS_PERMITIDAS = {"TblTinka", "TblKabala"}
CONNECTION_CONFIG = load_connection_config()
RAILWAY_CONFIG = load_config()
LOCAL_CONFIG = load_local_config()

logger = logging.getLogger("migrate")


# =========================
# VALIDACIÓN
# =========================
def validar_tabla(table_name):
    if table_name not in TABLAS_PERMITIDAS:
        raise ValueError(f"❌ Tabla no permitida: {table_name}")


# =========================
# CONEXIONES
# =========================
def get_railway_connection():
    try:
        conn = mysql.connector.connect(
            host=RAILWAY_CONFIG["host"],
            user=RAILWAY_CONFIG["user"],
            password=RAILWAY_CONFIG["password"],
            database=RAILWAY_CONFIG["database"],
            port=int(RAILWAY_CONFIG["port"]),
            connection_timeout=CONNECTION_CONFIG["timeout"]
        )
        logger.info("Conexión RAILWAY establecida")
        return conn
    except mysql.connector.Error as e:
        logger.warning(f"RAILWAY no disponible: {e}")
        return None


def get_local_connection():
    try:
        conn = mysql.connector.connect(
            host=LOCAL_CONFIG["host"],
            user=LOCAL_CONFIG["user"],
            password=LOCAL_CONFIG["password"],
            database=LOCAL_CONFIG["database"],
            connection_timeout=CONNECTION_CONFIG["timeout"]
        )
        logger.info("Conexión LOCAL establecida")
        return conn
    except mysql.connector.Error as e:
        logger.warning(f"LOCAL no disponible: {e}")
        return None


# =========================
# OBTENER TODOS LOS REGISTROS
# =========================
def fetch_all_records(conn, table, db_name):
    validar_tabla(table)
    cursor = conn.cursor()
    try:
        cursor.execute(
            f"SELECT fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei FROM {table}"
        )
        rows = cursor.fetchall()
        logger.info(f"[{db_name}] {len(rows)} registros obtenidos de {table}")
        return rows
    except Exception as e:
        logger.error(f"[{db_name}] Error al obtener datos de {table}: {e}")
        return []
    finally:
        cursor.close()


# =========================
# SINCRONIZAR RAILWAY → LOCAL
# =========================
def sync_table_to_local(table_name, railway_conn, local_conn):
    validar_tabla(table_name)
    logger.info(f"[Sync] {table_name} — Railway → LOCAL")

    railway_data = set(fetch_all_records(railway_conn, table_name, "RAILWAY"))
    local_data = set(fetch_all_records(local_conn, table_name, "LOCAL"))

    missing = railway_data - local_data

    logger.info(f"[Sync] {table_name} — Railway: {len(railway_data)}, LOCAL: {len(local_data)}, faltantes: {len(missing)}")

    if not missing:
        logger.info(f"[Sync] {table_name} — ✅ Ya sincronizados")
        return

    cursor = local_conn.cursor()
    insert_sql = f"""
        INSERT IGNORE INTO {table_name}
        (fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        cursor.executemany(insert_sql, list(missing))
        local_conn.commit()
        logger.info(f"[Sync] {table_name} — ✅ Insertados en LOCAL: {cursor.rowcount}")
    except Exception as e:
        local_conn.rollback()
        logger.error(f"[Sync] {table_name} — Error al insertar en LOCAL: {e}")
    finally:
        cursor.close()


# =========================
# POBLAR SQLITE
# =========================
def populate_sqlite(table, data, source_name):
    validar_tabla(table)

    if not data:
        logger.warning(f"[SQLite] Sin datos para poblar {table} desde {source_name}")
        return

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"DELETE FROM {table}")
        logger.info(f"[SQLite] {table} limpiada ({cursor.rowcount} eliminados)")

        cursor.executemany(
            f"""
            INSERT OR IGNORE INTO {table}
            (fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei)
            VALUES (?,?,?,?,?,?,?)
            """,
            data
        )

        conn.commit()
        logger.info(f"[SQLite] {table} poblada desde {source_name} → {cursor.rowcount} insertados")

    except Exception as e:
        conn.rollback()
        logger.error(f"[SQLite] Error al poblar {table}: {e}")

    finally:
        cursor.close()
        conn.close()


# =========================
# FLUJO SQLITE: LOCAL → RAILWAY → sin conexión (no aplica aquí)
# =========================
def setup_sqlite_for_table(table_name, local_conn, railway_conn):
    validar_tabla(table_name)
    logger.info(f"[SQLite Setup] {table_name} — iniciando")

    # LOCAL primero
    if local_conn:
        data = fetch_all_records(local_conn, table_name, "LOCAL")
        if data:
            populate_sqlite(table_name, data, "LOCAL")
            return
        logger.warning(f"[SQLite Setup] {table_name} — LOCAL sin datos, intentando RAILWAY")

    # Fallback RAILWAY
    if railway_conn:
        data = fetch_all_records(railway_conn, table_name, "RAILWAY")
        if data:
            populate_sqlite(table_name, data, "RAILWAY")
            return
        logger.warning(f"[SQLite Setup] {table_name} — RAILWAY sin datos")

    logger.error(f"[SQLite Setup] {table_name} — ❌ Sin datos disponibles para poblar SQLite")


# =========================
# MAIN
# =========================
def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

    log_dir = os.path.join(base_dir, "logs")
    os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        handlers=[
            logging.StreamHandler(),
            logging.FileHandler(os.path.join(log_dir, "migrate.log"), encoding="utf-8")
        ]
    )

    tables = ["TblTinka", "TblKabala"]

    railway_conn = get_railway_connection()
    local_conn = get_local_connection()

    if not railway_conn and not local_conn:
        logger.error("Sin conexión a RAILWAY ni a LOCAL — operación cancelada")
        return

    try:
        # PASO 1 — Sincronizar Railway → LOCAL
        if railway_conn and local_conn:
            logger.info("=" * 60)
            logger.info("PASO 1 — Sincronizando Railway → LOCAL")
            logger.info("=" * 60)
            for table in tables:
                sync_table_to_local(table, railway_conn, local_conn)
        elif not local_conn:
            logger.warning("LOCAL no disponible — sincronización omitida")
        elif not railway_conn:
            logger.warning("RAILWAY no disponible — sincronización omitida")

        # PASO 2 — Poblar SQLite
        logger.info("=" * 60)
        logger.info("PASO 2 — Poblando SQLite")
        logger.info("=" * 60)
        for table in tables:
            setup_sqlite_for_table(table, local_conn, railway_conn)

    finally:
        if local_conn:
            local_conn.close()
        if railway_conn:
            railway_conn.close()


if __name__ == "__main__":
    main()