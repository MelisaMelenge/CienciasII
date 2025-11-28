from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QLabel, QComboBox, QDialogButtonBox
)


class DialogoArista(QDialog):
    """Diálogo para ingresar una arista (no dirigida)"""

    def __init__(self, max_vertices, parent=None, etiquetas=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Arista")
        self.setModal(True)
        self.etiquetas = etiquetas if etiquetas else {}

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
            QComboBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
                color: #2d1f15;
            }
            QComboBox::drop-down {
                background-color: #9c724a;
                border: none;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 5px solid #FFEAC5;
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
        self.origen = QComboBox()
        self.origen.setEditable(False)  # Solo selección, no editable
        for i in range(max_vertices):
            etiqueta = self.etiquetas.get(i, str(i + 1))
            self.origen.addItem(f"{etiqueta}", i)  # Mostrar solo la etiqueta
        self.origen.setFixedHeight(35)
        layout.addWidget(self.origen)

        # Vértice destino
        layout.addWidget(QLabel("Vértice Destino:"))
        self.destino = QComboBox()
        self.destino.setEditable(False)  # Solo selección, no editable
        for i in range(max_vertices):
            etiqueta = self.etiquetas.get(i, str(i + 1))
            self.destino.addItem(f"{etiqueta}", i)  # Mostrar solo la etiqueta
        self.destino.setFixedHeight(35)
        layout.addWidget(self.destino)

        # Botones
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

    def get_arista(self):
        """Retorna la arista normalizada (el menor índice primero)
        para que (1,2) sea igual a (2,1) en grafos no dirigidos"""
        origen = self.origen.currentData()
        destino = self.destino.currentData()
        # Normalizar: siempre el menor índice primero
        return tuple(sorted([origen, destino]))