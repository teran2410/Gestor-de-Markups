import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db.queries import INSERT_EMPLOYEE, GET_ALL_ROLES, GET_ALL_AREAS, INSERT_MARKUP, GET_ALL_ROUTES, GET_ALL_STATUSES, GET_ALL_WORKCELLS, GET_ALL_MARKUPS_WITH_DETAILS
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

    # GET: mostrar celdas
    cursor.execute(GET_ALL_WORKCELLS)
    workcells = cursor.fetchall()

    if request.method == "POST":
        part_number = request.form["part_number"]
        description = request.form["description"]
        revision = request.form["revision"]
        workCell_id = request.form["workCell_id"]
        employee_id = session["user_id"]
        created_at_str = request.form["created_at"]

        try:
            created_at = datetime.strptime(created_at_str, "%Y-%m-%d").date()
        except ValueError:
            message = "Fecha inválida. Usa el formato correcto (YYYY-MM-DD)."
            conn.close()
            return render_template("new_markup.html",
                                   workcells=workcells,
                                   message=message)

        # Calcular fecha de entrega (7 días hábiles)
        due_date = created_at
        added_days = 0
        while added_days < 7:
            due_date += timedelta(days=1)
            if due_date.weekday() < 5:
                added_days += 1

        # Obtener ID de status y route predeterminados
        cursor.execute("SELECT id FROM status WHERE status = 'Pending'")
        result = cursor.fetchone()
        if not result:
            message = "No se encontró el estado 'Pending'."
            conn.close()
            return render_template("new_markup.html", workcells=workcells, message=message)
        status_id = result[0]

        cursor.execute("SELECT id FROM routes WHERE route = 'Actualizando'")
        result = cursor.fetchone()
        if not result:
            message = "No se encontró la ruta 'Actualizando'."
            conn.close()
            return render_template("new_markup.html", workcells=workcells, message=message)
        route_id = result[0]

        # Insertar markup
        cursor.execute(INSERT_MARKUP, (
            part_number, description, revision,
            created_at.isoformat(), due_date.isoformat(),
            employee_id, status_id, route_id, workCell_id
        ))

        conn.commit()
        conn.close()
        return redirect(url_for("dashboard"))

    # Si GET o si hubo error
    conn.close()
    return render_template("new_markup.html",
                           workcells=workcells,
                           message=message)

@app.route("/markups")
def list_markups():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # Para acceder a las columnas por nombre
    cursor = conn.cursor()

    cursor.execute(GET_ALL_MARKUPS_WITH_DETAILS)
    markups = cursor.fetchall()

    conn.close()
    return render_template("list_markups.html", markups=markups)

if __name__ == "__main__":
    app.run(debug=True)