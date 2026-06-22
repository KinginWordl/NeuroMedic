import sys
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView,
    QTextEdit, QGroupBox, QSplitter, QSizePolicy
)
from PyQt6.QtCore import Qt
from database import verificar_login, get_pacientes, crear_paciente, get_connection
from pdf_generator import generar_receta_pdf
from psycopg2 import extras


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🩺 Consultorio Médico - Login")
        self.setFixedSize(400, 300)
        self.setObjectName("loginWindow")  # habilita los estilos #loginWindow del QSS

        # Centrar ventana en la pantalla
        self.center_window()

        # Layout principal
        layout = QVBoxLayout()
        layout.setSpacing(15)

        # Título
        titulo = QLabel("🩺 CONSULTORIO DR. DÍAZ")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 20px; font-weight: bold; margin: 20px 0;")
        layout.addWidget(titulo)

        # Campo: Usuario
        layout.addWidget(QLabel("Usuario:"))
        self.usuario_input = QLineEdit()
        self.usuario_input.setText("doctor")
        self.usuario_input.setPlaceholderText("Ingrese su usuario")
        layout.addWidget(self.usuario_input)

        # Campo: Contraseña
        layout.addWidget(QLabel("Contraseña:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setText("demo123")
        self.password_input.setPlaceholderText("Ingrese su contraseña")
        layout.addWidget(self.password_input)

        # Botones
        btn_layout = QHBoxLayout()
        self.login_btn = QPushButton("Iniciar Sesión")
        self.login_btn.clicked.connect(self.login)
        btn_layout.addWidget(self.login_btn)

        self.salir_btn = QPushButton("Salir")
        self.salir_btn.clicked.connect(self.close)
        btn_layout.addWidget(self.salir_btn)
        layout.addLayout(btn_layout)

        self.setLayout(layout)

        # Conectar Enter
        self.usuario_input.returnPressed.connect(self.login)
        self.password_input.returnPressed.connect(self.login)

    def center_window(self):
        """Centra la ventana en la pantalla"""
        screen = QApplication.primaryScreen().geometry()
        x = (screen.width() - self.width()) // 2
        y = (screen.height() - self.height()) // 2
        self.move(x, y)

    def login(self):
        usuario = self.usuario_input.text().strip()
        contrasena = self.password_input.text().strip()

        if not usuario or not contrasena:
            QMessageBox.warning(self, "Campos vacíos", "Por favor, complete todos los campos.")
            return

        if verificar_login(usuario, contrasena):
            # Abrir MainWindow y cerrar el login
            self.main_window = MainWindow(usuario)
            self.main_window.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "❌ Usuario o contraseña incorrectos.")


class MainWindow(QMainWindow):
    def __init__(self, usuario="doctor"):
        super().__init__()
        self.setWindowTitle("🩺 Consultorio Médico")
        self.resize(1200, 700)
        self.setMinimumSize(800, 500)

        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Layout principal
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)

        # ============================================================
        # PANEL IZQUIERDO (Lista de pacientes)
        # ============================================================
        left_panel = QWidget()
        left_layout = QVBoxLayout()
        left_panel.setLayout(left_layout)

        # Botón Actualizar
        self.refresh_btn = QPushButton("🔄 Actualizar Lista")
        self.refresh_btn.clicked.connect(self.cargar_pacientes)
        left_layout.addWidget(self.refresh_btn)

        # Tabla de pacientes
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Cédula", "Nombre", "Apellido", "Teléfono"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setSelectionMode(QTableWidget.SelectionMode.SingleSelection)
        self.table.setAlternatingRowColors(True)  # Ticket #6: colores alternados en la tabla
        self.table.clicked.connect(self.on_paciente_seleccionado)
        left_layout.addWidget(self.table)

        # ============================================================
        # PANEL DERECHO (Formulario de paciente)
        # ============================================================
        right_panel = QWidget()
        right_layout = QVBoxLayout()
        right_panel.setLayout(right_layout)

        # Grupo: Datos del Paciente
        form_group = QGroupBox("📋 Datos del Paciente")
        form_layout = QVBoxLayout()
        form_group.setLayout(form_layout)

        # Campos del formulario
        self.cedula_input = QLineEdit()
        self.cedula_input.setPlaceholderText("Cédula *")
        form_layout.addWidget(self.cedula_input)

        self.nombre_input = QLineEdit()
        self.nombre_input.setPlaceholderText("Nombre *")
        form_layout.addWidget(self.nombre_input)

        self.apellido_input = QLineEdit()
        self.apellido_input.setPlaceholderText("Apellido *")
        form_layout.addWidget(self.apellido_input)

        self.telefono_input = QLineEdit()
        self.telefono_input.setPlaceholderText("Teléfono")
        form_layout.addWidget(self.telefono_input)

        form_layout.addWidget(QLabel("Diagnóstico:"))
        self.diagnostico_input = QTextEdit()
        self.diagnostico_input.setPlaceholderText("Ingrese el diagnóstico")
        self.diagnostico_input.setMinimumHeight(80)
        self.diagnostico_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        form_layout.addWidget(self.diagnostico_input)

        form_layout.addWidget(QLabel("Tratamiento:"))
        self.tratamiento_input = QTextEdit()
        self.tratamiento_input.setPlaceholderText("Ingrese el tratamiento")
        self.tratamiento_input.setMinimumHeight(80)
        self.tratamiento_input.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        form_layout.addWidget(self.tratamiento_input)

        # Botones
        btn_layout = QHBoxLayout()
        self.guardar_btn = QPushButton("💾 Guardar Paciente")
        self.guardar_btn.clicked.connect(self.guardar_paciente)
        btn_layout.addWidget(self.guardar_btn)

        self.receta_btn = QPushButton("📄 Generar Receta")
        self.receta_btn.setObjectName("accent")  # estilo verde-azulado médico del QSS
        self.receta_btn.clicked.connect(self.generar_receta)
        btn_layout.addWidget(self.receta_btn)

        form_layout.addLayout(btn_layout)
        right_layout.addWidget(form_group)

        # ============================================================
        # DIVISOR (Splitter)
        # ============================================================
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(left_panel)
        splitter.addWidget(right_panel)
        splitter.setSizes([480, 720])  # 40% / 60% sobre 1200px
        splitter.setStretchFactor(0, 2)
        splitter.setStretchFactor(1, 3)
        splitter.setChildrenCollapsible(False)
        main_layout.addWidget(splitter)

        # Estado
        self.paciente_actual_id = None
        self.usuario_actual = usuario

        # Cargar pacientes al iniciar
        self.cargar_pacientes()

    # ============================================================
    # FUNCIONES
    # ============================================================

    def cargar_pacientes(self):
        """Carga la lista de pacientes en la tabla"""
        pacientes = get_pacientes()
        self.table.setRowCount(len(pacientes))

        for i, p in enumerate(pacientes):
            self.table.setItem(i, 0, QTableWidgetItem(str(p['id'])))
            self.table.setItem(i, 1, QTableWidgetItem(p['cedula']))
            self.table.setItem(i, 2, QTableWidgetItem(p['nombre']))
            self.table.setItem(i, 3, QTableWidgetItem(p['apellido']))
            self.table.setItem(i, 4, QTableWidgetItem(p['telefono'] or ''))

    def on_paciente_seleccionado(self):
        """Carga los datos del paciente seleccionado en el formulario"""
        row = self.table.currentRow()
        if row < 0:
            return

        # Obtener datos de la tabla
        self.paciente_actual_id = int(self.table.item(row, 0).text())
        cedula = self.table.item(row, 1).text()
        nombre = self.table.item(row, 2).text()
        apellido = self.table.item(row, 3).text()
        telefono = self.table.item(row, 4).text()

        # Cargar en el formulario
        self.cedula_input.setText(cedula)
        self.nombre_input.setText(nombre)
        self.apellido_input.setText(apellido)
        self.telefono_input.setText(telefono)

        # Obtener diagnóstico y tratamiento desde la BD
        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                    cur.execute(
                        "SELECT diagnostico, tratamiento FROM pacientes WHERE id = %s",
                        (self.paciente_actual_id,)
                    )
                    result = cur.fetchone()
                    if result:
                        self.diagnostico_input.setText(result['diagnostico'] or '')
                        self.tratamiento_input.setText(result['tratamiento'] or '')
        except Exception as e:
            print(f"Error al cargar datos completos: {e}")

    def guardar_paciente(self):
        """Guarda un nuevo paciente o actualiza el existente"""
        # Obtener datos del formulario
        cedula = self.cedula_input.text().strip()
        nombre = self.nombre_input.text().strip()
        apellido = self.apellido_input.text().strip()
        telefono = self.telefono_input.text().strip()
        diagnostico = self.diagnostico_input.toPlainText().strip()
        tratamiento = self.tratamiento_input.toPlainText().strip()

        # Validar campos obligatorios
        if not cedula or not nombre or not apellido:
            QMessageBox.warning(self, "Campos vacíos", "Cédula, Nombre y Apellido son obligatorios.")
            return

        # Crear diccionario con los datos
        data = {
            'cedula': cedula,
            'nombre': nombre,
            'apellido': apellido,
            'telefono': telefono,
            'diagnostico': diagnostico,
            'tratamiento': tratamiento
        }

        # Guardar en la base de datos
        nuevo_id = crear_paciente(data)

        if nuevo_id:
            QMessageBox.information(self, "Éxito", f"✅ Paciente guardado correctamente (ID: {nuevo_id})")
            self.limpiar_formulario()
            self.cargar_pacientes()  # Actualizar tabla
        else:
            QMessageBox.critical(self, "Error", "❌ Error al guardar el paciente. Verifique que la cédula no esté duplicada.")

    def limpiar_formulario(self):
        """Limpia todos los campos del formulario"""
        self.cedula_input.clear()
        self.nombre_input.clear()
        self.apellido_input.clear()
        self.telefono_input.clear()
        self.diagnostico_input.clear()
        self.tratamiento_input.clear()
        self.paciente_actual_id = None

    def generar_receta(self):
        """Genera la receta médica en PDF (Ticket #7)."""
        if self.paciente_actual_id is None:
            QMessageBox.warning(self, "Sin selección", "Por favor, seleccione un paciente primero.")
            return

        try:
            with get_connection() as conn:
                with conn.cursor(cursor_factory=extras.RealDictCursor) as cur:
                    cur.execute(
                        "SELECT * FROM pacientes WHERE id = %s",
                        (self.paciente_actual_id,)
                    )
                    paciente = cur.fetchone()

            if not paciente:
                QMessageBox.warning(self, "Error", "Paciente no encontrado.")
                return

            # Generar PDF
            ruta_pdf = generar_receta_pdf(dict(paciente))

            if ruta_pdf:
                QMessageBox.information(
                    self,
                    "Éxito",
                    f"✅ Receta generada correctamente\n\n📁 {ruta_pdf}"
                )
            else:
                QMessageBox.critical(
                    self,
                    "Error",
                    "❌ Error al generar la receta. Verifique la carpeta 'templates/'."
                )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"❌ {e}")


# Cargar estilos QSS
def cargar_estilos():
    """Carga los estilos QSS desde src/styles.qss"""
    import os
    ruta_qss = os.path.join(os.path.dirname(__file__), 'styles.qss')
    try:
        with open(ruta_qss, 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        print(f"⚠️ Archivo styles.qss no encontrado en {ruta_qss}")
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