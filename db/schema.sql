-- Tabla de roles
CREATE TABLE IF NOT EXISTS roles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    role TEXT NOT NULL
);

-- Tabla de áreas
CREATE TABLE IF NOT EXISTS areas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    acronym TEXT NOT NULL,
    area TEXT NOT NULL
);

-- Tabla de empleados
CREATE TABLE IF NOT EXISTS employees (
    id_employee INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    lastname TEXT NOT NULL,
    password TEXT NOT NULL, -- Aquí se almacena la contraseña hasheada
    id_role INTEGER NOT NULL,
    id_area INTEGER NOT NULL,
    FOREIGN KEY (id_role) REFERENCES roles(id) ON DELETE CASCADE,
    FOREIGN KEY (id_area) REFERENCES areas(id) ON DELETE CASCADE
);

-- Tabla de markups
CREATE TABLE IF NOT EXISTS markups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    part_number TEXT NOT NULL,
    description TEXT NOT NULL,
    revision TEXT NOT NULL,
    created_at TEXT NOT NULL,
    due_date TEXT NOT NULL,
    employee_id INTEGER NOT NULL,
    status_id INTEGER NOT NULL,


    FOREIGN KEY (employee_id) REFERENCES employees(id_employee) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES Status(id) ON DELETE CASCADE
);

-- Tabla de estados
CREATE TABLE IF NOT EXISTS Status (
    id INTEGER PRIMARY KEY,
    status TEXT NOT NULL
);
