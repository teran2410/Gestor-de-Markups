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
    ("S1",),
    ("S2",)
]

initial_cells = [
    ("Bangkok", 1),
    ("Barcelona", 0),
    ("Berlin", 0),
    ("Frankfurt", 0),
    ("Londres", 0),
    ("Madrid 1", 1),
    ("Madrid 2", 1),
    ("Milan", 0),
    ("Munich", 0),
    ("Paris", 0),
    ("Pekin", 1),
    ("Praga", 0),
    ("Roma", 0),
    ("Seul", 1),
    ("Shangai 1", 1),
    ("Shangai 2", 1),
    ("Tokio", 0),
    ("Venecia", 0),
    ("Yakarta", 1)
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

    # Insertar estados si no existen
    cursor.execute("SELECT COUNT(*) FROM status")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO status (status) VALUES (?)", initial_statuses)
        print("✔️ Estados iniciales insertados.")

    # Insertar rutas si no existen
    cursor.execute("SELECT COUNT(*) FROM routes")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO routes (route) VALUES (?)", initial_routes)
        print("✔️ Rutas iniciales insertadas.")

    # Insertar equipos centrales si no existen
    cursor.execute("SELECT COUNT(*) FROM coreTeams")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO coreTeams (name) VALUES (?)", initial_coreteams)
        print("✔️ Equipos centrales iniciales insertados.")

    # Insertar celdas si no existen
    cursor.execute("SELECT COUNT(*) FROM workCells")
    if cursor.fetchone()[0] == 0:
        cursor.executemany("INSERT INTO workCells (name, coreteam_id) VALUES (?, ?)", initial_cells)
        print("✔️ Celdas iniciales insertadas.")

    # Imprimir tabla employees y markups para verificar los registros
    cursor.execute("SELECT * FROM employees")
    employees = cursor.fetchall()
    print("👥 Empleados registrados:", employees
        if employees else "Ningún empleado registrado.")
    
    cursor.execute("SELECT * FROM markups")
    markups = cursor.fetchall()
    print("📄 Markups registrados:", markups 
        if markups else "Ningún markup registrado.")

    # Confirmar y cerrar
    conn.commit()
    conn.close()
    print("✅ Base de datos inicializada correctamente.")

if __name__ == "__main__":
    initialize_database()
