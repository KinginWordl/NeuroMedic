# 🏗️ Arquitectura

Documento que describe cómo está organizado el código, el flujo de datos entre módulos y los patrones utilizados.

---

## 📐 Vista General

NeuroMedic sigue una arquitectura simple en capas, sin framework web:

```
┌────────────────────────────────────────┐
│          Capa de Presentación          │
│  PyQt6 (LoginWindow, MainWindow,       │
│  CrearCuentaDialog, PacienteDialog)    │
│  Estilos QSS (styles.qss)              │
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│          Capa de Lógica                │
│  generar_receta_pdf() (Jinja2+WeasyPrint)│
└────────────────┬───────────────────────┘
                 │
┌────────────────▼───────────────────────┐
│          Capa de Datos                 │
│  sqlite3 (database.py)                 │
│  SQLite (archivo neuromedic.db)        │
└────────────────────────────────────────┘
```

---

## 🧩 Módulos

### `src/main.py` — Entry point y UI
- **Entry point:** `if __name__ == '__main__':`
- **Carga estilos** desde `src/styles.qss` y los aplica con `app.setStyleSheet()` **antes** de mostrar la ventana.
- **Clases (4):**
  - `LoginWindow(QWidget)` — Formulario de autenticación + botón "Crear cuenta".
  - `CrearCuentaDialog(QDialog)` — Modal para registrar un usuario nuevo.
  - `MainWindow(QMainWindow)` — Buscador + tabla de pacientes + botones de acción.
  - `PacienteDialog(QDialog)` — Modal con el formulario completo del paciente (modo `nuevo` o `editar`).
- **Atajos de teclado:** `Ctrl+S` en `PacienteDialog` guarda.
- **Doble clic** en una fila de la tabla abre el paciente en modo edición.

### `src/database.py` — Persistencia (SQLite portable)
- `get_connection()` → abre conexión a `neuromedic.db`, filas como `dict` vía `sqlite3.Row`.
- `init_db()` → crea tablas `usuarios` y `pacientes` (e índice por cédula) si no existen. Inserta usuario demo `doctor / demo123` la primera vez.
- `verificar_login(usuario, contraseña)` → valida credenciales.
- `crear_usuario(usuario, contraseña)` → registra un usuario nuevo.
- `usuario_existe(usuario)` → previene duplicados.
- `get_pacientes()` → lista todos los pacientes (orden desc por id).
- `crear_paciente(data)` / `actualizar_paciente(id, data)` / `get_paciente_by_id(id)` → CRUD de pacientes.
- La BD se guarda junto al `.exe` (modo portable) o en `data/` (modo desarrollo).

### `src/pdf_generator.py` — Generación de PDF (Ticket #7)
- `generar_receta_pdf(paciente_data: dict) -> str | None`
  1. Crea la carpeta `recetas/` si no existe.
  2. Lee `templates/receta_template.html`.
  3. Renderiza con Jinja2 inyectando los datos del paciente.
  4. Convierte el HTML a PDF con WeasyPrint.
  5. Abre el PDF con el visor predeterminado del sistema.
- `abrir_archivo(ruta)` — helper multiplataforma (Windows/macOS/Linux).

### `src/styles.qss` — Estilos (Ticket #6)
Hoja de estilos con paleta profesional (azul corporativo, gris neutro, blanco + acento verde-azulado médico). Aplica a:
- Botones (con hover, pressed, disabled y variantes `#accent`, `#danger`).
- Campos de texto (con focus visible y padding compensado).
- Tabla (filas alternadas vía `setAlternatingRowColors(True)`).
- Menús, scrollbars, status bar, splitters, group boxes, separadores (QFrame HLine/VLine).
- Overrides por `objectName`:
  - `#loginWindow` — inputs grandes.
  - `#crearCuentaDialog` — estilo coherente con login.
  - `#pacienteDialog` — títulos azules, text-areas con focus.

### `templates/receta_template.html` — Plantilla PDF
HTML estático con CSS embebido. Variables Jinja2:
- `{{ nombre }}`, `{{ apellido }}`, `{{ cedula }}`, `{{ telefono }}`
- `{{ diagnostico }}`, `{{ tratamiento }}`
- `{{ fecha }}` — fecha/hora de emisión
- `{{ medico }}` — nombre del médico (hardcoded a `Dr. Luis Díaz`)

---

## 🔄 Flujos Principales

### Flujo de Login
```
LoginWindow.login()
  └─► verificar_login(usuario, contraseña)   [database.py]
        ├─► éxito  → crea MainWindow, .show(), .close()
        └─► error  → QMessageBox.warning
```

### Flujo de Crear Cuenta
```
LoginWindow.abrir_crear_cuenta()
  └─► CrearCuentaDialog.exec()
        ├─► Validar: usuario/contraseña no vacíos, contraseña ≥ 4 chars, confirmación coincide
        ├─► usuario_existe(usuario)           [database.py]
        ├─► crear_usuario(usuario, contraseña) [database.py]
        └─► accept()  → vuelve al login
```

### Flujo de la Ventana Principal
```
MainWindow.__init__()
  └─► cargar_pacientes()
        └─► get_pacientes()                   [database.py]
        └─► _aplicar_filtro("")               [pinta todas las filas]

buscar_input.textChanged
  └─► buscar_pacientes(texto)
        └─► _aplicar_filtro(texto)
              └─► Filtra por cédula / nombre / apellido (en memoria)

table.doubleClicked / editar_btn.clicked
  └─► abrir_editar()
        └─► PacienteDialog(modo="editar", paciente_id)
              ├─► Cargar datos desde BD
              ├─► guardar() → UPDATE pacientes WHERE id
              └─► generar_receta() → generar_receta_pdf() [pdf_generator.py]

nuevo_btn.clicked
  └─► abrir_nuevo()
        └─► PacienteDialog(modo="nuevo")
              └─► guardar() → crear_paciente() [database.py]

receta_btn.clicked
  └─► abrir_generar_receta()
        └─► PacienteDialog(modo="editar")     [el botón "Generar Receta" está dentro del diálogo]
```

---

## 🧪 Patrones y Decisiones

- **Sin frameworks pesados:** se eligió mantener dependencias mínimas (sin Django, Flask, SQLAlchemy) para que la demo sea fácil de ejecutar.
- **Diccionarios como DTOs:** los cursores devuelven `RealDictCursor`, lo que permite pasar directamente los datos a Jinja2 sin transformaciones.
- **Búsqueda en memoria:** la lista de pacientes se carga una vez y el filtrado se hace en cliente. Para una BD grande se migraría a `WHERE cedula LIKE ? OR nombre LIKE ?`.
- **Modales para edición:** `PacienteDialog` y `CrearCuentaDialog` aíslan tareas complejas fuera de la ventana principal, manteniéndola limpia.
- **Estilos centralizados:** todo el QSS vive en un solo archivo para facilitar ajustes visuales.
- **Multiplataforma explícito:** `pdf_generator.py` detecta el SO y elige el comando de apertura correcto (`startfile`, `open`, `xdg-open`).
- **Rutas absolutas:** `pdf_generator.py` calcula `BASE_DIR` con `os.path.dirname(os.path.dirname(__file__))` para que funcione sin importar desde dónde se ejecute el script.
- **Atajos de teclado:** `Ctrl+S` en `PacienteDialog` para guardar sin usar el ratón.

---

## 🔮 Mejoras Futuras

- Persistir contraseñas con `bcrypt` o `argon2`.
- Migrar la búsqueda a SQL con `LIKE` cuando la tabla crezca.
- Añadir paginación a la tabla.
- ~~Empaquetar la aplicación con PyInstaller.~~ ✅ Hecho (ver sección Distribución portable).
- Añadir un historial de recetas generadas por paciente.

---

## 📦 Distribución portable (PyInstaller)

La aplicación detecta automáticamente si está corriendo como script o congelada por PyInstaller:

```python
if getattr(sys, 'frozen', False):
    # Modo .exe: usar sys._MEIPASS para recursos, sys.executable para BD/recetas
else:
    # Modo desarrollo: rutas relativas al código fuente
```

Esto permite distribuir **un solo archivo `.exe`** que:
- Crea `neuromedic.db` (SQLite) junto al .exe en la primera ejecución.
- Genera PDFs en una carpeta `recetas/` también junto al .exe.
- Carga estilos y plantillas desde el bundle temporal (`sys._MEIPASS`).

### Construir el .exe

```bash
pyinstaller NeuroMedic.spec
```

El archivo `NeuroMedic.spec` incluye:
- Modo `--onefile` (un solo archivo .exe).
- Modo `--windowed` / `console=False` (sin consola en Windows).
- Recursos empaquetados: `styles.qss`, `templates/receta_template.html`.
- Exclusiones: `tkinter`, `matplotlib`, `numpy`, `pandas` (para reducir tamaño).

> ⚠️ El `.exe` en Linux mide ~74 MB. En Windows suele ser ~150 MB porque incluye las DLLs de PyQt6 y WeasyPrint.
> 📄 La guía paso a paso para compilar en Windows está en [`BUILD_WINDOWS.md`](../BUILD_WINDOWS.md).
