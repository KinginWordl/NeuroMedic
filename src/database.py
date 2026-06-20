import psycopg2
from psycopg2 import extras

# ============================================================
# CONFIGURACIÓN DE LA BASE DE DATOS
# ============================================================
DB_CONFIG = {
    'dbname': 'demoneuromedic',
    'user': 'luntony',
    'password': 'cumple0505',  # <--- CAMBIA ESTO
    'host': 'localhost',
    'port': 5432
}

# ============================================================
# FUNCIÓN: Obtener conexión
# ============================================================
def get_connection():
    """Retorna una conexión a PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        print(f"Error de conexión: {e}")
        return None

# ============================================================
# FUNCIÓN: Obtener todos los pacientes
# ============================================================
def get_pacientes():
    """Retorna lista de todos los pacientes"""
    try:
        with get_connection() as conn:
            with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                cur.execute("SELECT * FROM pacientes ORDER BY id DESC")
                return cur.fetchall()
    except Exception as e:
        print(f"Error al obtener pacientes: {e}")
        return []

# ============================================================
# FUNCIÓN: Crear nuevo paciente
# ============================================================
def crear_paciente(data):
    """
    Inserta un nuevo paciente
    data: diccionario con cedula, nombre, apellido, telefono, diagnostico, tratamiento
    """
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    INSERT INTO pacientes (cedula, nombre, apellido, telefono, diagnostico, tratamiento)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    RETURNING id
                """, (
                    data['cedula'],
                    data['nombre'],
                    data['apellido'],
                    data.get('telefono', ''),
                    data.get('diagnostico', ''),
                    data.get('tratamiento', '')
                ))
                result = cur.fetchone()
                conn.commit()
                return result[0] if result else None
    except Exception as e:
        print(f"Error al crear paciente: {e}")
        return None

# ============================================================
# FUNCIÓN: Verificar login
# ============================================================
def verificar_login(usuario, contrasena):
    """Valida las credenciales del usuario"""
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT * FROM usuarios WHERE usuario = %s AND contrasena = %s",
                    (usuario, contrasena)
                )
                result = cur.fetchone()
                return result is not None
    except Exception as e:
        print(f"Error al verificar login: {e}")
        return False

# ============================================================
# PRUEBA RÁPIDA (ejecutar solo si se corre este archivo directamente)
# ============================================================
if __name__ == '__main__':
    # Probar conexión
    print("🔌 Probando conexión...")
    conn = get_connection()
    if conn:
        print("Conexión exitosa")
        conn.close()
    
    # Probar get_pacientes()
    print("\nLista de pacientes:")
    pacientes = get_pacientes()
    for p in pacientes:
        print(f"  - {p['nombre']} {p['apellido']} ({p['cedula']})")
    
    # Probar verificar_login()
    print("\nProbando login:")
    print(f"  doctor/demo123: {verificar_login('doctor', 'demo123')}")
    print(f"  doctor/incorrecta: {verificar_login('doctor', 'incorrecta')}")