"""
============================================================
NEUROMEDIC - Generador de Recetas en PDF
Ticket #7

Renderiza una plantilla HTML con Jinja2 y la convierte a PDF
usando WeasyPrint. Compatible con Linux, macOS, Windows y
con ejecutables congelados por PyInstaller.
============================================================
"""

import os
import platform
import subprocess
import sys
from datetime import datetime

from jinja2 import Template
from weasyprint import HTML

def setup_dll_paths():
    """Agrega la carpeta de DLLs al PATH si estamos en un .exe"""
    if getattr(sys, 'frozen', False):
        # Estamos en el .exe
        base_dir = os.path.dirname(sys.executable)
        dll_dir = os.path.join(base_dir, 'libs')  # Cambiar a '.' si usas --add-binary sin carpeta
        if os.path.exists(dll_dir):
            os.environ['PATH'] = dll_dir + os.pathsep + os.environ['PATH']
        
        # También configurar WEASYPRINT_DLL_DIRECTORIES
        if os.path.exists(dll_dir):
            os.environ['WEASYPRINT_DLL_DIRECTORIES'] = dll_dir
setup_dll_paths()
# ============================================================
# CONFIGURACIÓN DE RUTAS
# ============================================================
def _app_dir():
    """Directorio base de la app.

    - Congelada por PyInstaller: carpeta donde está el .exe.
    - Modo desarrollo: raíz del proyecto (un nivel arriba de src/).
    """
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def _resource_path(rel):
    """Devuelve la ruta a un recurso, funcione desde .exe o desde script.

    - Congelada por PyInstaller: los recursos se incluyen con --add-data
      y se desempaquetan en sys._MEIPASS.
    - Modo desarrollo: la estructura del proyecto se mantiene igual que
      en el bundle (templates/ y styles.qss junto a src/main.py).
    """
    if getattr(sys, 'frozen', False):
        base = sys._MEIPASS  # type: ignore[attr-defined]
    else:
        # Modo desarrollo: BASE_DIR es la raíz del proyecto (un nivel
        # arriba de src/, donde vive este archivo).
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, rel)


APP_DIR = _app_dir()
TEMPLATES_DIR = os.path.join(APP_DIR, 'templates')
RECETAS_DIR = os.path.join(APP_DIR, 'recetas')


# ============================================================
# APERTURA MULTIPLATAFORMA
# ============================================================
def abrir_archivo(ruta):
    """Abre un archivo con el visor predeterminado del sistema."""
    sistema = platform.system()
    try:
        if sistema == 'Windows':
            os.startfile(ruta)  # type: ignore[attr-defined]
        elif sistema == 'Darwin':
            subprocess.Popen(['open', ruta])
        else:
            subprocess.Popen(['xdg-open', ruta])
    except Exception as e:
        print(f"No se pudo abrir el PDF automáticamente: {e}")


# ============================================================
# FUNCIÓN PRINCIPAL
# ============================================================
def generar_receta_pdf(paciente_data):
    """
    Genera una receta médica en PDF a partir de los datos del paciente.

    Args:
        paciente_data (dict): claves esperadas: nombre, apellido, cedula,
            telefono, diagnostico, tratamiento.

    Returns:
        str | None: ruta absoluta del PDF generado, o None si hubo error.
    """
    try:
        # 1. Carpeta de salida
        os.makedirs(RECETAS_DIR, exist_ok=True)

        # 2. Cargar plantilla (compatible con .exe congelado)
        template_path = _resource_path(os.path.join('templates', 'receta_template.html'))
        with open(template_path, 'r', encoding='utf-8') as f:
            template_html = f.read()

        # 3. Renderizar con Jinja2
        template = Template(template_html)
        fecha_actual = datetime.now().strftime('%d/%m/%Y %H:%M')

        html_rendered = template.render(
            nombre=paciente_data.get('nombre', ''),
            apellido=paciente_data.get('apellido', ''),
            cedula=paciente_data.get('cedula', ''),
            telefono=paciente_data.get('telefono', ''),
            diagnostico=paciente_data.get('diagnostico') or 'No especificado',
            tratamiento=paciente_data.get('tratamiento') or 'No especificado',
            fecha=fecha_actual,
            medico='Dr. Luis Díaz',
        )

        # 4. Nombre del archivo
        cedula_limpia = (paciente_data.get('cedula') or 'sin_cedula').replace(' ', '_')
        nombre_archivo = (
            f"receta_{cedula_limpia}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        ruta_pdf = os.path.join(RECETAS_DIR, nombre_archivo)

        # 5. Convertir HTML → PDF
        HTML(string=html_rendered).write_pdf(ruta_pdf)

        # 6. Abrir con el visor predeterminado
        abrir_archivo(ruta_pdf)

        return ruta_pdf

    except FileNotFoundError as e:
        print(f"Archivo no encontrado: {e}")
        return None
    except Exception as e:
        print(f"Error al generar PDF: {e}")
        return None
