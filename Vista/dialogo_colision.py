from PySide6.QtWidgets import QDialog, QVBoxLayout, QLabel, QComboBox, QPushButton
from PySide6.QtCore import Qt


class DialogoColisiones(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.setWindowTitle("Resolución de colisiones")
        self.setFixedSize(450, 250)
        self.setModal(True)

        # Estilo del diálogo
        self.setStyleSheet("QDialog { background-color: #FFEAC5; }")

        # Layout principal
        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setAlignment(Qt.AlignCenter)

        # Etiqueta
        etiqueta = QLabel("Se ha detectado una colisión.\nSeleccione el método de resolución:")
        etiqueta.setAlignment(Qt.AlignCenter)
        etiqueta.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2d1f15;
            margin-bottom: 10px;
        """)
        layout.addWidget(etiqueta)

        # ComboBox con las estrategias
        self.combo = QComboBox()
        self.combo.addItems([
            "Lineal",
            "Cuadrática",
            "Doble función hash",
            "Arreglo anidado",
            "Lista encadenada"
        ])
        self.combo.setStyleSheet("""
            QComboBox {
                border: 2px solid #bf8f62;
                border-radius: 10px;
                padding: 10px;
                font-size: 16px;
                background-color: #FFF3E0;
                color: #2d1f15;
                min-height: 40px;
            }
            QComboBox:hover {
                border: 2px solid #9c724a;
                background-color: #FFDBB5;
            }
            QComboBox::drop-down {
                border: none;
                width: 30px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 8px solid #6C4E31;
                margin-right: 10px;
            }
            QComboBox QAbstractItemView {
                border: 2px solid #bf8f62;
                border-radius: 8px;
                background-color: #FFF3E0;
                selection-background-color: #6C4E31;
                selection-color: #FFEAC5;
                padding: 5px;
            }
        """)
        layout.addWidget(self.combo)

        # Botón de aceptar
        btn_aceptar = QPushButton("Aceptar")
        btn_aceptar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                padding: 10px 30px;
                font-size: 16px;
                border-radius: 10px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #9c724a;
            }
            QPushButton:pressed {
                background-color: #2d1f15;
            }
        """)
        btn_aceptar.clicked.connect(self.accept)
        layout.addWidget(btn_aceptar, alignment=Qt.AlignCenter)

        # Espaciado al final
        layout.addStretch()

    def get_estrategia(self) -> str:
        """Devuelve el texto de la estrategia seleccionada."""
        return self.combo.currentText()