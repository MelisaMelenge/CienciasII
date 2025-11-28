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
        central.setStyleSheet("background-color: #FFEAC5;")
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62);
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Ciencias de la Computación II - Grafos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 28px; font-weight: bold; color: #2d1f15; margin: 15px;")
        header_layout.addWidget(titulo)

        # --- Menú ---
        menu_bar = QMenuBar()
        menu_bar.setStyleSheet("""
            QMenuBar {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFDBB5, stop:1 #FFF3E0);
                font-weight: bold;
                font-size: 16px;
                color: #2d1f15;
            }
            QMenuBar::item {
                spacing: 20px;
                padding: 8px 14px;
                border-radius: 8px;
            }
            QMenuBar::item:selected {
                background: #6C4E31;
                color: #FFEAC5;
            }
            QMenu {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #FFF3E0, stop:1 #FFDBB5);
                border: 1px solid #bf8f62;
                font-size: 15px;
                color: #2d1f15;
                padding: 6px;
                border-radius: 8px;
            }
            QMenu::item:selected {
                background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                    stop:0 #6C4E31, stop:1 #9c724a);
                color: #FFEAC5;
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
        self.label.setStyleSheet("font-size: 20px; color: #6C4E31; font-weight: bold; margin-top: 40px;")

        main_layout.addWidget(header)
        main_layout.addWidget(self.label, stretch=1)

    # ==== Métodos de navegación ====
    def mostrar_opcion(self, texto):
        self.label.setText(f"Opción seleccionada: {texto}")

    def abrir_interseccion(self): self.cambiar_ventana("interseccion_grafos")
    def abrir_union(self): self.cambiar_ventana("union_grafos")
    def abrir_suma_anillo(self): self.cambiar_ventana("suma_anillo_grafos")

