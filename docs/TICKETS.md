# 🎯 Tickets - Estado del Proyecto

Historial y resumen de cada ticket del proyecto NeuroMedic.

---

## Estado General

| # | Ticket | Estado | Día |
|---|--------|--------|-----|
| #1 | Inicializar Proyecto y Configurar Entorno | ✅ Completado | Día 1 |
| #2 | Configurar PostgreSQL y Crear Base de Datos | ✅ Completado | Día 1 |
| #3 | Crear Módulo de Conexión a Base de Datos | ✅ Completado | Día 1 |
| #4 | Implementar Ventana de Login | ✅ Completado | Día 2 |
| #5 | Diseñar Ventana Principal | ✅ Completado | Día 2 |
| #6 | Aplicar Estilos QSS Modernos | ✅ Completado | Día 2 |
| #7 | Implementar Generador de Recetas en PDF | ✅ Completado | Día 2 |
| #8 | Pruebas de Integración y Validación | ⏳ Pendiente | Día 3 |
| #9 | Preparar Demo para Presentación | ⏳ Pendiente | Día 3 |

**Progreso:** 7/9 tickets (78%)

> 📌 **Nota:** Tras completar el ticket #7 se realizó un refactor de UX antes de la presentación final.
> Cambios fuera de tickets formales:
> - Refactor de `MainWindow`: separador entre la lista de pacientes y los formularios. Ahora la ventana principal solo muestra buscador + tabla + 3 botones (`+ Nuevo`, `✏️ Ver/Editar`, `📄 Generar Receta`).
> - `PacienteDialog` (nuevo): modal con el formulario completo del paciente, abre desde cualquier acción de la lista.
> - `CrearCuentaDialog` (nuevo): modal para registrar usuarios nuevos desde la pantalla de login.
> - Búsqueda en vivo por cédula, nombre o apellido.
> - Atajos: `Ctrl+S` para guardar en el diálogo de paciente, doble clic en la fila abre el paciente.
> Detalles en `docs/ARCHITECTURE.md`.

---

## Ticket #1 — Inicializar Proyecto y Configurar Entorno
- ✅ Creación de la estructura de directorios (`src/`, `templates/`, `recetas/`, `tests/`, `data/`, `docs/`).
- ✅ Entorno virtual `.venv/`.
- ✅ `requirements.txt` con todas las dependencias.
- ✅ `.gitignore` configurado para Python, entornos virtuales y PDFs generados.

## Ticket #2 — Configurar PostgreSQL y Crear Base de Datos
- ✅ Instalación y configuración de PostgreSQL 15.
- ✅ Creación de la base de datos `demoneuromedic`.
- ✅ Definición del esquema: tablas `usuarios` y `pacientes`.
- ✅ Índices en campos consultados frecuentemente.

## Ticket #3 — Crear Módulo de Conexión a Base de Datos
- ✅ `src/database.py` con `get_connection()`.
- ✅ Funciones: `verificar_login()`, `get_pacientes()`, `crear_paciente()`.
- ✅ Uso de `RealDictCursor` para devolver diccionarios.
- ✅ Manejo de errores con try/except y logging por consola.

## Ticket #4 — Implementar Ventana de Login
- ✅ `LoginWindow(QWidget)` en `src/main.py`.
- ✅ Campos: usuario y contraseña (con `QLineEdit.EchoMode.Password`).
- ✅ Botones: "Iniciar Sesión" y "Salir".
- ✅ Validación de campos vacíos.
- ✅ Conexión con la BD para autenticar.
- ✅ Centrado automático de la ventana en pantalla.
- ✅ Enter en los inputs dispara el login.

## Ticket #5 — Diseñar Ventana Principal
- ✅ `MainWindow(QMainWindow)` en `src/main.py`.
- ✅ Layout con `QSplitter` horizontal (40% / 60%).
- ✅ Panel izquierdo: botón "Actualizar" + tabla de pacientes.
- ✅ Panel derecho: `QGroupBox` con formulario (cédula, nombre, apellido, teléfono, diagnóstico, tratamiento).
- ✅ Botones: "Guardar Paciente" y "Generar Receta".
- ✅ Selección de fila carga los datos en el formulario.
- ✅ Tamaño inicial: 1200×700, mínimo 800×500.

## Ticket #6 — Aplicar Estilos QSS Modernos
**Tiempo estimado:** 1 hora

- ✅ `src/styles.qss` creado.
- ✅ Estilos definidos para: ventana principal, botones, campos de texto, tabla, grupos, títulos, scrollbars, menú, status bar.
- ✅ Paleta profesional: azul corporativo (#1976D2), gris neutro, blanco + acento verde-azulado médico.
- ✅ Bordes redondeados en botones (`border-radius: 8px`).
- ✅ Estados `:hover`, `:pressed`, `:disabled` implementados.
- ✅ Variantes por `objectName`: `#accent` (verde-azulado) y `#danger` (rojo).
- ✅ Tabla con colores alternados (`alternate-background-color` + `setAlternatingRowColors(True)`).
- ✅ Aplicación global con `app.setStyleSheet()`.
- ✅ Estilos cargados **antes** de `window.show()`.
- ✅ `LoginWindow` con `objectName="loginWindow"` para estilos específicos.

## Ticket #7 — Implementar Generador de Recetas en PDF
**Tiempo estimado:** 2.5 horas

- ✅ `src/pdf_generator.py` creado.
- ✅ `templates/receta_template.html` con cabecera, datos del paciente, diagnóstico, tratamiento, firma del médico y pie de página.
- ✅ Renderizado con Jinja2.
- ✅ Generación de PDF con WeasyPrint.
- ✅ Nombre de archivo: `receta_{cedula}_{YYYYMMDD_HHMMSS}.pdf` en carpeta `recetas/`.
- ✅ Apertura automática con visor predeterminado (multiplataforma: Windows/macOS/Linux).
- ✅ Botón "Generar Receta" conectado en `MainWindow.generar_receta()`.
- ✅ Validación: muestra advertencia si no hay paciente seleccionado.
- ✅ Validación: muestra error si el paciente no se encuentra en la BD.
- ✅ Mensaje de éxito con la ruta del PDF generado.
- ✅ Manejo de errores con try/except y mensaje al usuario.

## Ticket #8 — Pruebas de Integración y Validación
⏳ **Pendiente**

Plan previsto:
- Tests unitarios con `pytest` para `database.py` y `pdf_generator.py`.
- Tests de UI con `pytest-qt` para `LoginWindow` y `MainWindow`.
- Verificación de criterios de aceptación de cada ticket.

## Ticket #9 — Preparar Demo para Presentación
⏳ **Pendiente**

Plan previsto:
- Datos de prueba insertados en la BD.
- Script de arranque rápido.
- Capturas de pantalla para documentación.
- Checklist final de criterios de aceptación.

---

## 📊 Métricas del Proyecto

- **Lenguaje principal:** Python 3
- **Líneas de código (aprox.):** ~700 (sin contar QSS/HTML)
- **Archivos Python:** 3 (`main.py`, `database.py`, `pdf_generator.py`)
- **Archivos de configuración:** 3 (`requirements.txt`, `.gitignore`, `README.md`)
- **Plantillas:** 1 (`receta_template.html`)
- **Dependencias:** 4 (PyQt6, psycopg2-binary, weasyprint, jinja2)
