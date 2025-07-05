import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3
from db.queries import (
    INSERT_EMPLOYEE, GET_ALL_ROLES, GET_ALL_AREAS, INSERT_MARKUP,
    GET_ALL_ROUTES, GET_ALL_STATUSES, GET_ALL_WORKCELLS
)
from datetime import datetime, timedelta
from dateutil.parser import parse as parse_date

app = Flask(__name__)
app.secret_key = "O~27GpQv0q4^HbMtz_!rJ$Xe#LAvkTdn6pZfu&B3mcs@Y81W"
DB_PATH = os.path.join("instance", "markups.db")

# Función para filtrar y formatear fechas en plantillas
@app.template_filter('datetimeformat')
def datetimeformat(value, format='%Y-%m-%d'):
    try:
        if isinstance(value, str):
            value = datetime.fromisoformat(value)
        return value.strftime(format)
    except Exception:
        return ''

@app.route("/register", methods=["GET", "POST"])
def register():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    message = None
    error = None

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

            password_hash = generate_password_hash(password)

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
        conn.execute("PRAGMA foreign_keys = ON;")
        cursor = conn.cursor()

        cursor.execute("SELECT id_employee, name, lastname, password, id_role FROM employees WHERE id_employee = ?", (id_employee,))
        user = cursor.fetchone()
        conn.close()

        if user:
            user_id, name, lastname, hashed_password, role = user
            if check_password_hash(hashed_password, password):
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

@app.route("/markups")
def list_markups():
    if "user_id" not in session:
        return redirect(url_for("login"))
    
    name = session.get("name")
    lastname = session.get("lastname")

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM view_markups")
    markups = cursor.fetchall()

    # Para los selects en los modales
    cursor.execute("SELECT id_employee, name || ' ' || lastname FROM employees")
    employees = cursor.fetchall()

    cursor.execute("SELECT * FROM status")
    statuses = cursor.fetchall()

    cursor.execute("SELECT * FROM routes")
    routes = cursor.fetchall()

    cursor.execute("SELECT id, name FROM workCells")
    workcells = cursor.fetchall()

    conn.close()
    return render_template("list_markups.html", markups=markups,
                           employees=employees, statuses=statuses,
                           routes=routes, workcells=workcells, name=name, lastname=lastname)

@app.route("/markups/new", methods=["POST"])
def new_markup():
    if "user_id" not in session:
        return redirect(url_for("login"))

    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    part_number = request.form["part_number"]
    description = request.form["description"]
    revision = request.form["revision"]
    workCell_id = request.form["workCell_id"]
    employee_id = session["user_id"]

    created_at_str = request.form["created_at"]
    try:
        created_at = datetime.strptime(created_at_str, "%Y-%m-%d").date()
    except ValueError:
        flash("❌ Fecha inválida. Usa el formato correcto (YYYY-MM-DD).", "danger")
        return redirect(url_for("list_markups"))

    # Calcular la fecha límite (7 días hábiles después de created_at)
    due_date = created_at
    added_days = 0
    while added_days < 7:
        due_date += timedelta(days=1)
        if due_date.weekday() < 5:
            added_days += 1

    # Obtener IDs de estado y ruta
    try:
        cursor.execute("SELECT id FROM status WHERE status = 'Pending'")
        status_id = cursor.fetchone()[0]

        cursor.execute("SELECT id FROM routes WHERE route = 'Actualizando'")
        route_id = cursor.fetchone()[0]
    except:
        flash("❌ No se encontró el estado 'Pending' o la ruta 'Actualizando'.", "danger")
        conn.close()
        return redirect(url_for("list_markups"))

    # Insertar nuevo markup
    try:
        cursor.execute(INSERT_MARKUP, (
            part_number, description, revision,
            created_at.isoformat(), due_date.isoformat(),
            employee_id, status_id, route_id, workCell_id
        ))
        conn.commit()
        flash("✅ Markup creado correctamente.", "success")
    except sqlite3.Error as e:
        flash(f"❌ Error al crear markup: {e}", "danger")
    finally:
        conn.close()

    return redirect(url_for("list_markups"))

@app.route("/markups/edit/<int:id>", methods=["POST"])
def edit_markup(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    part_number = request.form["part_number"]
    description = request.form["description"]
    revision = request.form["revision"]
    created_at_str = request.form["created_at"]
    employee_id = request.form["employee_id"]
    status_id = request.form["status_id"]
    route_id = request.form["route_id"]
    workcell_id = request.form["workcell_id"]

    # Calcular la nueva fecha límite (7 días hábiles después de created_at)
    try:
        created_at = parse_date(created_at_str).date()
        due_date = created_at
        added_days = 0
        while added_days < 7:
            due_date += timedelta(days=1)
            if due_date.weekday() < 5:  # solo lunes a viernes
                added_days += 1
    except ValueError:
        conn.close()
        return "❌ Error en la fecha", 400

    # Actualizar el registro
    cursor.execute("""
        UPDATE markups
        SET part_number = ?, description = ?, revision = ?, created_at = ?, due_date = ?,
            employee_id = ?, status_id = ?, route_id = ?, workCell_id = ?
        WHERE id = ?
    """, (
        part_number, description, revision, created_at.isoformat(), due_date.isoformat(),
        employee_id, status_id, route_id, workcell_id, id
    ))

    conn.commit()
    conn.close()
    return redirect(url_for("list_markups"))

# Función para eliminar markup
@app.route("/markups/delete/<int:id>", methods=["POST"])
def delete_markup(id):
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON;")
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM markups WHERE id = ?", (id,))
        conn.commit()
        flash("✅ Markup eliminado correctamente.", "success")
    except sqlite3.Error as e:
        flash(f"❌ Error al eliminar el markup: {e}", "error")
    finally:
        conn.close()

    return redirect(url_for("list_markups"))

if __name__ == "__main__":
    app.run(debug=True)
