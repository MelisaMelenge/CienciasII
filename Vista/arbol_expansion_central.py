from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QScrollArea, QMessageBox,
    QSpinBox, QFileDialog, QInputDialog, QSplitter, QTabWidget
)
from PySide6.QtCore import Qt, QTimer
from Vista.visualizador_grafo import VisualizadorGrafo
from Controlador.arboles.CentralController import CentralController
import math
import json


class ArbolExpansionCentral(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = CentralController()

        self.setWindowTitle("Árbol de Expansión Central")
        self.setGeometry(100, 50, 1700, 950)

        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)
        layout.setContentsMargins(10, 10, 10, 10)

        # HEADER
        header = self.crear_header()
        layout.addWidget(header)

        # SPLITTER PRINCIPAL (Izquierda-Derecha)
        splitter_principal = QSplitter(Qt.Horizontal)
        splitter_principal.setStyleSheet("""
            QSplitter::handle {
                background-color: #bf8f62;
                width: 3px;
            }
        """)

        # PANEL IZQUIERDO - Controles
        panel_izq = self.crear_panel_controles()
        splitter_principal.addWidget(panel_izq)

        # PANEL DERECHO - Visualización con Tabs
        panel_der = self.crear_panel_visualizacion()
        splitter_principal.addWidget(panel_der)

        # Proporciones: 20% izquierda, 80% derecha
        splitter_principal.setSizes([300, 1200])
        layout.addWidget(splitter_principal)

        # Variables de estado
        self.num_vertices = 7
        self.aristas = []
        self.etiquetas = {}
        self.vertice_seleccionado = None
        self.paso_actual = 0
        self.pasos_algoritmo = []
        self.centro_calculado = None
        self.visualizador_grafo = None

        # Timer para animación
        self.timer = QTimer()
        self.timer.timeout.connect(self.mostrar_siguiente_paso)

        # Mostrar pantalla inicial
        self.mostrar_pantalla_inicial()

    def crear_header(self):
        """Crea el encabezado"""
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62);
            border-radius: 10px;
        """)
        header.setMaximumHeight(100)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(15, 8, 15, 8)

        titulo = QLabel("Centro de Árbol - Algoritmo de Eliminación de Hojas")
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold; color: #2d1f15;")
        header_layout.addWidget(titulo)

        # Menú
        menu_layout = QHBoxLayout()
        menu_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        btn_inicio = QPushButton("Inicio")
        btn_grafos = QPushButton("Menú Grafos")

        for btn in (btn_inicio, btn_grafos):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2d1f15;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                    padding: 5px 20px;
                }
                QPushButton:hover { 
                    color: #FFEAC5; 
                    background-color: #6C4E31;
                    border-radius: 6px;
                }
            """)
            menu_layout.addWidget(btn)

        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_grafos.clicked.connect(lambda: self.cambiar_ventana("grafos"))
        header_layout.addLayout(menu_layout)

        return header

    def crear_panel_controles(self):
        """Crea el panel de controles izquierdo"""
        panel = QFrame()
        panel.setStyleSheet("""
            QFrame {
                background-color: #F5E6D3;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            }
        """)
        panel.setMinimumWidth(280)
        panel.setMaximumWidth(350)

        layout = QVBoxLayout(panel)
        layout.setSpacing(10)
        layout.setContentsMargins(12, 12, 12, 12)

        # Título
        titulo = QLabel("Vértice")
        titulo.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            color: #6C4E31;
            padding: 10px;
            background-color: #FFFEF7;
            border: 2px solid #bf8f62;
            border-radius: 6px;
        """)
        titulo.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(titulo)

        # Control de vértices
        vertices_layout = QHBoxLayout()
        lbl_vertices = QLabel("Vértices:")
        lbl_vertices.setStyleSheet("font-weight: bold; color: #2d1f15;")
        self.spin_vertices = QSpinBox()
        self.spin_vertices.setMinimum(3)
        self.spin_vertices.setMaximum(15)
        self.spin_vertices.setValue(7)
        self.spin_vertices.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
                font-weight: bold;
            }
        """)
        vertices_layout.addWidget(lbl_vertices)
        vertices_layout.addWidget(self.spin_vertices)
        layout.addLayout(vertices_layout)

        # Botones
        btn_generar = QPushButton("Generar Árbol Vacío")
        btn_generar.clicked.connect(self.generar_arbol_vacio)
        layout.addWidget(btn_generar)

        self.btn_eliminar_arista = QPushButton("Eliminar Arista")
        self.btn_eliminar_arista.clicked.connect(self.eliminar_arista)
        self.btn_eliminar_arista.setEnabled(False)
        layout.addWidget(self.btn_eliminar_arista)

        self.btn_eliminar_vertice = QPushButton("Eliminar Vértice")
        self.btn_eliminar_vertice.clicked.connect(self.eliminar_vertice)
        self.btn_eliminar_vertice.setEnabled(False)
        layout.addWidget(self.btn_eliminar_vertice)

        layout.addWidget(QLabel())

        self.btn_calcular = QPushButton("Encontrar Centro")
        self.btn_calcular.setStyleSheet(self.get_button_style("#6C4E31;", "#388E3C"))
        self.btn_calcular.clicked.connect(self.iniciar_animacion_centro)
        self.btn_calcular.setEnabled(False)
        layout.addWidget(self.btn_calcular)

        layout.addWidget(QLabel())  # Separador

        self.btn_guardar_grafo = QPushButton("Guardar Árbol")
        self.btn_guardar_grafo.clicked.connect(self.guardar_arbol)
        self.btn_guardar_grafo.setEnabled(False)
        layout.addWidget(self.btn_guardar_grafo)

        self.btn_cargar_grafo = QPushButton("Cargar Árbol")
        self.btn_cargar_grafo.clicked.connect(self.cargar_arbol)
        layout.addWidget(self.btn_cargar_grafo)

        self.btn_guardar_centro = QPushButton("Guardar Centro")
        self.btn_guardar_centro.clicked.connect(self.guardar_centro)
        self.btn_guardar_centro.setEnabled(False)
        layout.addWidget(self.btn_guardar_centro)

        layout.addWidget(QLabel())  # Separador

        btn_limpiar = QPushButton("Limpiar Todo")
        btn_limpiar.setStyleSheet(self.get_button_style("#6C4E31", "#D32F2F"))
        btn_limpiar.clicked.connect(self.limpiar)
        layout.addWidget(btn_limpiar)

        # Info teórica
        info_text = QTextEdit()
        info_text.setReadOnly(True)
        info_text.setStyleSheet("""
            background-color: #FFFEF7;
            border: 1px solid #bf8f62;
            border-radius: 5px;
            font-size: 11px;
            padding: 8px;
        """)
        info_text.setHtml("""
            <b> Conceptos:</b><br>
            <b>Centro:</b> Vértice(s) con menor excentricidad.<br>
            <b>Excentricidad:</b> Máxima distancia desde un vértice.<br>
            <b>Radio:</b> Mínima excentricidad.<br>
            <b>Diámetro:</b> Máxima excentricidad.<br><br>
            <b>Algoritmo:</b> Eliminar hojas (grado 1) hasta quedar 1-2 vértices.
        """)
        layout.addWidget(info_text)

        layout.addStretch()

        # Aplicar estilo a todos los botones
        for btn in panel.findChildren(QPushButton):
            if not btn.styleSheet():  # Si no tiene estilo personalizado
                btn.setStyleSheet(self.get_button_style())

        return panel

    def crear_panel_visualizacion(self):
        """Crea el panel de visualización con tabs"""
        panel = QFrame()
        panel.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Tabs para organizar contenido
        self.tabs = QTabWidget()
        self.tabs.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bf8f62;
                border-radius: 8px;
                background-color: #E8D4B8;
                padding: 10px;
            }
            QTabBar::tab {
                background-color: #D3C1A8;
                color: #2d1f15;
                padding: 10px 20px;
                margin-right: 3px;
                border: 2px solid #bf8f62;
                border-bottom: none;
                border-top-left-radius: 6px;
                border-top-right-radius: 6px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #E8D4B8;
                color: #6C4E31;
            }
            QTabBar::tab:hover {
                background-color: #DFC9B0;
            }
        """)

        # TAB 1: Árbol Principal
        self.tab_arbol = QWidget()
        self.tab_arbol.setStyleSheet("background-color: #E8D4B8;")
        tab_arbol_layout = QVBoxLayout(self.tab_arbol)

        scroll_arbol = QScrollArea()
        scroll_arbol.setWidgetResizable(True)
        scroll_arbol.setStyleSheet(self.get_scroll_style())

        scroll_arbol_widget = QWidget()
        scroll_arbol_widget.setStyleSheet("background-color: transparent;")
        self.layout_arbol = QVBoxLayout(scroll_arbol_widget)
        self.layout_arbol.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        scroll_arbol.setWidget(scroll_arbol_widget)
        tab_arbol_layout.addWidget(scroll_arbol)

        self.tabs.addTab(self.tab_arbol, "Árbol Principal")

        # TAB 2: Paso a Paso
        self.tab_pasos = QWidget()
        self.tab_pasos.setStyleSheet("background-color: #E8D4B8;")
        tab_pasos_layout = QVBoxLayout(self.tab_pasos)

        scroll_pasos = QScrollArea()
        scroll_pasos.setWidgetResizable(True)
        scroll_pasos.setStyleSheet(self.get_scroll_style())

        scroll_pasos_widget = QWidget()
        scroll_pasos_widget.setStyleSheet("background-color: transparent;")
        self.layout_pasos = QVBoxLayout(scroll_pasos_widget)
        self.layout_pasos.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.layout_pasos.setSpacing(15)

        scroll_pasos.setWidget(scroll_pasos_widget)
        tab_pasos_layout.addWidget(scroll_pasos)

        self.tabs.addTab(self.tab_pasos, "Paso a Paso")

        # TAB 3: Matriz y Resultados
        self.tab_resultados = QWidget()
        self.tab_resultados.setStyleSheet("background-color: #E8D4B8;")
        tab_resultados_layout = QVBoxLayout(self.tab_resultados)

        scroll_resultados = QScrollArea()
        scroll_resultados.setWidgetResizable(True)
        scroll_resultados.setStyleSheet(self.get_scroll_style())

        scroll_resultados_widget = QWidget()
        scroll_resultados_widget.setStyleSheet("background-color: transparent;")
        self.layout_resultados = QVBoxLayout(scroll_resultados_widget)
        self.layout_resultados.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        scroll_resultados.setWidget(scroll_resultados_widget)
        tab_resultados_layout.addWidget(scroll_resultados)

        self.tabs.addTab(self.tab_resultados, "Matriz & Resultados")

        layout.addWidget(self.tabs)
        return panel

    def get_button_style(self, bg="#6C4E31", hover="#8B6342"):
        return f"""
            QPushButton {{
                background-color: {bg};
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 12px;
                border-radius: 6px;
                font-size: 12px;
                border: 2px solid {bg};
            }}
            QPushButton:hover {{
                background-color: {hover};
            }}
            QPushButton:disabled {{
                background-color: #CCCCCC;
                color: #888888;
                border: 2px solid #AAAAAA;
            }}
        """

    def get_scroll_style(self):
        return """
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                background: #D3C1A8;
                width: 12px;
                border-radius: 6px;
            }
            QScrollBar::handle:vertical {
                background: #bf8f62;
                border-radius: 6px;
                min-height: 25px;
            }
            QScrollBar::handle:vertical:hover {
                background: #9c724a;
            }
        """

    def mostrar_pantalla_inicial(self):
        """Muestra pantalla inicial en tab de árbol"""
        self.limpiar_layout(self.layout_arbol)

        label_inicial = QLabel()
        label_inicial.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label_inicial.setStyleSheet("""
            background-color: #FAF3E8;
            border: 3px dashed #bf8f62;
            border-radius: 15px;
            padding: 40px;
            color: #6C4E31;
            font-size: 15px;
            font-weight: bold;
        """)
        label_inicial.setText(
            "Bienvenido al Algoritmo de Centro de Árbol\n\n"
            "1. Configura el número de vértices\n"
            "2. Presiona 'Generar Árbol Vacío'\n"
            "3. Haz clic en dos vértices para crear aristas\n"
            "4. Forma un árbol válido (n-1 aristas)\n"
            "5. Presiona 'Encontrar Centro' para ver la animación\n\n"
            "Usa las pestañas superiores para navegar"
        )
        label_inicial.setMinimumSize(700, 450)

        self.layout_arbol.addWidget(label_inicial)

    def generar_arbol_vacio(self):
        """Genera árbol vacío para dibujar"""
        self.num_vertices = self.spin_vertices.value()
        self.aristas = []
        self.etiquetas = {i: chr(97 + i) for i in range(self.num_vertices)}
        self.vertice_seleccionado = None
        self.centro_calculado = None

        self.limpiar_layout(self.layout_arbol)
        self.limpiar_layout(self.layout_pasos)
        self.limpiar_layout(self.layout_resultados)

        self.visualizador_grafo = VisualizadorGrafo(
            titulo="Árbol Editable - Haz clic en vértices para conectar",
            parent=self,
            es_editable=False,
            ancho = 900,
            alto = 650
        )

        self.visualizador_grafo.mousePressEvent = self.on_vertice_click
        self.visualizador_grafo.set_grafo(self.num_vertices, self.aristas, self.etiquetas)
        self.visualizador_grafo.setStyleSheet("""
            background-color: #FFFEF7;
            border: 2px solid #bf8f62;
            border-radius: 8px;
        """)
        self.visualizador_grafo.setMinimumSize(900, 650)
        self.visualizador_grafo.setMaximumSize(900, 650)

        self.layout_arbol.addWidget(self.visualizador_grafo, alignment=Qt.AlignmentFlag.AlignCenter)

        self.actualizar_estado()
        self.tabs.setCurrentIndex(0)

    def on_vertice_click(self, event):
        """Maneja clic en vértices"""
        if event.button() != Qt.LeftButton:
            return

        click_pos = event.pos()

        for i, pos in enumerate(self.visualizador_grafo.vertices):
            distancia = math.sqrt((click_pos.x() - pos.x()) ** 2 + (click_pos.y() - pos.y()) ** 2)

            if distancia <= 25:
                if self.vertice_seleccionado is None:
                    self.vertice_seleccionado = i
                    self.visualizador_grafo.vertice_resaltado = i
                    self.visualizador_grafo.update()
                else:
                    if self.vertice_seleccionado != i:
                        arista = (min(self.vertice_seleccionado, i), max(self.vertice_seleccionado, i))

                        if arista not in self.aristas:
                            self.aristas.append(arista)
                            self.visualizador_grafo.set_grafo(
                                self.num_vertices, self.aristas, self.etiquetas
                            )
                            self.actualizar_estado()

                    self.vertice_seleccionado = None
                    self.visualizador_grafo.vertice_resaltado = None
                    self.visualizador_grafo.update()
                return

    def actualizar_estado(self):
        """Actualiza estado de botones"""
        aristas_necesarias = self.num_vertices - 1

        if len(self.aristas) == aristas_necesarias:
            self.btn_calcular.setEnabled(True)
            self.btn_guardar_grafo.setEnabled(True)
            self.btn_eliminar_arista.setEnabled(True)
            self.btn_eliminar_vertice.setEnabled(True)
        elif len(self.aristas) > 0:
            self.btn_calcular.setEnabled(False)
            self.btn_guardar_grafo.setEnabled(True)
            self.btn_eliminar_arista.setEnabled(True)
            self.btn_eliminar_vertice.setEnabled(True)
        else:
            self.btn_calcular.setEnabled(False)
            self.btn_guardar_grafo.setEnabled(False)
            self.btn_eliminar_arista.setEnabled(False)
            self.btn_eliminar_vertice.setEnabled(False)

    def eliminar_arista(self):
        """Elimina una arista"""
        if not self.aristas:
            QMessageBox.information(self, "Info", "No hay aristas para eliminar")
            return

        aristas_texto = [f"{self.etiquetas[o]} - {self.etiquetas[d]}" for o, d in self.aristas]
        arista_texto, ok = QInputDialog.getItem(
            self, "Eliminar Arista", "Selecciona la arista:",
            aristas_texto, 0, False
        )

        if ok and arista_texto:
            idx = aristas_texto.index(arista_texto)
            self.aristas.pop(idx)
            self.visualizador_grafo.set_grafo(self.num_vertices, self.aristas, self.etiquetas)
            self.actualizar_estado()

    def eliminar_vertice(self):
        """Elimina un vértice"""
        if self.num_vertices <= 3:
            QMessageBox.warning(self, "Error", "Mínimo 3 vértices")
            return

        vertices_con_aristas = set()
        for o, d in self.aristas:
            vertices_con_aristas.add(o)
            vertices_con_aristas.add(d)

        if not vertices_con_aristas:
            QMessageBox.warning(self, "Error", "No hay vértices conectados")
            return

        opciones = [self.etiquetas[v] for v in sorted(vertices_con_aristas)]
        vertice_etiq, ok = QInputDialog.getItem(
            self, "Eliminar Vértice", "Selecciona:", opciones, 0, False
        )

        if ok:
            v_idx = None
            for idx, etiq in self.etiquetas.items():
                if etiq == vertice_etiq:
                    v_idx = idx
                    break

            if v_idx is not None:
                self.aristas = [(o, d) for o, d in self.aristas if o != v_idx and d != v_idx]

                mapeo = {}
                nuevo_idx = 0
                for i in range(self.num_vertices):
                    if i != v_idx:
                        mapeo[i] = nuevo_idx
                        nuevo_idx += 1

                nuevas_etiquetas = {mapeo[i]: self.etiquetas[i] for i in mapeo}
                nuevas_aristas = [(mapeo[o], mapeo[d]) for o, d in self.aristas]

                self.num_vertices -= 1
                self.etiquetas = nuevas_etiquetas
                self.aristas = nuevas_aristas

                self.visualizador_grafo.set_grafo(self.num_vertices, self.aristas, self.etiquetas)
                self.actualizar_estado()

    def guardar_arbol(self):
        """Guarda árbol en JSON"""
        if not self.aristas:
            QMessageBox.warning(self, "Error", "No hay árbol para guardar")
            return

        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar", "", "JSON (*.json)")

        if archivo:
            datos = {
                'num_vertices': self.num_vertices,
                'aristas': self.aristas,
                'etiquetas': self.etiquetas
            }
            try:
                with open(archivo, 'w') as f:
                    json.dump(datos, f, indent=4)
                QMessageBox.information(self, "Éxito", "Guardado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def cargar_arbol(self):
        """Carga árbol desde JSON"""
        archivo, _ = QFileDialog.getOpenFileName(self, "Cargar", "", "JSON (*.json)")

        if archivo:
            try:
                with open(archivo, 'r') as f:
                    datos = json.load(f)

                self.num_vertices = datos['num_vertices']
                self.aristas = [tuple(a) for a in datos['aristas']]
                self.etiquetas = {int(k): v for k, v in datos['etiquetas'].items()}

                self.spin_vertices.setValue(self.num_vertices)
                self.limpiar_layout(self.layout_arbol)

                self.visualizador_grafo = VisualizadorGrafo(
                    titulo="Árbol Cargado",
                    parent=self,
                    es_editable=False,
                    ancho=900,
                    alto=650
                )
                self.visualizador_grafo.mousePressEvent = self.on_vertice_click
                self.visualizador_grafo.set_grafo(self.num_vertices, self.aristas, self.etiquetas)
                self.visualizador_grafo.setStyleSheet("""
                    background-color: #FFFEF7;
                    border: 2px solid #bf8f62;
                    border-radius: 8px;
                """)
                self.layout_arbol.addWidget(self.visualizador_grafo)

                self.actualizar_estado()
                QMessageBox.information(self, "Éxito", "Cargado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def guardar_centro(self):
        """Guarda el resultado del centro"""
        if not self.centro_calculado:
            QMessageBox.warning(self, "Error", "Primero calcula el centro")
            return

        archivo, _ = QFileDialog.getSaveFileName(self, "Guardar", "", "Text (*.txt)")

        if archivo:
            try:
                centro = self.centro_calculado['centro']
                exc = self.centro_calculado['excentricidades']
                radio = self.centro_calculado['radio']
                diametro = self.centro_calculado['diametro']

                with open(archivo, 'w', encoding='utf-8') as f:
                    f.write("=" * 50 + "\n")
                    f.write("RESULTADO DEL CENTRO DE ÁRBOL\n")
                    f.write("=" * 50 + "\n\n")
                    f.write(f"Vértices: {self.num_vertices}\n")
                    f.write(f"Aristas: {len(self.aristas)}\n\n")
                    f.write("EXCENTRICIDADES:\n")
                    for v in sorted(exc.keys()):
                        etiq = self.etiquetas[v]
                        marca = "CENTRO" if v in centro else ""
                        f.write(f"  {etiq}: e({etiq}) = {exc[v]}{marca}\n")
                    f.write(f"\nRadio: {radio}\n")
                    f.write(f"Diámetro: {diametro}\n")
                    centro_etiq = [self.etiquetas[v] for v in centro]
                    f.write(f"\nCentro: {', '.join(centro_etiq)}\n")

                QMessageBox.information(self, "Éxito", "Guardado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", str(e))

    def iniciar_animacion_centro(self):
        """Inicia animación del algoritmo"""
        if not self.aristas:
            QMessageBox.warning(self, "Error", "Primero crea el árbol")
            return

        self.controller.set_grafo(self.num_vertices, self.aristas, self.etiquetas)

        if not self.controller.es_arbol():
            QMessageBox.warning(self, "Error", "El grafo no es un árbol válido")
            return

        self.pasos_algoritmo = self.controller.generar_pasos_algoritmo()
        self.paso_actual = 0

        self.limpiar_layout(self.layout_pasos)
        self.limpiar_layout(self.layout_resultados)

        self.btn_calcular.setEnabled(False)
        self.tabs.setCurrentIndex(1)  # Cambiar a tab de pasos

        self.timer.start(1500)

    def mostrar_siguiente_paso(self):
        """Muestra siguiente paso de animación"""
        if self.paso_actual >= len(self.pasos_algoritmo):
            self.timer.stop()
            self.btn_calcular.setEnabled(True)
            self.mostrar_resultados_finales()
            return

        paso = self.pasos_algoritmo[self.paso_actual]

        # Frame contenedor para el paso
        frame_paso = QFrame()
        frame_paso.setStyleSheet("""
            QFrame {
                background-color: #FFFEF7;
                border: 3px solid #bf8f62;
                border-radius: 10px;
                padding: 15px;
                margin: 10px;
            }
        """)
        layout_paso = QVBoxLayout(frame_paso)

        # Título del paso
        titulo_paso = QLabel(paso['titulo'])
        titulo_paso.setStyleSheet("""
            font-size: 14px;
            font-weight: bold;
            color: #6C4E31;
            padding: 8px;
            background-color: #E8D4B8;
            border-radius: 6px;
        """)
        titulo_paso.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_paso.addWidget(titulo_paso)

        # Descripción del paso
        desc_paso = QLabel(paso['descripcion'])
        desc_paso.setStyleSheet("""
            font-size: 12px;
            color: #2d1f15;
            padding: 10px;
            background-color: #FAF3E8;
            border-radius: 5px;
        """)
        desc_paso.setWordWrap(True)
        layout_paso.addWidget(desc_paso)

        # Visualizador del grafo para este paso
        vertices_activos = paso['vertices_activos']
        if vertices_activos:
            mapeo = {v_orig: i for i, v_orig in enumerate(vertices_activos)}
            etiquetas_mostrar = {i: paso['etiquetas'][v_orig] for i, v_orig in enumerate(vertices_activos)}

            aristas_mostrar = []
            for origen, destino in paso['aristas']:
                if origen in mapeo and destino in mapeo:
                    aristas_mostrar.append((mapeo[origen], mapeo[destino]))

            visualizador = VisualizadorGrafo(
                titulo="",
                parent=self,
                es_editable=False,
                ancho=700,
                alto=400
            )
            visualizador.set_grafo(len(vertices_activos), aristas_mostrar, etiquetas_mostrar)
            visualizador.setStyleSheet("background-color: white; border-radius: 8px;")
            # Tamaño fijo para los pasos
            layout_paso.addWidget(visualizador)

        self.layout_pasos.addWidget(frame_paso)
        self.paso_actual += 1

        # Auto-scroll al final
        scroll_area = self.layout_pasos.parentWidget().parentWidget()
        if isinstance(scroll_area, QScrollArea):
            scroll_area.verticalScrollBar().setValue(
                scroll_area.verticalScrollBar().maximum()
            )

    def mostrar_resultados_finales(self):
        """Muestra matriz de distancias y resultados finales"""
        centro, excentricidades, radio, diametro, detalles = self.controller.calcular_centro()

        self.centro_calculado = {
            'centro': centro,
            'excentricidades': excentricidades,
            'radio': radio,
            'diametro': diametro
        }
        self.btn_guardar_centro.setEnabled(True)

        # Cambiar a tab de resultados
        self.tabs.setCurrentIndex(2)

        # Título de resultados
        titulo_resultados = QLabel("Resultados del Análisis")
        titulo_resultados.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #6C4E31;
            padding: 15px;
            background-color: #FFFEF7;
            border: 3px solid #bf8f62;
            border-radius: 10px;
            margin: 10px;
        """)
        titulo_resultados.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout_resultados.addWidget(titulo_resultados)

        # Resumen ejecutivo - CAMBIO DE VERDE A CAFÉ
        resumen = QFrame()
        resumen.setStyleSheet("""
            background-color: #F5E6D3;
            border: 3px solid #8B6342;
            border-radius: 10px;
            padding: 15px;
            margin: 10px;
        """)
        resumen_layout = QVBoxLayout(resumen)

        centro_etiquetas = [self.etiquetas[v] for v in centro]
        if len(centro) == 1:
            texto_centro = f"<b>Centro del Árbol:</b> {centro_etiquetas[0]} "
        else:
            texto_centro = f"<b>Centro del Árbol:</b> {{{', '.join(centro_etiquetas)}}} "

        lbl_resumen = QLabel(f"""
            <div style='font-size: 13px;'>
            {texto_centro}<br>
            <b>Radio:</b> {radio}<br>
            <b>Diámetro:</b> {diametro}<br>
            <b>Excentricidad mínima:</b> {radio} (define el centro)
            </div>
        """)
        lbl_resumen.setStyleSheet("color: #6C4E31; padding: 5px; font-weight: bold;")
        resumen_layout.addWidget(lbl_resumen)
        self.layout_resultados.addWidget(resumen)

        # Matriz de distancias
        titulo_matriz = QLabel("Matriz de Distancias y Excentricidades")
        titulo_matriz.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #6C4E31;
            padding: 10px;
            margin-top: 20px;
        """)
        self.layout_resultados.addWidget(titulo_matriz)

        tabla_html = self.controller.generar_tabla_distancias_html()
        texto_matriz = QTextEdit()
        texto_matriz.setReadOnly(True)
        texto_matriz.setMinimumHeight(300)
        texto_matriz.setStyleSheet("""
            background-color: #FFFEF7;
            border: 2px solid #bf8f62;
            border-radius: 8px;
            padding: 10px;
        """)
        texto_matriz.setHtml(f"""
            <div style='font-family: Arial;'>
            <p style='color: #6C4E31; font-size: 12px;'>
            La <b>última columna</b> muestra la <b>Excentricidad (Exc.)</b> de cada vértice.<br>
            El vértice con menor excentricidad es el <b>centro</b> del árbol (resaltado en café claro).
            </p>
            {tabla_html}
            </div>
        """)
        self.layout_resultados.addWidget(texto_matriz)

        # Tabla de excentricidades detallada
        titulo_exc = QLabel("📏 Excentricidades Detalladas")
        titulo_exc.setStyleSheet("""
            font-size: 15px;
            font-weight: bold;
            color: #6C4E31;
            padding: 10px;
            margin-top: 20px;
        """)
        self.layout_resultados.addWidget(titulo_exc)

        frame_exc = QFrame()
        frame_exc.setStyleSheet("""
            background-color: #FFFEF7;
            border: 2px solid #bf8f62;
            border-radius: 8px;
            padding: 15px;
        """)
        layout_exc = QVBoxLayout(frame_exc)

        for v in sorted(excentricidades.keys()):
            etiq = self.etiquetas[v]
            exc = excentricidades[v]
            es_centro = v in centro

            if es_centro:
                # CAMBIO DE VERDE A CAFÉ CLARO
                estilo = """
                    background-color: #E8D4B8;
                    border: 2px solid #8B6342;
                    border-radius: 6px;
                    padding: 8px;
                    font-weight: bold;
                    color: #6C4E31;
                """
                texto = f"Vértice {etiq}: e({etiq}) = {exc}  CENTRO"
            else:
                estilo = """
                    background-color: #FAF3E8;
                    border: 1px solid #D3C1A8;
                    border-radius: 6px;
                    padding: 8px;
                    color: #2d1f15;
                """
                texto = f"Vértice {etiq}: e({etiq}) = {exc}"

            lbl_exc = QLabel(texto)
            lbl_exc.setStyleSheet(estilo)
            layout_exc.addWidget(lbl_exc)

        self.layout_resultados.addWidget(frame_exc)

        # Interpretación final - CAMBIO DE AZUL A CAFÉ
        interpretacion = QTextEdit()
        interpretacion.setReadOnly(True)
        interpretacion.setMaximumHeight(150)
        interpretacion.setStyleSheet("""
            background-color: #F5E6D3;
            border: 2px solid #9c724a;
            border-radius: 8px;
            padding: 10px;
            font-size: 12px;
            color: #2d1f15;
        """)

        if len(centro) == 1:
            texto_interpretacion = f"""
            <b>💡 Interpretación:</b><br><br>
            El vértice <b>{centro_etiquetas[0]}</b> es el centro del árbol porque tiene la menor 
            excentricidad ({radio}). Esto significa que este vértice está lo más "cerca posible" 
            de todos los demás vértices en el árbol.<br><br>
            El diámetro ({diametro}) representa la máxima distancia entre dos vértices cualesquiera.
            """
        else:
            texto_interpretacion = f"""
            <b>Interpretación:</b><br><br>
            Los vértices <b>{{{', '.join(centro_etiquetas)}}}</b> forman el centro del árbol porque 
            comparten la menor excentricidad ({radio}). Ambos están igualmente "cerca" de los 
            vértices más lejanos.<br><br>
            El diámetro ({diametro}) representa la máxima distancia entre dos vértices cualesquiera.
            """

        interpretacion.setHtml(texto_interpretacion)
        self.layout_resultados.addWidget(interpretacion)

        # Espaciador final
        self.layout_resultados.addStretch()

    def limpiar_layout(self, layout):
        """Limpia todos los widgets de un layout"""
        while layout.count():
            item = layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def limpiar(self):
        """Limpia todo y reinicia"""
        self.timer.stop()
        self.aristas = []
        self.etiquetas = {}
        self.paso_actual = 0
        self.pasos_algoritmo = []
        self.vertice_seleccionado = None
        self.centro_calculado = None
        self.visualizador_grafo = None

        self.btn_guardar_centro.setEnabled(False)
        self.btn_calcular.setEnabled(False)
        self.btn_guardar_grafo.setEnabled(False)
        self.btn_eliminar_arista.setEnabled(False)
        self.btn_eliminar_vertice.setEnabled(False)

        self.limpiar_layout(self.layout_arbol)
        self.limpiar_layout(self.layout_pasos)
        self.limpiar_layout(self.layout_resultados)

        self.mostrar_pantalla_inicial()
        self.tabs.setCurrentIndex(0)