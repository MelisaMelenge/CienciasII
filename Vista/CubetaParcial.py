from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QSpinBox, QComboBox, QPushButton, QGridLayout, QHBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt


class CubetaParcial(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setWindowTitle("Ciencias de la Computación II - Cubetas (Expansión y Reducción Parcial)")

        # --- Widget central ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #D8B4FE, stop:1 #A78BFA
            );
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Ciencias de la Computación II - Cubetas (Expansión y Reducción Parcial)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
        header_layout.addWidget(titulo)

        # --- Menú de navegación ---
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)
        menu_layout.setAlignment(Qt.AlignCenter)

        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")

        for btn in (btn_inicio, btn_busqueda):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2E1065;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    color: #6D28D9;
                    text-decoration: underline;
                }
            """)
            menu_layout.addWidget(btn)

        header_layout.addLayout(menu_layout)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        layout.addWidget(header)

        # --- Controles de parámetros ---
        self.spin_cubetas = QSpinBox()
        self.spin_cubetas.setRange(1, 100)
        self.spin_cubetas.setValue(10)
        self.spin_cubetas.setFixedWidth(100)

        self.spin_registros = QSpinBox()
        self.spin_registros.setRange(1, 50)
        self.spin_registros.setValue(5)
        self.spin_registros.setFixedWidth(100)

        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)
        self.spin_digitos.setValue(4)
        self.spin_digitos.setFixedWidth(100)

        self.combo_accion = QComboBox()
        self.combo_accion.addItems(["Expandir", "Reducir"])
        self.combo_accion.setFixedWidth(150)

        # Estilo para los controles
        estilo_control = "font-size: 16px; padding: 5px;"
        self.spin_cubetas.setStyleSheet(estilo_control)
        self.spin_registros.setStyleSheet(estilo_control)
        self.spin_digitos.setStyleSheet(estilo_control)
        self.combo_accion.setStyleSheet(estilo_control)

        # --- Botones principales ---
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_insertar = QPushButton("Insertar claves")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_buscar_clave = QPushButton("Buscar clave")

        estilo_boton = """
            QPushButton {
                background-color: #7C3AED;
                color: white;
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
        """

        botones = (
            self.btn_crear, self.btn_insertar, self.btn_guardar,
            self.btn_cargar, self.btn_eliminar, self.btn_deshacer,
            self.btn_eliminar_clave, self.btn_buscar_clave
        )
        for btn in botones:
            btn.setStyleSheet(estilo_boton)

        # --- Layout de controles ---
        controles = QVBoxLayout()

        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)

        lbl_cubetas = QLabel("Número de cubetas:")
        lbl_cubetas.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_registros = QLabel("Registros por cubeta:")
        lbl_registros.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_digitos = QLabel("Tamaño de claves:")
        lbl_digitos.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_accion = QLabel("Acción:")
        lbl_accion.setStyleSheet("font-size: 16px; font-weight: bold;")

        fila_controles.addWidget(lbl_cubetas)
        fila_controles.addWidget(self.spin_cubetas)
        fila_controles.addWidget(lbl_registros)
        fila_controles.addWidget(self.spin_registros)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.spin_digitos)
        fila_controles.addWidget(lbl_accion)
        fila_controles.addWidget(self.combo_accion)

        controles.addLayout(fila_controles)

        # --- Grid de botones ---
        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_insertar, 0, 1)
        grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)

        controles.addLayout(grid_botones)
        layout.addLayout(controles)

        # --- Área de visualización (scroll) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(10)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        # --- Mensaje inicial ---
        lbl_info = QLabel("Aquí se mostrará la simulación de la expansión o reducción parcial de cubetas.")
        lbl_info.setAlignment(Qt.AlignCenter)
        lbl_info.setStyleSheet("font-size: 18px; color: #2c3e50; margin: 20px;")
        self.contenedor_layout.addWidget(lbl_info)
