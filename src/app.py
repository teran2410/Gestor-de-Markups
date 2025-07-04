import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db.queries import INSERT_EMPLOYEE, GET_ALL_ROLES, GET_ALL_AREAS, INSERT_MARKUP, GET_ALL_ROUTES, GET_ALL_STATUSES, GET_ALL_WORKCELLS
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = "O~27GpQv0q4^HbMtz_!rJ$Xe#LAvkTdn6pZfu&B3mcs@Y81W"

# Ruta a la base de datos en la carpeta /instance
DB_PATH = os.path.join("instance", "markups.db")

@app.route("/register", methods=["GET", "POST"])
def register():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")  # 👈 activa restricciones de claves foráneas
    cursor = conn.cursor()

    message = None
    error = None

    # Obtener roles y áreas para el formulario
    cursor.execute(GET_ALL_ROLES)
    roles = cursor.fetchall()

    cursor.execute(GET_ALL_AREAS)
    areas = cursor.fetchall()

    if request.method == "POST":
        try:
            id_employee = int(request.form["id_employee"])
            name = request.form["name"]
            lastname = request.form["lastname"]
            password = request.form["password"]
            id_role = int(request.form["id_role"])
            id_area = int(request.form["id_area"])

            # Generar hash de la contraseña
            password_hash = generate_password_hash(password)

            # Insertar en la base de datos
            cursor.execute(INSERT_EMPLOYEE, (id_employee, name, lastname, password_hash, id_role, id_area))
            conn.commit()
            message = "Empleado registrado exitosamente."

        except sqlite3.IntegrityError as e:
            error = f"Error de integridad (¿ID duplicado?): {e}"
        except Exception as e:
            error = f"Ocurrió un error: {e}"

    conn.close()

    return render_template("register.html", roles=roles, areas=areas, message=message, error=error)

@app.route("/login", methods=["GET", "POST"])
def login():
    message = None

    if request.method == "POST":
        id_employee = request.form["id_employee"]
        password = request.form["password"]

        conn = sqlite3.connect(DB_PATH)
        conn.execute("PRAGMA foreign_keys = ON;")  # 👈 activa restricciones de claves foráneas
        cursor = conn.cursor()

        # Buscar al empleado por ID
        cursor.execute("SELECT id_employee, name, lastname, password, id_role FROM employees WHERE id_employee = ?", (id_employee,))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id, name, lastname, hashed_password, role = user
            if check_password_hash(hashed_password, password):
                # Iniciar sesión
                session["user_id"] = user_id
                session["name"] = name
                session["role"] = role
                return redirect(url_for("dashboard"))
            else:
                message = "Contraseña incorrecta."
        else:
            message = "Empleado no encontrado."

    return render_template("login.html", message=message)

@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect(url_for("login"))

    name = session.get("name")
    role = session.get("role")
    return f"<h1>Bienvenido, {name}. Rol: {role}</h1><a href='/logout'>Cerrar sesión</a>"

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))

@app.route("/markups/new", methods=["GET", "POST"])
def new_markup():
    if "user_id" not in session:
        return redirect(url_for("login"))

    message = None
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    if request.method == "POST":
        part_number = request.form["part_number"]
        description = request.form["description"]
        revision = request.form["revision"]
        workCell_id = request.form["workCell_id"]
        employee_id = session["user_id"]

        created_at = datetime.today().date()
        # Calcular 7 días hábiles después
        due_date = created_at
        added_days = 0
        while added_days < 7:
            due_date += timedelta(days=1)
            if due_date.weekday() < 5:  # 0 = lunes, 4 = viernes
                added_days += 1

        cursor.execute(INSERT_MARKUP, (
            part_number, description, revision,
            created_at.isoformat(), due_date.isoformat(),
            employee_id, status_id, route_id, workCell_id
        ))
        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    # GET: mostrar formulario
    cursor.execute(GET_ALL_ROUTES)
    routes = cursor.fetchall()
    cursor.execute(GET_ALL_STATUSES)
    statuses = cursor.fetchall()
    cursor.execute(GET_ALL_WORKCELLS)
    workcells = cursor.fetchall()
    conn.close()
    print("Workcells:", workcells)

    return render_template("new_markup.html",
                           routes=routes,
                           statuses=statuses,
                           workcells=workcells,
                           message=message)

if __name__ == "__main__":
    app.run(debug=True)