# 🗄️ Base de Datos

Documentación del esquema PostgreSQL de NeuroMedic.

---

## Configuración

La configuración de conexión está en `src/database.py`:

```python
DB_CONFIG = {
    'dbname': 'demoneuromedic',
    'user': 'luntony',
    'password': 'cumple0505',
    'host': 'localhost',
    'port': 5432,
}
```

> ⚠️ **Importante:** Cambia la contraseña antes de subir el código a un repositorio público. Considera migrar a variables de entorno.

---

## Creación de la Base de Datos

```sql
-- Crear la base de datos
CREATE DATABASE demoneuromedic;

-- Conectarse
\c demoneuromedic
```

---

## Esquema

### Tabla: `usuarios`

Almacena las credenciales de acceso a la aplicación.

```sql
CREATE TABLE usuarios (
    id          SERIAL PRIMARY KEY,
    usuario     VARCHAR(50)  NOT NULL UNIQUE,
    contrasena  VARCHAR(255) NOT NULL,
    created_at  TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);
```

**Usuario por defecto (para la demo):**

```sql
INSERT INTO usuarios (usuario, contrasena) VALUES
    ('doctor', 'demo123');
```

> 🔒 **Nota de seguridad:** las contraseñas se almacenan en texto plano para mantener la demo simple. En producción, usar `bcrypt` o `argon2`.

---

### Tabla: `pacientes`

Almacena los datos de los pacientes y su historial clínico.

```sql
CREATE TABLE pacientes (
    id           SERIAL PRIMARY KEY,
    cedula       VARCHAR(20)  NOT NULL UNIQUE,
    nombre       VARCHAR(100) NOT NULL,
    apellido     VARCHAR(100) NOT NULL,
    telefono     VARCHAR(20),
    diagnostico  TEXT,
    tratamiento  TEXT,
    created_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP,
    updated_at   TIMESTAMP    DEFAULT CURRENT_TIMESTAMP
);

-- Índice por cédula (búsquedas frecuentes)
CREATE INDEX idx_pacientes_cedula ON pacientes(cedula);
```

---

## Consultas Utilizadas

### Verificar login
```sql
SELECT * FROM usuarios
WHERE usuario = %s AND contrasena = %s;
```
*Usado en:* `verificar_login()` — `src/database.py:74`

### Verificar si un usuario existe
```sql
SELECT 1 FROM usuarios WHERE usuario = %s;
```
*Usado en:* `usuario_existe()` — `src/database.py` (previene duplicados al registrar).

### Crear un usuario nuevo
```sql
INSERT INTO usuarios (usuario, contrasena) VALUES (%s, %s) RETURNING id;
```
*Usado en:* `crear_usuario()` — `src/database.py`. Captura `UniqueViolation` si el usuario ya existe.

### Listar pacientes
```sql
SELECT * FROM pacientes ORDER BY id DESC;
```
*Usado en:* `get_pacientes()` — `src/database.py:30`

### Crear paciente
```sql
INSERT INTO pacientes (cedula, nombre, apellido, telefono, diagnostico, tratamiento)
VALUES (%s, %s, %s, %s, %s, %s)
RETURNING id;
```
*Usado en:* `crear_paciente()` — `src/database.py:44`

### Obtener datos completos de un paciente
```sql
SELECT * FROM pacientes WHERE id = %s;
```
*Usado en:* `MainWindow.generar_receta()` — `src/main.py`

### Cargar diagnóstico y tratamiento al seleccionar
```sql
SELECT diagnostico, tratamiento FROM pacientes WHERE id = %s;
```
*Usado en:* `MainWindow.on_paciente_seleccionado()` — `src/main.py`

---

## Datos de Prueba (Opcional)

```sql
INSERT INTO pacientes (cedula, nombre, apellido, telefono, diagnostico, tratamiento) VALUES
    ('1234567890', 'Juan',     'Pérez García',  '300-111-2222',
     'Hipertensión arterial leve', 'Losartán 50mg cada 12 horas por 30 días.'),
    ('0987654321', 'María',    'González Ruiz', '300-333-4444',
     'Gripe común', 'Acetaminofén 500mg cada 8 horas por 5 días. Reposo.'),
    ('1122334455', 'Carlos',   'Ramírez López', '300-555-6666',
     'Diabetes tipo 2', 'Metformina 850mg cada 12 horas con las comidas.');
```

---

## Diagrama Relacional

```
usuarios                          pacientes
─────────                          ─────────
PK  id              ───┐    ┌───  PK  id
    usuario              │    │       cedula (UNIQUE)
    contrasena           │    │       nombre
    created_at           │    │       apellido
                         │    │       telefono
                         │    │       diagnostico
                         │    │       tratamiento
                         │    │       created_at
                         │    │       updated_at
                         │    │
                    (sin relación directa;
                     autenticación y datos
                     clínicos independientes)
```

> En esta versión demo no hay relación FK entre `usuarios` y `pacientes`. Una mejora futura sería añadir una columna `medico_id` en `pacientes` para auditoría.
