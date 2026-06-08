import logging

from src.database.connection import get_connection
from src.utils.logger import APP_LOGGER_NAME

logger = logging.getLogger(APP_LOGGER_NAME)

TABLAS_PERMITIDAS = {"TblTinka", "TblKabala"}


def validar_tabla(table_name):
    if table_name not in TABLAS_PERMITIDAS:
        raise ValueError(f"❌ Tabla no permitida: {table_name}")


def get_winning_combinations(table_name):
    validar_tabla(table_name)

    conn = get_connection("get_winning_combinations")
    if not conn:
        return {}

    cursor = conn.cursor()

    try:
        query = f"""
            SELECT fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei 
            FROM {table_name}
        """

        cursor.execute(query)

        result = {
            tuple(sorted(row[1:])): row[0]
            for row in cursor.fetchall()
        }

        return result

    except Exception as e:
        logger.error(f"Error al obtener combinaciones de {table_name}: {e}")
        return {}

    finally:
        cursor.close()
        conn.close()


def get_last_draws(table_name, limit):
    validar_tabla(table_name)

    conn = get_connection("get_last_draws")
    if not conn:
        return []

    cursor = conn.cursor()

    try:
        query = f"""
            SELECT NumUno, NumDos, NumTre, NumCua, NumCin, NumSei 
            FROM {table_name}
            ORDER BY fecha DESC
            LIMIT {limit}
        """

        cursor.execute(query)

        result = [tuple(row) for row in cursor.fetchall()]

        return result

    except Exception as e:
        logger.error(f"Error al obtener últimos sorteos de {table_name}: {e}")
        return []

    finally:
        cursor.close()
        conn.close()