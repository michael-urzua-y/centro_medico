-- Usar el esquema 'centro_medico'
CREATE SCHEMA IF NOT EXISTS centro_medico;

-- Dar permisos al usuario sobre el esquema (opcional si ya están)
GRANT USAGE, CREATE ON SCHEMA centro_medico TO devuser;

-- Crear tablas en el esquema centro_medico
CREATE TABLE centro_medico.usuarios (
    usuario_id SERIAL PRIMARY KEY,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    rol TEXT NOT NULL CHECK (rol IN ('paciente', 'medico')),
    token TEXT
);

CREATE TABLE centro_medico.citas (
    cita_id SERIAL PRIMARY KEY,
    paciente_id INT NOT NULL REFERENCES centro_medico.usuarios(usuario_id) ON DELETE CASCADE,
    medico_id INT NOT NULL REFERENCES centro_medico.usuarios(usuario_id) ON DELETE CASCADE,
    fecha DATE NOT NULL,
    hora TIME NOT NULL,
    estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'pagada', 'confirmada', 'rechazada')),
    fecha_creada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE centro_medico.pagos (
    pago_id SERIAL PRIMARY KEY,
    cita_id INT NOT NULL REFERENCES centro_medico.citas(cita_id) ON DELETE CASCADE,
    estado TEXT NOT NULL CHECK (estado IN ('pendiente', 'completado', 'fallido')),
    monto NUMERIC(10, 2) NOT NULL,
    fecha_creada TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO centro_medico.usuarios (nombre, email, password, rol)
VALUES
('Alberto Guerra', 'alberto.guerra@gmail.com', '1234', 'paciente'),
('Marta Herrera', 'marta.herrera@gmail.com', '1234', 'medico');