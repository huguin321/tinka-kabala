from src.config.game_config import KABALA_CONFIG
from src.services.generator import generate_numbers
from src.utils.logger import setup_logger


def main():
    setup_logger("kabala")

    result = generate_numbers(
        KABALA_CONFIG["max_number"],
        KABALA_CONFIG["numbers_count"],
        KABALA_CONFIG["table"]
    )

    print("Kábala:", result)


if __name__ == "__main__":
    main()
