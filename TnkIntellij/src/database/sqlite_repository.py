from src.database.sqlite_connection import get_sqlite_connection


TABLAS_PERMITIDAS = {"TblTinka", "TblKabala"}


def validar_tabla(table_name):
    if table_name not in TABLAS_PERMITIDAS:
        raise ValueError(f"Tabla no permitida: {table_name}")


def get_table_stats(table_name):
    validar_tabla(table_name)

    conn = get_sqlite_connection()
    cursor = conn.cursor()

    try:
        cursor.execute(f"""
            SELECT
                COUNT(*),
                MAX(fecha)
            FROM {table_name}
        """)

        count, max_date = cursor.fetchone()

        return {
            "count": count or 0,
            "max_date": max_date
        }

    finally:
        cursor.close()
        conn.close()