from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QHBoxLayout, QScrollArea, QPushButton, QSpinBox, QFileDialog
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class SumaGrafos(QMainWindow):
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

        self.setWindowTitle("Ciencias de la Computación II - Suma de Grafos")

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

        titulo = QLabel("Ciencias de la Computación II - Suma de Grafos")
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

        # --- GRAFO 1 ---
        grafo1_container = QWidget()
        grafo1_layout = QVBoxLayout(grafo1_container)
        grafo1_layout.setSpacing(8)

        label_grafo1 = QLabel("Grafo 1")
        label_grafo1.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo1_layout.addWidget(label_grafo1, alignment=Qt.AlignCenter)

        config_g1 = QHBoxLayout()
        lbl_v1 = QLabel("Vértices:")
        lbl_v1.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g1.addWidget(lbl_v1)
        self.vertices_g1 = QSpinBox()
        self.vertices_g1.setRange(1, 20)
        self.vertices_g1.setValue(4)
        self.vertices_g1.setFixedWidth(60)
        config_g1.addWidget(self.vertices_g1)
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

        botones_extra_g1 = QHBoxLayout()
        self.btn_limpiar_g1 = QPushButton("Limpiar")
        self.btn_eliminar_vertice_g1 = QPushButton("- Vértice")
        botones_extra_g1.addWidget(self.btn_limpiar_g1)
        botones_extra_g1.addWidget(self.btn_eliminar_vertice_g1)
        grafo1_layout.addLayout(botones_extra_g1)

        # --- BOTÓN CALCULAR ---
        self.btn_calcular = QPushButton("Calcular Suma")
        self.btn_calcular.setFixedHeight(70)
        self.btn_calcular.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                padding: 5px 20px;
                font-size: 14px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #6C4E31; }
        """)

        # --- GRAFO 2 ---
        grafo2_container = QWidget()
        grafo2_layout = QVBoxLayout(grafo2_container)
        grafo2_layout.setSpacing(8)

        label_grafo2 = QLabel("Grafo 2")
        label_grafo2.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo2_layout.addWidget(label_grafo2, alignment=Qt.AlignCenter)

        config_g2 = QHBoxLayout()
        lbl_v2 = QLabel("Vértices:")
        lbl_v2.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g2.addWidget(lbl_v2)
        self.vertices_g2 = QSpinBox()
        self.vertices_g2.setRange(1, 20)
        self.vertices_g2.setValue(4)
        self.vertices_g2.setFixedWidth(60)
        config_g2.addWidget(self.vertices_g2)
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

        botones_extra_g2 = QHBoxLayout()
        self.btn_limpiar_g2 = QPushButton("Limpiar")
        self.btn_eliminar_vertice_g2 = QPushButton("- Vértice")
        botones_extra_g2.addWidget(self.btn_limpiar_g2)
        botones_extra_g2.addWidget(self.btn_eliminar_vertice_g2)
        grafo2_layout.addLayout(botones_extra_g2)

        # Estilos de botones
        for btn in (self.btn_crear_g1, self.btn_agregar_arista_g1, self.btn_eliminar_arista_g1,
                    self.btn_guardar_g1, self.btn_cargar_g1, self.btn_limpiar_g1, self.btn_eliminar_vertice_g1,
                    self.btn_crear_g2, self.btn_agregar_arista_g2, self.btn_eliminar_arista_g2,
                    self.btn_guardar_g2, self.btn_cargar_g2, self.btn_limpiar_g2, self.btn_eliminar_vertice_g2):
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

        for widget in (self.vertices_g1, self.vertices_g2):
            widget.setStyleSheet("""
                QSpinBox {
                    padding: 4px;
                    border: 2px solid #bf8f62;
                    border-radius: 5px;
                    background: white;
                }
            """)

        controles_layout.addWidget(grafo1_container)
        controles_layout.addWidget(self.btn_calcular)
        controles_layout.addWidget(grafo2_container)

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

        grafos_layout = QHBoxLayout()
        grafos_layout.setSpacing(20)
        grafos_layout.setAlignment(Qt.AlignCenter)

        self.visual_g1 = VisualizadorGrafo("Grafo 1", parent=self, es_editable=True)
        self.visual_g2 = VisualizadorGrafo("Grafo 2", parent=self, es_editable=True)
        self.visual_suma = VisualizadorGrafo("Suma (G1 + G2)", parent=self, es_editable=False)

        # Conectar señales
        self.visual_g1.etiqueta_cambiada.connect(self.actualizar_etiqueta_g1)
        self.visual_g1.ponderacion_cambiada.connect(self.actualizar_ponderacion_g1)
        self.visual_g2.etiqueta_cambiada.connect(self.actualizar_etiqueta_g2)
        self.visual_g2.ponderacion_cambiada.connect(self.actualizar_ponderacion_g2)

        for visual in (self.visual_g1, self.visual_g2, self.visual_suma):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_g1)
        grafos_layout.addWidget(self.visual_g2)
        grafos_layout.addWidget(self.visual_suma)

        self.contenedor_layout.addLayout(grafos_layout)

        # ======= BOTONES ADICIONALES =======
        botones_extras = QHBoxLayout()
        botones_extras.setSpacing(15)
        botones_extras.setAlignment(Qt.AlignCenter)

        btn_guardar_suma = QPushButton("Guardar Suma")
        btn_guardar_suma.setStyleSheet("""
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
        btn_guardar_suma.clicked.connect(self.guardar_suma)

        btn_limpiar_suma = QPushButton("Limpiar Suma")
        btn_limpiar_suma.setStyleSheet("""
            QPushButton {
                background-color: #9c724a ;
                color: #FFEAC5;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover { background-color: #9c724a; }
        """)
        btn_limpiar_suma.clicked.connect(self.limpiar_suma)

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

        botones_extras.addWidget(btn_guardar_suma)
        botones_extras.addWidget(btn_limpiar_suma)
        botones_extras.addWidget(btn_limpiar_todo)

        self.contenedor_layout.addLayout(botones_extras)

        self.setCentralWidget(central)

        # ======= CONEXIONES =======
        self.btn_crear_g1.clicked.connect(self.crear_grafo1)
        self.btn_crear_g2.clicked.connect(self.crear_grafo2)
        self.btn_agregar_arista_g1.clicked.connect(self.agregar_arista_g1)
        self.btn_agregar_arista_g2.clicked.connect(self.agregar_arista_g2)
        self.btn_eliminar_arista_g1.clicked.connect(self.eliminar_arista_g1)
        self.btn_eliminar_arista_g2.clicked.connect(self.eliminar_arista_g2)
        self.btn_guardar_g1.clicked.connect(self.guardar_grafo1)
        self.btn_cargar_g1.clicked.connect(self.cargar_grafo1)
        self.btn_guardar_g2.clicked.connect(self.guardar_grafo2)
        self.btn_cargar_g2.clicked.connect(self.cargar_grafo2)
        self.btn_limpiar_g1.clicked.connect(self.limpiar_grafo1)
        self.btn_limpiar_g2.clicked.connect(self.limpiar_grafo2)
        self.btn_eliminar_vertice_g1.clicked.connect(self.eliminar_vertice_g1)
        self.btn_eliminar_vertice_g2.clicked.connect(self.eliminar_vertice_g2)
        self.btn_calcular.clicked.connect(self.calcular_suma)

    # ==================== CALLBACKS ====================
    def actualizar_etiqueta_g1(self, indice, nueva_etiqueta):
        self.grafo1_etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion_g1(self, arista, ponderacion):
        self.grafo1_ponderaciones[arista] = ponderacion

    def actualizar_etiqueta_g2(self, indice, nueva_etiqueta):
        self.grafo2_etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion_g2(self, arista, ponderacion):
        self.grafo2_ponderaciones[arista] = ponderacion

    # ==================== GRAFO 1 ====================
    def crear_grafo1(self):
        self.grafo1_vertices = self.vertices_g1.value()
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {i: str(i + 1) for i in range(self.grafo1_vertices)}
        self.grafo1_ponderaciones = {}
        self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                 self.grafo1_etiquetas, self.grafo1_ponderaciones)
        DialogoClave(0, "Grafo 1", "mensaje", self,
                     f"Grafo 1 creado con {self.grafo1_vertices} vértices.").exec()

    def agregar_arista_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el Grafo 1.").exec()
            return

        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista[0] == arista[1]:
                DialogoClave(0, "Error", "mensaje", self, "No se permiten bucles.").exec()
                return
            self.grafo1_aristas.append(arista)
            self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def eliminar_arista_g1(self):
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
                self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                         self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def limpiar_grafo1(self):
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo1_ponderaciones = {}
        self.visual_g1.set_grafo(0, [], {}, {})
        self.vertices_g1.setValue(4)

    def guardar_grafo1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo 1", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_g1.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo1(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo 1", "", "JSON Files (*.json)")
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
            self.vertices_g1.setValue(self.grafo1_vertices)
            self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)

    def eliminar_vertice_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay vértices para eliminar.").exec()
            return

        from PySide6.QtWidgets import QInputDialog
        opciones = [f"{i+1}: {self.grafo1_etiquetas.get(i, str(i+1))}" for i in range(self.grafo1_vertices)]
        opcion, ok = QInputDialog.getItem(self, "Eliminar Vértice", "Selecciona el vértice:", opciones, 0, False)

        if ok and opcion:
            indice = int(opcion.split(":")[0]) - 1
            aristas_nuevas = []
            ponderaciones_nuevas = {}

            for arista in self.grafo1_aristas:
                origen, destino = arista
                if origen != indice and destino != indice:
                    nuevo_origen = origen if origen < indice else origen - 1
                    nuevo_destino = destino if destino < indice else destino - 1
                    nueva_arista = (nuevo_origen, nuevo_destino)
                    aristas_nuevas.append(nueva_arista)
                    if arista in self.grafo1_ponderaciones:
                        ponderaciones_nuevas[nueva_arista] = self.grafo1_ponderaciones[arista]

            etiquetas_nuevas = {}
            for i in range(self.grafo1_vertices):
                if i < indice:
                    etiquetas_nuevas[i] = self.grafo1_etiquetas.get(i, str(i + 1))
                elif i > indice:
                    etiquetas_nuevas[i - 1] = self.grafo1_etiquetas.get(i, str(i + 1))

            self.grafo1_vertices -= 1
            self.grafo1_aristas = aristas_nuevas
            self.grafo1_etiquetas = etiquetas_nuevas
            self.grafo1_ponderaciones = ponderaciones_nuevas
            self.vertices_g1.setValue(self.grafo1_vertices)
            self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)

    # ==================== GRAFO 2 ====================
    def crear_grafo2(self):
        self.grafo2_vertices = self.vertices_g2.value()
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {i: str(i + 1) for i in range(self.grafo2_vertices)}
        self.grafo2_ponderaciones = {}
        self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                 self.grafo2_etiquetas, self.grafo2_ponderaciones)
        DialogoClave(0, "Grafo 2", "mensaje", self,
                     f"Grafo 2 creado con {self.grafo2_vertices} vértices.").exec()

    def agregar_arista_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el Grafo 2.").exec()
            return

        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista[0] == arista[1]:
                DialogoClave(0, "Error", "mensaje", self, "No se permiten bucles.").exec()
                return
            self.grafo2_aristas.append(arista)
            self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def eliminar_arista_g2(self):
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
                self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                         self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def limpiar_grafo2(self):
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.grafo2_ponderaciones = {}
        self.visual_g2.set_grafo(0, [], {}, {})
        self.vertices_g2.setValue(4)

    def guardar_grafo2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo 2", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_g2.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo2(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo 2", "", "JSON Files (*.json)")
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
            self.vertices_g2.setValue(self.grafo2_vertices)
            self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)

    def eliminar_vertice_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay vértices para eliminar.").exec()
            return

        from PySide6.QtWidgets import QInputDialog
        opciones = [f"{i+1}: {self.grafo2_etiquetas.get(i, str(i+1))}" for i in range(self.grafo2_vertices)]
        opcion, ok = QInputDialog.getItem(self, "Eliminar Vértice", "Selecciona el vértice:", opciones, 0, False)

        if ok and opcion:
            indice = int(opcion.split(":")[0]) - 1
            etiqueta_eliminada = self.grafo2_etiquetas.get(indice, str(indice + 1))

            aristas_nuevas = []
            ponderaciones_nuevas = {}

            for arista in self.grafo2_aristas:
                origen, destino = arista
                if origen != indice and destino != indice:
                    nuevo_origen = origen if origen < indice else origen - 1
                    nuevo_destino = destino if destino < indice else destino - 1
                    nueva_arista = (nuevo_origen, nuevo_destino)
                    aristas_nuevas.append(nueva_arista)
                    if arista in self.grafo2_ponderaciones:
                        ponderaciones_nuevas[nueva_arista] = self.grafo2_ponderaciones[arista]

            etiquetas_nuevas = {}
            for i in range(self.grafo2_vertices):
                if i < indice:
                    etiquetas_nuevas[i] = self.grafo2_etiquetas.get(i, str(i + 1))
                elif i > indice:
                    etiquetas_nuevas[i - 1] = self.grafo2_etiquetas.get(i, str(i + 1))

            self.grafo2_vertices -= 1
            self.grafo2_aristas = aristas_nuevas
            self.grafo2_etiquetas = etiquetas_nuevas
            self.grafo2_ponderaciones = ponderaciones_nuevas
            self.vertices_g2.setValue(self.grafo2_vertices)
            self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)

            DialogoClave(0, "Vértice eliminado", "mensaje", self,
                         f"Vértice '{etiqueta_eliminada}' eliminado del Grafo 2.\n\n"
                         f"Vértices restantes: {self.grafo2_vertices}\n"
                         f"Aristas eliminadas: {len(self.grafo2_aristas) - len(aristas_nuevas)}").exec()

    # ==================== CALCULAR SUMA ====================
    def calcular_suma(self):
        if self.grafo1_vertices == 0 or self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Debes crear ambos grafos primero.").exec()
            return

        # Paso 1: Mapeo de etiquetas (unión de vértices)
        etiquetas_unicas = set()
        for i in range(self.grafo1_vertices):
            etiquetas_unicas.add(self.grafo1_etiquetas.get(i, str(i + 1)))
        for i in range(self.grafo2_vertices):
            etiquetas_unicas.add(self.grafo2_etiquetas.get(i, str(i + 1)))

        etiquetas_ordenadas = sorted(etiquetas_unicas)
        etiqueta_a_indice = {etiq: idx for idx, etiq in enumerate(etiquetas_ordenadas)}

        vertices_suma = len(etiquetas_ordenadas)
        etiquetas_suma = {idx: etiq for etiq, idx in etiqueta_a_indice.items()}

        # Crear grafo completo (todas las conexiones posibles)
        aristas_finales = []
        ponderaciones_finales = {}  # 👈 CAMBIAR DE LISTA A DICCIONARIO

        # Conectar cada vértice con todos los demás
        for i in range(vertices_suma):
            for j in range(i + 1, vertices_suma):
                arista = (i, j)
                aristas_finales.append(arista)
                ponderaciones_finales[arista] = ""  # 👈 USAR DICCIONARIO

        # Visualizar el grafo completo
        self.visual_suma.set_grafo(
            vertices_suma,
            aristas_finales,
            etiquetas_suma,
            ponderaciones_finales  # Ahora es un diccionario
        )

        DialogoClave(0, "Suma calculada", "mensaje", self,
                     f"Grafo Completo calculado:\n\n"
                     f"• Vértices totales: {vertices_suma}\n"
                     f"• Vértices de G1: {self.grafo1_vertices}\n"
                     f"• Vértices de G2: {self.grafo2_vertices}\n"
                     f"• Aristas en grafo completo: {len(aristas_finales)}").exec()
        # ==================== FUNCIONES SUMA ====================
    def guardar_suma(self):
        datos_suma = self.visual_suma.get_datos_grafo()

        if datos_suma['vertices'] == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay suma para guardar.\nPrimero calcula la suma.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Suma", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos_suma, f, indent=4, ensure_ascii=False)
                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Suma guardada exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()

    def limpiar_suma(self):
        """Limpia solo la visualización de la suma"""
        self.visual_suma.set_grafo(0, [], {}, {})
        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Visualización de Suma limpiada.").exec()

    def limpiar_todo(self):
        """Limpia completamente todos los grafos"""
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
        self.visual_suma.set_grafo(0, [], {}, {})

        self.vertices_g1.setValue(4)
        self.vertices_g2.setValue(4)

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Todos los grafos han sido limpiados.").exec()
