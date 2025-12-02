from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QScrollArea, QMessageBox,
    QSpinBox, QFileDialog, QSplitter, QDialog, QComboBox, QDoubleSpinBox
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Controlador.arboles.DistanciaController import DistanciaController
import json


class DialogoAristaDistancia(QDialog):
    """Diálogo personalizado para agregar aristas con el estilo del programa"""

    def __init__(self, num_vertices, parent=None, etiquetas=None, titulo_arbol="Árbol"):
        super().__init__(parent)
        self.num_vertices = num_vertices
        self.etiquetas = etiquetas if etiquetas else {}
        self.titulo_arbol = titulo_arbol

        self.setWindowTitle(f"Agregar Arista - {titulo_arbol}")
        self.setModal(True)
        self.setMinimumWidth(350)

        # Estilo del diálogo
        self.setStyleSheet("""
            QDialog {
                background-color: #FFEAC5;
            }
            QLabel {
                color: #2d1f15;
                font-size: 13px;
            }
            QComboBox, QDoubleSpinBox {
                padding: 6px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
                font-weight: bold;
                min-height: 25px;
            }
            QComboBox::drop-down {
                border: none;
                width: 25px;
            }
            QComboBox::down-arrow {
                image: none;
                border-left: 5px solid transparent;
                border-right: 5px solid transparent;
                border-top: 6px solid #6C4E31;
                margin-right: 5px;
            }
        """)

        layout = QVBoxLayout(self)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Título
        titulo = QLabel(f"Agregar Arista en {titulo_arbol}")
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

        # Vértice origen
        origen_layout = QHBoxLayout()
        lbl_origen = QLabel("Vértice Origen:")
        lbl_origen.setStyleSheet("font-weight: bold; color: #6C4E31;")
        self.combo_origen = QComboBox()
        for i in range(num_vertices):
            etiqueta = self.etiquetas.get(i, chr(97 + i))
            self.combo_origen.addItem(f"{i + 1}: {etiqueta}", i)
        origen_layout.addWidget(lbl_origen)
        origen_layout.addWidget(self.combo_origen)
        layout.addLayout(origen_layout)

        # Vértice destino
        destino_layout = QHBoxLayout()
        lbl_destino = QLabel("Vértice Destino:")
        lbl_destino.setStyleSheet("font-weight: bold; color: #6C4E31;")
        self.combo_destino = QComboBox()
        for i in range(num_vertices):
            etiqueta = self.etiquetas.get(i, chr(97 + i))
            self.combo_destino.addItem(f"{i + 1}: {etiqueta}", i)
        destino_layout.addWidget(lbl_destino)
        destino_layout.addWidget(self.combo_destino)
        layout.addLayout(destino_layout)

        # Ponderación
        pond_layout = QHBoxLayout()
        lbl_pond = QLabel("Ponderación:")
        lbl_pond.setStyleSheet("font-weight: bold; color: #6C4E31;")
        self.spin_ponderacion = QDoubleSpinBox()
        self.spin_ponderacion.setRange(0.1, 100.0)
        self.spin_ponderacion.setValue(1.0)
        self.spin_ponderacion.setDecimals(1)
        self.spin_ponderacion.setSingleStep(0.1)
        pond_layout.addWidget(lbl_pond)
        pond_layout.addWidget(self.spin_ponderacion)
        layout.addLayout(pond_layout)

        # Nota informativa
        nota = QLabel("💡 Los bucles no están permitidos")
        nota.setStyleSheet("""
            color: #8B6342;
            font-size: 11px;
            font-style: italic;
            padding: 8px;
            background-color: #FFF3E0;
            border-radius: 5px;
        """)
        layout.addWidget(nota)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        btn_aceptar = QPushButton("Agregar Arista")
        btn_aceptar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_aceptar.clicked.connect(self.accept)

        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #bf8f62;
            }
        """)
        btn_cancelar.clicked.connect(self.reject)

        botones_layout.addWidget(btn_aceptar)
        botones_layout.addWidget(btn_cancelar)
        layout.addLayout(botones_layout)

    def get_arista(self):
        """Retorna la arista seleccionada (origen, destino)"""
        origen = self.combo_origen.currentData()
        destino = self.combo_destino.currentData()
        # Normalizar la arista
        return tuple(sorted([origen, destino]))

    def get_ponderacion(self):
        """Retorna la ponderación ingresada"""
        return self.spin_ponderacion.value()


class DistanciaArboles(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = DistanciaController()

        self.setWindowTitle("Distancia entre Dos Árboles")
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

        # SPLITTER PRINCIPAL
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

        # PANEL DERECHO - Visualización
        panel_der = self.crear_panel_visualizacion()
        splitter_principal.addWidget(panel_der)

        splitter_principal.setSizes([300, 1200])
        layout.addWidget(splitter_principal)

        # Variables de estado
        self.arbol_actual = 1
        self.num_vertices_1 = 0
        self.aristas_1 = []
        self.etiquetas_1 = {}
        self.ponderaciones_1 = {}
        self.visualizador_1 = None
        self.vertice_seleccionado_1 = None

        self.num_vertices_2 = 0
        self.aristas_2 = []
        self.etiquetas_2 = {}
        self.ponderaciones_2 = {}
        self.visualizador_2 = None
        self.vertice_seleccionado_2 = None

        self.resultado_distancia = None

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

        titulo = QLabel("Distancia entre Dos Árboles - D(T1,T2)")
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
        titulo = QLabel("Configuración")
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

        # ÁRBOL 1
        lbl_arbol1 = QLabel("ÁRBOL T1")
        lbl_arbol1.setStyleSheet("font-weight: bold; color: #6C4E31; font-size: 14px;")
        layout.addWidget(lbl_arbol1)

        vertices_layout_1 = QHBoxLayout()
        lbl_vertices_1 = QLabel("Vértices:")
        lbl_vertices_1.setStyleSheet("font-weight: bold; color: #2d1f15;")
        self.spin_vertices_1 = QSpinBox()
        self.spin_vertices_1.setMinimum(3)
        self.spin_vertices_1.setMaximum(10)
        self.spin_vertices_1.setValue(3)
        self.spin_vertices_1.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
                font-weight: bold;
            }
        """)
        vertices_layout_1.addWidget(lbl_vertices_1)
        vertices_layout_1.addWidget(self.spin_vertices_1)
        layout.addLayout(vertices_layout_1)

        self.btn_generar_1 = QPushButton("Generar T1")
        self.btn_generar_1.clicked.connect(lambda: self.generar_arbol(1))
        layout.addWidget(self.btn_generar_1)

        self.btn_agregar_arista_1 = QPushButton("Agregar Arista T1")
        self.btn_agregar_arista_1.clicked.connect(lambda: self.agregar_arista_manual(1))
        self.btn_agregar_arista_1.setEnabled(False)
        layout.addWidget(self.btn_agregar_arista_1)

        # Botones de guardar/cargar T1
        botones_t1_layout = QHBoxLayout()
        self.btn_guardar_1 = QPushButton("Guardar")
        self.btn_guardar_1.clicked.connect(lambda: self.guardar_arbol(1))
        self.btn_guardar_1.setEnabled(False)
        self.btn_cargar_1 = QPushButton("Cargar")
        self.btn_cargar_1.clicked.connect(lambda: self.cargar_arbol(1))
        botones_t1_layout.addWidget(self.btn_guardar_1)
        botones_t1_layout.addWidget(self.btn_cargar_1)
        layout.addLayout(botones_t1_layout)

        layout.addWidget(QLabel())  # Separador

        # ÁRBOL 2
        lbl_arbol2 = QLabel("ÁRBOL T2")
        lbl_arbol2.setStyleSheet("font-weight: bold; color: #6C4E31; font-size: 14px;")
        layout.addWidget(lbl_arbol2)

        vertices_layout_2 = QHBoxLayout()
        lbl_vertices_2 = QLabel("Vértices:")
        lbl_vertices_2.setStyleSheet("font-weight: bold; color: #2d1f15;")
        self.spin_vertices_2 = QSpinBox()
        self.spin_vertices_2.setMinimum(3)
        self.spin_vertices_2.setMaximum(10)
        self.spin_vertices_2.setValue(3)
        self.spin_vertices_2.setStyleSheet("""
            QSpinBox {
                padding: 6px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
                font-weight: bold;
            }
        """)
        vertices_layout_2.addWidget(lbl_vertices_2)
        vertices_layout_2.addWidget(self.spin_vertices_2)
        layout.addLayout(vertices_layout_2)

        self.btn_generar_2 = QPushButton("Generar T2")
        self.btn_generar_2.clicked.connect(lambda: self.generar_arbol(2))
        layout.addWidget(self.btn_generar_2)

        self.btn_agregar_arista_2 = QPushButton("Agregar Arista T2")
        self.btn_agregar_arista_2.clicked.connect(lambda: self.agregar_arista_manual(2))
        self.btn_agregar_arista_2.setEnabled(False)
        layout.addWidget(self.btn_agregar_arista_2)

        # Botones de guardar/cargar T2
        botones_t2_layout = QHBoxLayout()
        self.btn_guardar_2 = QPushButton("Guardar")
        self.btn_guardar_2.clicked.connect(lambda: self.guardar_arbol(2))
        self.btn_guardar_2.setEnabled(False)
        self.btn_cargar_2 = QPushButton("Cargar")
        self.btn_cargar_2.clicked.connect(lambda: self.cargar_arbol(2))
        botones_t2_layout.addWidget(self.btn_guardar_2)
        botones_t2_layout.addWidget(self.btn_cargar_2)
        layout.addLayout(botones_t2_layout)

        layout.addWidget(QLabel())  # Separador

        # CALCULAR DISTANCIA
        self.btn_calcular = QPushButton("Calcular Distancia")
        self.btn_calcular.setStyleSheet(self.get_button_style("#6C4E31", "#388E3C"))
        self.btn_calcular.clicked.connect(self.calcular_distancia)
        self.btn_calcular.setEnabled(False)
        layout.addWidget(self.btn_calcular)


        layout.addWidget(QLabel())  # Separador

        btn_limpiar = QPushButton("Limpiar Todo")
        btn_limpiar.setStyleSheet(self.get_button_style("#6C4E31", "#D32F2F"))
        btn_limpiar.clicked.connect(self.limpiar)
        layout.addWidget(btn_limpiar)

        layout.addStretch()

        # Aplicar estilo a botones
        for btn in panel.findChildren(QPushButton):
            if not btn.styleSheet():
                btn.setStyleSheet(self.get_button_style())

        return panel

    def crear_panel_visualizacion(self):
        """Crea el panel de visualización"""
        panel = QFrame()
        panel.setStyleSheet("background-color: transparent;")

        layout = QVBoxLayout(panel)
        layout.setContentsMargins(0, 0, 0, 0)

        # Área con scroll
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setStyleSheet(self.get_scroll_style())

        scroll_widget = QWidget()
        scroll_widget.setStyleSheet("background-color: #E8D4B8;")
        self.layout_visualizacion = QVBoxLayout(scroll_widget)
        self.layout_visualizacion.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.layout_visualizacion.setSpacing(15)

        scroll.setWidget(scroll_widget)
        layout.addWidget(scroll)

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
                border: 2px solid #bf8f62;
                border-radius: 8px;
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
        """Muestra pantalla inicial"""
        self.limpiar_layout(self.layout_visualizacion)

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
            "Bienvenido al Cálculo de Distancia entre Árboles\n\n"
            "1. Genera o carga el Árbol T1\n"
            "2. Genera o carga el Árbol T2\n"
            "3. Haz clic en 'Agregar Arista' para conectar vértices\n"
            "4. Haz clic en aristas para asignar ponderación\n"
            "5. Forma árboles válidos (n-1 aristas)\n"
            "6. Presiona 'Calcular Distancia'\n\n"
            "La distancia mide qué tan diferentes son dos árboles\n"
            "considerando las ponderaciones de sus aristas"
        )
        label_inicial.setMinimumSize(700, 450)

        self.layout_visualizacion.addWidget(label_inicial)

    def generar_arbol(self, num_arbol):
        """Genera árbol vacío"""
        if num_arbol == 1:
            self.num_vertices_1 = self.spin_vertices_1.value()
            self.aristas_1 = []
            self.etiquetas_1 = {i: chr(97 + i) for i in range(self.num_vertices_1)}
            self.ponderaciones_1 = {}
            self.vertice_seleccionado_1 = None
            self.btn_agregar_arista_1.setEnabled(True)
        else:
            self.num_vertices_2 = self.spin_vertices_2.value()
            self.aristas_2 = []
            self.etiquetas_2 = {i: chr(97 + i) for i in range(self.num_vertices_2)}
            self.ponderaciones_2 = {}
            self.vertice_seleccionado_2 = None
            self.btn_agregar_arista_2.setEnabled(True)

        self.mostrar_arboles()
        self.actualizar_estado()

    def mostrar_arboles(self):
        """Muestra ambos árboles en la visualización"""
        self.limpiar_layout(self.layout_visualizacion)

        # Contenedor para Árbol 1
        if self.num_vertices_1 > 0:
            frame1 = QFrame()
            frame1.setStyleSheet("""
                background-color: #FAF3E8;
                border: 2px solid #bf8f62;
                border-radius: 10px;
                padding: 10px;
            """)
            frame1.setMinimumSize(700, 350)

            layout1 = QVBoxLayout(frame1)
            titulo1 = QLabel("Árbol T1")
            titulo1.setStyleSheet("font-size: 16px; font-weight: bold; color: #6C4E31;")
            titulo1.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout1.addWidget(titulo1)

            self.visualizador_1 = VisualizadorGrafo(
                titulo="Haz clic izquierdo en aristas para ponderar",
                parent=self,
                es_editable=True,
                ancho=680,
                alto=300
            )
            self.visualizador_1.set_grafo(
                self.num_vertices_1,
                self.aristas_1,
                self.etiquetas_1,
                self.ponderaciones_1
            )

            # Conectar señales
            self.visualizador_1.ponderacion_cambiada.connect(self.on_ponderacion_cambiada_1)
            self.visualizador_1.etiqueta_cambiada.connect(self.on_etiqueta_cambiada_1)

            layout1.addWidget(self.visualizador_1)
            self.layout_visualizacion.addWidget(frame1)

        # Contenedor para Árbol 2
        if self.num_vertices_2 > 0:
            frame2 = QFrame()
            frame2.setStyleSheet("""
                background-color: #FAF3E8;
                border: 2px solid #bf8f62;
                border-radius: 10px;
                padding: 10px;
            """)
            frame2.setMinimumSize(700, 350)

            layout2 = QVBoxLayout(frame2)
            titulo2 = QLabel("Árbol T2")
            titulo2.setStyleSheet("font-size: 16px; font-weight: bold; color: #6C4E31;")
            titulo2.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout2.addWidget(titulo2)

            self.visualizador_2 = VisualizadorGrafo(
                titulo="Haz clic izquierdo en aristas para ponderar",
                parent=self,
                es_editable=True,
                ancho=680,
                alto=300
            )
            self.visualizador_2.set_grafo(
                self.num_vertices_2,
                self.aristas_2,
                self.etiquetas_2,
                self.ponderaciones_2
            )

            # Conectar señales
            self.visualizador_2.ponderacion_cambiada.connect(self.on_ponderacion_cambiada_2)
            self.visualizador_2.etiqueta_cambiada.connect(self.on_etiqueta_cambiada_2)

            layout2.addWidget(self.visualizador_2)
            self.layout_visualizacion.addWidget(frame2)

        # Mostrar resultado si existe
        if self.resultado_distancia is not None:
            self.mostrar_resultado_en_layout()

    def mostrar_resultado_en_layout(self):
        """Muestra el resultado cuando ya fue calculado"""
        if not self.resultado_distancia:
            return

        frame_resultado = QFrame()
        frame_resultado.setStyleSheet("""
            background-color: #FFFEF7;
            border: 3px solid #6C4E31;
            border-radius: 10px;
            padding: 15px;
        """)

        layout_resultado = QVBoxLayout(frame_resultado)

        titulo_resultado = QLabel("Resultado del Cálculo")
        titulo_resultado.setStyleSheet("font-size: 18px; font-weight: bold; color: #6C4E31;")
        titulo_resultado.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout_resultado.addWidget(titulo_resultado)

        html_reporte = self.controller.generar_reporte_html(self.resultado_distancia)

        text_resultado = QTextEdit()
        text_resultado.setReadOnly(True)
        text_resultado.setHtml(html_reporte)
        text_resultado.setMinimumHeight(400)
        text_resultado.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #bf8f62;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout_resultado.addWidget(text_resultado)

        self.layout_visualizacion.addWidget(frame_resultado)

    def actualizar_estado(self):
        """Actualiza el estado de los botones"""
        arbol1_valido = (
                self.num_vertices_1 > 0 and
                len(self.aristas_1) == self.num_vertices_1 - 1
        )
        arbol2_valido = (
                self.num_vertices_2 > 0 and
                len(self.aristas_2) == self.num_vertices_2 - 1
        )

        self.btn_calcular.setEnabled(arbol1_valido and arbol2_valido)

        # Habilitar/deshabilitar botones de agregar arista
        if self.num_vertices_1 > 0:
            self.btn_agregar_arista_1.setEnabled(len(self.aristas_1) < self.num_vertices_1 - 1)
            self.btn_guardar_1.setEnabled(len(self.aristas_1) > 0)  # Nuevo

        if self.num_vertices_2 > 0:
            self.btn_agregar_arista_2.setEnabled(len(self.aristas_2) < self.num_vertices_2 - 1)
            self.btn_guardar_2.setEnabled(len(self.aristas_2) > 0)  # Nuevo

    def calcular_distancia(self):
        """Calcula la distancia entre los dos árboles"""
        self.controller.set_arbol1(
            self.num_vertices_1,
            self.aristas_1,
            self.etiquetas_1,
            self.ponderaciones_1
        )
        self.controller.set_arbol2(
            self.num_vertices_2,
            self.aristas_2,
            self.etiquetas_2,
            self.ponderaciones_2
        )

        distancia, detalles = self.controller.calcular_distancia_arboles()

        if distancia is None:
            self.mostrar_mensaje("Error", detalles, "error")
            return

        # Guardar resultado para poder mostrarlo después
        self.resultado_distancia = detalles

        # Mostrar resultado
        self.mostrar_resultado(distancia, detalles)

    def mostrar_resultado(self, distancia, detalles):
        """Muestra el resultado de la distancia"""
        # Crear frame para resultado
        frame_resultado = QFrame()
        frame_resultado.setStyleSheet("""
            background-color: #FFFEF7;
            border: 3px solid #6C4E31;
            border-radius: 10px;
            padding: 15px;
        """)

        layout_resultado = QVBoxLayout(frame_resultado)

        # Header con título y botón guardar
        header_layout = QHBoxLayout()

        titulo_resultado = QLabel("Resultado del Cálculo")
        titulo_resultado.setStyleSheet("font-size: 18px; font-weight: bold; color: #6C4E31;")
        header_layout.addWidget(titulo_resultado)

        header_layout.addStretch()

        btn_guardar_resultado = QPushButton("Guardar Resultado")
        btn_guardar_resultado.setStyleSheet(self.get_button_style("#6C4E31", "#388E3C"))
        btn_guardar_resultado.clicked.connect(self.guardar_resultado)
        header_layout.addWidget(btn_guardar_resultado)

        layout_resultado.addLayout(header_layout)

        # Generar reporte HTML
        html_reporte = self.controller.generar_reporte_html(detalles)

        text_resultado = QTextEdit()
        text_resultado.setReadOnly(True)
        text_resultado.setHtml(html_reporte)
        text_resultado.setMinimumHeight(400)
        text_resultado.setStyleSheet("""
            QTextEdit {
                background-color: white;
                border: 1px solid #bf8f62;
                border-radius: 5px;
                padding: 10px;
            }
        """)
        layout_resultado.addWidget(text_resultado)

        self.layout_visualizacion.addWidget(frame_resultado)

    def guardar_arbol(self, num_arbol):
        """Guarda un árbol en formato JSON"""
        if num_arbol == 1:
            num_vertices = self.num_vertices_1
            aristas = self.aristas_1
            etiquetas = self.etiquetas_1
            ponderaciones = self.ponderaciones_1
            nombre = "T1"
        else:
            num_vertices = self.num_vertices_2
            aristas = self.aristas_2
            etiquetas = self.etiquetas_2
            ponderaciones = self.ponderaciones_2
            nombre = "T2"

        if num_vertices == 0:
            self.mostrar_mensaje("Error", f"No hay árbol {nombre} para guardar", "error")
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            f"Guardar Árbol {nombre}",
            f"arbol_{nombre}.json",
            "JSON Files (*.json)"
        )

        if not archivo:
            return

        try:
            # Convertir ponderaciones a formato serializable
            ponderaciones_serializables = {
                f"{k[0]},{k[1]}": v for k, v in ponderaciones.items()
            }

            datos = {
                'vertices': num_vertices,
                'aristas': aristas,
                'etiquetas': etiquetas,
                'ponderaciones': ponderaciones_serializables
            }

            with open(archivo, 'w') as f:
                json.dump(datos, f, indent=2)

            self.mostrar_mensaje("Éxito", f"Árbol {nombre} guardado correctamente", "info")

        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al guardar archivo:\n{str(e)}", "error")

    def cargar_arbol(self, num_arbol):
        """Carga un árbol desde archivo JSON"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            f"Cargar Árbol T{num_arbol}",
            "",
            "JSON Files (*.json)"
        )

        if not archivo:
            return

        try:
            with open(archivo, 'r') as f:
                datos = json.load(f)

            if num_arbol == 1:
                self.num_vertices_1 = datos['vertices']
                self.aristas_1 = [tuple(a) for a in datos['aristas']]
                self.etiquetas_1 = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
                self.ponderaciones_1 = {tuple(map(int, k.split(','))): v for k, v in
                                        datos.get('ponderaciones', {}).items()}
                self.spin_vertices_1.setValue(self.num_vertices_1)
                self.btn_agregar_arista_1.setEnabled(True)
            else:
                self.num_vertices_2 = datos['vertices']
                self.aristas_2 = [tuple(a) for a in datos['aristas']]
                self.etiquetas_2 = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
                self.ponderaciones_2 = {tuple(map(int, k.split(','))): v for k, v in
                                        datos.get('ponderaciones', {}).items()}
                self.spin_vertices_2.setValue(self.num_vertices_2)
                self.btn_agregar_arista_2.setEnabled(True)

            self.mostrar_arboles()
            self.actualizar_estado()

            self.mostrar_mensaje("Éxito", f"Árbol T{num_arbol} cargado correctamente", "info")

        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al cargar archivo:\n{str(e)}", "error")

    def guardar_resultado(self):
        """Guarda el resultado del cálculo en formato JSON"""
        if not self.resultado_distancia:
            self.mostrar_mensaje("Error", "No hay resultado para guardar", "error")
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Resultado",
            "resultado_distancia.json",
            "JSON Files (*.json)"
        )

        if not archivo:
            return

        try:
            # Preparar datos para serializar
            resultado_serializable = {
                'distancia': self.resultado_distancia['distancia'],
                'arbol1': {
                    'sv': list(self.resultado_distancia['arbol1']['sv']),
                    'sa': {f"{k[0]},{k[1]}": v for k, v in self.resultado_distancia['arbol1']['sa'].items()},
                    'cardinalidad_sv': self.resultado_distancia['arbol1']['cardinalidad_sv'],
                    'cardinalidad_sa': self.resultado_distancia['arbol1']['cardinalidad_sa'],
                    'suma_ponderaciones': self.resultado_distancia['arbol1']['suma_ponderaciones']
                },
                'arbol2': {
                    'sv': list(self.resultado_distancia['arbol2']['sv']),
                    'sa': {f"{k[0]},{k[1]}": v for k, v in self.resultado_distancia['arbol2']['sa'].items()},
                    'cardinalidad_sv': self.resultado_distancia['arbol2']['cardinalidad_sv'],
                    'cardinalidad_sa': self.resultado_distancia['arbol2']['cardinalidad_sa'],
                    'suma_ponderaciones': self.resultado_distancia['arbol2']['suma_ponderaciones']
                },
                'operaciones': {
                    'vertices_union': list(self.resultado_distancia['operaciones']['vertices_union']),
                    'vertices_interseccion': list(self.resultado_distancia['operaciones']['vertices_interseccion']),
                    'aristas_union': [list(a) for a in self.resultado_distancia['operaciones']['aristas_union']],
                    'aristas_interseccion': [list(a) for a in
                                             self.resultado_distancia['operaciones']['aristas_interseccion']],
                    'aristas_solo_t1': [list(a) for a in self.resultado_distancia['operaciones']['aristas_solo_t1']],
                    'aristas_solo_t2': [list(a) for a in self.resultado_distancia['operaciones']['aristas_solo_t2']],
                    'card_vertices_union': self.resultado_distancia['operaciones']['card_vertices_union'],
                    'card_vertices_interseccion': self.resultado_distancia['operaciones']['card_vertices_interseccion'],
                    'card_aristas_union': self.resultado_distancia['operaciones']['card_aristas_union'],
                    'card_aristas_interseccion': self.resultado_distancia['operaciones']['card_aristas_interseccion'],
                    'suma_diferencias': self.resultado_distancia['operaciones']['suma_diferencias'],
                    'detalles_aristas': self.resultado_distancia['operaciones']['detalles_aristas']
                }
            }

            with open(archivo, 'w') as f:
                json.dump(resultado_serializable, f, indent=2)

            self.mostrar_mensaje("Éxito", "Resultado guardado correctamente", "info")

        except Exception as e:
            self.mostrar_mensaje("Error", f"Error al guardar resultado:\n{str(e)}", "error")

    def limpiar(self):
        """Limpia todos los datos"""
        self.num_vertices_1 = 0
        self.aristas_1 = []
        self.etiquetas_1 = {}
        self.ponderaciones_1 = {}
        self.vertice_seleccionado_1 = None
        self.btn_agregar_arista_1.setEnabled(False)

        self.num_vertices_2 = 0
        self.aristas_2 = []
        self.etiquetas_2 = {}
        self.ponderaciones_2 = {}
        self.vertice_seleccionado_2 = None
        self.btn_agregar_arista_2.setEnabled(False)

        self.visualizador_1 = None
        self.visualizador_2 = None
        self.resultado_distancia = None

        self.mostrar_pantalla_inicial()
        self.actualizar_estado()

    def limpiar_layout(self, layout):
        """Limpia todos los widgets de un layout"""
        while layout.count():
            item = layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def on_ponderacion_cambiada_1(self, arista, ponderacion):
        """Callback cuando cambia la ponderación en árbol 1"""
        arista_norm = tuple(sorted(arista))
        if ponderacion:
            try:
                peso = float(ponderacion)
                self.ponderaciones_1[arista_norm] = peso
            except ValueError:
                self.ponderaciones_1[arista_norm] = ponderacion
        else:
            if arista_norm in self.ponderaciones_1:
                del self.ponderaciones_1[arista_norm]

        self.actualizar_estado()

    def on_ponderacion_cambiada_2(self, arista, ponderacion):
        """Callback cuando cambia la ponderación en árbol 2"""
        arista_norm = tuple(sorted(arista))
        if ponderacion:
            try:
                peso = float(ponderacion)
                self.ponderaciones_2[arista_norm] = peso
            except ValueError:
                self.ponderaciones_2[arista_norm] = ponderacion
        else:
            if arista_norm in self.ponderaciones_2:
                del self.ponderaciones_2[arista_norm]

        self.actualizar_estado()

    def on_etiqueta_cambiada_1(self, indice, etiqueta):
        """Callback cuando cambia la etiqueta en árbol 1"""
        self.etiquetas_1[indice] = etiqueta

    def on_etiqueta_cambiada_2(self, indice, etiqueta):
        """Callback cuando cambia la etiqueta en árbol 2"""
        self.etiquetas_2[indice] = etiqueta

    def mostrar_mensaje(self, titulo, mensaje, tipo="info"):
        """Muestra un mensaje personalizado con los colores de la app"""
        msg = QMessageBox(self)
        msg.setWindowTitle(titulo)
        msg.setText(mensaje)

        if tipo == "error":
            msg.setIcon(QMessageBox.Warning)
        elif tipo == "info":
            msg.setIcon(QMessageBox.Information)
        else:
            msg.setIcon(QMessageBox.Information)

        msg.setStyleSheet("""
            QMessageBox {
                background-color: #FFEAC5;
            }
            QMessageBox QLabel {
                color: #2d1f15;
                font-size: 13px;
            }
            QMessageBox QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 20px;
                border-radius: 6px;
                font-size: 12px;
                min-width: 80px;
            }
            QMessageBox QPushButton:hover {
                background-color: #8B6342;
            }
        """)

        msg.exec()

    def pedir_ponderacion(self, titulo, mensaje, valor_inicial=1.0):
        """Diálogo personalizado para pedir ponderación"""
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QDoubleSpinBox

        dlg = QDialog(self)
        dlg.setWindowTitle(titulo)
        dlg.setModal(True)
        dlg.setFixedSize(400, 180)

        dlg.setStyleSheet("""
            QDialog {
                background-color: #FFEAC5;
            }
            QLabel {
                color: #2d1f15;
                font-size: 13px;
                font-weight: bold;
            }
            QDoubleSpinBox {
                padding: 8px;
                border: 2px solid #bf8f62;
                border-radius: 6px;
                background: white;
                font-size: 12px;
                color: #2d1f15;
                min-width: 150px;
            }
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 13px;
                border: none;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)

        layout = QVBoxLayout(dlg)
        layout.setSpacing(15)
        layout.setContentsMargins(20, 20, 20, 20)

        # Mensaje
        lbl = QLabel(mensaje)
        lbl.setWordWrap(True)
        layout.addWidget(lbl)

        # SpinBox para ponderación
        spin = QDoubleSpinBox()
        spin.setRange(0.1, 100.0)
        spin.setValue(valor_inicial)
        spin.setDecimals(1)
        spin.setSingleStep(0.1)
        layout.addWidget(spin)

        # Botones
        botones_layout = QHBoxLayout()
        botones_layout.setSpacing(10)

        btn_ok = QPushButton("Aceptar")
        btn_cancel = QPushButton("Cancelar")

        btn_ok.clicked.connect(dlg.accept)
        btn_cancel.clicked.connect(dlg.reject)

        botones_layout.addWidget(btn_ok)
        botones_layout.addWidget(btn_cancel)
        layout.addLayout(botones_layout)

        if dlg.exec():
            return spin.value(), True
        return valor_inicial, False

    def agregar_arista_manual(self, num_arbol):
        """Permite agregar una arista manualmente usando un diálogo"""
        if num_arbol == 1:
            num_vertices = self.num_vertices_1
            aristas = self.aristas_1
            etiquetas = self.etiquetas_1
            ponderaciones = self.ponderaciones_1
            nombre = "T1"
        else:
            num_vertices = self.num_vertices_2
            aristas = self.aristas_2
            etiquetas = self.etiquetas_2
            ponderaciones = self.ponderaciones_2
            nombre = "T2"

        if num_vertices == 0:
            self.mostrar_mensaje("Error", f"Primero genera el árbol {nombre}", "error")
            return

        # Verificar si ya está completo
        if len(aristas) >= num_vertices - 1:
            self.mostrar_mensaje(
                "Árbol Completo",
                f"El árbol {nombre} ya tiene {num_vertices - 1} aristas (completo)",
                "info"
            )
            return

        # Abrir diálogo para seleccionar arista
        from Vista.dialogo_arista import DialogoArista
        dlg = DialogoArista(num_vertices, self, etiquetas)

        if dlg.exec():
            arista = dlg.get_arista()

            # Validar que no sean el mismo vértice
            if arista[0] == arista[1]:
                self.mostrar_mensaje(
                    "Error",
                    "No se pueden conectar un vértice consigo mismo",
                    "error"
                )
                return

            # Crear arista normalizada
            arista_norm = tuple(sorted([arista[0], arista[1]]))

            # Verificar si la arista ya existe
            if arista_norm in aristas:
                self.mostrar_mensaje(
                    "Error",
                    f"La arista entre {etiquetas.get(arista[0])} y {etiquetas.get(arista[1])} ya existe",
                    "error"
                )
                return

            # Pedir ponderación
            peso, ok = self.pedir_ponderacion(
                f"Ponderación - {nombre}",
                f"Ingrese la ponderación para la arista\n({etiquetas.get(arista[0])}, {etiquetas.get(arista[1])}):",
                1.0
            )

            if not ok:
                return

            # Agregar arista
            aristas.append(arista_norm)
            ponderaciones[arista_norm] = peso

            # Actualizar
            if num_arbol == 1:
                self.aristas_1 = aristas
                self.ponderaciones_1 = ponderaciones
            else:
                self.aristas_2 = aristas
                self.ponderaciones_2 = ponderaciones

            self.mostrar_arboles()
            self.actualizar_estado()

            # Mostrar info
            aristas_restantes = (num_vertices - 1) - len(aristas)
            if aristas_restantes > 0:
                self.mostrar_mensaje(
                    "Arista Agregada",
                    f"Arista agregada correctamente.\nFaltan {aristas_restantes} arista(s) para completar el árbol.",
                    "info"
                )
            else:
                self.mostrar_mensaje(
                    "Árbol Completo",
                    f"¡Árbol {nombre} completado con {len(aristas)} aristas!",
                    "info"
                )

    def generar_arbol(self, num_arbol):
        """Genera árbol vacío"""
        if num_arbol == 1:
            self.num_vertices_1 = self.spin_vertices_1.value()
            self.aristas_1 = []
            self.etiquetas_1 = {i: chr(97 + i) for i in range(self.num_vertices_1)}
            self.ponderaciones_1 = {}
            self.vertice_seleccionado_1 = None
            self.btn_agregar_arista_1.setEnabled(True)
        else:
            self.num_vertices_2 = self.spin_vertices_2.value()
            self.aristas_2 = []
            self.etiquetas_2 = {i: chr(97 + i) for i in range(self.num_vertices_2)}
            self.ponderaciones_2 = {}
            self.vertice_seleccionado_2 = None
            self.btn_agregar_arista_2.setEnabled(True)

        self.mostrar_arboles()
        self.actualizar_estado()



