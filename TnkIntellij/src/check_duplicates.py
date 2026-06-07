from src.database.sqlite_connection import get_sqlite_connection

TABLAS = ["TblTinka", "TblKabala"]


def check_duplicates(table_name):
    conn = get_sqlite_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT
                NumUno, NumDos, NumTre, NumCua, NumCin, NumSei,
                COUNT(*) as veces,
                GROUP_CONCAT(fecha, ' | ') as fechas
            FROM {table_name}
            GROUP BY NumUno, NumDos, NumTre, NumCua, NumCin, NumSei
            HAVING COUNT(*) > 1
            ORDER BY veces DESC
        """)

        rows = cursor.fetchall()

        print(f"\n{'=' * 60}")
        print(f"DUPLICADOS EN {table_name}")
        print(f"{'=' * 60}")

        if not rows:
            print("✅ Sin duplicados")
            return

        print(f"⚠️ Se encontraron {len(rows)} combinaciones repetidas:\n")

        for row in rows:
            nums = row[:6]
            veces = row[6]
            fechas = row[7]
            print(f"  {nums} → aparece {veces} veces")
            print(f"  Fechas: {fechas}")
            print()

    except Exception as e:
        print(f"❌ Error al consultar {table_name}: {e}")

    finally:
        cursor.close()
        conn.close()


def main():
    for tabla in TABLAS:
        check_duplicates(tabla)


if __name__ == "__main__":
    main()