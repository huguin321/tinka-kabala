import logging

import mysql.connector

from src.config.config_loader import load_config

logger = logging.getLogger(__name__)


def get_connection(source="unknown"):
    config = load_config()

    try:
        conn = mysql.connector.connect(
            host=config["host"],
            user=config["user"],
            password=config["password"],
            database=config["database"],
            port=int(config["port"])
        )

        logger.info(f"Conexión BD OK - {source} - id: {id(conn)}")

        return conn

    except mysql.connector.Error as err:
        logger.error(f"Error BD: {err}")
        return None
