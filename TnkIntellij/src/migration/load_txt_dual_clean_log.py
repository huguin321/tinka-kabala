import os
from datetime import datetime

import mysql.connector

from src.config.config_loader import load_config

# =========================
# CONFIG
# =========================
FILE_MAP = {
    "Resul_Tnk.txt": "TblTinka",
    "Resul_Kbl.txt": "TblKabala"
}


# =========================
# CONEXIONES
# =========================
def get_local_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="M14J35u5=uWu",
        database="tinka"
    )


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
# LEER Y LIMPIAR TXT
# =========================
def read_and_clean(file_path):
    registros = []

    with open(file_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if not line:
                continue

            parts = line.split()

            # fecha
            fecha_raw = parts[0]
            fecha = datetime.strptime(fecha_raw, "%d/%m/%Y").date()

            # números → quitar ceros + ordenar
            numeros = sorted([int(n) for n in parts[1:]])

            registros.append((fecha, *numeros))

    # ordenar cronológicamente
    registros.sort(key=lambda x: x[0])
    return registros


# =========================
# INSERT OPTIMIZADO
# =========================
def process_records(conn, table, data, db_name):
    cursor = conn.cursor()

    insert_sql = f"""
        INSERT IGNORE INTO {table}
        (fecha, NumUno, NumDos, NumTre, NumCua, NumCin, NumSei)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """

    insertados = 0
    ignorados = 0

    for registro in data:
        cursor.execute(insert_sql, registro)

        if cursor.rowcount == 1:
            print(f"✅ [{db_name}] INSERTADO: {registro}")
            insertados += 1
        else:
            print(f"⚠️ [{db_name}] YA EXISTE: {registro}")
            ignorados += 1

    conn.commit()
    cursor.close()

    print(f"\n📊 [{db_name}] RESUMEN:")
    print(f"✔ Insertados: {insertados}")
    print(f"⚠️ Ignorados: {ignorados}")


# =========================
# PROCESAR ARCHIVO
# =========================
def process_file(file_path):
    file_name = os.path.basename(file_path)  # 👈 CLAVE

    if file_name not in FILE_MAP:
        print(f"❌ Archivo no reconocido: {file_name}")
        return

    table = FILE_MAP[file_name]

    print(f"\n📄 Procesando: {file_name} → {table}")

    data = read_and_clean(file_path)

    print(f"➡️ Registros procesados: {len(data)}")

    if not data:
        print("⚠️ Sin datos")
        return

    local_conn = get_local_connection()
    railway_conn = get_railway_connection()

    try:
        print("\n--- LOCAL ---")
        process_records(local_conn, table, data, "LOCAL")

        print("\n--- RAILWAY ---")
        process_records(railway_conn, table, data, "RAILWAY")

    except Exception as e:
        print(f"❌ Error: {e}")

    finally:
        local_conn.close()
        railway_conn.close()


# =========================
# MAIN
# =========================
def main():
    files = [
        r"D:\Tinka\TnkIntellij\data\Resul_Tnk.txt",
        r"D:\Tinka\TnkIntellij\data\Resul_Kbl.txt"
    ]

    for file in files:
        process_file(file)


if __name__ == "__main__":
    main()
