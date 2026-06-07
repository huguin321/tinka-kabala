import configparser
import logging
import os
import sys

REQUIRED_KEYS = {
    "mysql": ["host", "usuario", "contrasena", "base_de_datos", "port"],
    "mysql_local": ["host", "usuario", "contrasena", "base_de_datos"],
    "conexion": ["timeout"]
}

# Logger de emergencia aislado del root logger
emergency_logger = logging.getLogger("config_emergency")
emergency_logger.setLevel(logging.ERROR)
emergency_logger.propagate = False

if not emergency_logger.handlers:
    _handler = logging.StreamHandler()
    _handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
    emergency_logger.addHandler(_handler)


def _get_config_path():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_dir, "config.ini")

    if not os.path.exists(config_path):
        msg = (
            "\n"
            "╔══════════════════════════════════════════════╗\n"
            "║         ERROR DE CONFIGURACIÓN               ║\n"
            "╠══════════════════════════════════════════════╣\n"
            "║ No se encontró: config.ini                   ║\n"
            "║ Ruta esperada:                               ║\n"
            f"║ {config_path[:44]:<44} ║\n"
            "╠══════════════════════════════════════════════╣\n"
            "║ Crea el archivo con secciones:               ║\n"
            "║   [mysql], [mysql_local] y [conexion]        ║\n"
            "╚══════════════════════════════════════════════╝"
        )
        emergency_logger.error(msg)
        sys.exit(1)

    return config_path


def _validate_keys(config):
    missing = []

    for section, keys in REQUIRED_KEYS.items():
        if section not in config:
            missing.append(f"  Sección [{section}] no encontrada")
            continue
        for key in keys:
            if key not in config[section]:
                missing.append(f"  [{section}] → clave '{key}' no encontrada")

    if missing:
        msg = (
            "\n"
            "╔══════════════════════════════════════════════╗\n"
            "║      ERROR DE CONFIGURACIÓN INCOMPLETA       ║\n"
            "╠══════════════════════════════════════════════╣\n"
            "║ Faltan los siguientes valores en config.ini: ║\n"
        )
        for m in missing:
            msg += f"║ {m:<44} ║\n"
        msg += "╚══════════════════════════════════════════════╝"

        emergency_logger.error(msg)
        sys.exit(1)


def _get_config():
    config = configparser.ConfigParser()
    config.read(_get_config_path())
    _validate_keys(config)
    return config


def load_config():
    config = _get_config()

    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["usuario"],
        "password": config["mysql"]["contrasena"],
        "database": config["mysql"]["base_de_datos"],
        "port": config["mysql"].get("port", 3306)
    }


def load_local_config():
    config = _get_config()

    return {
        "host": config["mysql_local"]["host"],
        "user": config["mysql_local"]["usuario"],
        "password": config["mysql_local"]["contrasena"],
        "database": config["mysql_local"]["base_de_datos"],
    }


def load_connection_config():
    config = _get_config()

    return {
        "timeout": config["conexion"].getint("timeout", 10)
    }