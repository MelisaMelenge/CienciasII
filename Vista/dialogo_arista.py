from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QDialogButtonBox
)

class DialogoArista(QDialog):
    """Diálogo para ingresar una arista"""

    def __init__(self, max_vertices, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Arista")
        self.setModal(True)

        # Estilo general del diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #FFEAC5;
            }
            QLabel {
                color: #2d1f15;
                font-size: 14px;
                font-weight: bold;
                margin-top: 10px;
            }
            QSpinBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #2d1f15;
            }
            QSpinBox::up-button, QSpinBox::down-button {
                background-color: #9c724a;
                border: none;
            }
            QSpinBox::up-button:hover, QSpinBox::down-button:hover {
                background-color: #6C4E31;
            }
            QDialogButtonBox QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                border: none;
                border-radius: 5px;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                min-width: 80px;
            }
            QDialogButtonBox QPushButton:hover {
                background-color: #9c724a;
            }
            QDialogButtonBox QPushButton:pressed {
                background-color: #2d1f15;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        layout.setContentsMargins(20, 20, 20, 20)

        # Vértice origen
        layout.addWidget(QLabel("Vértice Origen:"))
        self.origen = QSpinBox()
        self.origen.setRange(1, max_vertices)
        self.origen.setFixedHeight(35)
        layout.addWidget(self.origen)

        # Vértice destino
        layout.addWidget(QLabel("Vértice Destino:"))
        self.destino = QSpinBox()
        self.destino.setRange(1, max_vertices)
        self.destino.setFixedHeight(35)
        layout.addWidget(self.destino)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_arista(self):
        return (self.origen.value() - 1, self.destino.value() - 1)