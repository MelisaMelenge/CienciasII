from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QHBoxLayout, QScrollArea, QPushButton, QSpinBox, QFileDialog
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class InterseccionGrafos(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos de los grafos
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}

        self.setWindowTitle("Ciencias de la Computación II - Intersección de Grafos")

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

        titulo = QLabel("Ciencias de la Computación II - Intersección de Grafos")
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

        # NUEVO: Botones Limpiar y Eliminar Vértice en la misma fila
        botones_extra_g1 = QHBoxLayout()
        self.btn_limpiar_g1 = QPushButton("Limpiar")
        self.btn_eliminar_vertice_g1 = QPushButton("- Vértice")
        botones_extra_g1.addWidget(self.btn_limpiar_g1)
        botones_extra_g1.addWidget(self.btn_eliminar_vertice_g1)
        grafo1_layout.addLayout(botones_extra_g1)

        # --- BOTÓN CALCULAR ---
        self.btn_calcular = QPushButton("Calcular Intersección")
        self.btn_calcular.setFixedHeight(60)
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

        # NUEVO: Botones Limpiar y Eliminar Vértice en la misma fila
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
        self.visual_interseccion = VisualizadorGrafo("Intersección (G1 ∩ G2)", parent=self, es_editable=False)

        for visual in (self.visual_g1, self.visual_g2, self.visual_interseccion):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_g1)
        grafos_layout.addWidget(self.visual_g2)
        grafos_layout.addWidget(self.visual_interseccion)

        self.contenedor_layout.addLayout(grafos_layout)

        # ======= BOTONES ADICIONALES =======
        botones_extras = QHBoxLayout()
        botones_extras.setSpacing(15)
        botones_extras.setAlignment(Qt.AlignCenter)

        # Botón para guardar la intersección
        btn_guardar_interseccion = QPushButton("Guardar Intersección")
        btn_guardar_interseccion.setStyleSheet("""
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
        btn_guardar_interseccion.clicked.connect(self.guardar_interseccion)

        # Botón para limpiar la intersección
        btn_limpiar_interseccion = QPushButton(" Limpiar Intersección")
        btn_limpiar_interseccion.setStyleSheet("""
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
        btn_limpiar_interseccion.clicked.connect(self.limpiar_interseccion)

        # Botón para limpiar todo
        btn_limpiar_todo = QPushButton(" Limpiar Todo")
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

        botones_extras.addWidget(btn_guardar_interseccion)
        botones_extras.addWidget(btn_limpiar_interseccion)
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
        self.btn_calcular.clicked.connect(self.calcular_interseccion)

    # ==================== FUNCIONES GRAFO 1 ====================
    def crear_grafo1(self):
        self.grafo1_vertices = self.vertices_g1.value()
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {i: str(i + 1) for i in range(self.grafo1_vertices)}
        self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas, self.grafo1_etiquetas)
        DialogoClave(0, "Grafo 1", "mensaje", self,
                     f"Grafo 1 creado con {self.grafo1_vertices} vértices.\n\n"
                     "Haz clic en un vértice para cambiar su etiqueta.").exec()

    def agregar_arista_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero debes crear el Grafo 1.").exec()
            return

        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista[0] == arista[1]:
                DialogoClave(0, "Error", "mensaje", self,
                             "No se permiten bucles\n(arista de un vértice a sí mismo).").exec()
                return
            if arista not in self.grafo1_aristas:
                self.grafo1_aristas.append(arista)
                self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas, self.grafo1_etiquetas)
                etiq_origen = self.grafo1_etiquetas.get(arista[0], str(arista[0] + 1))
                etiq_destino = self.grafo1_etiquetas.get(arista[1], str(arista[1] + 1))
                DialogoClave(0, "Arista agregada", "mensaje", self,
                             f"Arista ({etiq_origen} ↔ {etiq_destino}) agregada al Grafo 1.").exec()
            else:
                DialogoClave(0, "Advertencia", "mensaje", self,
                             "Esta arista ya existe en el Grafo 1.").exec()

    def eliminar_arista_g1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero debes crear el Grafo 1.").exec()
            return

        if not self.grafo1_aristas:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar en el Grafo 1.").exec()
            return

        dlg = DialogoArista(self.grafo1_vertices, self, self.grafo1_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo1_aristas:
                self.grafo1_aristas.remove(arista)
                self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas, self.grafo1_etiquetas)
                etiq_origen = self.grafo1_etiquetas.get(arista[0], str(arista[0] + 1))
                etiq_destino = self.grafo1_etiquetas.get(arista[1], str(arista[1] + 1))
                DialogoClave(0, "Arista eliminada", "mensaje", self,
                             f"Arista ({etiq_origen} ↔ {etiq_destino}) eliminada del Grafo 1.").exec()
            else:
                etiq_origen = self.grafo1_etiquetas.get(arista[0], str(arista[0] + 1))
                etiq_destino = self.grafo1_etiquetas.get(arista[1], str(arista[1] + 1))
                DialogoClave(0, "Error", "mensaje", self,
                             f"La arista ({etiq_origen} ↔ {etiq_destino}) no existe en el Grafo 1.").exec()

    def limpiar_grafo1(self):
        """Limpia completamente el Grafo 1"""
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Información", "mensaje", self,
                         "El Grafo 1 ya está vacío.").exec()
            return

        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.visual_g1.set_grafo(0, [], {})
        self.vertices_g1.setValue(4)  # Resetear a valor por defecto

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Grafo 1 limpiado completamente.").exec()

    def guardar_grafo1(self):
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay grafo para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Grafo 1", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                datos = self.visual_g1.get_datos_grafo()
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Grafo 1 guardado exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()

    def cargar_grafo1(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Cargar Grafo 1", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)

                self.grafo1_vertices = datos['vertices']
                self.grafo1_aristas = [tuple(a) for a in datos['aristas']]
                self.grafo1_etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}

                self.vertices_g1.setValue(self.grafo1_vertices)
                self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas, self.grafo1_etiquetas)

                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Grafo 1 cargado exitosamente:\n"
                             f"• Vértices: {self.grafo1_vertices}\n"
                             f"• Aristas: {len(self.grafo1_aristas)}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al cargar el archivo:\n{str(e)}").exec()

    # ==================== FUNCIONES GRAFO 2 ====================
    def crear_grafo2(self):
        self.grafo2_vertices = self.vertices_g2.value()
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {i: str(i + 1) for i in range(self.grafo2_vertices)}
        self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas, self.grafo2_etiquetas)
        DialogoClave(0, "Grafo 2", "mensaje", self,
                     f"Grafo 2 creado con {self.grafo2_vertices} vértices.\n\n"
                     "Haz clic en un vértice para cambiar su etiqueta.").exec()

    def agregar_arista_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero debes crear el Grafo 2.").exec()
            return

        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista[0] == arista[1]:
                DialogoClave(0, "Error", "mensaje", self,
                             "No se permiten bucles\n(arista de un vértice a sí mismo).").exec()
                return
            if arista not in self.grafo2_aristas:
                self.grafo2_aristas.append(arista)
                self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas, self.grafo2_etiquetas)
                etiq_origen = self.grafo2_etiquetas.get(arista[0], str(arista[0] + 1))
                etiq_destino = self.grafo2_etiquetas.get(arista[1], str(arista[1] + 1))
                DialogoClave(0, "Arista agregada", "mensaje", self,
                             f"Arista ({etiq_origen} ↔ {etiq_destino}) agregada al Grafo 2.").exec()
            else:
                DialogoClave(0, "Advertencia", "mensaje", self,
                             "Esta arista ya existe en el Grafo 2.").exec()

    def eliminar_arista_g2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero debes crear el Grafo 2.").exec()
            return

        if not self.grafo2_aristas:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para eliminar en el Grafo 2.").exec()
            return

        dlg = DialogoArista(self.grafo2_vertices, self, self.grafo2_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo2_aristas:
                self.grafo2_aristas.remove(arista)
                self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas, self.grafo2_etiquetas)
                etiq_origen = self.grafo2_etiquetas.get(arista[0], str(arista[0] + 1))
                etiq_destino = self.grafo2_etiquetas.get(arista[1], str(arista[1] + 1))
                DialogoClave(0, "Arista eliminada", "mensaje", self,
                             f"Arista ({etiq_origen} ↔ {etiq_destino}) eliminada del Grafo 2.").exec()
            else:
                etiq_origen = self.grafo2_etiquetas.get(arista[0], str(arista[0] + 1))
                etiq_destino = self.grafo2_etiquetas.get(arista[1], str(arista[1] + 1))
                DialogoClave(0, "Error", "mensaje", self,
                             f"La arista ({etiq_origen} ↔ {etiq_destino}) no existe en el Grafo 2.").exec()

    def limpiar_grafo2(self):
        """Limpia completamente el Grafo 2"""
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Información", "mensaje", self,
                         "El Grafo 2 ya está vacío.").exec()
            return

        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.visual_g2.set_grafo(0, [], {})
        self.vertices_g2.setValue(4)  # Resetear a valor por defecto

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Grafo 2 limpiado completamente.").exec()

    def guardar_grafo2(self):
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay grafo para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Grafo 2", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                datos = self.visual_g2.get_datos_grafo()
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Grafo 2 guardado exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()

    def cargar_grafo2(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Cargar Grafo 2", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)

                self.grafo2_vertices = datos['vertices']
                self.grafo2_aristas = [tuple(a) for a in datos['aristas']]
                self.grafo2_etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}

                self.vertices_g2.setValue(self.grafo2_vertices)
                self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas, self.grafo2_etiquetas)

                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Grafo 2 cargado exitosamente:\n"
                             f"• Vértices: {self.grafo2_vertices}\n"
                             f"• Aristas: {len(self.grafo2_aristas)}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al cargar el archivo:\n{str(e)}").exec()

    def limpiar_grafo1(self):
        """Limpia completamente el Grafo 1"""
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.vertices_g1.setValue(4)
        self.visual_g1.set_grafo(0, [], {})
        DialogoClave(0, "Limpieza completada", "mensaje", self,
                     "Grafo 1 limpiado exitosamente.").exec()

    def limpiar_grafo2(self):
        """Limpia completamente el Grafo 2"""
        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.vertices_g2.setValue(4)
        self.visual_g2.set_grafo(0, [], {})
        DialogoClave(0, "Limpieza completada", "mensaje", self,
                     "Grafo 2 limpiado exitosamente.").exec()

    # ==================== CALCULAR INTERSECCIÓN ====================
    def calcular_interseccion(self):
        if self.grafo1_vertices == 0 or self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Debes crear ambos grafos primero.").exec()
            return

        # Obtener etiquetas de ambos grafos
        etiquetas_g1 = set(self.grafo1_etiquetas.values())
        etiquetas_g2 = set(self.grafo2_etiquetas.values())

        # Vértices de la intersección: etiquetas que están en ambos grafos
        etiquetas_comunes = etiquetas_g1.intersection(etiquetas_g2)

        if not etiquetas_comunes:
            DialogoClave(0, "Intersección vacía", "mensaje", self,
                         "No hay vértices con etiquetas comunes\n"
                         "entre ambos grafos.\n\n"
                         "La intersección está vacía.").exec()
            self.visual_interseccion.set_grafo(0, [], {})
            return

        # Crear mapeo de etiquetas a índices para cada grafo
        etiq_a_indice_g1 = {etiq: idx for idx, etiq in self.grafo1_etiquetas.items()}
        etiq_a_indice_g2 = {etiq: idx for idx, etiq in self.grafo2_etiquetas.items()}

        # Crear nuevo mapeo para la intersección
        etiquetas_interseccion = {}
        etiq_a_nuevo_indice = {}
        nuevo_indice = 0
        for etiq in sorted(etiquetas_comunes):
            etiquetas_interseccion[nuevo_indice] = etiq
            etiq_a_nuevo_indice[etiq] = nuevo_indice
            nuevo_indice += 1

        vertices_interseccion = len(etiquetas_comunes)

        # Buscar aristas comunes basadas en etiquetas
        aristas_interseccion = []
        for arista1 in self.grafo1_aristas:
            idx_orig_g1, idx_dest_g1 = arista1
            etiq_orig = self.grafo1_etiquetas.get(idx_orig_g1)
            etiq_dest = self.grafo1_etiquetas.get(idx_dest_g1)

            # Verificar si ambas etiquetas están en la intersección
            if etiq_orig in etiquetas_comunes and etiq_dest in etiquetas_comunes:
                # Buscar si existe la misma arista (por etiquetas) en grafo 2
                idx_orig_g2 = etiq_a_indice_g2.get(etiq_orig)
                idx_dest_g2 = etiq_a_indice_g2.get(etiq_dest)

                if idx_orig_g2 is not None and idx_dest_g2 is not None:
                    arista2 = tuple(sorted([idx_orig_g2, idx_dest_g2]))
                    if arista2 in self.grafo2_aristas:
                        # Agregar arista con nuevos índices
                        nuevo_orig = etiq_a_nuevo_indice[etiq_orig]
                        nuevo_dest = etiq_a_nuevo_indice[etiq_dest]
                        nueva_arista = tuple(sorted([nuevo_orig, nuevo_dest]))
                        if nueva_arista not in aristas_interseccion:
                            aristas_interseccion.append(nueva_arista)

        self.visual_interseccion.set_grafo(vertices_interseccion, aristas_interseccion,
                                           etiquetas_interseccion)

        DialogoClave(0, "Intersección calculada", "mensaje", self,
                     f"Intersección calculada exitosamente:\n\n"
                     f"Vértices comunes: {vertices_interseccion}\n"
                     f"    Etiquetas: {', '.join(sorted(etiquetas_comunes))}\n\n"
                     f"Aristas comunes: {len(aristas_interseccion)}\n\n"
                     f"Solo incluye vértices y aristas que existen\n"
                     f"en ambos grafos con las mismas etiquetas.").exec()

    # ==================== ACTUALIZAR ETIQUETAS ====================
    def actualizar_etiquetas(self, titulo_grafo, nuevas_etiquetas):
        """Actualiza las etiquetas cuando se modifican desde el visualizador"""
        if "Grafo 1" in titulo_grafo:
            self.grafo1_etiquetas = nuevas_etiquetas
        elif "Grafo 2" in titulo_grafo:
            self.grafo2_etiquetas = nuevas_etiquetas

        # ==================== GUARDAR INTERSECCIÓN ====================
    def guardar_interseccion(self):
        if self.visual_interseccion.num_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "Primero debes calcular la intersección.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Intersección", "", "JSON Files (*.json)")

        if archivo:
            try:
                datos = self.visual_interseccion.get_datos_grafo()
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)
                DialogoClave(0, "Éxito", "mensaje", self,
                            f"Intersección guardada exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                            f"Error al guardar el archivo:\n{str(e)}").exec()

    # ==================== LIMPIAR TODO ====================
    def limpiar_todo(self):
        """Limpia todos los grafos y la intersección"""
        self.grafo1_vertices = 0
        self.grafo1_aristas = []
        self.grafo1_etiquetas = {}
        self.vertices_g1.setValue(4)
        self.visual_g1.set_grafo(0, [], {})

        self.grafo2_vertices = 0
        self.grafo2_aristas = []
        self.grafo2_etiquetas = {}
        self.vertices_g2.setValue(4)
        self.visual_g2.set_grafo(0, [], {})

        self.visual_interseccion.set_grafo(0, [], {})

        DialogoClave(0, "Limpieza completada", "mensaje", self,
                     "Todos los grafos han sido limpiados:\n\n"
                     "• Grafo 1: limpio\n"
                     "• Grafo 2: limpio\n"
                     "• Intersección: limpia").exec()

    # ==================== LIMPIAR INTERSECCIÓN ====================
    def limpiar_interseccion(self):
        """Limpia solo la visualización de la intersección"""
        if self.visual_interseccion.num_vertices == 0:
            DialogoClave(0, "Información", "mensaje", self,
                         "La intersección ya está vacía.").exec()
            return

        self.visual_interseccion.set_grafo(0, [], {})
        DialogoClave(0, "Intersección limpiada", "mensaje", self,
                     "La visualización de la intersección\nha sido limpiada exitosamente.").exec()

    def eliminar_vertice_g1(self):
        """Elimina un vértice del Grafo 1"""
        if self.grafo1_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay vértices para eliminar en el Grafo 1.").exec()
            return

        from PySide6.QtWidgets import QInputDialog

        # Crear lista de opciones con etiquetas
        opciones = [f"{i + 1}: {self.grafo1_etiquetas.get(i, str(i + 1))}"
                    for i in range(self.grafo1_vertices)]

        opcion, ok = QInputDialog.getItem(
            self,
            "Eliminar Vértice",
            "Selecciona el vértice a eliminar:",
            opciones,
            0,
            False
        )

        if ok and opcion:
            # Extraer el índice del vértice seleccionado
            indice = int(opcion.split(":")[0]) - 1
            etiqueta_eliminada = self.grafo1_etiquetas.get(indice, str(indice + 1))

            # Eliminar todas las aristas conectadas a este vértice
            aristas_nuevas = []
            ponderaciones_nuevas = {}

            for arista in self.grafo1_aristas:
                origen, destino = arista
                # Si la arista no involucra al vértice eliminado
                if origen != indice and destino != indice:
                    # Ajustar índices si son mayores que el índice eliminado
                    nuevo_origen = origen if origen < indice else origen - 1
                    nuevo_destino = destino if destino < indice else destino - 1
                    nueva_arista = (nuevo_origen, nuevo_destino)
                    aristas_nuevas.append(nueva_arista)

                    # Transferir ponderación si existe
                    if arista in self.grafo1_ponderaciones:
                        ponderaciones_nuevas[nueva_arista] = self.grafo1_ponderaciones[arista]

            # Actualizar etiquetas
            etiquetas_nuevas = {}
            for i in range(self.grafo1_vertices):
                if i < indice:
                    etiquetas_nuevas[i] = self.grafo1_etiquetas.get(i, str(i + 1))
                elif i > indice:
                    etiquetas_nuevas[i - 1] = self.grafo1_etiquetas.get(i, str(i + 1))

            # Actualizar el grafo
            self.grafo1_vertices -= 1
            self.grafo1_aristas = aristas_nuevas
            self.grafo1_etiquetas = etiquetas_nuevas
            self.grafo1_ponderaciones = ponderaciones_nuevas

            self.vertices_g1.setValue(self.grafo1_vertices)
            self.visual_g1.set_grafo(self.grafo1_vertices, self.grafo1_aristas,
                                     self.grafo1_etiquetas, self.grafo1_ponderaciones)

            DialogoClave(0, "Vértice eliminado", "mensaje", self,
                         f"Vértice '{etiqueta_eliminada}' eliminado del Grafo 1.\n\n"
                         f"Vértices restantes: {self.grafo1_vertices}\n"
                         f"Aristas eliminadas: {len(self.grafo1_aristas) - len(aristas_nuevas)}").exec()

    def eliminar_vertice_g2(self):
        """Elimina un vértice del Grafo 2"""
        if self.grafo2_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay vértices para eliminar en el Grafo 2.").exec()
            return

        from PySide6.QtWidgets import QInputDialog

        # Crear lista de opciones con etiquetas
        opciones = [f"{i + 1}: {self.grafo2_etiquetas.get(i, str(i + 1))}"
                    for i in range(self.grafo2_vertices)]

        opcion, ok = QInputDialog.getItem(
            self,
            "Eliminar Vértice",
            "Selecciona el vértice a eliminar:",
            opciones,
            0,
            False
        )

        if ok and opcion:
            # Extraer el índice del vértice seleccionado
            indice = int(opcion.split(":")[0]) - 1
            etiqueta_eliminada = self.grafo2_etiquetas.get(indice, str(indice + 1))

            # Eliminar todas las aristas conectadas a este vértice
            aristas_nuevas = []
            ponderaciones_nuevas = {}

            for arista in self.grafo2_aristas:
                origen, destino = arista
                # Si la arista no involucra al vértice eliminado
                if origen != indice and destino != indice:
                    # Ajustar índices si son mayores que el índice eliminado
                    nuevo_origen = origen if origen < indice else origen - 1
                    nuevo_destino = destino if destino < indice else destino - 1
                    nueva_arista = (nuevo_origen, nuevo_destino)
                    aristas_nuevas.append(nueva_arista)

                    # Transferir ponderación si existe
                    if arista in self.grafo2_ponderaciones:
                        ponderaciones_nuevas[nueva_arista] = self.grafo2_ponderaciones[arista]

            # Actualizar etiquetas
            etiquetas_nuevas = {}
            for i in range(self.grafo2_vertices):
                if i < indice:
                    etiquetas_nuevas[i] = self.grafo2_etiquetas.get(i, str(i + 1))
                elif i > indice:
                    etiquetas_nuevas[i - 1] = self.grafo2_etiquetas.get(i, str(i + 1))

            # Actualizar el grafo
            self.grafo2_vertices -= 1
            self.grafo2_aristas = aristas_nuevas
            self.grafo2_etiquetas = etiquetas_nuevas
            self.grafo2_ponderaciones = ponderaciones_nuevas

            self.vertices_g2.setValue(self.grafo2_vertices)
            self.visual_g2.set_grafo(self.grafo2_vertices, self.grafo2_aristas,
                                     self.grafo2_etiquetas, self.grafo2_ponderaciones)

            aristas_eliminadas = len(self.grafo2_aristas) - len(aristas_nuevas)
            DialogoClave(0, "Vértice eliminado", "mensaje", self,
                         f"Vértice '{etiqueta_eliminada}' eliminado del Grafo 2.\n\n"
                         f"Vértices restantes: {self.grafo2_vertices}\n"
                         f"Aristas eliminadas: {aristas_eliminadas}").exec()