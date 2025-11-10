from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QSpinBox, QDialogButtonBox
)

class DialogoArista(QDialog):
    """Diálogo para ingresar una arista"""

    def __init__(self, max_vertices, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Arista")
        self.setModal(True)

        layout = QVBoxLayout(self)

        # Vértice origen
        layout.addWidget(QLabel("Vértice Origen:"))
        self.origen = QSpinBox()
        self.origen.setRange(1, max_vertices)
        layout.addWidget(self.origen)

        # Vértice destino
        layout.addWidget(QLabel("Vértice Destino:"))
        self.destino = QSpinBox()
        self.destino.setRange(1, max_vertices)
        layout.addWidget(self.destino)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_arista(self):
        return (self.origen.value() - 1, self.destino.value() - 1)
