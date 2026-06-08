import logging

import mysql.connector

from src.config.config_loader import load_config, load_local_config, load_connection_config
from src.utils.logger import APP_LOGGER_NAME

logger = logging.getLogger(APP_LOGGER_NAME)

DB_CONFIG = load_config()
LOCAL_CONFIG = load_local_config()
CONNECTION_CONFIG = load_connection_config()


def get_connection(source):
    # Intentar Railway primero
    try:
        conn = mysql.connector.connect(
            host=DB_CONFIG["host"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
            database=DB_CONFIG["database"],
            port=int(DB_CONFIG["port"]),
            connection_timeout=CONNECTION_CONFIG["timeout"]
        )
        logger.info(f"Conexión RAILWAY OK - {source} - id: {id(conn)}")
        return conn

    except mysql.connector.Error as err:
        logger.error(f"RAILWAY no disponible ({source}): {err}")

    # Fallback a LOCAL
    try:
        conn = mysql.connector.connect(
            host=LOCAL_CONFIG["host"],
            user=LOCAL_CONFIG["user"],
            password=LOCAL_CONFIG["password"],
            database=LOCAL_CONFIG["database"],
            connection_timeout=CONNECTION_CONFIG["timeout"]
        )
        logger.warning(f"Usando LOCAL como fallback - {source} - id: {id(conn)}")
        return conn

    except mysql.connector.Error as err:
        logger.error(f"LOCAL tampoco disponible ({source}): {err}")
        return None