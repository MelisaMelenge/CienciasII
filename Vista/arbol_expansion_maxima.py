from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QSpinBox, QFileDialog, QScrollArea, QTextEdit, QTabWidget
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo import VisualizadorGrafo
from Controlador.arboles.maximaController import MaximaController


class ArbolExpansionMaxima(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Inicializar controlador
        self.controller = MaximaController(self)

        self.setWindowTitle("Ciencias de la Computación II - Árbol de Expansión Máxima")

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

        titulo = QLabel("Ciencias de la Computación II - Árbol de Expansión Máxima")
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

        # --- CONFIGURACIÓN DEL GRAFO ---
        grafo_container = QWidget()
        grafo_layout = QVBoxLayout(grafo_container)
        grafo_layout.setSpacing(8)

        label_grafo = QLabel("Configuración del Grafo")
        label_grafo.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        grafo_layout.addWidget(label_grafo, alignment=Qt.AlignCenter)

        config = QHBoxLayout()
        lbl_v = QLabel("Vértices:")
        lbl_v.setStyleSheet("font-size: 12px; color: #2d1f15;")
        config.addWidget(lbl_v)
        self.vertices_spin = QSpinBox()
        self.vertices_spin.setRange(2, 15)
        self.vertices_spin.setValue(4)
        self.vertices_spin.setFixedWidth(60)
        self.vertices_spin.setStyleSheet("""
            QSpinBox {
                padding: 4px;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                background: white;
            }
        """)
        config.addWidget(self.vertices_spin)
        self.btn_crear = QPushButton("Crear")
        config.addWidget(self.btn_crear)
        grafo_layout.addLayout(config)

        botones = QHBoxLayout()
        self.btn_agregar_arista = QPushButton("+ Arista")
        self.btn_eliminar_arista = QPushButton("- Arista")
        botones.addWidget(self.btn_agregar_arista)
        botones.addWidget(self.btn_eliminar_arista)
        grafo_layout.addLayout(botones)

        botones_archivo = QHBoxLayout()
        self.btn_guardar = QPushButton("Guardar")
        self.btn_cargar = QPushButton("Cargar")
        botones_archivo.addWidget(self.btn_guardar)
        botones_archivo.addWidget(self.btn_cargar)
        grafo_layout.addLayout(botones_archivo)

        self.btn_limpiar = QPushButton("Limpiar")
        grafo_layout.addWidget(self.btn_limpiar)

        # --- ALGORITMO ---
        algoritmo_container = QWidget()
        algoritmo_layout = QVBoxLayout(algoritmo_container)
        algoritmo_layout.setSpacing(8)

        label_algoritmo = QLabel("Algoritmo")
        label_algoritmo.setStyleSheet("font-size: 15px; font-weight: bold; color: #6C4E31;")
        algoritmo_layout.addWidget(label_algoritmo, alignment=Qt.AlignCenter)

        self.btn_ejecutar = QPushButton("🌳 Generar Árbol")
        self.btn_ejecutar.setStyleSheet("""
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
        algoritmo_layout.addWidget(self.btn_ejecutar)

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

        controles_layout.addWidget(grafo_container)
        controles_layout.addWidget(algoritmo_container)
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

        # Grafos
        grafos_layout = QHBoxLayout()
        grafos_layout.setSpacing(20)
        grafos_layout.setAlignment(Qt.AlignCenter)

        self.visual_grafo = VisualizadorGrafo("Grafo Original", parent=self, es_editable=True)
        self.visual_arbol = VisualizadorGrafo("Árbol de Expansión Máxima", parent=self, es_editable=False)

        self.visual_grafo.etiqueta_cambiada.connect(self.controller.actualizar_etiqueta)
        self.visual_grafo.ponderacion_cambiada.connect(self.controller.actualizar_ponderacion)

        for visual in (self.visual_grafo, self.visual_arbol):
            visual.setStyleSheet("""
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            """)

        grafos_layout.addWidget(self.visual_grafo)
        grafos_layout.addWidget(self.visual_arbol)
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

        # ======= TABS DE RESULTADOS =======
        self.tabs_resultados = QTabWidget()
        self.tabs_resultados.setStyleSheet("""
            QTabWidget::pane {
                border: 2px solid #bf8f62;
                border-radius: 8px;
                background-color: #FFF3E0;
            }
            QTabBar::tab {
                background-color: #FFDBB5;
                color: #2d1f15;
                padding: 8px 16px;
                border: 1px solid #bf8f62;
                border-bottom: none;
                border-top-left-radius: 4px;
                border-top-right-radius: 4px;
                margin-right: 2px;
                font-weight: bold;
            }
            QTabBar::tab:selected {
                background-color: #FFF3E0;
                color: #6C4E31;
            }
        """)

        # Tab Información General
        self.info_text = QTextEdit()
        self.info_text.setReadOnly(True)
        self.info_text.setMinimumHeight(250)
        self.info_text.setStyleSheet("""
            QTextEdit {
                background-color: #FFF8E7;
                border: 1px solid #bf8f62;
                border-radius: 4px;
                padding: 10px;
                font-size: 13px;
                color: #2d1f15;
            }
        """)
        self.tabs_resultados.addTab(self.info_text, "📊 Información General")

        # Tab Circuitos
        self.circuitos_text = QTextEdit()
        self.circuitos_text.setReadOnly(True)
        self.circuitos_text.setMinimumHeight(250)
        self.circuitos_text.setStyleSheet(self.info_text.styleSheet())
        self.tabs_resultados.addTab(self.circuitos_text, "🔄 Circuitos del Grafo")

        # Tab Circuitos Fundamentales
        self.circuitos_fund_text = QTextEdit()
        self.circuitos_fund_text.setReadOnly(True)
        self.circuitos_fund_text.setMinimumHeight(250)
        self.circuitos_fund_text.setStyleSheet(self.info_text.styleSheet())
        self.tabs_resultados.addTab(self.circuitos_fund_text, "⭕ Circuitos Fundamentales")

        # Tab Conjuntos de Corte
        self.conjuntos_text = QTextEdit()
        self.conjuntos_text.setReadOnly(True)
        self.conjuntos_text.setMinimumHeight(250)
        self.conjuntos_text.setStyleSheet(self.info_text.styleSheet())
        self.tabs_resultados.addTab(self.conjuntos_text, "✂️ Conjuntos de Corte")

        # Tab Matrices
        self.matrices_text = QTextEdit()
        self.matrices_text.setReadOnly(True)
        self.matrices_text.setMinimumHeight(300)
        self.matrices_text.setStyleSheet(self.info_text.styleSheet())
        self.tabs_resultados.addTab(self.matrices_text, "🔢 Matrices")

        self.contenedor_layout.addWidget(self.tabs_resultados)

        self.setCentralWidget(central)

        # ======= CONEXIONES =======
        self.btn_crear.clicked.connect(self.controller.crear_grafo)
        self.btn_agregar_arista.clicked.connect(self.controller.agregar_arista)
        self.btn_eliminar_arista.clicked.connect(self.controller.eliminar_arista)
        self.btn_guardar.clicked.connect(self.controller.guardar_grafo)
        self.btn_cargar.clicked.connect(self.controller.cargar_grafo)
        self.btn_limpiar.clicked.connect(self.controller.limpiar_grafo)
        self.btn_ejecutar.clicked.connect(self.controller.ejecutar_algoritmo)