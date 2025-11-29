from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea, QComboBox
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class FusionVertice(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos del grafo
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}

        self.setWindowTitle("Ciencias de la Computación II - Fusión de Vértices")

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

        titulo = QLabel("Ciencias de la Computación II - Fusión de Vértices")
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

        # --- GRAFO ORIGINAL ---
        grafo_container = QWidget()
        grafo_layout = QVBoxLayout(grafo_container)
        grafo_layout.setSpacing(8)

        label_grafo = QLabel("Grafo Original")
        label_grafo.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo_layout.addWidget(label_grafo, alignment=Qt.AlignCenter)

        config_g = QHBoxLayout()
        lbl_v = QLabel("Vértices:")
        lbl_v.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config_g.addWidget(lbl_v)
        self.vertices_spin = QSpinBox()
        self.vertices_spin.setRange(2, 20)
        self.vertices_spin.setValue(4)
        self.vertices_spin.setFixedWidth(60)
        config_g.addWidget(self.vertices_spin)
        self.btn_crear = QPushButton("Crear")
        config_g.addWidget(self.btn_crear)
        grafo_layout.addLayout(config_g)

        botones_g = QHBoxLayout()
        self.btn_agregar_arista = QPushButton("+ Arista")
        self.btn_eliminar_arista = QPushButton("- Arista")
        botones_g.addWidget(self.btn_agregar_arista)
        botones_g.addWidget(self.btn_eliminar_arista)
        grafo_layout.addLayout(botones_g)

        botones_archivo = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cargar = QPushButton("Cargar")
        botones_archivo.addWidget(self.btn_guardar)
        botones_archivo.addWidget(self.btn_cargar)
        grafo_layout.addLayout(botones_archivo)

        self.btn_limpiar = QPushButton("Limpiar")
        grafo_layout.addWidget(self.btn_limpiar)

        # --- FUSIÓN ---
        fusion_container = QWidget()
        fusion_layout = QVBoxLayout(fusion_container)
        fusion_layout.setSpacing(8)

        label_fusion = QLabel("Fusionar Vértices")
        label_fusion.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        fusion_layout.addWidget(label_fusion, alignment=Qt.AlignCenter)

        # Selección de vértices
        sel1_layout = QHBoxLayout()
        lbl_v1 = QLabel("Vértice 1:")
        lbl_v1.setStyleSheet("font-size: 12px; color: #2d1f15;")
        sel1_layout.addWidget(lbl_v1)
        self.combo_v1 = QComboBox()
        self.combo_v1.setFixedWidth(100)
        sel1_layout.addWidget(self.combo_v1)
        fusion_layout.addLayout(sel1_layout)

        sel2_layout = QHBoxLayout()
        lbl_v2 = QLabel("Vértice 2:")
        lbl_v2.setStyleSheet("font-size: 12px; color: #2d1f15;")
        sel2_layout.addWidget(lbl_v2)
        self.combo_v2 = QComboBox()
        self.combo_v2.setFixedWidth(100)
        sel2_layout.addWidget(self.combo_v2)
        fusion_layout.addLayout(sel2_layout)

        self.btn_fusionar = QPushButton("🔗 Fusionar")
        self.btn_fusionar.setStyleSheet("""
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
        fusion_layout.addWidget(self.btn_fusionar)

        # Estilos de botones
        for btn in (self.btn_crear, self.btn_agregar_arista, self.btn_eliminar_arista,
                    self.btn_guardar, self.btn_cargar, self.btn_limpiar):
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

        for widget in (self.vertices_spin, self.combo_v1, self.combo_v2):
            widget.setStyleSheet("""
                QSpinBox, QComboBox {
                    padding: 4px;
                    border: 2px solid #bf8f62;
                    border-radius: 5px;
                    background: white;
                }
            """)

        controles_layout.addWidget(grafo_container)
        controles_layout.addWidget(fusion_container)

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

        self.visual_original = VisualizadorGrafo("Grafo Original", parent=self, es_editable=True)
        self.visual_fusion = VisualizadorGrafo("Grafo con Fusión", parent=self, es_editable=False)

        # Conectar señales
        self.visual_original.etiqueta_cambiada.connect(self.actualizar_etiqueta)
        self.visual_original.ponderacion_cambiada.connect(self.actualizar_ponderacion)

        for visual in (self.visual_original, self.visual_fusion):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_original)
        grafos_layout.addWidget(self.visual_fusion)

        self.contenedor_layout.addLayout(grafos_layout)

        # ======= BOTONES ADICIONALES =======
        botones_extras = QHBoxLayout()
        botones_extras.setSpacing(15)
        botones_extras.setAlignment(Qt.AlignCenter)

        btn_guardar_fusion = QPushButton("Guardar Fusión")
        btn_guardar_fusion.setStyleSheet("""
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
        btn_guardar_fusion.clicked.connect(self.guardar_fusion)

        btn_limpiar_fusion = QPushButton("Limpiar Fusión")
        btn_limpiar_fusion.setStyleSheet("""
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
        btn_limpiar_fusion.clicked.connect(self.limpiar_fusion)

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

        botones_extras.addWidget(btn_guardar_fusion)
        botones_extras.addWidget(btn_limpiar_fusion)
        botones_extras.addWidget(btn_limpiar_todo)

        self.contenedor_layout.addLayout(botones_extras)

        self.setCentralWidget(central)

        # ======= CONEXIONES =======
        self.btn_crear.clicked.connect(self.crear_grafo)
        self.btn_agregar_arista.clicked.connect(self.agregar_arista)
        self.btn_eliminar_arista.clicked.connect(self.eliminar_arista)
        self.btn_guardar.clicked.connect(self.guardar_grafo)
        self.btn_cargar.clicked.connect(self.cargar_grafo)
        self.btn_limpiar.clicked.connect(self.limpiar_grafo)
        self.btn_fusionar.clicked.connect(self.fusionar_vertices)

    # ==================== CALLBACKS ====================
    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        self.grafo_etiquetas[indice] = nueva_etiqueta
        self.actualizar_combos()

    def actualizar_ponderacion(self, arista, ponderacion):
        self.grafo_ponderaciones[arista] = ponderacion

    # ==================== GRAFO ORIGINAL ====================
    def crear_grafo(self):
        self.grafo_vertices = self.vertices_spin.value()
        self.grafo_aristas = []
        self.grafo_etiquetas = {i: str(i + 1) for i in range(self.grafo_vertices)}
        self.grafo_ponderaciones = {}
        self.visual_original.set_grafo(self.grafo_vertices, self.grafo_aristas,
                                       self.grafo_etiquetas, self.grafo_ponderaciones)
        self.actualizar_combos()
        DialogoClave(0, "Grafo creado", "mensaje", self,
                     f"Grafo creado con {self.grafo_vertices} vértices.").exec()

    def agregar_arista(self):
        if self.grafo_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "Primero debes crear el grafo.").exec()
            return

        dlg = DialogoArista(self.grafo_vertices, self, self.grafo_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            self.grafo_aristas.append(arista)
            self.visual_original.set_grafo(self.grafo_vertices, self.grafo_aristas,
                                           self.grafo_etiquetas, self.grafo_ponderaciones)

    def eliminar_arista(self):
        if not self.grafo_aristas:
            DialogoClave(0, "Error", "mensaje", self, "No hay aristas para eliminar.").exec()
            return

        dlg = DialogoArista(self.grafo_vertices, self, self.grafo_etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.grafo_aristas:
                self.grafo_aristas.remove(arista)
                if arista in self.grafo_ponderaciones:
                    del self.grafo_ponderaciones[arista]
                self.visual_original.set_grafo(self.grafo_vertices, self.grafo_aristas,
                                               self.grafo_etiquetas, self.grafo_ponderaciones)

    def limpiar_grafo(self):
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}
        self.visual_original.set_grafo(0, [], {}, {})
        self.vertices_spin.setValue(4)
        self.actualizar_combos()

    def guardar_grafo(self):
        if self.grafo_vertices == 0:
            DialogoClave(0, "Error", "mensaje", self, "No hay grafo para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar Grafo", "", "JSON Files (*.json)")
        if archivo:
            datos = self.visual_original.get_datos_grafo()
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

    def cargar_grafo(self):
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar Grafo", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)
            self.grafo_vertices = datos['vertices']
            self.grafo_aristas = [tuple(a) for a in datos['aristas']]
            self.grafo_etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
            self.grafo_ponderaciones = {}
            for k, v in datos.get('ponderaciones', {}).items():
                arista_tuple = tuple(map(int, k.strip('()').split(', ')))
                self.grafo_ponderaciones[arista_tuple] = v
            self.vertices_spin.setValue(self.grafo_vertices)
            self.visual_original.set_grafo(self.grafo_vertices, self.grafo_aristas,
                                           self.grafo_etiquetas, self.grafo_ponderaciones)
            self.actualizar_combos()

    # ==================== FUSIÓN ====================
    def actualizar_combos(self):
        """Actualiza los ComboBox con los vértices disponibles"""
        self.combo_v1.clear()
        self.combo_v2.clear()

        if self.grafo_vertices == 0:
            return

        for i in range(self.grafo_vertices):
            etiqueta = self.grafo_etiquetas.get(i, str(i + 1))
            self.combo_v1.addItem(f"{i + 1}: {etiqueta}", i)
            self.combo_v2.addItem(f"{i + 1}: {etiqueta}", i)

    def fusionar_vertices(self):
        if self.grafo_vertices < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Se necesitan al menos 2 vértices para fusionar.").exec()
            return

        indice_v1 = self.combo_v1.currentData()
        indice_v2 = self.combo_v2.currentData()

        if indice_v1 == indice_v2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Debes seleccionar dos vértices diferentes.").exec()
            return

        # Asegurar que v1 < v2 para consistencia
        if indice_v1 > indice_v2:
            indice_v1, indice_v2 = indice_v2, indice_v1

        etiq_v1 = self.grafo_etiquetas.get(indice_v1, str(indice_v1 + 1))
        etiq_v2 = self.grafo_etiquetas.get(indice_v2, str(indice_v2 + 1))

        # Crear nueva etiqueta fusionada
        nueva_etiqueta = f"{etiq_v1},{etiq_v2}"

        # Crear nuevo grafo con un vértice menos
        vertices_fusion = self.grafo_vertices - 1
        etiquetas_fusion = {}
        aristas_fusion = []
        ponderaciones_fusion = []  # 👈 CAMBIAR A LISTA

        # Mapeo de índices antiguos a nuevos
        mapeo = {}
        nuevo_indice = 0
        for i in range(self.grafo_vertices):
            if i == indice_v1:
                # El vértice fusionado mantiene el primer índice
                mapeo[i] = nuevo_indice
                etiquetas_fusion[nuevo_indice] = nueva_etiqueta
                nuevo_indice += 1
            elif i == indice_v2:
                # El segundo vértice se mapea al mismo índice que el primero
                mapeo[i] = mapeo[indice_v1]
            else:
                mapeo[i] = nuevo_indice
                etiquetas_fusion[nuevo_indice] = self.grafo_etiquetas.get(i, str(i + 1))
                nuevo_indice += 1

        # Procesar aristas - MANTENER TODAS, INCLUSO PARALELAS
        for arista in self.grafo_aristas:
            origen, destino = arista
            nuevo_origen = mapeo[origen]
            nuevo_destino = mapeo[destino]

            # IMPORTANTE: NO normalizar, mantener orden original
            nueva_arista = (nuevo_origen, nuevo_destino)
            aristas_fusion.append(nueva_arista)

            # Transferir ponderación
            ponderacion = self.grafo_ponderaciones.get(arista, "")
            ponderaciones_fusion.append(ponderacion)

        # Visualizar el grafo fusionado usando LISTA de ponderaciones
        self.visual_fusion.set_grafo(vertices_fusion, aristas_fusion,
                                     etiquetas_fusion, ponderaciones_fusion)

        DialogoClave(0, "Fusión completada", "mensaje", self,
                     f"Vértices '{etiq_v1}' y '{etiq_v2}' fusionados.\n\n"
                     f"Nueva etiqueta: '{nueva_etiqueta}'\n"
                     f"Vértices resultantes: {vertices_fusion}\n"
                     f"Aristas: {len(aristas_fusion)}").exec()

    # ==================== FUNCIONES ADICIONALES ====================
    def guardar_fusion(self):
        """Guarda el grafo fusionado en un archivo JSON"""
        # Obtener datos del visualizador
        vertices_fusion = self.visual_fusion.num_vertices

        if vertices_fusion == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay fusión para guardar.\nPrimero fusiona vértices.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Fusión", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                # Construir datos manualmente para evitar problemas con ponderaciones
                aristas = self.visual_fusion.aristas
                etiquetas = self.visual_fusion.etiquetas

                # Convertir ponderaciones de lista a diccionario
                ponderaciones_dict = {}
                if hasattr(self.visual_fusion, 'ponderaciones_lista'):
                    for i, arista in enumerate(aristas):
                        if i < len(self.visual_fusion.ponderaciones_lista):
                            pond = self.visual_fusion.ponderaciones_lista[i]
                            if pond:  # Solo guardar si tiene ponderación
                                ponderaciones_dict[str(arista)] = pond

                datos = {
                    'vertices': vertices_fusion,
                    'aristas': aristas,
                    'etiquetas': etiquetas,
                    'ponderaciones': ponderaciones_dict
                }

                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)

                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Fusión guardada exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()
    def limpiar_fusion(self):
        """Limpia solo la visualización de la fusión"""
        self.visual_fusion.set_grafo(0, [], {}, {})
        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Visualización de Fusión limpiada.").exec()

    def limpiar_todo(self):
        """Limpia completamente todos los grafos"""
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}

        self.visual_original.set_grafo(0, [], {}, {})
        self.visual_fusion.set_grafo(0, [], {}, {})

        self.vertices_spin.setValue(4)
        self.actualizar_combos()

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Todos los grafos han sido limpiados.").exec()
