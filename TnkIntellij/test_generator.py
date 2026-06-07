from src.config.game_config import TINKA_CONFIG, KABALA_CONFIG
from src.services.generator import generate_numbers
from src.utils.logger import setup_logger


def main():
    setup_logger()  # 🔥 ESTO ES LO QUE TE FALTA

    tinka = generate_numbers(
        TINKA_CONFIG["max_number"],
        TINKA_CONFIG["numbers_count"],
        TINKA_CONFIG["table"]
    )

    print("Tinka:", tinka)

    kabala = generate_numbers(
        KABALA_CONFIG["max_number"],
        KABALA_CONFIG["numbers_count"],
        KABALA_CONFIG["table"]
    )

    print("Kábala:", kabala)


if __name__ == "__main__":
    main()
