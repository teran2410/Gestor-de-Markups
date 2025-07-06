# ================================
# Empleados
# ================================

# Insertar nuevo empleado
INSERT_EMPLOYEE = """
INSERT INTO employees (id_employee, name, lastname, password, id_role, id_area)
VALUES (?, ?, ?, ?, ?, ?);
"""

# Obtener todos los empleados
GET_ALL_EMPLOYEES = "SELECT * FROM employees;"

# Buscar empleado por ID (login)
GET_EMPLOYEE_BY_ID = "SELECT * FROM employees WHERE id_employee = ?;"

# Buscar empleado por apellido (opcional)
GET_EMPLOYEE_BY_USERNAME = """
SELECT * FROM employees WHERE lastname = ?;
"""

# ================================
# Roles
# ================================

GET_ALL_ROLES = "SELECT * FROM roles;"

# ================================
# Áreas
# ================================

GET_ALL_AREAS = "SELECT * FROM areas;"

# ================================
# Markups
# ================================

# Insertar nuevo markup
INSERT_MARKUP = """
INSERT INTO markups (
    part_number, description, revision, created_at, due_date,
    employee_id, status_id, route_id, workCell_id
) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);
"""

# Obtener todos los markups
GET_ALL_MARKUPS = "SELECT * FROM markups;"

# Obtener markup por ID
GET_MARKUP_BY_ID = "SELECT * FROM markups WHERE id = ?;"

# Obtener todos los markups de un empleado
GET_MARKUPS_BY_EMPLOYEE = "SELECT * FROM markups WHERE employee_id = ?;"

# Actualizar un markup
UPDATE_MARKUP = """
UPDATE markups
SET part_number = ?, description = ?, revision = ?, created_at = ?, due_date = ?,
    employee_id = ?, status_id = ?, route_id = ?, workCell_id = ?
WHERE id = ?;
"""

# Eliminar un markup
DELETE_MARKUP = "DELETE FROM markups WHERE id = ?;"

# ================================
# Status
# ================================

GET_ALL_STATUSES = "SELECT * FROM status;"
GET_STATUS_BY_ID = "SELECT * FROM status WHERE id = ?;"

# ================================
# Routes
# ================================

GET_ALL_ROUTES = "SELECT * FROM routes;"
GET_ROUTE_BY_ID = "SELECT * FROM routes WHERE id = ?;"

# ================================
# Work Cells
# ================================

GET_ALL_WORKCELLS = "SELECT * FROM workCells;"
GET_WORKCELL_BY_ID = "SELECT * FROM workCells WHERE id = ?;"

# ================================
# Core Teams
# ================================

GET_ALL_CORETEAMS = "SELECT * FROM coreTeams;"
GET_CORETEAM_BY_ID = "SELECT * FROM coreTeams WHERE id = ?;"

# ================================
# Vista: Markups con detalles
# ================================

GET_ALL_MARKUPS_WITH_DETAILS = "SELECT * FROM view_markups ORDER BY created_at DESC;"
GET_MARKUP_DETAILS_BY_ID = "SELECT * FROM view_markups WHERE id = ?;"