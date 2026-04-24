from src.repository.game_repository import get_winning_combinations, get_last_draws


def main():
    ganadoras = get_winning_combinations()
    historial = get_last_draws()

    print("Total combinaciones:", len(ganadoras))
    print("Últimos sorteos:", historial)


if __name__ == "__main__":
    main()
