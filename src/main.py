import sys
import os
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox, QDialog,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QGroupBox, QFrame
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QShortcut, QKeySequence

from database import (
    verificar_login, get_pacientes, crear_paciente, get_connection,
    crear_usuario, usuario_existe,
)
from pdf_generator import generar_receta_pdf
from psycopg2 import extras


# ============================================================
# DIÁLOGO: Crear cuenta
# ============================================================
class CrearCuentaDialog(QDialog):
    """Diálogo modal para registrar un nuevo usuario."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Consultorio Médico - Crear cuenta")
        self.setFixedSize(360, 320)
        self.setObjectName("crearCuentaDialog")

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Nuevo usuario")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        layout.addWidget(QLabel("Usuario:"))
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Elige un nombre de usuario")
        layout.addWidget(self.usuario_input)

        layout.addWidget(QLabel("Contraseña:"))
        self.contrasena_input = QLineEdit()
        self.contrasena_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.contrasena_input.setPlaceholderText("Mínimo 4 caracteres")
        layout.addWidget(self.contrasena_input)

        layout.addWidget(QLabel("Confirmar contraseña:"))
        self.confirmar_input = QLineEdit()
        self.confirmar_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirmar_input.setPlaceholderText("Repite la contraseña")
        layout.addWidget(self.confirmar_input)

        btn_layout = QHBoxLayout()
        self.crear_btn = QPushButton("Crear cuenta")
        self.crear_btn.clicked.connect(self.crear)
        btn_layout.addWidget(self.crear_btn)

        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.setObjectName("danger")
        self.cancelar_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancelar_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Enter crea la cuenta
        self.confirmar_input.returnPressed.connect(self.crear)

    def crear(self):
        usuario = self.usuario_input.text().strip()
        contrasena = self.contrasena_input.text()
        confirmar = self.confirmar_input.text()

        if not usuario or not contrasena or not confirmar:
            QMessageBox.warning(self, "Campos vacíos", "Completa todos los campos.")
            return

        if len(contrasena) < 4:
            QMessageBox.warning(self, "Contraseña débil", "La contraseña debe tener al menos 4 caracteres.")
            return

        if contrasena != confirmar:
            QMessageBox.warning(self, "No coinciden", "Las contraseñas no coinciden.")
            return

        if usuario_existe(usuario):
            QMessageBox.warning(self, "Usuario existente", f"Ya existe un usuario con el nombre '{usuario}'.")
            return

        nuevo_id = crear_usuario(usuario, contrasena)
        if nuevo_id:
            QMessageBox.information(self, "Éxito", f"Cuenta '{usuario}' creada. Ya puedes iniciar sesión.")
            self.accept()
        else:
            QMessageBox.critical(self, "Error", "No se pudo crear la cuenta. Inténtalo de nuevo.")


# ============================================================
# VENTANA: Login
# ============================================================
class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Consultorio Médico - Login")
        self.setFixedSize(400, 360)
        self.setObjectName("loginWindow")

        self.center_window()

        layout = QVBoxLayout()
        layout.setSpacing(12)
        layout.setContentsMargins(30, 25, 30, 25)

        titulo = QLabel("🩺  CONSULTORIO DR. DÍAZ")
        titulo.setObjectName("titulo")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        subtitulo = QLabel("Iniciar sesión")
        subtitulo.setObjectName("subtitulo")
        subtitulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(subtitulo)

        layout.addSpacing(8)

        layout.addWidget(QLabel("Usuario:"))
        self.usuario_input = QLineEdit()
        self.usuario_input.setPlaceholderText("Ingrese su usuario")
        layout.addWidget(self.usuario_input)

        layout.addWidget(QLabel("Contraseña:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.clicked.connect(self.login)
        layout.addWidget(self.login_btn)

        # Separador
        separador = QFrame()
        separador.setFrameShape(QFrame.Shape.HLine)
        separador.setFrameShadow(QFrame.Shadow.Sunken)
        layout.addWidget(separador)

        layout.addWidget(QLabel("¿No tienes cuenta?"))

        self.crear_cuenta_btn = QPushButton("Crear cuenta nueva")
        self.crear_cuenta_btn.setObjectName("accent")
        self.crear_cuenta_btn.clicked.connect(self.abrir_crear_cuenta)
        layout.addWidget(self.crear_cuenta_btn)

        self.salir_btn = QPushButton("Salir")
        self.salir_btn.setObjectName("danger")
        self.salir_btn.clicked.connect(self.close)
        layout.addWidget(self.salir_btn)

        self.setLayout(layout)

        self.usuario_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

    def center_window(self):
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def abrir_crear_cuenta(self):
        dialogo = CrearCuentaDialog(self)
        dialogo.exec()

    def login(self):
        usuario = self.usuario_input.text().strip()
        contrasena = self.password_input.text()

        if not usuario or not contrasena:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete todos los campos.")
            return

        if verificar_login(usuario, contrasena):
            self.main_window = MainWindow(usuario)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Usuario o contraseña incorrectos.")


# ============================================================
# DIÁLOGO: Paciente (Nuevo / Editar / Generar Receta)
# ============================================================
class PacienteDialog(QDialog):
    """
    Ventana modal con el formulario completo de paciente.
    Se abre desde MainWindow con un modo:
      - "nuevo":   crea un paciente (campos vacíos).
      - "editar":  edita uno existente (recibe paciente_id).
    Permite también generar la receta desde aquí mismo.
    """

    def __init__(self, parent=None, modo="nuevo", paciente_id=None):
        super().__init__(parent)
        self.modo = modo
        self.paciente_id = paciente_id

        self.setWindowTitle(
            "Nuevo Paciente" if modo == "nuevo" else "Editar Paciente"
        )
        self.setFixedSize(520, 620)
        self.setObjectName("pacienteDialog")

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        titulo = QLabel("Datos del Paciente")
        titulo.setObjectName("titulo")
        layout.addWidget(titulo)

        # Cédula
        layout.addWidget(QLabel("Cédula: *"))
        self.cedula_input = QLineEdit()
        self.cedula_input.setPlaceholderText("Cédula *")
        layout.addWidget(self.cedula_input)

        # Nombre / Apellido
        fila1 = QHBoxLayout()
        col_nombre = QVBoxLayout()
        col_nombre.addWidget(QLabel("Nombre: *"))
        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre *")
        col_nombre.addWidget(self.nombre_input)
        fila1.addLayout(col_nombre)

        col_apellido = QVBoxLayout()
        col_apellido.addWidget(QLabel("Apellido: *"))
        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Apellido *")
        col_apellido.addWidget(self.apellido_input)
        fila1.addLayout(col_apellido)
        layout.addLayout(fila1)

        # Teléfono
        layout.addWidget(QLabel("Teléfono:"))
        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")
        layout.addWidget(self.telefono_input)

        # Diagnóstico
        layout.addWidget(QLabel("Diagnóstico:"))
        self.diagnostico_input = QTextEdit()
        self.diagnostico_input.setPlaceholderText("Ingrese el diagnóstico")
        self.diagnostico_input.setMinimumHeight(100)
        layout.addWidget(self.diagnostico_input)

        # Tratamiento
        layout.addWidget(QLabel("Tratamiento:"))
        self.tratamiento_input = QTextEdit()
        self.tratamiento_input.setPlaceholderText("Ingrese el tratamiento")
        self.tratamiento_input.setMinimumHeight(100)
        layout.addWidget(self.tratamiento_input)

        # Botones
        btn_layout = QHBoxLayout()
        self.guardar_btn = QPushButton("Guardar")
        self.guardar_btn.clicked.connect(self.guardar)
        btn_layout.addWidget(self.guardar_btn)

        if modo == "editar":
            self.receta_btn = QPushButton("Generar Receta")
            self.receta_btn.setObjectName("accent")
            self.receta_btn.clicked.connect(self.generar_receta)
            btn_layout.addWidget(self.receta_btn)

        self.cancelar_btn = QPushButton("Cancelar")
        self.cancelar_btn.setObjectName("danger")
        self.cancelar_btn.clicked.connect(self.reject)
        btn_layout.addWidget(self.cancelar_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Si es edición, cargar datos
        if modo == "editar" and paciente_id is not None:
            self.cargar_datos()

        # Ctrl+S para guardar
        QShortcut(QKeySequence("Ctrl+S"), self, self.guardar)

    def cargar_datos(self):
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                    cur.execute("SELECT * FROM pacientes WHERE id = %s", (self.paciente_id,))
                    p = cur.fetchone()
            if p:
                self.cedula_input.setText(p['cedula'])
                self.nombre_input.setText(p['nombre'])
                self.apellido_input.setText(p['apellido'])
                self.telefono_input.setText(p['telefono'] or '')
                self.diagnostico_input.setText(p['diagnostico'] or '')
                self.tratamiento_input.setText(p['tratamiento'] or '')
        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo cargar el paciente: {e}")

    def guardar(self):
        cedula = self.cedula_input.text().strip()
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        telefono = self.telefono_input.text().strip()
        diagnostico = self.diagnostico_input.toPlainText().strip()
        tratamiento = self.tratamiento_input.toPlainText().strip()

        if not cedula or not nombre or not apellido:
            QMessageBox.warning(self, "Campos vacíos", "Cédula, Nombre y Apellido son obligatorios.")
            return

        data = {
            'cedula': cedula,
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'diagnostico': diagnostico,
            'tratamiento': tratamiento,
        }

        if self.modo == "nuevo":
            nuevo_id = crear_paciente(data)
            if nuevo_id:
                QMessageBox.information(self, "Éxito", f"Paciente guardado correctamente (ID: {nuevo_id})")
                self.accept()
            else:
                QMessageBox.critical(self, "Error", "Error al guardar. Verifique que la cédula no esté duplicada.")
        else:
            # actualizar paciente existente
            try:
                with get_connection() as conn:
                    with conn.cursor() as cur:
                        cur.execute("""
                            UPDATE pacientes
                            SET cedula=%s, nombre=%s, apellido=%s,
                                telefono=%s, diagnostico=%s, tratamiento=%s
                            WHERE id=%s
                        """, (cedula, nombre, apellido, telefono, diagnostico, tratamiento, self.paciente_id))
                        conn.commit()
                QMessageBox.information(self, "Éxito", "Paciente actualizado correctamente.")
                self.accept()
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo actualizar: {e}")

    def generar_receta(self):
        """Genera la receta en PDF desde los datos del formulario (sin cerrar el diálogo)."""
        cedula = self.cedula_input.text().strip()
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        telefono = self.telefono_input.text().strip()
        diagnostico = self.diagnostico_input.toPlainText().strip()
        tratamiento = self.tratamiento_input.toPlainText().strip()

        if not cedula or not nombre or not apellido:
            QMessageBox.warning(self, "Datos incompletos", "Cédula, Nombre y Apellido son obligatorios para generar la receta.")
            return

        paciente = {
            'cedula': cedula,
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'diagnostico': diagnostico,
            'tratamiento': tratamiento,
        }

        ruta_pdf = generar_receta_pdf(paciente)
        if ruta_pdf:
            QMessageBox.information(self, "Éxito", f"Receta generada correctamente\n\n{ruta_pdf}")
        else:
            QMessageBox.critical(self, "Error", "Error al generar la receta.")


# ============================================================
# VENTANA: Principal
# ============================================================
class MainWindow(QMainWindow):
    def __init__(self, usuario="doctor"):
        super().__init__()
        self.setWindowTitle("Consultorio Médico")
        self.resize(900, 600)
        self.setMinimumSize(700, 500)
        self.usuario_actual = usuario

        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        # ---------- Cabecera ----------
        cabecera = QHBoxLayout()
        titulo = QLabel("🩺  CONSULTORIO DR. DÍAZ")
        titulo.setObjectName("titulo")
        cabecera.addWidget(titulo)

        cabecera.addStretch()

        self.saludo = QLabel(f"Sesión: {self.usuario_actual}")
        self.saludo.setObjectName("subtitulo")
        cabecera.addWidget(self.saludo)
        main_layout.addLayout(cabecera)

        # ---------- Buscador ----------
        busqueda_layout = QHBoxLayout()
        busqueda_layout.addWidget(QLabel("Buscar:"))

        self.buscar_input = QLineEdit()
        self.buscar_input.setPlaceholderText("Buscar por cédula, nombre o apellido...")
        self.buscar_input.textChanged.connect(self.buscar_pacientes)
        busqueda_layout.addWidget(self.buscar_input)

        self.limpiar_buscar_btn = QPushButton("Limpiar")
        self.limpiar_buscar_btn.setObjectName("danger")
        self.limpiar_buscar_btn.setFixedWidth(40)
        self.limpiar_buscar_btn.setToolTip("Limpiar búsqueda")
        self.limpiar_buscar_btn.clicked.connect(self.limpiar_busqueda)
        busqueda_layout.addWidget(self.limpiar_buscar_btn)

        main_layout.addLayout(busqueda_layout)

        # ---------- Tabla de pacientes ----------
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Cédula", "Nombre", "Apellido", "Teléfono"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.abrir_editar)
        main_layout.addWidget(self.table)

        # ---------- Botones inferiores ----------
        acciones_layout = QHBoxLayout()
        self.nuevo_btn = QPushButton("Nuevo Paciente")
        self.nuevo_btn.clicked.connect(self.abrir_nuevo)
        acciones_layout.addWidget(self.nuevo_btn)

        self.editar_btn = QPushButton("Ver / Editar")
        self.editar_btn.clicked.connect(self.abrir_editar)
        acciones_layout.addWidget(self.editar_btn)

        self.receta_btn = QPushButton("Generar Receta")
        self.receta_btn.setObjectName("accent")
        self.receta_btn.clicked.connect(self.abrir_generar_receta)
        acciones_layout.addWidget(self.receta_btn)

        acciones_layout.addStretch()

        self.refresh_btn = QPushButton("Actualizar")
        self.refresh_btn.clicked.connect(self.cargar_pacientes)
        acciones_layout.addWidget(self.refresh_btn)

        main_layout.addLayout(acciones_layout)

        # ---------- Status bar ----------
        self.statusBar().showMessage("Listo")

        # Cargar pacientes al iniciar
        self.cargar_pacientes()

    # ============================================================
    # FUNCIONES
    # ============================================================
    def cargar_pacientes(self, filtro=None):
        """Carga la lista de pacientes en la tabla, opcionalmente filtrada."""
        pacientes = get_pacientes()
        self._pacientes = pacientes  # cache para filtrado en cliente
        self._aplicar_filtro(filtro if filtro is not None else self.buscar_input.text())

    def _aplicar_filtro(self, texto):
        texto = (texto or "").strip().lower()
        pacientes = getattr(self, '_pacientes', [])

        if texto:
            filtrados = [
                p for p in pacientes
                if texto in (p['cedula'] or '').lower()
                or texto in (p['nombre'] or '').lower()
                or texto in (p['apellido'] or '').lower()
            ]
        else:
            filtrados = pacientes

        self.table.setRowCount(len(filtrados))
        for i, p in enumerate(filtrados):
            self.table.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(p['cedula']))
            self.table.setItem(i, 2, QTableWidgetItem(p['nombre']))
            self.table.setItem(i, 3, QTableWidgetItem(p['apellido']))
            self.table.setItem(i, 4, QTableWidgetItem(p['telefono'] or ''))

        self.statusBar().showMessage(
            f"{len(filtrados)} paciente(s) mostrado(s)"
            + (f" de {len(pacientes)} totales" if texto else "")
        )

    def buscar_pacientes(self, texto):
        self._aplicar_filtro(texto)

    def limpiar_busqueda(self):
        self.buscar_input.clear()
        self._aplicar_filtro("")

    def _paciente_seleccionado_id(self):
        row = self.table.currentRow()
        if row < 0:
            return None
        item = self.table.item(row, 0)
        return int(item.text()) if item else None

    def abrir_nuevo(self):
        dialogo = PacienteDialog(self, modo="nuevo")
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_pacientes()

    def abrir_editar(self):
        paciente_id = self._paciente_seleccionado_id()
        if paciente_id is None:
            QMessageBox.warning(self, "Sin selección", "Por favor, seleccione un paciente de la tabla.")
            return
        dialogo = PacienteDialog(self, modo="editar", paciente_id=paciente_id)
        if dialogo.exec() == QDialog.DialogCode.Accepted:
            self.cargar_pacientes()

    def abrir_generar_receta(self):
        paciente_id = self._paciente_seleccionado_id()
        if paciente_id is None:
            QMessageBox.warning(self, "Sin selección", "Por favor, seleccione un paciente de la tabla.")
            return
        # Abre el diálogo en modo "editar"; el botón "Generar Receta" está dentro
        dialogo = PacienteDialog(self, modo="editar", paciente_id=paciente_id)
        dialogo.exec()


# ============================================================
# ESTILOS QSS
# ============================================================
def cargar_estilos():
    """Carga los estilos QSS desde src/styles.qss."""
    ruta_qss = os.path.join(os.path.dirname(__file__), 'styles.qss')
    try:
        with open(ruta_qss, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"Archivo styles.qss no encontrado en {ruta_qss}")
        return ""


if __name__ == '__main__':
    app = QApplication(sys.argv)

    # Aplicar estilos QSS (Ticket #6)
    estilo = cargar_estilos()
    if estilo:
        app.setStyleSheet(estilo)

    window = LoginWindow()
    window.show()
    sys.exit(app.exec())
