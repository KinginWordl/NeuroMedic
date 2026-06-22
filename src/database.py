"""
============================================================
NEUROMEDIC - Capa de Persistencia (SQLite)
============================================================

Base de datos SQLite portable: un solo archivo en data/neuromedic.db.
Las tablas se crean automáticamente al primer arranque.
"""

import os
import sqlite3

# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
# La BD se guarda junto al .exe (modo portable) o en la raíz del
# proyecto (modo desarrollo).
def _data_dir():
    """Devuelve la ruta del directorio de datos.

    - Si el programa corre congelado por PyInstaller, usa la carpeta
      junto al .exe (modo portable).
    - Si corre como script, usa la carpeta data/ del proyecto.
    """
    if getattr(os.sys, 'frozen', False):
        # Ejecutable: la BD junto al .exe
        return os.path.dirname(os.sys.executable)
    return os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'data')


DATA_DIR = _data_dir()
DB_PATH = os.path.join(DATA_DIR, 'neuromedic.db')


# ============================================================
# CONEXIÓN
# ============================================================
def get_connection():
    """Abre una conexión a la BD SQLite y devuelve la fila como diccionario."""
    os.makedirs(DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # filas accesibles por nombre de columna
    return conn


# ============================================================
# INICIALIZACIÓN DE ESQUEMA
# ============================================================
def init_db():
    """Crea las tablas si no existen y un usuario por defecto."""
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id          INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario     TEXT NOT NULL UNIQUE,
                contrasena  TEXT NOT NULL,
                created_at  TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE TABLE IF NOT EXISTS pacientes (
                id           INTEGER PRIMARY KEY AUTOINCREMENT,
                cedula       TEXT NOT NULL UNIQUE,
                nombre       TEXT NOT NULL,
                apellido     TEXT NOT NULL,
                telefono     TEXT,
                diagnostico  TEXT,
                tratamiento  TEXT,
                created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cur.execute("""
            CREATE INDEX IF NOT EXISTS idx_pacientes_cedula
            ON pacientes(cedula)
        """)

        # Usuario por defecto para la demo
        cur.execute("SELECT 1 FROM usuarios WHERE usuario = ?", ('doctor',))
        if cur.fetchone() is None:
            cur.execute(
                "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?)",
                ('doctor', 'demo123')
            )
            print("✅ Usuario por defecto creado: doctor / demo123")

        conn.commit()


# Inicializar la BD al importar el módulo
init_db()


# ============================================================
# HELPERS
# ============================================================
def _row_to_dict(row):
    """Convierte una sqlite3.Row en dict (None si es None)."""
    return dict(row) if row is not None else None


# ============================================================
# FUNCIONES PÚBLICAS
# ============================================================
def verificar_login(usuario, contrasena):
    """Valida las credenciales del usuario."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "SELECT * FROM usuarios WHERE usuario = ? AND contrasena = ?",
                (usuario, contrasena)
            )
            return cur.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar login: {e}")
        return False


def usuario_existe(usuario):
    """Devuelve True si ya existe un usuario con ese nombre."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM usuarios WHERE usuario = ?", (usuario,))
            return cur.fetchone() is not None
    except Exception as e:
        print(f"Error al verificar usuario: {e}")
        return False


def crear_usuario(usuario, contrasena):
    """Crea un usuario nuevo. Devuelve el id creado o None si ya existe."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute(
                "INSERT INTO usuarios (usuario, contrasena) VALUES (?, ?) RETURNING id",
                (usuario, contrasena)
            )
            row = cur.fetchone()
            conn.commit()
            return row[0] if row else None
    except sqlite3.IntegrityError:
        print(f"Error: el usuario '{usuario}' ya existe.")
        return None
    except Exception as e:
        print(f"Error al crear usuario: {e}")
        return None


def get_pacientes():
    """Retorna lista de todos los pacientes (ordenados por id desc)."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pacientes ORDER BY id DESC")
            return [_row_to_dict(row) for row in cur.fetchall()]
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return []


def crear_paciente(data):
    """Inserta un nuevo paciente. Devuelve el id o None si hay error."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO pacientes
                    (cedula, nombre, apellido, telefono, diagnostico, tratamiento)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                data['cedula'],
                data['nombre'],
                data['apellido'],
                data.get('telefono', ''),
                data.get('diagnostico', ''),
                data.get('tratamiento', ''),
            ))
            new_id = cur.lastrowid
            conn.commit()
            return new_id
    except sqlite3.IntegrityError:
        print(f"Error: la cédula '{data.get('cedula')}' ya está registrada.")
        return None
    except Exception as e:
        print(f"Error al crear paciente: {e}")
        return None


def actualizar_paciente(paciente_id, data):
    """Actualiza un paciente existente. Devuelve True si OK."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("""
                UPDATE pacientes
                SET cedula=?, nombre=?, apellido=?,
                    telefono=?, diagnostico=?, tratamiento=?,
                    updated_at=CURRENT_TIMESTAMP
                WHERE id=?
            """, (
                data['cedula'],
                data['nombre'],
                data['apellido'],
                data.get('telefono', ''),
                data.get('diagnostico', ''),
                data.get('tratamiento', ''),
                paciente_id,
            ))
            conn.commit()
            return cur.rowcount > 0
    except Exception as e:
        print(f"Error al actualizar paciente: {e}")
        return False


def get_paciente_by_id(paciente_id):
    """Devuelve un paciente por id, o None si no existe."""
    try:
        with get_connection() as conn:
            cur = conn.cursor()
            cur.execute("SELECT * FROM pacientes WHERE id = ?", (paciente_id,))
            return _row_to_dict(cur.fetchone())
    except Exception as e:
        print(f"Error al obtener paciente: {e}")
        return None