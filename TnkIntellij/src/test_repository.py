from src.repository.game_repository import get_winning_combinations, get_last_draws


def main():
    for tabla in ["TblTinka", "TblKabala"]:
        print(f"\n=== {tabla} ===")
        ganadoras = get_winning_combinations(tabla)
        historial = get_last_draws(tabla, 10)

        print("Total combinaciones:", len(ganadoras))
        print("Últimos sorteos:", historial)


if __name__ == "__main__":
    main()
