import logging
import os
from datetime import datetime

import mysql.connector

from src.config.config_loader import load_config, load_local_config, load_connection_config
from src.config.game_config import TINKA_CONFIG, KABALA_CONFIG

# =========================
# CONFIG
# =========================
FILE_MAP = {
    "Resul_Tnk.txt": TINKA_CONFIG,
    "Resul_Kbl.txt": KABALA_CONFIG
}

TABLAS_PERMITIDAS = {"TblTinka", "TblKabala"}
CONNECTION_CONFIG = load_connection_config()
RAILWAY_CONFIG = load_config()
LOCAL_CONFIG = load_local_config()

logger = logging.getLogger("load_txt")


# =========================
# VALIDACIÓN DE TABLA
# =========================
def validar_tabla(table_name):
    if table_name not in TABLAS_PERMITIDAS:
        raise ValueError(f"❌ Tabla no permitida: {table_name}")


# =========================
# CONEXIONES MySQL
# =========================
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


# =========================
# LEER Y LIMPIAR TXT
# =========================
def read_and_clean(file_path, game_config):
    registros = []
    errores = []

    min_num = game_config["min_number"]
    max_num = game_config["max_number"]
    numeros_esperados = game_config["numbers_count"]

    with open(file_path, "r", encoding="utf-8") as file:
        for num_linea, line in enumerate(file, start=1):
            line = line.strip()
            if not line:
                continue

            parts = line.split()

            # Validar que haya al menos un elemento antes de acceder a parts[0]
            if not parts:
                errores.append(f"  Línea {num_linea}: línea vacía o sin contenido válido")
                continue

            # Validar fecha
            try:
                fecha = datetime.strptime(parts[0], "%d/%m/%Y").date()
            except ValueError:
                errores.append(f"  Línea {num_linea}: fecha inválida → '{parts[0]}'")
                continue

            # Validar cantidad de números
            nums_raw = parts[1:]
            if len(nums_raw) != numeros_esperados:
                errores.append(
                    f"  Línea {num_linea}: se esperaban {numeros_esperados} números, "
                    f"se encontraron {len(nums_raw)} → {nums_raw}"
                )
                continue

            # Validar que sean numéricos
            try:
                numeros = sorted([int(n) for n in nums_raw])
            except ValueError:
                errores.append(f"  Línea {num_linea}: valores no numéricos → {nums_raw}")
                continue

            # Validar duplicados
            if len(set(numeros)) != numeros_esperados:
                errores.append(f"  Línea {num_linea}: números duplicados → {numeros}")
                continue

            # Validar rango
            fuera_de_rango = [n for n in numeros if n < min_num or n > max_num]
            if fuera_de_rango:
                errores.append(
                    f"  Línea {num_linea}: números fuera de rango [{min_num}-{max_num}] "
                    f"→ {fuera_de_rango}"
                )
                continue

            registros.append((fecha, *numeros))

    if errores:
        logger.warning(f"Líneas ignoradas en {os.path.basename(file_path)}:")
        for e in errores:
            logger.warning(e)

    registros.sort(key=lambda x: x[0])
    logger.info(f"TXT leído: {len(registros)} registros válidos en {os.path.basename(file_path)}")
    return registros


# =========================
# INSERT MySQL — RÁPIDO CON executemany
# =========================
def process_records(conn, table, data, db_name):
    validar_tabla(table)
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT IGNORE INTO {table}
        (fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    try:
        cursor.executemany(insert_sql, data)
        conn.commit()

        insertados = cursor.rowcount
        ignorados = len(data) - insertados

        logger.info(f"[{db_name}] Resumen → insertados: {insertados}, ignorados: {ignorados}")

    except Exception as e:
        conn.rollback()
        logger.error(f"[{db_name}] Error, rollback ejecutado: {e}")

    finally:
        cursor.close()


# =========================
# PROCESAR ARCHIVO
# =========================
def process_file(file_path):
    file_name = os.path.basename(file_path)

    if file_name not in FILE_MAP:
        logger.error(f"Archivo no reconocido: {file_name}")
        return

    game_config = FILE_MAP[file_name]
    table = game_config["table"]

    logger.info(f"{'=' * 60}")
    logger.info(f"Procesando: {file_name} → {table}")
    logger.info(f"{'=' * 60}")

    # PASO 1 — Leer y limpiar TXT
    data = read_and_clean(file_path, game_config)

    if not data:
        logger.warning(f"Sin datos válidos en {file_name}")
        return

    # PASO 2 — Cargar a MySQL (LOCAL + RAILWAY)
    local_conn = get_local_connection()
    railway_conn = get_railway_connection()

    if not local_conn and not railway_conn:
        logger.error("Sin conexión a LOCAL ni a RAILWAY — carga MySQL omitida")
    else:
        if local_conn:
            logger.info("--- Cargando a LOCAL ---")
            process_records(local_conn, table, data, "LOCAL")
            local_conn.close()
        else:
            logger.warning("LOCAL omitido")

        if railway_conn:
            logger.info("--- Cargando a RAILWAY ---")
            process_records(railway_conn, table, data, "RAILWAY")
            railway_conn.close()
        else:
            logger.warning("RAILWAY omitido")


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
            logging.FileHandler(os.path.join(log_dir, "load_txt.log"), encoding="utf-8")
        ]
    )

    data_dir = os.path.join(base_dir, "data")

    files = [
        os.path.join(data_dir, "Resul_Tnk.txt"),
        os.path.join(data_dir, "Resul_Kbl.txt")
    ]

    for file in files:
        if not os.path.exists(file):
            logger.error(f"Archivo no encontrado: {file}")
            continue

        process_file(file)


if __name__ == "__main__":
    main()