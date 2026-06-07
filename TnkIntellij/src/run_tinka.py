from src.config.game_config import TINKA_CONFIG
from src.services.generator import generate_numbers
from src.utils.logger import setup_logger


def main():
    setup_logger("tinka")

    result = generate_numbers(TINKA_CONFIG["table"])

    if result:
        print("Tinka:", result)
    else:
        print("❌ No se pudo generar una combinación válida para Tinka")


if __name__ == "__main__":
    main()