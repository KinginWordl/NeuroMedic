# Tickets para Demo de 3 Días - NeuroMedic

## 📋 DÍA 1: CONFIGURACIÓN Y FUNDACIONES (4-5 horas)

### 🎯 Ticket #1: Inicializar Proyecto y Configurar Entorno
**Tiempo estimado:** 1.5 horas

**Descripción:** Crear la estructura base del proyecto, instalar dependencias y configurar el entorno de desarrollo.

**Tareas:**
- [ ] Crear repositorio en GitHub (público o privado)
- [ ] Clonar localmente
- [ ] Crear estructura de carpetas:
  - `src/` (código fuente)
  - `templates/` (plantillas HTML para PDF)
  - `docs/` (documentación)
- [ ] Crear `requirements.txt` con: PyQt6, psycopg2-binary, weasyprint, jinja2
- [ ] Instalar dependencias: `pip install -r requirements.txt`
- [ ] Crear `README.md` con descripción del proyecto
- [ ] Crear `.gitignore` para Python, PostgreSQL, y archivos temporales
- [ ] Hacer commit inicial

**Criterios de Aceptación:**
- ✅ Estructura de carpetas creada
- ✅ `pip install` funciona sin errores
- ✅ Repositorio configurado correctamente

---

### 🗄️ Ticket #2: Configurar PostgreSQL y Crear Base de Datos
**Tiempo estimado:** 1.5 horas

**Descripción:** Instalar PostgreSQL, crear la base de datos demo y las tablas necesarias.

**Tareas:**
- [ ] Descargar e instalar PostgreSQL 15+ desde postgresql.org
- [ ] Instalar pgAdmin (opcional pero recomendado)
- [ ] Crear base de datos: `CREATE DATABASE demo_consultorio;`
- [ ] Crear usuario: `CREATE USER demo_user WITH PASSWORD 'demo123';`
- [ ] Conceder permisos: `GRANT ALL PRIVILEGES ON DATABASE demo_consultorio TO demo_user;`
- [ ] Ejecutar script SQL para crear:
  - Tabla `pacientes` (id, cedula, nombre, apellido, telefono, diagnostico, tratamiento, fecha_registro)
  - Tabla `usuarios` (id, usuario, contrasena)
- [ ] Insertar usuario de prueba: `doctor` / `demo123`
- [ ] Insertar 3-5 pacientes de muestra
- [ ] Verificar conexión: `psql -U demo_user -d demo_consultorio -c "SELECT * FROM pacientes;"`

**Criterios de Aceptación:**
- ✅ PostgreSQL instalado y funcionando
- ✅ Base de datos creada con tablas
- ✅ Datos de prueba insertados correctamente
- ✅ Conexión exitosa desde línea de comandos

---

### 🔌 Ticket #3: Crear Módulo de Conexión a Base de Datos
**Tiempo estimado:** 1.5 horas

**Descripción:** Implementar funciones básicas para interactuar con PostgreSQL.

**Tareas:**
- [ ] Crear `src/database.py`
- [ ] Configurar diccionario con credenciales de conexión
- [ ] Implementar función `get_connection()` que retorna conexión a PostgreSQL
- [ ] Implementar función `get_pacientes()` que retorna lista de todos los pacientes
- [ ] Implementar función `crear_paciente(data)` que inserta un nuevo paciente
- [ ] Implementar función `verificar_login(usuario, contrasena)` que valida credenciales
- [ ] Probar cada función con datos reales
- [ ] Manejar excepciones básicas (try/except)

**Criterios de Aceptación:**
- ✅ `get_pacientes()` retorna lista de pacientes
- ✅ `crear_paciente()` inserta correctamente
- ✅ `verificar_login()` funciona con credenciales correctas/incorrectas
- ✅ Errores de conexión manejados

---

## 📋 DÍA 2: INTERFAZ DE USUARIO (5-6 horas)

### 🔐 Ticket #4: Implementar Ventana de Login
**Tiempo estimado:** 2 horas

**Descripción:** Crear ventana de login con PyQt6.

**Tareas:**
- [ ] Crear `src/main.py` como punto de entrada
- [ ] Diseñar ventana de login con:
  - Título: "🩺 CONSULTORIO DR. DÍAZ"
  - Campo de texto para usuario
  - Campo de texto para contraseña (con modo password)
  - Botón "Iniciar Sesión"
  - Botón "Salir"
- [ ] Aplicar estilos básicos para que se vea profesional
- [ ] Conectar botón "Iniciar Sesión" con función `verificar_login()`
- [ ] Si login exitoso: cerrar ventana de login y abrir ventana principal
- [ ] Si login fallido: mostrar QMessageBox con error
- [ ] Permitir que la tecla Enter ejecute el login
- [ ] Establecer tamaño fijo de ventana

**Criterios de Aceptación:**
- ✅ Ventana de login se ve limpia y profesional
- ✅ Login exitoso abre ventana principal
- ✅ Login fallido muestra mensaje de error
- ✅ Enter funciona para hacer login
- ✅ Contraseña oculta con asteriscos

---

### 📊 Ticket #5: Diseñar Ventana Principal
**Tiempo estimado:** 3 horas

**Descripción:** Crear ventana principal con lista de pacientes y formulario de registro.

**Tareas:**
- [ ] En `src/main.py`, crear clase `MainWindow` que herede de QMainWindow
- [ ] Dividir la ventana en dos paneles con QSplitter:
  - **Panel izquierdo (40%):**
    - Botón "Actualizar Lista"
    - QTableWidget con columnas: ID, Cédula, Nombre, Apellido, Teléfono
    - Tabla debe seleccionar fila completa al hacer clic
  - **Panel derecho (60%):**
    - QGroupBox "Datos del Paciente"
    - Campos: Cédula, Nombre, Apellido, Teléfono, Diagnóstico (QTextEdit), Tratamiento (QTextEdit)
    - Botones: "Guardar Paciente" y "Generar Receta"
- [ ] Conectar botón "Actualizar Lista" con `cargar_pacientes()`
- [ ] Conectar evento `clicked` de la tabla con `on_paciente_seleccionado()`
- [ ] Conectar botón "Guardar Paciente" con `guardar_paciente()`
- [ ] Conectar botón "Generar Receta" con `generar_receta()`
- [ ] Implementar `cargar_pacientes()` usando `get_pacientes()`
- [ ] Implementar `guardar_paciente()` usando `crear_paciente()`
- [ ] Al guardar: limpiar formulario y actualizar tabla automáticamente

**Criterios de Aceptación:**
- ✅ Lista de pacientes se carga al abrir la ventana
- ✅ Al hacer clic en un paciente, sus datos se cargan en el formulario
- ✅ Guardar paciente inserta en base de datos
- ✅ Después de guardar, la tabla se actualiza automáticamente
- ✅ Interfaz responsive al redimensionar

---

### 🎨 Ticket #6: Aplicar Estilos QSS Modernos
**Tiempo estimado:** 1 hora

**Descripción:** Dar un acabado visual profesional a la aplicación con QSS.

**Tareas:**
- [ ] Crear `src/styles.qss`
- [ ] Definir estilos para:
  - Ventana principal y fondo
  - Botones (con hover y pressed)
  - Campos de texto
  - Tabla (alternar colores de filas)
  - Grupos y títulos
- [ ] Usar paleta de colores profesional (azul/gris/blanco)
- [ ] Agregar bordes redondeados a botones
- [ ] Aplicar estilos globalmente: `app.setStyleSheet()`
- [ ] Asegurar que los estilos se carguen antes de mostrar la ventana

**Criterios de Aceptación:**
- ✅ La aplicación se ve moderna y profesional
- ✅ Botones tienen efectos hover y pressed
- ✅ Tabla tiene colores alternados
- ✅ Texto legible y buena legibilidad

---

## 📋 DÍA 3: FUNCIONALIDADES CLAVE Y PRUEBAS (5-6 horas)

### 📄 Ticket #7: Implementar Generador de Recetas en PDF
**Tiempo estimado:** 2.5 horas

**Descripción:** Generar recetas médicas en PDF usando WeasyPrint con plantillas HTML.

**Tareas:**
- [ ] Crear `src/pdf_generator.py`
- [ ] Crear `templates/receta_template.html` con diseño profesional:
  - Cabecera: "CONSULTORIO DR. DÍAZ" con datos de contacto
  - Datos del paciente: nombre, cédula, fecha
  - Diagnóstico
  - Tratamiento
  - Pie de página: firma del médico
- [ ] Usar Jinja2 para inyectar datos dinámicos en HTML
- [ ] Implementar función `generar_receta_pdf(paciente_data)` que:
  - Renderiza el HTML con los datos del paciente
  - Genera PDF con WeasyPrint
  - Guarda PDF en carpeta `recetas/` con nombre: `receta_{cedula}_{fecha}.pdf`
  - Abre automáticamente el PDF con visor predeterminado
- [ ] Conectar botón "Generar Receta" con esta función
- [ ] Mostrar mensaje de éxito después de generar el PDF
- [ ] Manejar errores (ej: paciente no seleccionado)

**Criterios de Aceptación:**
- ✅ Al hacer clic en "Generar Receta", se crea un PDF
- ✅ El PDF tiene formato profesional y legible
- ✅ El PDF se abre automáticamente al generarse
- ✅ Mensaje de éxito visible
- ✅ Si no hay paciente seleccionado, muestra advertencia

---

### ✅ Ticket #8: Pruebas de Integración y Validación
**Tiempo estimado:** 2 horas

**Descripción:** Probar todo el flujo de la aplicación y corregir errores.

**Tareas:**
- [ ] Probar flujo completo: Login → Ver pacientes → Registrar nuevo paciente → Generar receta
- [ ] Probar casos borde:
  - Campos vacíos al guardar
  - Cédula duplicada
  - Paciente sin seleccionar al generar receta
  - Credenciales incorrectas en login
- [ ] Probar que los PDFs se generan en la carpeta correcta
- [ ] Verificar que la tabla se actualiza después de guardar
- [ ] Probar redimensionamiento de ventanas
- [ ] Ejecutar aplicación desde diferentes ubicaciones (ruta absoluta vs relativa)
- [ ] Verificar que no haya errores en consola
- [ ] Documentar errores encontrados y corregirlos

**Criterios de Aceptación:**
- ✅ Todos los flujos principales funcionan sin errores
- ✅ Casos borde manejados con mensajes claros
- ✅ No hay errores de consola durante el uso normal
- ✅ La aplicación es estable

---

### 🎬 Ticket #9: Preparar Demo para Presentación
**Tiempo estimado:** 1.5 horas

**Descripción:** Preparar la demo y materiales para presentación.

**Tareas:**
- [ ] Verificar que todos los textos estén en español y sean claros
- [ ] Asegurar que el logo o nombre "Dr. Díaz" esté visible
- [ ] Crear una guía rápida de uso (PDF o texto) para tu padre
- [ ] Preparar 5 casos de ejemplo con datos reales (pueden ser ficticios pero realistas)
- [ ] Verificar que los PDFs generados tengan formato profesional
- [ ] Probar la aplicación en una PC limpia (sin entorno de desarrollo)
- [ ] Crear un acceso directo o script de inicio fácil de usar
- [ ] Ensayar la presentación: mostrar el flujo completo en 5 minutos

**Criterios de Aceptación:**
- ✅ La aplicación funciona perfectamente
- ✅ Todos los textos son claros y profesionales
- ✅ Los PDFs tienen aspecto profesional
- ✅ Tu padre puede entender el flujo sin explicaciones complejas

---

## 📊 RESUMEN DE ESTIMACIONES

| Día | Tickets | Horas Totales |
|-----|---------|---------------|
| **Día 1** | #1, #2, #3 | 4-5 horas |
| **Día 2** | #4, #5, #6 | 5-6 horas |
| **Día 3** | #7, #8, #9 | 5-6 horas |
| **TOTAL** | **9 tickets** | **14-17 horas** |
