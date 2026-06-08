from src.database.connection import get_connection


def main():
    conn = get_connection("test_db")

    if conn:
        print("Conexión exitosa")
        conn.close()
    else:
        print("Error de conexión")


if __name__ == "__main__":
    main()
