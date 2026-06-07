import logging

from src.database.sqlite_connection import get_sqlite_connection
from src.utils.logger import APP_LOGGER_NAME

logger = logging.getLogger(APP_LOGGER_NAME)

TABLAS_PERMITIDAS = {"TblTinka", "TblKabala"}


def validar_tabla(table_name):
    if table_name not in TABLAS_PERMITIDAS:
        raise ValueError(f"❌ Tabla no permitida: {table_name}")


def get_winning_combinations(table_name):
    """
    Retorna dict { tuple(nums): fecha } con todas las combinaciones ganadoras.
    Retorna {} si falla o no hay datos.
    """
    validar_tabla(table_name)

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"SELECT fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei FROM {table_name}"
        )

        result = {
            tuple(sorted(row[1:])): row[0]
            for row in cursor.fetchall()
        }

        logger.info(f"[SQLite] {table_name} — {len(result)} combinaciones ganadoras cargadas")
        return result

    except Exception as e:
        logger.error(f"[SQLite] Error al obtener combinaciones de {table_name}: {e}")
        return {}

    finally:
        cursor.close()
        conn.close()


def get_last_draws(table_name, limit):
    """
    Retorna lista de tuplas con los últimos `limit` sorteos ordenados por fecha DESC.
    Retorna [] si falla o no hay datos.
    """
    validar_tabla(table_name)

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(
            f"""
            SELECT NumUno, NumDos, NumTre, NumCua, NumCin, NumSei
            FROM {table_name}
            ORDER BY fecha DESC
            LIMIT ?
            """,
            (limit,)
        )

        result = [tuple(row) for row in cursor.fetchall()]

        logger.info(f"[SQLite] {table_name} — {len(result)} últimos sorteos cargados")
        return result

    except Exception as e:
        logger.error(f"[SQLite] Error al obtener últimos sorteos de {table_name}: {e}")
        return []

    finally:
        cursor.close()
        conn.close()