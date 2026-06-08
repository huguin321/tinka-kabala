import mysql.connector

from src.config.config_loader import load_config, load_local_config


# =========================
# CONEXIÓN LOCAL
# =========================
def get_local_connection():
    config = load_local_config()

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"]
    )


# =========================
# CONEXIÓN RAILWAY
# =========================
def get_railway_connection():
    config = load_config()

    return mysql.connector.connect(
        host=config["host"],
        user=config["user"],
        password=config["password"],
        database=config["database"],
        port=int(config["port"])
    )


# =========================
# OBTENER DATOS LOCAL
# =========================
def fetch_all_data(conn, table):
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {table}")
    data = cursor.fetchall()
    columns = cursor.column_names
    cursor.close()
    return data, columns


# =========================
# INSERTAR EN RAILWAY
# =========================
def insert_data(conn, table, columns, data):
    cursor = conn.cursor()
    cols = ",".join(columns)
    placeholders = ",".join(["%s"] * len(columns))
    sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
    cursor.executemany(sql, data)
    conn.commit()
    cursor.close()


# =========================
# MIGRACIÓN POR TABLA
# =========================
def migrate_table(table_name):
    print(f"\n📦 Migrando tabla: {table_name}")

    local_conn = get_local_connection()
    railway_conn = get_railway_connection()

    try:
        # 🔥 OPCIONAL: limpiar tabla en Railway antes de insertar
        cursor = railway_conn.cursor()
        cursor.execute(f"DELETE FROM {table_name}")
        railway_conn.commit()
        cursor.close()

        # 📥 leer local
        data, columns = fetch_all_data(local_conn, table_name)
        print(f"➡️ Registros encontrados en LOCAL: {len(data)}")

        if not data:
            print("⚠️ Tabla vacía, se omite")
            return

        # 🚀 insertar en Railway
        insert_data(railway_conn, table_name, columns, data)
        print(f"✅ Migración completada: {table_name}")

    except Exception as e:
        print(f"❌ Error en tabla {table_name}: {e}")

    finally:
        local_conn.close()
        railway_conn.close()


# =========================
# MAIN
# =========================
def main():
    tables = [
        "TblTinka",
        "TblKabala"
        # agrega más si tienes
    ]

    for table in tables:
        migrate_table(table)


if __name__ == "__main__":
    main()
