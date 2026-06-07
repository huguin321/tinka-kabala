from src.config.game_config import KABALA_CONFIG
from src.services.generator import generate_numbers
from src.utils.logger import setup_logger


def main():
    setup_logger("kabala")

    result = generate_numbers(KABALA_CONFIG["table"])

    if result:
        print("Kábala:", result)
    else:
        print("❌ No se pudo generar una combinación válida para Kábala")


if __name__ == "__main__":
    main()