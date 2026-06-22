# 🏗️ Arquitectura

Documento que describe cómo está organizado el código, el flujo de datos entre módulos y los patrones utilizados.

---

## 📐 Vista General

NeuroMedic sigue una arquitectura simple en capas, sin framework web:

```
┌────────────────────────────────────────┐
│          Capa de Presentación          │
│  PyQt6 (LoginWindow, MainWindow)       │
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
│  psycopg2 (database.py)                │
│  PostgreSQL                            │
└────────────────────────────────────────┘
```

---

## 🧩 Módulos

### `src/main.py` — Entry point y UI
- **Entry point:** `if __name__ == '__main__':`
- **Carga estilos** desde `src/styles.qss` y los aplica con `app.setStyleSheet()` **antes** de mostrar la ventana.
- **Clases:**
  - `LoginWindow(QWidget)` — Formulario de autenticación.
  - `MainWindow(QMainWindow)` — Ventana principal con tabla de pacientes y formulario.
- **Conexiones clave:**
  - `self.receta_btn.clicked.connect(self.generar_receta)` → Ticket #7
  - `self.table.clicked.connect(self.on_paciente_seleccionado)` → carga datos del paciente seleccionado

### `src/database.py` — Persistencia
Funciones públicas:
- `get_connection()` → contexto de conexión.
- `verificar_login(usuario, contraseña)` → valida credenciales.
- `get_pacientes()` → lista todos los pacientes.
- `crear_paciente(data)` → inserta un paciente.

Usa `RealDictCursor` para devolver resultados como diccionarios (compatibles con Jinja2).

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
- Menús, scrollbars, status bar, splitters, group boxes.
- Override `#loginWindow` con inputs más grandes.

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

### Flujo de Carga de Pacientes
```
MainWindow.__init__()
  └─► cargar_pacientes()
        └─► get_pacientes()                  [database.py]
              └─► QTableWidget.setItem(...)  por cada fila
```

### Flujo de Selección
```
table.clicked
  └─► on_paciente_seleccionado()
        └─► SELECT diagnostico, tratamiento WHERE id = ?
        └─► Rellena formulario con datos
```

### Flujo de Generación de Receta (Ticket #7)
```
receta_btn.clicked
  └─► generar_receta()
        ├─► Valida que haya paciente seleccionado
        ├─► SELECT * FROM pacientes WHERE id = ?
        ├─► generar_receta_pdf(dict(paciente))   [pdf_generator.py]
        │     ├─► Carga templates/receta_template.html
        │     ├─► Template(html).render(...)
        │     ├─► HTML(string=...).write_pdf(ruta)
        │     └─► abrir_archivo(ruta)            [multiplataforma]
        └─► QMessageBox.information("Éxito", ruta)
```

---

## 🧪 Patrones y Decisiones

- **Sin frameworks pesados:** se eligió mantener dependencias mínimas (sin Django, Flask, SQLAlchemy) para que la demo sea fácil de ejecutar.
- **Diccionarios como DTOs:** los cursores devuelven `RealDictCursor`, lo que permite pasar directamente los datos a Jinja2 sin transformaciones.
- **Estilos centralizados:** todo el QSS vive en un solo archivo para facilitar ajustes visuales.
- **Multiplataforma explícito:** `pdf_generator.py` detecta el SO y elige el comando de apertura correcto (`startfile`, `open`, `xdg-open`).
- **Rutas absolutas:** `pdf_generator.py` calcula `BASE_DIR` con `os.path.dirname(os.path.dirname(__file__))` para que funcione sin importar desde dónde se ejecute el script.

---

## 🔮 Mejoras Futuras

- Separar la UI en módulos (login, main, dialogs) si crece.
- Mover la configuración a un archivo `.env` y leerlo con `python-dotenv`.
- Añadir tests unitarios (Ticket #8): pytest + pytest-qt.
- Empaquetar la aplicación con PyInstaller para distribuirla.
