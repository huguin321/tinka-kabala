import logging
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
LOG_DIR = os.path.join(BASE_DIR, "logs")

APP_LOGGER_NAME = "tinka_app"


def setup_logger(game_name):
    """
    Configura el logger de la aplicación de forma aislada,
    sin afectar librerías de terceros.
    """
    os.makedirs(LOG_DIR, exist_ok=True)

    log_file = os.path.join(LOG_DIR, f"{game_name.lower()}.log")

    logger = logging.getLogger(APP_LOGGER_NAME)
    logger.setLevel(logging.INFO)

    # Limpiar handlers previos
    logger.handlers.clear()

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # Handler archivo
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setFormatter(formatter)

    # Handler consola
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    # Evitar propagación al root logger
    logger.propagate = False

    return logger