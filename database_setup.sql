-- Crear base de datos (si no existe)
-- CREATE DATABASE sistema_calificaciones;

-- Conectar a la base de datos
-- \c sistema_calificaciones;

-- Crear extensión para UUID si es necesario
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabla de usuarios personalizada
CREATE TABLE IF NOT EXISTS gestion_calificaciones_usuario (
    id SERIAL PRIMARY KEY,
    password VARCHAR(128) NOT NULL,
    last_login TIMESTAMP WITH TIME ZONE,
    is_superuser BOOLEAN NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    first_name VARCHAR(150) NOT NULL,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOLEAN NOT NULL,
    is_active BOOLEAN NOT NULL,
    date_joined TIMESTAMP WITH TIME ZONE NOT NULL,
    tipo_usuario VARCHAR(10) NOT NULL CHECK (tipo_usuario IN ('admin', 'docente', 'estudiante')),
    telefono VARCHAR(15)
);

-- Tabla de materias
CREATE TABLE IF NOT EXISTS gestion_calificaciones_materia (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    codigo VARCHAR(10) UNIQUE NOT NULL,
    descripcion TEXT,
    activa BOOLEAN DEFAULT TRUE
);

-- Tabla de estudiantes (SIN matrícula)
CREATE TABLE IF NOT EXISTS gestion_calificaciones_estudiante (
    id SERIAL PRIMARY KEY,
    grado VARCHAR(10) NOT NULL,
    grupo VARCHAR(5) NOT NULL,
    fecha_inscripcion DATE NOT NULL,
    usuario_id INTEGER UNIQUE REFERENCES gestion_calificaciones_usuario(id) ON DELETE CASCADE
);

-- Tabla de docentes (CON nombre en lugar de número de empleado)
CREATE TABLE IF NOT EXISTS gestion_calificaciones_docente (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    especialidad VARCHAR(100) NOT NULL,
    usuario_id INTEGER UNIQUE REFERENCES gestion_calificaciones_usuario(id) ON DELETE CASCADE
);

-- Tabla de asignaciones (docente-materia-grupo)
CREATE TABLE IF NOT EXISTS gestion_calificaciones_asignacion (
    id SERIAL PRIMARY KEY,
    grado VARCHAR(10) NOT NULL,
    grupo VARCHAR(5) NOT NULL,
    ciclo_escolar VARCHAR(20) NOT NULL,
    docente_id INTEGER REFERENCES gestion_calificaciones_docente(id) ON DELETE CASCADE,
    materia_id INTEGER REFERENCES gestion_calificaciones_materia(id) ON DELETE CASCADE
);

-- Tabla de calificaciones
CREATE TABLE IF NOT EXISTS gestion_calificaciones_calificacion (
    id SERIAL PRIMARY KEY,
    periodo VARCHAR(2) NOT NULL CHECK (periodo IN ('1', '2', '3')),
    calificacion DECIMAL(4,2) NOT NULL CHECK (calificacion >= 0 AND calificacion <= 10),
    fecha_registro TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    comentarios TEXT,
    estudiante_id INTEGER REFERENCES gestion_calificaciones_estudiante(id) ON DELETE CASCADE,
    asignacion_id INTEGER REFERENCES gestion_calificaciones_asignacion(id) ON DELETE CASCADE,
    UNIQUE(estudiante_id, asignacion_id, periodo)
);

-- Tablas de autenticación de Django (necesarias)
CREATE TABLE IF NOT EXISTS auth_group (
    id SERIAL PRIMARY KEY,
    name VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS auth_permission (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS django_content_type (
    id SERIAL PRIMARY KEY,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Índices para mejorar el rendimiento
CREATE INDEX IF NOT EXISTS idx_estudiante_grado_grupo ON gestion_calificaciones_estudiante(grado, grupo);
CREATE INDEX IF NOT EXISTS idx_calificacion_estudiante_periodo ON gestion_calificaciones_calificacion(estudiante_id, periodo);
CREATE INDEX IF NOT EXISTS idx_calificacion_asignacion ON gestion_calificaciones_calificacion(asignacion_id);
CREATE INDEX IF NOT EXISTS idx_usuario_tipo ON gestion_calificaciones_usuario(tipo_usuario);
CREATE INDEX IF NOT EXISTS idx_materia_activa ON gestion_calificaciones_materia(activa);
CREATE INDEX IF NOT EXISTS idx_docente_nombre ON gestion_calificaciones_docente(nombre);

-- Datos iniciales de ejemplo
INSERT INTO gestion_calificaciones_materia (nombre, codigo, descripcion, activa) VALUES
('Matemáticas', 'MAT-001', 'Matemáticas básicas y álgebra', true),
('Español', 'ESP-001', 'Lengua y literatura', true),
('Ciencias Naturales', 'CIE-001', 'Biología, física y química', true),
('Historia', 'HIS-001', 'Historia universal y de México', true),
('Geografía', 'GEO-001', 'Geografía física y humana', true)
ON CONFLICT (codigo) DO NOTHING;

-- Insertar docentes de ejemplo
INSERT INTO gestion_calificaciones_docente (nombre, especialidad) VALUES
('María García López', 'Matemáticas'),
('Juan Pérez Hernández', 'Español'),
('Ana Martínez Ruiz', 'Ciencias'),
('Carlos Rodríguez Silva', 'Historia')
ON CONFLICT DO NOTHING;