# 🩺 NeuroMedic - Demo Consultorio Médico

Aplicación de escritorio para la gestión de pacientes y generación de recetas médicas en PDF, con interfaz moderna pensada para consultorios particulares.

> **Estado:** Demo funcional · 7/9 tickets completados

---

## ✨ Características

- 🔐 **Login de usuario** con credenciales almacenadas en PostgreSQL.
- 📋 **Gestión de pacientes** (registro, consulta y selección desde tabla).
- 📄 **Generación de recetas en PDF** con plantilla HTML profesional (WeasyPrint + Jinja2).
- 🎨 **Interfaz moderna** con hoja de estilos QSS (azul corporativo, bordes redondeados, filas alternadas).
- 🗄️ **Persistencia en PostgreSQL** vía `psycopg2`.
- 🖥️ **Multiplataforma**: abre el PDF generado con el visor predeterminado del sistema (Windows / macOS / Linux).

---

## 🧰 Stack Tecnológico

| Capa | Tecnología | Uso |
|------|-----------|-----|
| UI | PyQt6 | Ventanas, layouts, estilos QSS |
| Persistencia | PostgreSQL 15 | Base de datos relacional |
| Conector | psycopg2-binary | Acceso a PostgreSQL desde Python |
| Plantillas | Jinja2 | Renderizado de HTML dinámico |
| PDF | WeasyPrint 69 | Conversión HTML → PDF |
| Lenguaje | Python 3.8+ | — |

---

## 📦 Requisitos

- Python 3.8 o superior
- PostgreSQL 15 o superior (en ejecución local)
- Sistema operativo: **Windows 10+**, **Linux** o **macOS**
- Dependencias nativas de WeasyPrint (Pango, Cairo, GDK-Pixbuf) — ver [Troubleshooting](#-troubleshooting)

---

## 🚀 Instalación

### 1. Clonar el repositorio
```bash
git clone <url-del-repo>
cd NeuroMedic
```

### 2. Crear y activar entorno virtual
```bash
python3 -m venv .venv
source .venv/bin/activate          # Linux / macOS
# .venv\Scripts\activate           # Windows
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar PostgreSQL
- Crear la base de datos `demoneuromedic`.
- Crear las tablas `usuarios` y `pacientes` (ver [`docs/DATABASE.md`](docs/DATABASE.md)).
- Insertar un usuario inicial (`doctor` / `demo123` por defecto para la demo).

### 5. Ajustar credenciales
Edita `src/database.py` si tu usuario/contraseña de PostgreSQL difieren:
```python
DB_CONFIG = {
    'dbname': 'demoneuromedic',
    'user': 'tu_usuario',
    'password': 'tu_contraseña',
    'host': 'localhost',
    'port': 5432,
}
```

---

## ▶️ Uso

```bash
source .venv/bin/activate
python src/main.py
```

### Flujo de la aplicación
1. **Login** — Usuario: `doctor` · Contraseña: `demo123`
2. **Ventana principal** — Se muestra la lista de pacientes.
3. **Seleccionar paciente** en la tabla → se cargan sus datos en el formulario.
4. **Generar Receta** → se crea un PDF en `recetas/receta_{cedula}_{fecha}.pdf` y se abre automáticamente.

---

## 📁 Estructura del Proyecto

```
NeuroMedic/
├── src/
│   ├── main.py            # Ventanas Login + MainWindow (entrypoint)
│   ├── database.py        # Conexión y consultas a PostgreSQL
│   ├── pdf_generator.py   # Generación de PDF con WeasyPrint
│   └── styles.qss         # Hoja de estilos QSS (Ticket #6)
├── templates/
│   └── receta_template.html  # Plantilla HTML de la receta
├── recetas/                  # PDFs generados (ignorado por git)
│   └── .gitkeep
├── docs/                     # Documentación extendida
│   ├── ARCHITECTURE.md
│   ├── DATABASE.md
│   ├── TICKETS.md
│   └── ideas.md
├── tests/                    # Tests (pendiente Ticket #8)
├── data/                     # Datos auxiliares
├── requirements.txt
├── .gitignore
└── README.md
```

---

## 📚 Documentación Adicional

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — Arquitectura y flujo de datos.
- [`docs/DATABASE.md`](docs/DATABASE.md) — Esquema de la base de datos.
- [`docs/TICKETS.md`](docs/TICKETS.md) — Estado y resumen de cada ticket.
- [`docs/ideas.md`](docs/ideas.md) — Contexto general y planificación.

---

## 🧪 Troubleshooting

### WeasyPrint no genera el PDF
Instala las dependencias nativas:
- **Ubuntu/Debian**: `sudo apt install libpango-1.0-0 libpangoft2-1.0-0`
- **macOS**: `brew install pango`
- **Windows**: WeasyPrint 69 trae binarios precompilados en muchos casos; si falla, instala GTK3 runtime desde [gtk.org](https://www.gtk.org/docs/installations/windows/).

### PostgreSQL no conecta
- Verifica que el servicio esté corriendo: `sudo systemctl status postgresql`
- Revisa credenciales en `src/database.py`.
- Asegúrate de que la base `demoneuromedic` exista: `psql -l`

### El PDF no se abre automáticamente
- El sistema no tiene un visor PDF predeterminado. Instala uno (Evince, Adobe Reader, etc.) o abre el archivo desde la carpeta `recetas/`.

### Estilos QSS no se aplican
- Confirma que `src/styles.qss` existe y que `app.setStyleSheet(estilo)` se llama **antes** de `window.show()` en `main.py`.
- Verifica que no haya errores en consola al cargar el archivo.

---

## 🤝 Contribución

1. Crea una rama desde `main`: `git checkout -b feature/mi-mejora`
2. Realiza commits descriptivos.
3. Asegúrate de que el código compile: `python -m py_compile src/*.py`
4. Abre un Pull Request.

---

## 📝 Licencia

Proyecto demo de uso privado.
