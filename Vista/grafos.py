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
        menu_operaciones.addAction("Suma", lambda: self.cambiar_ventana("suma_grafos"))
        menu_operaciones.addAction("Fusión de vértice", lambda: self.cambiar_ventana("fusion_vertice"))
        menu_operaciones.addAction("Contracción de arista", lambda: self.cambiar_ventana("contraccion_arista"))
        menu_operaciones.addAction("Grafo línea", lambda: self.cambiar_ventana("grafo_linea"))
        menu_operaciones.addAction("Grafo complementario", lambda: self.cambiar_ventana("grafo_complementario"))
        menu_operaciones.addAction("Producto cartesiano", lambda: self.cambiar_ventana("producto_cartesiano"))
        menu_operaciones.addAction("Producto tensorial", lambda: self.cambiar_ventana("producto_tensorial"))
        menu_operaciones.addAction("Composición de grafos", lambda: self.cambiar_ventana("composicion_grafos"))

        operaciones_action = menu_bar.addAction("🧩 Operaciones entre grafos")
        operaciones_action.setMenu(menu_operaciones)

        # --- 🌳 Grafos como Árboles ---
        menu_arboles = QMenu("🌳 Grafos como Árboles", self)
        menu_arboles.addAction("Árbol expansión mínima", lambda: self.cambiar_ventana("arbol_expansion_minima"))
        menu_arboles.addAction("Árbol expansión máxima", lambda: self.cambiar_ventana("arbol_expansion_maxima"))
        menu_arboles.addAction("Árbol expansión central", lambda: self.cambiar_ventana("arbol_expansion_central"))
        menu_arboles.addAction("Distancia entre dos árboles", lambda: self.cambiar_ventana("distancia_arboles"))

        arboles_action = menu_bar.addAction("🌳 Grafos como Árboles")
        arboles_action.setMenu(menu_arboles)

        # --- Algoritmos ---
        menu_algoritmos = QMenu("Algoritmos", self)
        menu_algoritmos.addAction("Bellman", lambda: self.cambiar_ventana("bellman"))
        menu_algoritmos.addAction("Dijkstra", lambda: self.cambiar_ventana("dijkstra"))
        menu_algoritmos.addAction("Floyd", lambda: self.cambiar_ventana("floyd"))  # Cambiar a minúscula

        algoritmos_action = menu_bar.addAction("🔢 Algoritmos")
        algoritmos_action.setMenu(menu_algoritmos)
        
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

    # Operaciones entre grafos
    def abrir_interseccion(self): self.cambiar_ventana("interseccion_grafos")
    def abrir_union(self): self.cambiar_ventana("union_grafos")
    def abrir_suma_anillo(self): self.cambiar_ventana("suma_anillo_grafos")
    def abrir_suma(self): self.cambiar_ventana("suma_grafos")
    def abrir_fusion_vertice(self): self.cambiar_ventana("fusion_vertice")
    def abrir_contraccion_arista(self): self.cambiar_ventana("contraccion_arista")
    def abrir_grafo_linea(self): self.cambiar_ventana("grafo_linea")
    def abrir_grafo_complementario(self): self.cambiar_ventana("grafo_complementario")
    def abrir_producto_cartesiano(self): self.cambiar_ventana("producto_cartesiano")
    def abrir_producto_tensorial(self): self.cambiar_ventana("producto_tensorial")
    def abrir_composicion(self): self.cambiar_ventana("composicion_grafos")

    # Grafos como Árboles
    def abrir_arbol_expansion_minima(self): self.cambiar_ventana("arbol_expansion_minima")
    def abrir_arbol_expansion_maxima(self): self.cambiar_ventana("arbol_expansion_maxima")
    def abrir_arbol_expansion_central(self): self.cambiar_ventana("arbol_expansion_central")
    def abrir_distancia_arboles(self): self.cambiar_ventana("distancia_arboles")
    # Algoritmos
    def abrir_bellman(self): self.cambiar_ventana("bellman")
    def abrir_dijkstra(self): self.cambiar_ventana("dijkstra")
    def abrir_floyd(self): self.cambiar_ventana("floyd")


