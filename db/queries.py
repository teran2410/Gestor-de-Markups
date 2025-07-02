# Insertar nuevo empleado
INSERT_EMPLOYEE = """
INSERT INTO employees (id_employee, name, lastname, password, id_role, id_area)
VALUES (?, ?, ?, ?, ?, ?);
"""

# Obtener todos los roles
GET_ALL_ROLES = """
SELECT * FROM roles;
"""

# Obtener todas las áreas
GET_ALL_AREAS = """
SELECT * FROM areas;
"""

# Obtener todos los empleados (útil para debugging o listar)
GET_ALL_EMPLOYEES = """
SELECT * FROM employees;
"""

# Buscar un usuario por id_employee (ej. para login)
GET_EMPLOYEE_BY_ID = """
SELECT * FROM employees WHERE id_employee = ?;
"""

# Buscar un usuario por nombre o email si en el futuro usas login con email
GET_EMPLOYEE_BY_USERNAME = """
SELECT * FROM employees WHERE name = ? AND lastname = ?;
"""
