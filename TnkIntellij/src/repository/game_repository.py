from src.database.connection import get_connection


def get_winning_combinations(table_name):
    conn = get_connection("get_winning_combinations")
    if not conn:
        return {}

    cursor = conn.cursor()

    query = f"""
        SELECT fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei 
        FROM {table_name}
    """

    cursor.execute(query)

    result = {
        tuple(sorted(row[1:])): row[0]
        for row in cursor.fetchall()
    }

    cursor.close()
    conn.close()

    return result


def get_last_draws(table_name, limit=4):
    conn = get_connection("get_last_draws")
    if not conn:
        return []

    cursor = conn.cursor()

    query = f"""
        SELECT NumUno, NumDos, NumTre, NumCua, NumCin, NumSei 
        FROM {table_name}
        ORDER BY fecha DESC
        LIMIT {limit}
    """

    cursor.execute(query)

    result = [tuple(row) for row in cursor.fetchall()]

    cursor.close()
    conn.close()

    return result
