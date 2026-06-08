import os

from src.config.game_config import TINKA_CONFIG, KABALA_CONFIG
from src.services.validator import validate_combination

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEST_FILE = os.path.join(
    BASE_DIR,
    "data",
    "test_validator_cases.txt"
)

GAME_CONFIGS = {
    "TINKA": TINKA_CONFIG,
    "KABALA": KABALA_CONFIG
}


def parse_line(line, game_config):
    """
    Convierte línea TXT en combinación válida.
    """

    parts = line.split()

    expected_numbers = game_config["numbers_count"]
    min_number = game_config["min_number"]
    max_number = game_config["max_number"]

    # =========================
    # CANTIDAD
    # =========================
    if len(parts) != expected_numbers:
        return None, (
            f"Cantidad inválida "
            f"(esperados={expected_numbers}, encontrados={len(parts)})"
        )

    # =========================
    # NUMÉRICOS
    # =========================
    try:
        numbers = [int(n) for n in parts]
    except ValueError:
        return None, "Valor no numérico"

    # =========================
    # DUPLICADOS
    # =========================
    if len(set(numbers)) != expected_numbers:
        return None, "Números duplicados"

    # =========================
    # RANGO
    # =========================
    fuera_de_rango = [
        n for n in numbers
        if n < min_number or n > max_number
    ]

    if fuera_de_rango:
        return None, (
            f"Fuera de rango {fuera_de_rango} "
            f"[{min_number}-{max_number}]"
        )

    return tuple(sorted(numbers)), None


def process_test_file():
    """
    Procesa todos los casos del TXT.
    """

    if not os.path.exists(TEST_FILE):
        print(f"❌ Archivo no encontrado: {TEST_FILE}")
        return

    current_game = None
    game_config = None

    history = []
    winning = {}

    with open(TEST_FILE, "r", encoding="utf-8") as file:

        for line_number, raw_line in enumerate(file, start=1):

            line = raw_line.strip()

            # =========================
            # IGNORAR VACÍOS
            # =========================
            if not line:
                continue

            # =========================
            # IGNORAR COMENTARIOS
            # =========================
            if line.startswith("#"):
                continue

            # =========================
            # SECCIONES
            # =========================
            if line.startswith("[") and line.endswith("]"):

                game_name = line[1:-1].strip().upper()

                if game_name not in GAME_CONFIGS:
                    print(
                        f"❌ Línea {line_number}: "
                        f"Juego no reconocido [{game_name}]"
                    )
                    current_game = None
                    game_config = None
                    continue

                current_game = game_name
                game_config = GAME_CONFIGS[game_name]

                print("\n" + "=" * 60)
                print(f"TESTING: {current_game}")
                print("=" * 60)

                continue

            # =========================
            # SIN SECCIÓN
            # =========================
            if not game_config:
                print(
                    f"❌ Línea {line_number}: "
                    f"No hay sección activa"
                )
                continue

            # =========================
            # PARSEAR
            # =========================
            combination, error = parse_line(line, game_config)

            if error:
                print(
                    f"[ERROR]     {line}"
                    f" -> {error}"
                )
                continue

            # =========================
            # VALIDAR
            # =========================
            is_valid, reason = validate_combination(
                combination,
                history,
                winning,
                game_config
            )

            status = "[OK]" if is_valid else "[INVALIDA]"

            print(
                f"{status:<12} "
                f"{combination} -> {reason}"
            )


def main():
    process_test_file()


if __name__ == "__main__":
    main()