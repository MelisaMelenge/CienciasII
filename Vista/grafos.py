from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt

class Grafos(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setWindowTitle("Ciencias de la Computación II - Grafos")
        self.setGeometry(300, 200, 1000, 600)

        # --- Widget central ---
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #D8B4FE, stop:1 #A78BFA);
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Ciencias de la Computación II - Grafos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: white; margin: 15px;")
        header_layout.addWidget(titulo)

        # --- Menú ---
        menu_bar = QMenuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #E9D5FF, stop:1 #C4B5FD);
                font-weight: bold;
                font-size: 16px;
                color: #4C1D95;
            }
            QMenuBar::item {
                spacing: 20px;
                padding: 8px 14px;
                border-radius: 8px;
            }
            QMenuBar::item:selected {
                background: #7e22ce;
                color: white;
            }
            QMenu {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #F8F4FF, stop:1 #E9D5FF);
                border: 1px solid #C4B5FD;
                font-size: 15px;
                color: #4C1D95;
                padding: 6px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #7e22ce, stop:1 #5a2ea6);
                color: white;
                border-radius: 6px;
            }
        """)

        # --- 🏠 Inicio ---
        inicio_action = menu_bar.addAction("🏠 Inicio")
        inicio_action.triggered.connect(lambda: self.cambiar_ventana("inicio"))

        # --- 🧩 Operaciones entre grafos ---
        menu_operaciones = QMenu("🧩 Operaciones entre grafos", self)
        menu_operaciones.addAction("Intersección", lambda: self.cambiar_ventana("interseccion_grafos"))
        menu_operaciones.addAction("Unión", lambda: self.cambiar_ventana("union_grafos"))
        menu_operaciones.addAction("Suma de anillo", lambda: self.cambiar_ventana("suma_anillo_grafos"))

        operaciones_action = menu_bar.addAction("🧩 Operaciones entre grafos")
        operaciones_action.setMenu(menu_operaciones)

        # --- Añadir al header ---
        header_layout.addWidget(menu_bar)

        # --- Contenido principal ---
        self.label = QLabel("Selecciona una opción del menú de Grafos")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; color: #2c3e50; font-weight: bold; margin-top: 40px;")

        main_layout.addWidget(header)
        main_layout.addWidget(self.label, stretch=1)

    # ==== Métodos de navegación ====
    def mostrar_opcion(self, texto):
        self.label.setText(f"Opción seleccionada: {texto}")

    def abrir_interseccion(self): self.cambiar_ventana("interseccion_grafos")
    def abrir_union(self): self.cambiar_ventana("union_grafos")
    def abrir_suma_anillo(self): self.cambiar_ventana("suma_anillo_grafos")

