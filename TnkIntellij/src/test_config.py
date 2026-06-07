from src.config.config_loader import load_config


def main():
    config = load_config()
    print(config)


if __name__ == "__main__":
    main()
