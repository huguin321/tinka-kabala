from src.database.sqlite_connection import get_sqlite_connection


def create_tables():
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    tables = ["TblTinka", "TblKabala"]

    for table in tables:
        cursor.execute(f"""
            CREATE TABLE IF NOT EXISTS {table} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha DATE NOT NULL,
                NumUno INTEGER NOT NULL,
                NumDos INTEGER NOT NULL,
                NumTre INTEGER NOT NULL,
                NumCua INTEGER NOT NULL,
                NumCin INTEGER NOT NULL,
                NumSei INTEGER NOT NULL,

                UNIQUE (
                    fecha,
                    NumUno,
                    NumDos,
                    NumTre,
                    NumCua,
                    NumCin,
                    NumSei
                )
            )
        """)

        print(f"✅ Tabla creada/verificada: {table}")

    conn.commit()
    conn.close()


if __name__ == "__main__":
    create_tables()