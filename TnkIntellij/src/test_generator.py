from src.config.game_config import TINKA_CONFIG, KABALA_CONFIG
from src.services.generator import generate_numbers
from src.utils.logger import setup_logger


def main():
    setup_logger("tinka")

    tinka = generate_numbers(TINKA_CONFIG["table"])

    if tinka:
        print("Tinka:", tinka)
    else:
        print("❌ No se pudo generar una combinación válida para Tinka")

    setup_logger("kabala")

    kabala = generate_numbers(KABALA_CONFIG["table"])

    if kabala:
        print("Kábala:", kabala)
    else:
        print("❌ No se pudo generar una combinación válida para Kábala")


if __name__ == "__main__":
    main()