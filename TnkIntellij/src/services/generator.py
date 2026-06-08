import logging
import os
import random

from src.config.game_config import TINKA_CONFIG, KABALA_CONFIG
from src.repository.game_repository import (get_last_draws as mysql_get_last_draws,get_winning_combinations as mysql_get_winning_combinations)
from src.repository import sqlite_game_repository
from src.services.validator import validate_combination
from src.utils.logger import APP_LOGGER_NAME

logger = logging.getLogger(APP_LOGGER_NAME)

MAX_INTENTOS = 10_000

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
OUTPUT_DIR = os.path.join(BASE_DIR, "output")


def save_successful(combination, table_name):
    """
    Guarda combinaciones válidas generadas.
    """
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    file_name = os.path.join(OUTPUT_DIR, f"exitosos_{table_name}.txt")

    with open(file_name, "a", encoding="utf-8") as file:
        file.write(f"{combination}\n")

    logger.info(f"Combinación guardada en {file_name}: {combination}")


def get_game_config(table_name):
    """
    Retorna la configuración según la tabla.
    """
    if table_name == TINKA_CONFIG["table"]:
        return TINKA_CONFIG
    if table_name == KABALA_CONFIG["table"]:
        return KABALA_CONFIG

    raise ValueError(f"Configuración no encontrada para {table_name}")


def _load_data(table_name, limit):
    """
    Carga historial y combinaciones ganadoras.
    Intenta SQLite primero; si está vacío o falla, cae a MySQL.

    Retorna: (history, winning_combinations, source)
    """

    # ─── Intentar SQLite ──────────────────────────────────────────────────────
    try:
        history = sqlite_game_repository.get_last_draws(table_name, limit)
        winning_combinations = sqlite_game_repository.get_winning_combinations(table_name)

        if history and winning_combinations:
            logger.info(
                f"[{table_name}] Datos cargados desde SQLite — "
                f"historial: {len(history)}, ganadoras: {len(winning_combinations)}"
            )
            return history, winning_combinations, "SQLite"

        logger.warning(
            f"[{table_name}] SQLite vacío o incompleto "
            f"(historial={len(history)}, ganadoras={len(winning_combinations)}) — "
            f"cayendo a MySQL"
        )

    except Exception as e:
        logger.error(f"[{table_name}] Error al leer SQLite: {e} — cayendo a MySQL")

    # ─── Fallback MySQL ───────────────────────────────────────────────────────
    try:
        history = mysql_get_last_draws(table_name, limit)
        winning_combinations = mysql_get_winning_combinations(table_name)

        if history or winning_combinations:
            logger.info(
                f"[{table_name}] Datos cargados desde MySQL — "
                f"historial: {len(history)}, ganadoras: {len(winning_combinations)}"
            )
            return history, winning_combinations, "MySQL"

        logger.error(f"[{table_name}] MySQL también vacío o sin datos")

    except Exception as e:
        logger.error(f"[{table_name}] Error al leer MySQL: {e}")

    # ─── Sin datos ────────────────────────────────────────────────────────────
    logger.error(f"[{table_name}] Sin datos disponibles en ninguna fuente")
    return [], {}, "ninguna"


def generate_numbers(table_name):
    """
    Genera combinaciones válidas según reglas del juego.
    Usa SQLite como fuente primaria; MySQL como fallback.
    """
    game_config = get_game_config(table_name)

    logger.info(f"Iniciando generación para {table_name}")

    history, winning_combinations, source = _load_data(
        table_name,
        game_config["last_draws_limit"]
    )

    if source == "ninguna":
        logger.error(f"[{table_name}] No se puede generar sin datos históricos")
        return None

    logger.info(f"[{table_name}] Fuente de datos: {source}")

    attempts = 0

    while attempts < MAX_INTENTOS:
        attempts += 1

        combination = tuple(
            sorted(
                random.sample(
                    range(1, game_config["max_number"] + 1),
                    game_config["numbers_count"]
                )
            )
        )

        is_valid, reason = validate_combination(
            combination,
            history,
            winning_combinations,
            game_config
        )

        if combination not in winning_combinations and is_valid:
            logger.info(f"Generada en {attempts} intentos: {combination}")
            save_successful(combination, table_name)
            return combination

        logger.warning(f"Intento {attempts}: {combination} rechazada ({reason})")

    logger.error(f"❌ No se encontró combinación válida en {MAX_INTENTOS} intentos")
    return None