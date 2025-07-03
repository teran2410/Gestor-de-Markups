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
    route_id INTEGER NOT NULL,
    workCell_id INTEGER NOT NULL,

    FOREIGN KEY (employee_id) REFERENCES employees(id_employee) ON DELETE CASCADE,
    FOREIGN KEY (status_id) REFERENCES status(id) ON DELETE CASCADE,
    FOREIGN KEY (route_id) REFERENCES routes(id) ON DELETE CASCADE,
    FOREIGN KEY (workCell_id) REFERENCES workCells(id) ON DELETE CASCADE
);

-- Tabla de estados
CREATE TABLE IF NOT EXISTS status (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    status TEXT NOT NULL
);

-- Tabla de rutas
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    route TEXT NOT NULL
);

-- Tabla de Celda
CREATE TABLE IF NOT EXISTS workCells (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    coreteam_id INTEGER NOT NULL,

    FOREIGN KEY (coreteam_id) REFERENCES coreTeams(id) ON DELETE CASCADE
);

-- Tabla de CoreTeam
CREATE TABLE IF NOT EXISTS coreTeams (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);