import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QLineEdit, QPushButton, QMessageBox
)
from PyQt6.QtCore import Qt
from database import verificar_login


class LoginWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("🩺 Consultorio Médico - Login")
        self.setFixedSize(400, 300)
        
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
            self.close()
            # Aquí abriremos MainWindow (Ticket #5)
            QMessageBox.information(None, "Éxito", f"✅ Bienvenido, {usuario}!")
        else:
            QMessageBox.warning(self, "Error", "❌ Usuario o contraseña incorrectos.")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec())