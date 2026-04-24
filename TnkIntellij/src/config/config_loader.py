import configparser
import os


def load_config():
    config = configparser.ConfigParser()

    # Ruta absoluta al config.ini (sube dos niveles desde este archivo)
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    config_path = os.path.join(base_dir, "config.ini")

    config.read(config_path)

    return {
        "host": config["mysql"]["host"],
        "user": config["mysql"]["usuario"],
        "password": config["mysql"]["contrasena"],
        "database": config["mysql"]["base_de_datos"],
        "port": config["mysql"].get("port", 3306)
    }
