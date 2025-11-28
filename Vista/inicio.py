from PySide6.QtWidgets import QMainWindow, QWidget, QLabel, QVBoxLayout, QHBoxLayout, QPushButton
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont


class Inicio(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.setWindowTitle("Ciencias de la Computación II")
        self.setGeometry(200, 200, 1000, 600)

        # ----------- WIDGET CENTRAL -----------
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout(central_widget)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        # ----------- ENCABEZADO SUPERIOR -----------
        header = QLabel("Ciencias de la Computación II")
        header.setAlignment(Qt.AlignCenter)
        header.setFont(QFont("Arial", 26, QFont.Bold))
        header.setStyleSheet("""
            QLabel {
                color: #473627;
                padding: 25px;
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9c724a, stop:1 #bf8f62
                );
            }
        """)

        layout.addWidget(header)

        # ----------- MENÚ PRINCIPAL -----------
        menu_bar = QWidget()
        menu_layout = QHBoxLayout(menu_bar)
        menu_layout.setContentsMargins(0, 0, 0, 0)
        menu_layout.setSpacing(30)
        menu_bar.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #bf8f62, stop:1 #9c724a
                );
            }
            QPushButton {
                background: transparent;
                border: none;
                color: #473627;
                font-weight: bold;
                font-size: 16px;
                padding: 12px 20px;
            }
            QPushButton:hover {
                color: #FFEAC5;
                background: #473627;
                border-radius: 8px;
            }
        """)

        # Botones del menú
        btn_busqueda = QPushButton("Búsqueda")
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        btn_grafos = QPushButton("Grafos")
        btn_grafos.clicked.connect(lambda: self.cambiar_ventana("grafos"))

        menu_layout.addStretch()
        menu_layout.addWidget(btn_busqueda)
        menu_layout.addWidget(btn_grafos)
        menu_layout.addStretch()

        layout.addWidget(menu_bar)

        # ----------- ESPACIO EN BLANCO PRINCIPAL -----------
        content = QWidget()
        content.setStyleSheet("background-color: #FFEAC5;")
        layout.addWidget(content, stretch=1)