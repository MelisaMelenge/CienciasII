from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class GrafoComplementario(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos del grafo
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}

        self.setWindowTitle("Ciencias de la Computación II - Grafo Complementario")

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

        titulo = QLabel("Ciencias de la Computación II - Grafo Complementario")
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

        # --- TRANSFORMACIÓN ---
        transformacion_container = QWidget()
        transformacion_layout = QVBoxLayout(transformacion_container)
        transformacion_layout.setSpacing(8)

        label_transformacion = QLabel("Generar Complemento")
        label_transformacion.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        transformacion_layout.addWidget(label_transformacion, alignment=Qt.AlignCenter)

        self.btn_generar = QPushButton("🔄 Generar Complemento")
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

        self.vertices_spin.setStyleSheet("""
            QSpinBox {
                padding: 4px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
            }
        """)

        controles_layout.addWidget(grafo_container)
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
        grafos_layout.setSpacing(30)
        grafos_layout.setAlignment(Qt.AlignCenter)

        self.visual_original = VisualizadorGrafo("Grafo Original G", parent=self, es_editable=True)
        self.visual_complemento = VisualizadorGrafo("Grafo Complemento Ḡ", parent=self, es_editable=False)

        # Conectar señales
        self.visual_original.etiqueta_cambiada.connect(self.actualizar_etiqueta)
        self.visual_original.ponderacion_cambiada.connect(self.actualizar_ponderacion)

        for visual in (self.visual_original, self.visual_complemento):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_original)
        grafos_layout.addWidget(self.visual_complemento)

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

        btn_guardar_complemento = QPushButton("Guardar Complemento")
        btn_guardar_complemento.setStyleSheet("""
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
        btn_guardar_complemento.clicked.connect(self.guardar_grafo_complemento)

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

        botones_extras.addWidget(btn_guardar_complemento)
        botones_extras.addWidget(btn_limpiar_resultado)
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
        self.btn_generar.clicked.connect(self.generar_grafo_complemento)

    # ==================== CALLBACKS ====================
    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        self.grafo_etiquetas[indice] = nueva_etiqueta

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

    # ==================== GRAFO COMPLEMENTARIO ====================
    def generar_grafo_complemento(self):
        if self.grafo_vertices < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Se necesitan al menos 2 vértices.").exec()
            return

        # Generar todas las aristas posibles (grafo completo)
        todas_aristas = []
        for i in range(self.grafo_vertices):
            for j in range(i + 1, self.grafo_vertices):
                todas_aristas.append((i, j))

        # Crear conjunto de aristas existentes (sin considerar orden)
        aristas_existentes = set()
        for arista in self.grafo_aristas:
            origen, destino = arista
            # Normalizar arista (menor primero)
            arista_norm = (min(origen, destino), max(origen, destino))
            aristas_existentes.add(arista_norm)

        # Aristas del complemento = todas las aristas - aristas existentes
        aristas_complemento = []
        for arista in todas_aristas:
            if arista not in aristas_existentes:
                aristas_complemento.append(arista)

        # Visualizar grafo complemento con las mismas etiquetas
        etiquetas_complemento = self.grafo_etiquetas.copy()
        self.visual_complemento.set_grafo(self.grafo_vertices, aristas_complemento,
                                          etiquetas_complemento, {})

        # Calcular información
        total_aristas_posibles = (self.grafo_vertices * (self.grafo_vertices - 1)) // 2
        aristas_originales = len(self.grafo_aristas)
        aristas_complemento_count = len(aristas_complemento)

        DialogoClave(0, "Grafo Complementario Generado", "mensaje", self,
                     f"Grafo Original G: {self.grafo_vertices} vértices, {aristas_originales} aristas\n\n"
                     f"Grafo Complemento Ḡ: {self.grafo_vertices} vértices, {aristas_complemento_count} aristas\n\n"
                     f"Total de aristas posibles: {total_aristas_posibles}\n"
                     f"G + Ḡ = Grafo Completo K{self.grafo_vertices}").exec()

    # ==================== FUNCIONES ADICIONALES ====================
    def guardar_grafo_complemento(self):
        vertices_complemento = self.visual_complemento.num_vertices

        if vertices_complemento == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay grafo complemento para guardar.\nPrimero genera el complemento.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Grafo Complemento", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                datos = self.visual_complemento.get_datos_grafo()
                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)

                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Grafo complemento guardado exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()

    def limpiar_resultado(self):
        self.visual_complemento.set_grafo(0, [], {}, {})
        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Grafo complemento limpiado.").exec()

    def limpiar_todo(self):
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}

        self.visual_original.set_grafo(0, [], {}, {})
        self.visual_complemento.set_grafo(0, [], {}, {})

        self.vertices_spin.setValue(4)

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Todos los grafos han sido limpiados.").exec()