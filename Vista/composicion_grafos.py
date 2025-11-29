from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class ComposicionGrafos(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos del grafo G₁
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo1_ponderaciones = {}

        # Datos del grafo G₂
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.grafo2_ponderaciones = {}

        self.setWindowTitle("Ciencias de la Computación II - Composición de Grafos")

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

        titulo = QLabel("Ciencias de la Computación II - Composición de Grafos")
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
        controles_layout.setSpacing(20)
        controles_layout.setContentsMargins(15, 12, 15, 12)

        # --- GRAFO G₁ ---
        grafo1_container = QWidget()
        grafo1_layout = QVBoxLayout(grafo1_container)
        grafo1_layout.setSpacing(8)

        label_g1 = QLabel("Grafo G₁")
        label_g1.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo1_layout.addWidget(label_g1, alignment=Qt.AlignCenter)

        config_g1 = QHBoxLayout()
        lbl_v1 = QLabel("Vértices:")
        lbl_v1.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g1.addWidget(lbl_v1)
        self.vertices_spin_g1 = QSpinBox()
        self.vertices_spin_g1.setRange(2, 15)
        self.vertices_spin_g1.setValue(3)
        self.vertices_spin_g1.setFixedWidth(60)
        config_g1.addWidget(self.vertices_spin_g1)
        self.btn_crear_g1 = QPushButton("Crear")
        config_g1.addWidget(self.btn_crear_g1)
        grafo1_layout.addLayout(config_g1)

        botones_g1 = QHBoxLayout()
        self.btn_agregar_arista_g1 = QPushButton("+ Arista")
        self.btn_eliminar_arista_g1 = QPushButton("- Arista")
        botones_g1.addWidget(self.btn_agregar_arista_g1)
        botones_g1.addWidget(self.btn_eliminar_arista_g1)
        grafo1_layout.addLayout(botones_g1)

        botones_archivo_g1 = QHBoxLayout()
        self.btn_guardar_g1 = QPushButton("Guardar")
        self.btn_cargar_g1 = QPushButton("Cargar")
        botones_archivo_g1.addWidget(self.btn_guardar_g1)
        botones_archivo_g1.addWidget(self.btn_cargar_g1)
        grafo1_layout.addLayout(botones_archivo_g1)

        self.btn_limpiar_g1 = QPushButton("Limpiar")
        grafo1_layout.addWidget(self.btn_limpiar_g1)

        # --- GRAFO G₂ ---
        grafo2_container = QWidget()
        grafo2_layout = QVBoxLayout(grafo2_container)
        grafo2_layout.setSpacing(8)

        label_g2 = QLabel("Grafo G₂")
        label_g2.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo2_layout.addWidget(label_g2, alignment=Qt.AlignCenter)

        config_g2 = QHBoxLayout()
        lbl_v2 = QLabel("Vértices:")
        lbl_v2.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g2.addWidget(lbl_v2)
        self.vertices_spin_g2 = QSpinBox()
        self.vertices_spin_g2.setRange(2, 15)
        self.vertices_spin_g2.setValue(3)
        self.vertices_spin_g2.setFixedWidth(60)
        config_g2.addWidget(self.vertices_spin_g2)
        self.btn_crear_g2 = QPushButton("Crear")
        config_g2.addWidget(self.btn_crear_g2)
        grafo2_layout.addLayout(config_g2)

        botones_g2 = QHBoxLayout()
        self.btn_agregar_arista_g2 = QPushButton("+ Arista")
        self.btn_eliminar_arista_g2 = QPushButton("- Arista")
        botones_g2.addWidget(self.btn_agregar_arista_g2)
        botones_g2.addWidget(self.btn_eliminar_arista_g2)
        grafo2_layout.addLayout(botones_g2)

        botones_archivo_g2 = QHBoxLayout()
        self.btn_guardar_g2 = QPushButton("Guardar")
        self.btn_cargar_g2 = QPushButton("Cargar")
        botones_archivo_g2.addWidget(self.btn_guardar_g2)
        botones_archivo_g2.addWidget(self.btn_cargar_g2)
        grafo2_layout.addLayout(botones_archivo_g2)

        self.btn_limpiar_g2 = QPushButton("Limpiar")
        grafo2_layout.addWidget(self.btn_limpiar_g2)

        # --- COMPOSICIÓN ---
        composicion_container = QWidget()
        composicion_layout = QVBoxLayout(composicion_container)
        composicion_layout.setSpacing(8)

        label_composicion = QLabel("Generar Composición")
        label_composicion.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        composicion_layout.addWidget(label_composicion, alignment=Qt.AlignCenter)

        self.btn_generar = QPushButton("∘ Composición G₁ ∘ G₂")
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
        composicion_layout.addWidget(self.btn_generar)

        # Estilos de botones
        for btn in (self.btn_crear_g1, self.btn_agregar_arista_g1, self.btn_eliminar_arista_g1,
                    self.btn_guardar_g1, self.btn_cargar_g1, self.btn_limpiar_g1,
                    self.btn_crear_g2, self.btn_agregar_arista_g2, self.btn_eliminar_arista_g2,
                    self.btn_guardar_g2, self.btn_cargar_g2, self.btn_limpiar_g2):
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

        for spin in (self.vertices_spin_g1, self.vertices_spin_g2):
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
        controles_layout.addWidget(composicion_container)

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

        self.visual_g1 = VisualizadorGrafo("Grafo G₁", parent=self, es_editable=True)
        self.visual_g2 = VisualizadorGrafo("Grafo G₂", parent=self, es_editable=True)
        self.visual_composicion = VisualizadorGrafo("Composición G₁ ∘ G₂", parent=self, es_editable=False)

        # Conectar señales
        self.visual_g1.etiqueta_cambiada.connect(self.actualizar_etiqueta_g1)
        self.visual_g1.ponderacion_cambiada.connect(self.actualizar_ponderacion_g1)
        self.visual_g2.etiqueta_cambiada.connect(self.actualizar_etiqueta_g2)
        self.visual_g2.ponderacion_cambiada.connect(self.actualizar_ponderacion_g2)

        for visual in (self.visual_g1, self.visual_g2, self.visual_composicion):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_g1)
        grafos_layout.addWidget(self.visual_g2)
        grafos_layout.addWidget(self.visual_composicion)

        self.contenedor_layout.addLayout(grafos_layout)

        # Instrucciones
        instrucciones = QLabel(
            "💡 Clic izquierdo: Editar etiquetas/ponderaciones | Clic derecho + arrastrar: Mover aristas")
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

        btn_guardar_composicion = QPushButton("Guardar Composición")
        btn_guardar_composicion.setStyleSheet("""
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
        btn_guardar_composicion.clicked.connect(self.guardar_grafo_composicion)

        btn_limpiar_resultado = QPushButton("Limpiar Resultado")
        btn_limpiar_resultado.setStyleSheet("""
            QPushButton {
                background-color: #bf8f62;
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
                background-color: #d9534f;
                color: white;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #c9302c; }
        """)
        btn_limpiar_todo.clicked.connect(self.limpiar_todo)

        botones_extras.addWidget(btn_guardar_composicion)
        botones_extras.addWidget(btn_limpiar_resultado)
        botones_extras.addWidget(btn_limpiar_todo)

        self.contenedor_layout.addLayout(botones_extras)

        self.setCentralWidget(central)

        # ======= CONEXIONES G₁ =======
        self.btn_crear_g1.clicked.connect(self.crear_grafo_g1)
        self.btn_agregar_arista_g1.clicked.connect(self.agregar_arista_g1)
        self.btn_eliminar_arista_g1.clicked.connect(self.eliminar_arista_g1)
        self.btn_guardar_g1.clicked.connect(self.guardar_grafo_g1)
        self.btn_cargar_g1.clicked.connect(self.cargar_grafo_g1)
        self.btn_limpiar_g1.clicked.connect(self.limpiar_grafo_g1)

        # ======= CONEXIONES G₂ =======
        self.btn_crear_g2.clicked.connect(self.crear_grafo_g2)
        self.btn_agregar_arista_g2.clicked.connect(self.agregar_arista_g2)
        self.btn_eliminar_arista_g2.clicked.connect(self.eliminar_arista_g2)
        self.btn_guardar_g2.clicked.connect(self.guardar_grafo_g2)
        self.btn_cargar_g2.clicked.connect(self.cargar_grafo_g2)
        self.btn_limpiar_g2.clicked.connect(self.limpiar_grafo_g2)

        # ======= CONEXIÓN COMPOSICIÓN =======
        self.btn_generar.clicked.connect(self.generar_composicion)

    # ==================== CALLBACKS G₁ ====================
    def actualizar_etiqueta_g1(self, indice, nueva_etiqueta):
        self.grafo1_etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion_g1(self, arista, ponderacion):
        self.grafo1_ponderaciones[arista] = ponderacion

    # ==================== CALLBACKS G₂ ====================
    def actualizar_etiqueta_g2(self, indice, nueva_etiqueta):
        self.grafo2_etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion_g2(self, arista, ponderacion):
        self.grafo2_ponderaciones[arista] = ponderacion

    # ==================== GRAFO G₁ ====================
    def crear_grafo_g1(self):
        self.grafo1_vertices = self.vertices_spin_g1.value()
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {i: str(i + 1) for i in range(self.grafo1_vertices)}
        self.grafo1_ponderaciones = {}
        self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                 self.grafo1_etiquetas, self.grafo1_ponderaciones)
        DialogoClave(0, "Grafo G₁ creado", "mensaje", self,
                     f"Grafo G₁ creado con {self.grafo1_vertices} vértices.").exec()

    def agregar_arista_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el grafo G₁.").exec()
            return
        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            self.grafo1_aristas.append(arista)
            self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def eliminar_arista_g1(self):
        if not self.grafo1_aristas:
            DialogoClave(0, "Error", "mensaje", self, "No hay aristas para eliminar en G₁.").exec()
            return
        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo1_aristas:
                self.grafo1_aristas.remove(arista)
                if arista in self.grafo1_ponderaciones:
                    del self.grafo1_ponderaciones[arista]
                self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                         self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def limpiar_grafo_g1(self):
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo1_ponderaciones = {}
        self.visual_g1.set_grafo(0, [], {}, {})
        self.vertices_spin_g1.setValue(3)

    def guardar_grafo_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo G₁ para guardar.").exec()
            return
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo G₁", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_g1.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo_g1(self):
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
            self.vertices_spin_g1.setValue(self.grafo1_vertices)
            self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)

    # ==================== GRAFO G₂ ====================
    def crear_grafo_g2(self):
        self.grafo2_vertices = self.vertices_spin_g2.value()
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {i: chr(97 + i) for i in range(self.grafo2_vertices)}
        self.grafo2_ponderaciones = {}
        self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                 self.grafo2_etiquetas, self.grafo2_ponderaciones)
        DialogoClave(0, "Grafo G₂ creado", "mensaje", self,
                     f"Grafo G₂ creado con {self.grafo2_vertices} vértices.").exec()

    def agregar_arista_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el grafo G₂.").exec()
            return
        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            self.grafo2_aristas.append(arista)
            self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def eliminar_arista_g2(self):
        if not self.grafo2_aristas:
            DialogoClave(0, "Error", "mensaje", self, "No hay aristas para eliminar en G₂.").exec()
            return
        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo2_aristas:
                self.grafo2_aristas.remove(arista)
                if arista in self.grafo2_ponderaciones:
                    del self.grafo2_ponderaciones[arista]
                self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                         self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def limpiar_grafo_g2(self):
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.grafo2_ponderaciones = {}
        self.visual_g2.set_grafo(0, [], {}, {})
        self.vertices_spin_g2.setValue(3)

    def guardar_grafo_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo G₂ para guardar.").exec()
            return
        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo G₂", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_g2.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo_g2(self):
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
            self.vertices_spin_g2.setValue(self.grafo2_vertices)
            self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)

    # ==================== COMPOSICIÓN DE GRAFOS ====================
    def generar_composicion(self):
        if self.grafo1_vertices < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "El grafo G₁ necesita al menos 2 vértices.").exec()
            return

        if self.grafo2_vertices < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "El grafo G₂ necesita al menos 2 vértices.").exec()
            return

        # COMPOSICIÓN DE GRAFOS (G₁ ∘ G₂) - Producto Lexicográfico
        # V(G₁ ∘ G₂) = V(G₁) × V(G₂)
        # Dos vértices (g₁,h₁) y (g₂,h₂) son adyacentes en G₁ ∘ G₂ si y solo si:
        # 1. g₁ es adyacente a g₂ en G₁, O
        # 2. g₁ = g₂ Y h₁ es adyacente a h₂ en G₂

        vertices_composicion = self.grafo1_vertices * self.grafo2_vertices
        etiquetas_composicion = {}
        aristas_composicion = []

        # Crear mapeo de índices del producto cartesiano a par (i,j)
        indice_a_par = {}
        par_a_indice = {}
        indice = 0
        for i in range(self.grafo1_vertices):
            for j in range(self.grafo2_vertices):
                indice_a_par[indice] = (i, j)
                par_a_indice[(i, j)] = indice

                etiq_g1 = self.grafo1_etiquetas.get(i, str(i + 1))
                etiq_g2 = self.grafo2_etiquetas.get(j, chr(97 + j))
                etiquetas_composicion[indice] = f"({etiq_g1},{etiq_g2})"
                indice += 1

        # Crear conjuntos de adyacencia para búsqueda rápida
        adyacentes_g1 = set()
        for arista in self.grafo1_aristas:
            u, v = arista
            adyacentes_g1.add((min(u, v), max(u, v)))

        adyacentes_g2 = set()
        for arista in self.grafo2_aristas:
            u, v = arista
            adyacentes_g2.add((min(u, v), max(u, v)))

        # Generar aristas de la composición
        aristas_vistas = set()
        for idx1 in range(vertices_composicion):
            g1, h1 = indice_a_par[idx1]
            for idx2 in range(idx1 + 1, vertices_composicion):
                g2, h2 = indice_a_par[idx2]

                # Condición 1: g1 es adyacente a g2 en G₁
                g_arista = (min(g1, g2), max(g1, g2))
                es_adyacente_g1 = g_arista in adyacentes_g1

                # Condición 2: g1 = g2 Y h1 es adyacente a h2 en G₂
                h_arista = (min(h1, h2), max(h1, h2))
                es_mismo_vertice_g1_y_adyacente_g2 = (g1 == g2) and (h_arista in adyacentes_g2)

                # En la composición: conectar si se cumple condición 1 O condición 2
                if es_adyacente_g1 or es_mismo_vertice_g1_y_adyacente_g2:
                    arista_composicion = (min(idx1, idx2), max(idx1, idx2))
                    if arista_composicion not in aristas_vistas:
                        aristas_composicion.append(arista_composicion)
                        aristas_vistas.add(arista_composicion)

        ponderaciones_composicion = {}

        self.visual_composicion.set_grafo(
            vertices_composicion,
            aristas_composicion,
            etiquetas_composicion,
            ponderaciones_composicion
        )

        DialogoClave(0, "Composición Generada", "mensaje", self,
                     f"Composición generada:\n"
                     f"Vértices: {vertices_composicion}\n"
                     f"Aristas: {len(aristas_composicion)}").exec()

    # ==================== OPERACIONES ADICIONALES ====================
    def guardar_grafo_composicion(self):
        if not hasattr(self.visual_composicion, 'vertices') or self.visual_composicion.vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay composición para guardar.").exec()
            return
        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Composición", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_composicion.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def limpiar_resultado(self):
        self.visual_composicion.set_grafo(0, [], {}, {})

    def limpiar_todo(self):
        self.limpiar_grafo_g1()
        self.limpiar_grafo_g2()
        self.limpiar_resultado()