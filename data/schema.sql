-- ============================================================
-- DDL - DEFINICIÓN DE TABLAS
-- ============================================================

-- Tabla: usuarios (demo)
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    usuario VARCHAR(50) UNIQUE NOT NULL,
    contrasena VARCHAR(50) NOT NULL
);

-- Tabla: pacientes (demo)
CREATE TABLE pacientes (
    id SERIAL PRIMARY KEY,
    cedula VARCHAR(20) UNIQUE NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    telefono VARCHAR(20),
    diagnostico TEXT,
    tratamiento TEXT,
    fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- ============================================================
-- DML - INSERCIÓN DE DATOS DE PRUEBA
-- ============================================================

-- Usuario de prueba (contraseña: demo123)
INSERT INTO usuarios (usuario, contrasena) 
VALUES ('doctor', 'demo123');

-- Pacientes de prueba
INSERT INTO pacientes (cedula, nombre, apellido, telefono, diagnostico, tratamiento) VALUES
('12345678', 'María', 'González', '3001234567', 'Hipertensión arterial', 'Enalapril 10mg cada 12 horas'),
('87654321', 'Carlos', 'Pérez', '3007654321', 'Diabetes tipo 2', 'Metformina 850mg cada 8 horas'),
('11223344', 'Ana', 'Martínez', '3009988776', 'Infección respiratoria', 'Amoxicilina 500mg cada 8 horas por 7 días'),
('55667788', 'Roberto', 'Jiménez', '3005544332', 'Dolor lumbar', 'Reposo y antiinflamatorios'),
('99887766', 'Laura', 'Rodríguez', '3006677889', 'Ansiedad', 'Terapia y sertralina 50mg')

-- ============================================================
-- DQL - CONSULTAS DE VERIFICACIÓN
-- ============================================================

-- Ver todos los usuarios
SELECT * FROM usuarios;

-- Ver todos los pacientes
SELECT * FROM pacientes;