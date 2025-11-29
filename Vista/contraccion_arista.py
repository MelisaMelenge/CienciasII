from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea, QComboBox
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class ContraccionArista(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Datos del grafo
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}

        self.setWindowTitle("Ciencias de la Computación II - Contracción de Arista")

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

        titulo = QLabel("Ciencias de la Computación II - Contracción de Arista")
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

        # --- CONTRACCIÓN ---
        contraccion_container = QWidget()
        contraccion_layout = QVBoxLayout(contraccion_container)
        contraccion_layout.setSpacing(8)

        label_contraccion = QLabel("Contraer Arista")
        label_contraccion.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        contraccion_layout.addWidget(label_contraccion, alignment=Qt.AlignCenter)

        # Selección de arista
        sel_arista_layout = QHBoxLayout()
        lbl_arista = QLabel("Arista:")
        lbl_arista.setStyleSheet("font-size: 12px; color: #2d1f15;")
        sel_arista_layout.addWidget(lbl_arista)
        self.combo_arista = QComboBox()
        self.combo_arista.setFixedWidth(150)
        sel_arista_layout.addWidget(self.combo_arista)
        contraccion_layout.addLayout(sel_arista_layout)

        self.btn_contraer = QPushButton("⚡ Contraer")
        self.btn_contraer.setStyleSheet("""
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
        contraccion_layout.addWidget(self.btn_contraer)

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

        for widget in (self.vertices_spin, self.combo_arista):
            widget.setStyleSheet("""
                QSpinBox, QComboBox {
                    padding: 4px;
                    border: 2px solid #bf8f62;
                    border-radius: 5px;
                    background: white;
                }
            """)

        controles_layout.addWidget(grafo_container)
        controles_layout.addWidget(contraccion_container)

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
        self.visual_contraccion = VisualizadorGrafo("Grafo con Contracción", parent=self, es_editable=False)

        # Conectar señales
        self.visual_original.etiqueta_cambiada.connect(self.actualizar_etiqueta)
        self.visual_original.ponderacion_cambiada.connect(self.actualizar_ponderacion)

        for visual in (self.visual_original, self.visual_contraccion):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_original)
        grafos_layout.addWidget(self.visual_contraccion)

        self.contenedor_layout.addLayout(grafos_layout)

        # Agregar instrucciones de uso
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

        btn_guardar_contraccion = QPushButton("Guardar Contracción")
        btn_guardar_contraccion.setStyleSheet("""
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
        btn_guardar_contraccion.clicked.connect(self.guardar_contraccion)

        btn_limpiar_contraccion = QPushButton("Limpiar Contracción")
        btn_limpiar_contraccion.setStyleSheet("""
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
        btn_limpiar_contraccion.clicked.connect(self.limpiar_contraccion)

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

        botones_extras.addWidget(btn_guardar_contraccion)
        botones_extras.addWidget(btn_limpiar_contraccion)
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
        self.btn_contraer.clicked.connect(self.contraer_arista)

    # ==================== CALLBACKS ====================
    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        self.grafo_etiquetas[indice] = nueva_etiqueta
        self.actualizar_combo_aristas()

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
        self.actualizar_combo_aristas()
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
            self.actualizar_combo_aristas()

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
                self.actualizar_combo_aristas()

    def limpiar_grafo(self):
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}
        self.visual_original.set_grafo(0, [], {}, {})
        self.vertices_spin.setValue(4)
        self.actualizar_combo_aristas()

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
            self.actualizar_combo_aristas()

    # ==================== CONTRACCIÓN ====================
    def actualizar_combo_aristas(self):
        """Actualiza el ComboBox con las aristas disponibles"""
        self.combo_arista.clear()

        if not self.grafo_aristas:
            return

        for arista in self.grafo_aristas:
            origen, destino = arista
            etiq_origen = self.grafo_etiquetas.get(origen, str(origen + 1))
            etiq_destino = self.grafo_etiquetas.get(destino, str(destino + 1))

            # Mostrar ponderación si existe
            ponderacion = self.grafo_ponderaciones.get(arista, "")
            if ponderacion:
                texto = f"({etiq_origen} - {etiq_destino}) [{ponderacion}]"
            else:
                texto = f"({etiq_origen} - {etiq_destino})"

            self.combo_arista.addItem(texto, arista)

    def contraer_arista(self):
        if self.grafo_vertices < 2:
            DialogoClave(0, "Error", "mensaje", self,
                         "Se necesitan al menos 2 vértices para contraer una arista.").exec()
            return

        if not self.grafo_aristas:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay aristas para contraer.").exec()
            return

        # Obtener la arista seleccionada
        arista_seleccionada = self.combo_arista.currentData()
        if not arista_seleccionada:
            DialogoClave(0, "Error", "mensaje", self,
                         "Selecciona una arista válida.").exec()
            return

        origen, destino = arista_seleccionada

        # No permitir contraer bucles
        if origen == destino:
            DialogoClave(0, "Error", "mensaje", self,
                         "No se puede contraer un bucle (arista que conecta un vértice consigo mismo).").exec()
            return

        # Asegurar que origen < destino para consistencia
        if origen > destino:
            origen, destino = destino, origen

        etiq_origen = self.grafo_etiquetas.get(origen, str(origen + 1))
        etiq_destino = self.grafo_etiquetas.get(destino, str(destino + 1))

        # Crear nueva etiqueta fusionada
        nueva_etiqueta = f"{etiq_origen},{etiq_destino}"

        # Crear nuevo grafo con un vértice menos
        vertices_contraccion = self.grafo_vertices - 1
        etiquetas_contraccion = {}
        aristas_contraccion = []
        ponderaciones_contraccion = []

        # Mapeo de índices antiguos a nuevos
        mapeo = {}
        nuevo_indice = 0
        for i in range(self.grafo_vertices):
            if i == origen:
                # El vértice fusionado mantiene el primer índice
                mapeo[i] = nuevo_indice
                etiquetas_contraccion[nuevo_indice] = nueva_etiqueta
                nuevo_indice += 1
            elif i == destino:
                # El segundo vértice se mapea al mismo índice que el primero
                mapeo[i] = mapeo[origen]
            else:
                mapeo[i] = nuevo_indice
                etiquetas_contraccion[nuevo_indice] = self.grafo_etiquetas.get(i, str(i + 1))
                nuevo_indice += 1

        # Procesar aristas - ELIMINAR la arista contraída, mantener todas las demás
        for arista in self.grafo_aristas:
            o, d = arista

            # Saltar la arista que se está contrayendo
            if (o == origen and d == destino) or (o == destino and d == origen):
                continue

            nuevo_origen = mapeo[o]
            nuevo_destino = mapeo[d]

            nueva_arista = (nuevo_origen, nuevo_destino)
            aristas_contraccion.append(nueva_arista)

            # Transferir ponderación
            ponderacion = self.grafo_ponderaciones.get(arista, "")
            ponderaciones_contraccion.append(ponderacion)

        # DEBUG
        print("=== DEBUG CONTRACCIÓN ===")
        print(f"Arista contraída: ({etiq_origen} - {etiq_destino})")
        print(f"Aristas originales: {self.grafo_aristas}")
        print(f"Mapeo de vértices: {mapeo}")
        print(f"Aristas resultantes: {aristas_contraccion}")
        print(f"Ponderaciones: {ponderaciones_contraccion}")
        print(f"Total aristas: {len(aristas_contraccion)}")
        print("========================")

        # Visualizar el grafo contraído
        self.visual_contraccion.set_grafo(vertices_contraccion, aristas_contraccion,
                                          etiquetas_contraccion, ponderaciones_contraccion)

        DialogoClave(0, "Contracción completada", "mensaje", self,
                     f"Arista ({etiq_origen} - {etiq_destino}) contraída.\n\n"
                     f"Vértices fusionados en: '{nueva_etiqueta}'\n"
                     f"Vértices resultantes: {vertices_contraccion}\n"
                     f"Aristas: {len(aristas_contraccion)}").exec()

    # ==================== FUNCIONES ADICIONALES ====================
    def guardar_contraccion(self):
        """Guarda el grafo contraído en un archivo JSON"""
        vertices_contraccion = self.visual_contraccion.num_vertices

        if vertices_contraccion == 0:
            DialogoClave(0, "Error", "mensaje", self,
                         "No hay contracción para guardar.\nPrimero contrae una arista.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Contracción", "", "JSON Files (*.json)"
        )

        if archivo:
            try:
                aristas = self.visual_contraccion.aristas
                etiquetas = self.visual_contraccion.etiquetas

                # Convertir ponderaciones de lista a diccionario
                ponderaciones_dict = {}
                if hasattr(self.visual_contraccion, 'ponderaciones_lista'):
                    for i, arista in enumerate(aristas):
                        if i < len(self.visual_contraccion.ponderaciones_lista):
                            pond = self.visual_contraccion.ponderaciones_lista[i]
                            if pond:
                                ponderaciones_dict[str(arista)] = pond

                datos = {
                    'vertices': vertices_contraccion,
                    'aristas': aristas,
                    'etiquetas': etiquetas,
                    'ponderaciones': ponderaciones_dict
                }

                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=4, ensure_ascii=False)

                DialogoClave(0, "Éxito", "mensaje", self,
                             f"Contracción guardada exitosamente en:\n{archivo}").exec()
            except Exception as e:
                DialogoClave(0, "Error", "mensaje", self,
                             f"Error al guardar el archivo:\n{str(e)}").exec()

    def limpiar_contraccion(self):
        """Limpia solo la visualización de la contracción"""
        self.visual_contraccion.set_grafo(0, [], {}, {})
        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Visualización de Contracción limpiada.").exec()

    def limpiar_todo(self):
        """Limpia completamente todos los grafos"""
        self.grafo_vertices = 0
        self.grafo_aristas = []
        self.grafo_etiquetas = {}
        self.grafo_ponderaciones = {}

        self.visual_original.set_grafo(0, [], {}, {})
        self.visual_contraccion.set_grafo(0, [], {}, {})

        self.vertices_spin.setValue(4)
        self.actualizar_combo_aristas()

        DialogoClave(0, "Limpieza exitosa", "mensaje", self,
                     "Todos los grafos han sido limpiados.").exec()