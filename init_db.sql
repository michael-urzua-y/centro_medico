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
	cita_id serial4 NOT NULL,
	paciente_id int4 NOT NULL,
	medico_id int4 NOT NULL,
	fecha date NOT NULL,
	hora time NOT NULL,
	estado text NOT NULL,
	fecha_creada timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	CONSTRAINT citas_estado_check CHECK ((estado = ANY (ARRAY['pendiente'::text, 'pagada'::text, 'confirmada'::text, 'rechazada'::text]))),
	CONSTRAINT citas_pkey PRIMARY KEY (cita_id),
	CONSTRAINT citas_medico_id_fkey FOREIGN KEY (medico_id) REFERENCES centro_medico.usuarios(usuario_id) ON DELETE CASCADE,
	CONSTRAINT citas_paciente_id_fkey FOREIGN KEY (paciente_id) REFERENCES centro_medico.usuarios(usuario_id) ON DELETE CASCADE
);

CREATE TABLE centro_medico.pagos (
	pago_id serial4 NOT NULL,
	cita_id int4 NOT NULL,
	estado text NOT NULL,
	monto numeric(10, 2) NOT NULL,
	fecha_creada timestamp DEFAULT CURRENT_TIMESTAMP NULL,
	id_pago_stripe varchar(100) NULL,
    metodo_pago varchar(50) NULL,
	CONSTRAINT pagos_estado_check CHECK ((estado = ANY (ARRAY['pendiente'::text, 'completado'::text, 'fallido'::text]))),
	CONSTRAINT pagos_pkey PRIMARY KEY (pago_id),
	CONSTRAINT pagos_cita_id_fkey FOREIGN KEY (cita_id) REFERENCES centro_medico.citas(cita_id) ON DELETE CASCADE
);
CREATE INDEX idx_pagos_stripe_id ON centro_medico.pagos USING btree (id_pago_stripe);


INSERT INTO centro_medico.usuarios (nombre, email, password, rol)
VALUES
('Alberto Guerra', 'alberto.guerra@gmail.com', '1234', 'paciente'),
('Marta Herrera', 'marta.herrera@gmail.com', '1234', 'medico');