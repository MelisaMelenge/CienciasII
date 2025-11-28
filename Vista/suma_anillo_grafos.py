from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QHBoxLayout, QScrollArea, QPushButton, QSpinBox,
    QGridLayout, QMessageBox
)
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
from Vista.dialogo_arista import DialogoArista
from Vista.visualizador_grafo import VisualizadorGrafo
import math


class SumaAnilloGrafos(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos de los grafos
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo2_vertices = 0
        self.grafo2_aristas = []

        self.setWindowTitle("Ciencias de la Computación II - Suma de Anillo de Grafos")

        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        layout = QVBoxLayout(central)
        layout.setSpacing(15)
        layout.setContentsMargins(10, 10, 10, 10)

        # ======= HEADER =======
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62);
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Ciencias de la Computación II - Suma de Anillo de Grafos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2d1f15; margin: 10px;")
        header_layout.addWidget(titulo)

        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)
        menu_layout.setAlignment(Qt.AlignCenter)
        btn_inicio = QPushButton("Inicio")
        btn_grafos = QPushButton("Menú de Grafos")
        for btn in (btn_inicio, btn_grafos):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2d1f15;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover { 
                    color: #FFEAC5; 
                    background-color: #6C4E31;
                    border-radius: 8px;
                }
            """)
            menu_layout.addWidget(btn)
        header_layout.addLayout(menu_layout)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_grafos.clicked.connect(lambda: self.cambiar_ventana("grafos"))
        layout.addWidget(header)

        # ======= CONTROLES COMPACTOS Y ESTÉTICOS =======
        controles_frame = QFrame()
        controles_frame.setStyleSheet("""
            QFrame {
                background-color: #FFDBB5;
                border-radius: 10px;
            }
        """)
        controles_layout = QHBoxLayout(controles_frame)
        controles_layout.setSpacing(30)
        controles_layout.setContentsMargins(25, 12, 25, 12)

        # --- GRAFO 1 ---
        grafo1_container = QWidget()
        grafo1_layout = QHBoxLayout(grafo1_container)
        grafo1_layout.setSpacing(10)
        grafo1_layout.setContentsMargins(0, 0, 0, 0)

        label_grafo1 = QLabel("Grafo 1")
        label_grafo1.setStyleSheet("font-size: 14px; font-weight: bold; color: #6C4E31;")

        lbl_v1 = QLabel("Vértices:")
        lbl_v1.setStyleSheet("font-size: 13px; color: #2d1f15;")
        self.vertices_g1 = QSpinBox()
        self.vertices_g1.setRange(1, 20)
        self.vertices_g1.setValue(4)
        self.vertices_g1.setFixedWidth(60)
        self.vertices_g1.setStyleSheet("""
            QSpinBox {
                padding: 4px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
            }
        """)

        self.btn_crear_g1 = QPushButton("Crear")
        self.btn_agregar_arista_g1 = QPushButton("+ Arista")

        grafo1_layout.addWidget(label_grafo1)
        grafo1_layout.addWidget(lbl_v1)
        grafo1_layout.addWidget(self.vertices_g1)
        grafo1_layout.addWidget(self.btn_crear_g1)
        grafo1_layout.addWidget(self.btn_agregar_arista_g1)

        # --- BOTÓN CALCULAR ---
        self.btn_calcular = QPushButton("⊕ Calcular\nSuma Anillo")
        self.btn_calcular.setFixedHeight(50)
        self.btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                padding: 5px 20px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #6C4E31; }
        """)

        # --- GRAFO 2 ---
        grafo2_container = QWidget()
        grafo2_layout = QHBoxLayout(grafo2_container)
        grafo2_layout.setSpacing(10)
        grafo2_layout.setContentsMargins(0, 0, 0, 0)

        label_grafo2 = QLabel("Grafo 2")
        label_grafo2.setStyleSheet("font-size: 14px; font-weight: bold; color: #6C4E31;")

        lbl_v2 = QLabel("Vértices:")
        lbl_v2.setStyleSheet("font-size: 13px; color: #2d1f15;")
        self.vertices_g2 = QSpinBox()
        self.vertices_g2.setRange(1, 20)
        self.vertices_g2.setValue(4)
        self.vertices_g2.setFixedWidth(60)
        self.vertices_g2.setStyleSheet("""
            QSpinBox {
                padding: 4px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
            }
        """)

        self.btn_crear_g2 = QPushButton("Crear")
        self.btn_agregar_arista_g2 = QPushButton("+ Arista")

        grafo2_layout.addWidget(label_grafo2)
        grafo2_layout.addWidget(lbl_v2)
        grafo2_layout.addWidget(self.vertices_g2)
        grafo2_layout.addWidget(self.btn_crear_g2)
        grafo2_layout.addWidget(self.btn_agregar_arista_g2)

        # Estilos de botones
        for btn in (self.btn_crear_g1, self.btn_agregar_arista_g1,
                    self.btn_crear_g2, self.btn_agregar_arista_g2):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6C4E31;
                    color: #FFEAC5;
                    padding: 6px 12px;
                    font-size: 13px;
                    border-radius: 6px;
                    min-width: 70px;
                }
                QPushButton:hover { background-color: #9c724a; }
            """)

        # Agregar todo al layout principal
        controles_layout.addWidget(grafo1_container)
        controles_layout.addWidget(self.btn_calcular)
        controles_layout.addWidget(grafo2_container)

        layout.addWidget(controles_frame)

        # ======= AREA DE VISUALIZACION =======
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("background-color: transparent;")
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(20)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        # Visualizadores de grafos
        grafos_layout = QHBoxLayout()
        grafos_layout.setSpacing(20)
        grafos_layout.setAlignment(Qt.AlignCenter)

        self.visual_g1 = VisualizadorGrafo("Grafo 1")
        self.visual_g2 = VisualizadorGrafo("Grafo 2")
        self.visual_suma_anillo = VisualizadorGrafo("Suma Anillo (G1 ⊕ G2)")

        for visual in (self.visual_g1, self.visual_g2, self.visual_suma_anillo):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_g1)
        grafos_layout.addWidget(self.visual_g2)
        grafos_layout.addWidget(self.visual_suma_anillo)

        self.contenedor_layout.addLayout(grafos_layout)

        self.setCentralWidget(central)

        # ======= CONEXIONES =======
        self.btn_crear_g1.clicked.connect(self.crear_grafo1)
        self.btn_crear_g2.clicked.connect(self.crear_grafo2)
        self.btn_agregar_arista_g1.clicked.connect(self.agregar_arista_g1)
        self.btn_agregar_arista_g2.clicked.connect(self.agregar_arista_g2)
        self.btn_calcular.clicked.connect(self.calcular_suma_anillo)

    # ==================== FUNCIONES ====================
    def crear_grafo1(self):
        self.grafo1_vertices = self.vertices_g1.value()
        self.grafo1_aristas = []
        self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas)
        QMessageBox.information(self, "Grafo 1", f"Grafo 1 creado con {self.grafo1_vertices} vértices.")

    def crear_grafo2(self):
        self.grafo2_vertices = self.vertices_g2.value()
        self.grafo2_aristas = []
        self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas)
        QMessageBox.information(self, "Grafo 2", f"Grafo 2 creado con {self.grafo2_vertices} vértices.")

    def agregar_arista_g1(self):
        if self.grafo1_vertices == 0:
            QMessageBox.warning(self, "Error", "Primero debes crear el Grafo 1.")
            return

        dlg = DialogoArista(self.grafo1_vertices, self)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista not in self.grafo1_aristas:
                self.grafo1_aristas.append(arista)
                self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas)
                QMessageBox.information(self, "Arista agregada",
                                        f"Arista ({arista[0] + 1}, {arista[1] + 1}) agregada al Grafo 1.")

    def agregar_arista_g2(self):
        if self.grafo2_vertices == 0:
            QMessageBox.warning(self, "Error", "Primero debes crear el Grafo 2.")
            return

        dlg = DialogoArista(self.grafo2_vertices, self)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista not in self.grafo2_aristas:
                self.grafo2_aristas.append(arista)
                self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas)
                QMessageBox.information(self, "Arista agregada",
                                        f"Arista ({arista[0] + 1}, {arista[1] + 1}) agregada al Grafo 2.")

    def calcular_suma_anillo(self):
        if self.grafo1_vertices == 0 or self.grafo2_vertices == 0:
            QMessageBox.warning(self, "Error", "Debes crear ambos grafos primero.")
            return

        # S3 = S1 ∪ S2 (Unión de vértices)
        vertices_suma_anillo = max(self.grafo1_vertices, self.grafo2_vertices)

        # A3 = (A1 ∪ A2) - (A1 ∩ A2)
        # Paso 1: Calcular A1 ∪ A2 (unión de aristas)
        aristas_union = list(self.grafo1_aristas)
        for arista in self.grafo2_aristas:
            if arista not in aristas_union:
                origen, destino = arista
                if origen < vertices_suma_anillo and destino < vertices_suma_anillo:
                    aristas_union.append(arista)

        # Paso 2: Calcular A1 ∩ A2 (intersección de aristas)
        vertices_interseccion = min(self.grafo1_vertices, self.grafo2_vertices)
        aristas_interseccion = []
        for arista in self.grafo1_aristas:
            origen, destino = arista
            if (origen < vertices_interseccion and
                    destino < vertices_interseccion and
                    arista in self.grafo2_aristas):
                aristas_interseccion.append(arista)

        # Paso 3: A3 = (A1 ∪ A2) - (A1 ∩ A2)
        aristas_suma_anillo = []
        for arista in aristas_union:
            if arista not in aristas_interseccion:
                aristas_suma_anillo.append(arista)

        self.visual_suma_anillo.set_grafo(vertices_suma_anillo, aristas_suma_anillo)

        QMessageBox.information(self, "Suma Anillo calculada",
                                f"Suma Anillo calculada:\n\n"
                                f"• Vértices: {vertices_suma_anillo}\n"
                                f"• Aristas en A1 ∪ A2: {len(aristas_union)}\n"
                                f"• Aristas en A1 ∩ A2: {len(aristas_interseccion)}\n"
                                f"• Aristas finales (A1 ∪ A2) - (A1 ∩ A2): {len(aristas_suma_anillo)}\n\n"
                                f"La suma anillo incluye las aristas que están\n"
                                f"en un grafo u otro, pero NO en ambos.")