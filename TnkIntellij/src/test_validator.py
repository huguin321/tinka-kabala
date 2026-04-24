from src.services.validator import validate_combination


def main():
    combo = (5, 9, 22, 24, 40, 41)
    history = [(5, 9, 22, 24, 40, 41)]
    winning = {}

    result = validate_combination(combo, history, winning)
    print(result)


if __name__ == "__main__":
    main()
