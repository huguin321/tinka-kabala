from src.database.sqlite_connection import get_sqlite_connection


def main():
    conn = get_sqlite_connection()

    print("✅ SQLite conectado")

    conn.close()


if __name__ == "__main__":
    main()