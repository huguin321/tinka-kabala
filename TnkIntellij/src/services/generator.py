import logging
import random

from src.repository.game_repository import get_last_draws, get_winning_combinations
from src.services.validator import validate_combination, calculate_entropy

logger = logging.getLogger(__name__)


def save_successful(combination, table_name):
    file_name = f"exitosos_{table_name}.txt"

    with open(file_name, "a") as file:
        file.write(f"{combination}\n")

    logger.info(f"Combinación guardada en {file_name}: {combination}")


def generate_numbers(max_number, numbers_count, table_name):
    logger.info(f"Iniciando generación para {table_name}")

    history = get_last_draws(table_name)
    winning_combinations = get_winning_combinations(table_name)

    attempts = 0

    while True:
        attempts += 1

        combination = tuple(sorted(random.sample(range(1, max_number + 1), numbers_count)))
        entropy = calculate_entropy(combination)

        is_valid, reason = validate_combination(
            combination,
            history,
            winning_combinations
        )

        if entropy > 2.2 and combination not in winning_combinations and is_valid:
            logger.info(f"Generada en {attempts} intentos: {combination}")
            save_successful(combination, table_name)
            return combination

        else:
            logger.warning(
                f"Intento {attempts}: {combination} rechazada ({reason}, entropía={round(entropy, 2)})"
            )
