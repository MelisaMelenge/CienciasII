# --- Importar vistas internas ---
from Vista.lineal_interna import LinealInterna
from Vista.binaria_interna import BinariaInterna
from Vista.mod_interna import ModInterna
from Vista.cuadrado_interna import CuadradoInterna
from Vista.truncamiento_interna import TruncamientoInterna
from Vista.plegamiento_interna import PlegamientoInterna

# --- Importar vistas externas ---
from Vista.lineal_externa import LinealExterna
from Vista.binaria_externa import BinariaExterna
from Vista.mod_externa import ModExterna
from Vista.cuadrado_externa import CuadradoExterna
from Vista.truncamiento_externa import TruncamientoExterna
from Vista.plegamiento_externa import PlegamientoExterna
from Vista.cambio_base import CambioBase
from Vista.CubetaTotal import CubetaTotal
from Vista.CubetaParcial import CubetaParcial
from Vista.Indices import Indices

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QMenuBar, QMenu
)
from PySide6.QtCore import Qt


class Busqueda(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda")
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

        titulo = QLabel("Ciencias de la Computación II")
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

        # --- 🔎 Búsquedas Internas ---
        menu_internas = QMenu("🔎 Búsquedas Internas", self)
        menu_internas.addAction("Lineal", lambda: self.cambiar_ventana("lineal_interna"))
        menu_internas.addAction("Binaria", lambda: self.cambiar_ventana("binaria_interna"))

        submenu_hash = QMenu("Funciones Hash", self)
        submenu_hash.addAction("Función mod", lambda: self.cambiar_ventana("mod_interna"))
        submenu_hash.addAction("Función cuadrado", lambda: self.cambiar_ventana("cuadrado_interna"))
        submenu_hash.addAction("Función truncamiento", lambda: self.cambiar_ventana("truncamiento_interna"))
        submenu_hash.addAction("Función plegamiento", lambda: self.cambiar_ventana("plegamiento_interna"))
        menu_internas.addMenu(submenu_hash)

        busquedas_action = menu_bar.addAction("🔎 Búsquedas Internas")
        busquedas_action.setMenu(menu_internas)

        # --- 🌍 Búsquedas Externas ---
        menu_externas = QMenu("🌍 Búsquedas Externas", self)
        menu_externas.addAction("Lineal", lambda: self.cambiar_ventana("lineal_externa"))
        menu_externas.addAction("Binaria", lambda: self.cambiar_ventana("binaria_externa"))

        submenu_hash_ext = QMenu("Funciones Hash", self)
        submenu_hash_ext.addAction("Función mod", lambda: self.cambiar_ventana("mod_externa"))
        submenu_hash_ext.addAction("Función cuadrado", lambda: self.cambiar_ventana("cuadrado_externa"))
        submenu_hash_ext.addAction("Función truncamiento", lambda: self.cambiar_ventana("truncamiento_externa"))
        submenu_hash_ext.addAction("Función plegamiento", lambda: self.cambiar_ventana("plegamiento_externa"))
        submenu_hash_ext.addAction("Cambio de base", lambda: self.cambiar_ventana("cambio_base"))
        menu_externas.addMenu(submenu_hash_ext)

        # 🪣 Cubetas
        submenu_cubetas = QMenu("Cubetas", self)
        submenu_cubetas.addAction("Expansión y reducción total", lambda: self.cambiar_ventana("cubeta_total"))
        submenu_cubetas.addAction("Expansión y reducción parcial", lambda: self.cambiar_ventana("cubeta_parcial"))
        menu_externas.addMenu(submenu_cubetas)

        busquedas_ext_action = menu_bar.addAction("🌍 Búsquedas Externas")
        busquedas_ext_action.setMenu(menu_externas)

        # --- 📚 Índices ---
        indices_action = menu_bar.addAction("📚 Índices")
        indices_action.triggered.connect(lambda: self.cambiar_ventana("indices"))
        # --- Añadir al header ---
        header_layout.addWidget(menu_bar)

        # --- Contenido principal ---
        self.label = QLabel("Selecciona una opción del menú")
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setStyleSheet("font-size: 20px; color: #2c3e50; font-weight: bold; margin-top: 40px;")

        main_layout.addWidget(header)
        main_layout.addWidget(self.label, stretch=1)

    # ==== Métodos de navegación ====
    def mostrar_opcion(self, texto):
        self.label.setText(f"Opción seleccionada: {texto}")

    # Internas
    def abrir_lineal(self): self.cambiar_ventana("lineal_interna")
    def abrir_binaria(self): self.cambiar_ventana("binaria_interna")
    def abrir_mod(self): self.cambiar_ventana("mod_interna")
    def abrir_cuadrado(self): self.cambiar_ventana("cuadrado_interna")
    def abrir_truncamiento(self): self.cambiar_ventana("truncamiento_interna")
    def abrir_plegamiento(self): self.cambiar_ventana("plegamiento_interna")
    def abrir_arboles_digitales(self): self.cambiar_ventana("arboles_digitales")
    def abrir_tries_residuos(self): self.cambiar_ventana("tries_residuos")
    def abrir_multiples_residuos(self): self.cambiar_ventana("multiples_residuos")
    def abrir_arboles_huffman(self): self.cambiar_ventana("arboles_huffman")

    # Externas
    def abrir_lineal_externa(self): self.cambiar_ventana("lineal_externa")
    def abrir_binaria_externa(self): self.cambiar_ventana("binaria_externa")
    def abrir_mod_externa(self): self.cambiar_ventana("mod_externa")
    def abrir_cuadrado_externa(self): self.cambiar_ventana("cuadrado_externa")
    def abrir_truncamiento_externa(self): self.cambiar_ventana("truncamiento_externa")
    def abrir_plegamiento_externa(self): self.cambiar_ventana("plegamiento_externa")
    def abrir_cambio_base(self): self.cambiar_ventana("cambio_base")

    # Cubetas (Externas)
    def abrir_cubeta_total(self): self.cambiar_ventana("cubeta_total")
    def abrir_cubeta_parcial(self): self.cambiar_ventana("cubeta_parcial")
    def abrir_indices(self): self.cambiar_ventana("indices")
