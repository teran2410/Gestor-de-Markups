import sqlite3
import os

# Rutas relativas desde /src/
SCHEMA_PATH = os.path.join("db", "schema.sql")
DB_PATH = os.path.join("instance", "markups.db")

# Datos iniciales
initial_roles = [
    ("admin",),
    ("engineer",),
    ("tech",)
]

initial_areas = [
    ("DB", "DirectBond"),
    ("XDCR", "Cables"),
    ("FA", "Final")
]

initial_statuses = [
    ("Pending",),
    ("Completed",),
    ("Late",)
]

initial_routes = [
    ("Actualizando",),
    ("En firmas",),
    ("Enviado a drafting",)
]

initial_coreteams = [
    ("S1",)
    ("S2",)
]

def initialize_database():
    # Conectar a la base de datos
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Leer y ejecutar el archivo schema.sql
    with open(SCHEMA_PATH, "r", encoding="utf-8") as schema_file:
        schema_sql = schema_file.read()
        cursor.executescript(schema_sql)
        print("✔️ Esquema creado o verificado correctamente.")

    # Insertar roles si no existen
    cursor.execute("SELECT COUNT(*) FROM roles")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO roles (role) VALUES (?)", initial_roles)
        print("✔️ Roles iniciales insertados.")

    # Insertar áreas si no existen
    cursor.execute("SELECT COUNT(*) FROM areas")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO areas (acronym, area) VALUES (?, ?)", initial_areas)
        print("✔️ Áreas iniciales insertadas.")

    # Confirmar y cerrar
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    initialize_database()
