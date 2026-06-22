"""
============================================================
NEUROMEDIC - Generador de Recetas en PDF
Ticket #7

Renderiza una plantilla HTML con Jinja2 y la convierte a PDF
usando WeasyPrint. Compatible con Linux, macOS y Windows.
============================================================
"""

import os
import platform
import subprocess
from datetime import datetime

from jinja2 import Template
from weasyprint import HTML


# ============================================================
# CONFIGURACIÓN DE RUTAS
# =========================================================
# pdf_generator.py vive en src/, así que la raíz del proyecto
# es el directorio padre de src/.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, 'templates')
RECETAS_DIR = os.path.join(BASE_DIR, 'recetas')


# ============================================================
# APERTURA MULTIPLATAFORMA
# =========================================================
def abrir_archivo(ruta):
    """Abre un archivo con el visor predeterminado del sistema."""
    sistema = platform.system()
    try:
        if sistema == 'Windows':
            os.startfile(ruta)  # type: ignore[attr-defined]
        elif sistema == 'Darwin':  # macOS
            subprocess.Popen(['open', ruta])
        else:  # Linux y otros Unix
            subprocess.Popen(['xdg-open', ruta])
    except Exception as e:
        print(f"⚠️ No se pudo abrir el PDF automáticamente: {e}")


# ============================================================
# FUNCIÓN PRINCIPAL
# =========================================================
def generar_receta_pdf(paciente_data):
    """
    Genera una receta médica en PDF a partir de los datos del paciente.

    Args:
        paciente_data (dict): diccionario con los datos del paciente.
            Claves esperadas: nombre, apellido, cedula, telefono,
            diagnostico, tratamiento.

    Returns:
        str | None: ruta absoluta del PDF generado, o None si hubo error.
    """
    try:
        # 1. Asegurar que la carpeta de salida exista
        os.makedirs(RECETAS_DIR, exist_ok=True)

        # 2. Cargar la plantilla HTML
        template_path = os.path.join(TEMPLATES_DIR, 'receta_template.html')
        with open(template_path, 'r', encoding='utf-8') as f:
            template_html = f.read()

        # 3. Renderizar con los datos del paciente
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

        # 4. Generar nombre del archivo: receta_{cedula}_{YYYYMMDD_HHMMSS}.pdf
        cedula_limpia = (paciente_data.get('cedula') or 'sin_cedula').replace(' ', '_')
        nombre_archivo = (
            f"receta_{cedula_limpia}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        )
        ruta_pdf = os.path.join(RECETAS_DIR, nombre_archivo)

        # 5. Convertir HTML a PDF con WeasyPrint
        HTML(string=html_rendered).write_pdf(ruta_pdf)

        # 6. Abrir el PDF con el visor predeterminado
        abrir_archivo(ruta_pdf)

        return ruta_pdf

    except FileNotFoundError as e:
        print(f"❌ Archivo no encontrado: {e}")
        return None
    except Exception as e:
        print(f"❌ Error al generar PDF: {e}")
        return None
