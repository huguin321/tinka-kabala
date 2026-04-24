from src.config.game_config import TINKA_CONFIG
from src.services.generator import generate_numbers
from src.utils.logger import setup_logger


def main():
    setup_logger("tinka")

    result = generate_numbers(
        TINKA_CONFIG["max_number"],
        TINKA_CONFIG["numbers_count"],
        TINKA_CONFIG["table"]
    )

    print("Tinka:", result)


if __name__ == "__main__":
    main()
