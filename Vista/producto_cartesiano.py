from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class ProductoCartesiano(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos de los grafos
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo1_ponderaciones = {}

        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.grafo2_ponderaciones = {}

        self.setWindowTitle("Ciencias de la Computación II - Producto Cartesiano")

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

        titulo = QLabel("Ciencias de la Computación II - Producto Cartesiano")
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

        # ======= CONTROLES =======
        controles_frame = QFrame()
        controles_frame.setStyleSheet("""
            QFrame {
                background-color: #FFDBB5;
                border-radius: 10px;
            }
        """)
        controles_layout = QHBoxLayout(controles_frame)
        controles_layout.setSpacing(15)
        controles_layout.setContentsMargins(15, 12, 15, 12)

        # --- GRAFO 1 ---
        grafo1_container = QWidget()
        grafo1_layout = QVBoxLayout(grafo1_container)
        grafo1_layout.setSpacing(8)

        label_grafo1 = QLabel("Grafo G₁")
        label_grafo1.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo1_layout.addWidget(label_grafo1, alignment=Qt.AlignCenter)

        config_g1 = QHBoxLayout()
        lbl_v1 = QLabel("Vértices:")
        lbl_v1.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g1.addWidget(lbl_v1)
        self.vertices1_spin = QSpinBox()
        self.vertices1_spin.setRange(2, 10)
        self.vertices1_spin.setValue(3)
        self.vertices1_spin.setFixedWidth(60)
        config_g1.addWidget(self.vertices1_spin)
        self.btn_crear1 = QPushButton("Crear")
        config_g1.addWidget(self.btn_crear1)
        grafo1_layout.addLayout(config_g1)

        botones_g1 = QHBoxLayout()
        self.btn_agregar_arista1 = QPushButton("+ Arista")
        self.btn_eliminar_arista1 = QPushButton("- Arista")
        botones_g1.addWidget(self.btn_agregar_arista1)
        botones_g1.addWidget(self.btn_eliminar_arista1)
        grafo1_layout.addLayout(botones_g1)

        botones_archivo1 = QHBoxLayout()
        self.btn_guardar1 = QPushButton("Guardar")
        self.btn_cargar1 = QPushButton("Cargar")
        botones_archivo1.addWidget(self.btn_guardar1)
        botones_archivo1.addWidget(self.btn_cargar1)
        grafo1_layout.addLayout(botones_archivo1)

        self.btn_limpiar1 = QPushButton("Limpiar")
        grafo1_layout.addWidget(self.btn_limpiar1)

        # --- GRAFO 2 ---
        grafo2_container = QWidget()
        grafo2_layout = QVBoxLayout(grafo2_container)
        grafo2_layout.setSpacing(8)

        label_grafo2 = QLabel("Grafo G₂")
        label_grafo2.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo2_layout.addWidget(label_grafo2, alignment=Qt.AlignCenter)

        config_g2 = QHBoxLayout()
        lbl_v2 = QLabel("Vértices:")
        lbl_v2.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g2.addWidget(lbl_v2)
        self.vertices2_spin = QSpinBox()
        self.vertices2_spin.setRange(2, 10)
        self.vertices2_spin.setValue(3)
        self.vertices2_spin.setFixedWidth(60)
        config_g2.addWidget(self.vertices2_spin)
        self.btn_crear2 = QPushButton("Crear")
        config_g2.addWidget(self.btn_crear2)
        grafo2_layout.addLayout(config_g2)

        botones_g2 = QHBoxLayout()
        self.btn_agregar_arista2 = QPushButton("+ Arista")
        self.btn_eliminar_arista2 = QPushButton("- Arista")
        botones_g2.addWidget(self.btn_agregar_arista2)
        botones_g2.addWidget(self.btn_eliminar_arista2)
        grafo2_layout.addLayout(botones_g2)

        botones_archivo2 = QHBoxLayout()
        self.btn_guardar2 = QPushButton("Guardar")
        self.btn_cargar2 = QPushButton("Cargar")
        botones_archivo2.addWidget(self.btn_guardar2)
        botones_archivo2.addWidget(self.btn_cargar2)
        grafo2_layout.addLayout(botones_archivo2)

        self.btn_limpiar2 = QPushButton("Limpiar")
        grafo2_layout.addWidget(self.btn_limpiar2)

        # --- TRANSFORMACIÓN ---
        transformacion_container = QWidget()
        transformacion_layout = QVBoxLayout(transformacion_container)
        transformacion_layout.setSpacing(8)

        label_transformacion = QLabel("Producto Cartesiano")
        label_transformacion.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        transformacion_layout.addWidget(label_transformacion, alignment=Qt.AlignCenter)

        self.btn_generar = QPushButton(" Calcular G₁ x G₂")
        self.btn_generar.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                padding: 8px 16px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #6C4E31; }
        """)
        transformacion_layout.addWidget(self.btn_generar)

        # Estilos de botones
        for btn in (self.btn_crear1, self.btn_agregar_arista1, self.btn_eliminar_arista1,
                    self.btn_guardar1, self.btn_cargar1, self.btn_limpiar1,
                    self.btn_crear2, self.btn_agregar_arista2, self.btn_eliminar_arista2,
                    self.btn_guardar2, self.btn_cargar2, self.btn_limpiar2):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6C4E31;
                    color: #FFEAC5;
                    padding: 6px 10px;
                    font-size: 13px;
                    border-radius: 6px;
                    min-width: 70px;
                }
                QPushButton:hover { background-color: #9c724a; }
            """)

        for spin in (self.vertices1_spin, self.vertices2_spin):
            spin.setStyleSheet("""
                QSpinBox {
                    padding: 4px;
                    border: 2px solid #bf8f62;
                    border-radius: 5px;
                    background: white;
                }
            """)

        controles_layout.addWidget(grafo1_container)
        controles_layout.addWidget(grafo2_container)
        controles_layout.addWidget(transformacion_container)

        layout.addWidget(controles_frame)

        # ======= VISUALIZACIÓN =======
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

        # Contenedor de grafos
        grafos_layout = QHBoxLayout()
        grafos_layout.setSpacing(20)
        grafos_layout.setAlignment(Qt.AlignCenter)

        self.visual_grafo1 = VisualizadorGrafo("Grafo G₁", parent=self, es_editable=True)
        self.visual_grafo2 = VisualizadorGrafo("Grafo G₂", parent=self, es_editable=True)
        self.visual_producto = VisualizadorGrafo("Producto G₁ □ G₂", parent=self, es_editable=False)

        # Conectar señales
        self.visual_grafo1.etiqueta_cambiada.connect(self.actualizar_etiqueta1)
        self.visual_grafo1.ponderacion_cambiada.connect(self.actualizar_ponderacion1)
        self.visual_grafo2.etiqueta_cambiada.connect(self.actualizar_etiqueta2)
        self.visual_grafo2.ponderacion_cambiada.connect(self.actualizar_ponderacion2)

        for visual in (self.visual_grafo1, self.visual_grafo2, self.visual_producto):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_grafo1)
        grafos_layout.addWidget(self.visual_grafo2)
        grafos_layout.addWidget(self.visual_producto)

        self.contenedor_layout.addLayout(grafos_layout)

        # Instrucciones
        instrucciones = QLabel(
            "💡 Clic izquierdo: Editar etiquetas/ponderaciones ")
        instrucciones.setStyleSheet("""
            QLabel {
                background-color: #FFDBB5;
                color: #6C4E31;
                padding: 8px 15px;
                border-radius: 8px;
                font-size: 12px;
                font-weight: bold;
            }
        """)
        instrucciones.setAlignment(Qt.AlignCenter)
        self.contenedor_layout.addWidget(instrucciones)

        # ======= BOTONES ADICIONALES =======
        botones_extras = QHBoxLayout()
        botones_extras.setSpacing(15)
        botones_extras.setAlignment(Qt.AlignCenter)

        btn_guardar_producto = QPushButton("Guardar Producto")
        btn_guardar_producto.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #6C4E31; }
        """)
        btn_guardar_producto.clicked.connect(self.guardar_grafo_producto)

        btn_limpiar_resultado = QPushButton("Limpiar Resultado")
        btn_limpiar_resultado.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #9c724a; }
        """)
        btn_limpiar_resultado.clicked.connect(self.limpiar_resultado)

        btn_limpiar_todo = QPushButton("Limpiar Todo")
        btn_limpiar_todo.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: white;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #c9302c; }
        """)
        btn_limpiar_todo.clicked.connect(self.limpiar_todo)

        botones_extras.addWidget(btn_guardar_producto)
        botones_extras.addWidget(btn_limpiar_resultado)
        botones_extras.addWidget(btn_limpiar_todo)

        self.contenedor_layout.addLayout(botones_extras)

        self.setCentralWidget(central)

        # ======= CONEXIONES =======
        self.btn_crear1.clicked.connect(self.crear_grafo1)
        self.btn_agregar_arista1.clicked.connect(self.agregar_arista1)
        self.btn_eliminar_arista1.clicked.connect(self.eliminar_arista1)
        self.btn_guardar1.clicked.connect(self.guardar_grafo1)
        self.btn_cargar1.clicked.connect(self.cargar_grafo1)
        self.btn_limpiar1.clicked.connect(self.limpiar_grafo1)

        self.btn_crear2.clicked.connect(self.crear_grafo2)
        self.btn_agregar_arista2.clicked.connect(self.agregar_arista2)
        self.btn_eliminar_arista2.clicked.connect(self.eliminar_arista2)
        self.btn_guardar2.clicked.connect(self.guardar_grafo2)
        self.btn_cargar2.clicked.connect(self.cargar_grafo2)
        self.btn_limpiar2.clicked.connect(self.limpiar_grafo2)

        self.btn_generar.clicked.connect(self.generar_producto_cartesiano)

    # ==================== CALLBACKS ====================
    def actualizar_etiqueta1(self, indice, nueva_etiqueta):
        self.grafo1_etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion1(self, arista, ponderacion):
        self.grafo1_ponderaciones[arista] = ponderacion

    def actualizar_etiqueta2(self, indice, nueva_etiqueta):
        self.grafo2_etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion2(self, arista, ponderacion):
        self.grafo2_ponderaciones[arista] = ponderacion

    # ==================== GRAFO 1 ====================
    def crear_grafo1(self):
        self.grafo1_vertices = self.vertices1_spin.value()
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {i: chr(97 + i) for i in range(self.grafo1_vertices)}  # a, b, c...
        self.grafo1_ponderaciones = {}
        self.visual_grafo1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)
        DialogoClave(0, "Grafo G₁ creado", "mensaje", self,
                     f"Grafo G₁ creado con {self.grafo1_vertices} vértices.").exec()

    def agregar_arista1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el grafo G₁.").exec()
            return
        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            self.grafo1_aristas.append(arista)
            self.visual_grafo1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                         self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def eliminar_arista1(self):
        if not self.grafo1_aristas:
            DialogoClave(0, "Error", "mensaje", self, "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo1_aristas:
                self.grafo1_aristas.remove(arista)
                if arista in self.grafo1_ponderaciones:
                    del self.grafo1_ponderaciones[arista]
                self.visual_grafo1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                             self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def limpiar_grafo1(self):
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo1_ponderaciones = {}
        self.visual_grafo1.set_grafo(0, [], {}, {})
        self.vertices1_spin.setValue(3)

    def guardar_grafo1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo para guardar.").exec()
            return
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo G₁", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_grafo1.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo1(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo G₁", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.grafo1_vertices = datos['vertices']
            self.grafo1_aristas = [tuple(a) for a in datos['aristas']]
            self.grafo1_etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
            self.grafo1_ponderaciones = {}
            for k, v in datos.get('ponderaciones', {}).items():
                arista_tuple = tuple(map(int, k.strip('()').split(', ')))
                self.grafo1_ponderaciones[arista_tuple] = v
            self.vertices1_spin.setValue(self.grafo1_vertices)
            self.visual_grafo1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                         self.grafo1_etiquetas, self.grafo1_ponderaciones)

    # ==================== GRAFO 2 ====================
    def crear_grafo2(self):
        self.grafo2_vertices = self.vertices2_spin.value()
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {i: str(i + 1) for i in range(self.grafo2_vertices)}  # 1, 2, 3...
        self.grafo2_ponderaciones = {}
        self.visual_grafo2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)
        DialogoClave(0, "Grafo G₂ creado", "mensaje", self,
                     f"Grafo G₂ creado con {self.grafo2_vertices} vértices.").exec()

    def agregar_arista2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el grafo G₂.").exec()
            return
        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            self.grafo2_aristas.append(arista)
            self.visual_grafo2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                         self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def eliminar_arista2(self):
        if not self.grafo2_aristas:
            DialogoClave(0, "Error", "mensaje", self, "No hay aristas para eliminar.").exec()
            return
        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo2_aristas:
                self.grafo2_aristas.remove(arista)
                if arista in self.grafo2_ponderaciones:
                    del self.grafo2_ponderaciones[arista]
                self.visual_grafo2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                             self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def limpiar_grafo2(self):
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.grafo2_ponderaciones = {}
        self.visual_grafo2.set_grafo(0, [], {}, {})
        self.vertices2_spin.setValue(3)

    def guardar_grafo2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo para guardar.").exec()
            return
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo G₂", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_grafo2.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo2(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo G₂", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.grafo2_vertices = datos['vertices']
            self.grafo2_aristas = [tuple(a) for a in datos['aristas']]
            self.grafo2_etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
            self.grafo2_ponderaciones = {}
            for k, v in datos.get('ponderaciones', {}).items():
                arista_tuple = tuple(map(int, k.strip('()').split(', ')))
                self.grafo2_ponderaciones[arista_tuple] = v
            self.vertices2_spin.setValue(self.grafo2_vertices)
            self.visual_grafo2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                         self.grafo2_etiquetas, self.grafo2_ponderaciones)

    # ==================== PRODUCTO CARTESIANO ====================
    def generar_producto_cartesiano(self):
        if self.grafo1_vertices < 2 or self.grafo2_vertices < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Ambos grafos deben tener al menos 2 vértices.").exec()
            return

        # ALGORITMO DEL PRODUCTO CARTESIANO G₁ □ G₂
        # V(G₁ □ G₂) = V(G₁) × V(G₂)
        # Dos vértices (u₁,v₁) y (u₂,v₂) son adyacentes si:
        # 1. u₁ = u₂ y (v₁,v₂) ∈ E(G₂), O
        # 2. v₁ = v₂ y (u₁,u₂) ∈ E(G₁)

        vertices_producto = self.grafo1_vertices * self.grafo2_vertices
        aristas_producto = []
        etiquetas_producto = {}

        # Crear mapeo de índices: (i, j) -> índice_producto
        mapeo = {}
        indice = 0
        for i in range(self.grafo1_vertices):
            for j in range(self.grafo2_vertices):
                mapeo[(i, j)] = indice
                etiq1 = self.grafo1_etiquetas.get(i, chr(97 + i))
                etiq2 = self.grafo2_etiquetas.get(j, str(j + 1))
                etiquetas_producto[indice] = f"({etiq1},{etiq2})"
                indice += 1

        # Crear aristas del producto cartesiano
        # Caso 1: u₁ = u₂ y (v₁,v₂) ∈ E(G₂)
        for u in range(self.grafo1_vertices):
            for arista2 in self.grafo2_aristas:
                v1, v2 = arista2
                vertice1 = mapeo[(u, v1)]
                vertice2 = mapeo[(u, v2)]
                arista_nueva = tuple(sorted([vertice1, vertice2]))
                if arista_nueva not in aristas_producto:
                    aristas_producto.append(arista_nueva)

        # Caso 2: v₁ = v₂ y (u₁,u₂) ∈ E(G₁)
        for v in range(self.grafo2_vertices):
            for arista1 in self.grafo1_aristas:
                u1, u2 = arista1
                vertice1 = mapeo[(u1, v)]
                vertice2 = mapeo[(u2, v)]
                arista_nueva = tuple(sorted([vertice1, vertice2]))
                if arista_nueva not in aristas_producto:
                    aristas_producto.append(arista_nueva)

        # Visualizar grafo producto
        self.visual_producto.set_grafo(vertices_producto, aristas_producto,
                                       etiquetas_producto, {})

        DialogoClave(0, "Producto Cartesiano Generado", "mensaje", self,
                     f"Grafo G₁: {self.grafo1_vertices} vértices, {len(self.grafo1_aristas)} aristas\n"
                     f"Grafo G₂: {self.grafo2_vertices} vértices, {len(self.grafo2_aristas)} aristas\n\n"
                     f"Producto Cartesiano G₁ □ G₂: {vertices_producto} vértices, {len(aristas_producto)} aristas\n\n"
                     f"Cada vértice (g,h) en G₁ □ G₂ representa un par del producto cartesiano V(G₁) × V(G₂)").exec()

    # ==================== FUNCIONES ADICIONALES ====================
    def guardar_grafo_producto(self):
        vertices_producto = self.visual_producto.num_vertices

        if vertices_producto == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay producto cartesiano para guardar.\nPrimero genera el producto.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Producto Cartesiano", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                datos = self.visual_producto.get_datos_grafo()
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)

                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Producto cartesiano guardado exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()

    def limpiar_resultado(self):
        self.visual_producto.set_grafo(0, [], {}, {})
        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Producto cartesiano limpiado.").exec()

    def limpiar_todo(self):
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo1_ponderaciones = {}

        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.grafo2_ponderaciones = {}

        self.visual_g1.set_grafo(0, [], {}, {})
        self.visual_g2.set_grafo(0, [], {}, {})
        self.visual_producto.set_grafo(0, [], {}, {})

        self.vertices_spin_g1.setValue(3)
        self.vertices_spin_g2.setValue(3)

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                         "Todos los grafos han sido limpiados.").exec()