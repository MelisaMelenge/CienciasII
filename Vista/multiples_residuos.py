from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem,
    QHBoxLayout
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from Controlador.Internas.MultiplesResiduosController import MultiplesResiduosController
from Vista.dialogo_clave import DialogoClave


class MultiplesResiduos(QMainWindow):
    def __init__(self, cambiar_ventana=None):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = MultiplesResiduosController()
        self.nodo_resaltado = None  # Para resaltar el nodo buscado

        self.setWindowTitle("Ciencias de la Computación II - Múltiples Residuos")
        self.resize(1200, 750)

        # =================== WIDGET CENTRAL ===================
        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        main_layout = QVBoxLayout(central)

        # ================= ENCABEZADO =================
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)

        header_frame.setStyleSheet("""
            QFrame {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:0,
                    stop:0 #9c724a, stop:1 #bf8f62
                );
                border-radius: 12px;
            }
            QLabel {
                color: #2d1f15;
            }
        """)

        titulo = QLabel("Ciencias de la Computación II - Múltiples Residuos")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        nav_layout = QHBoxLayout()
        btn_inicio = QPushButton("Inicio")
        btn_volver = QPushButton("Menú Búsqueda")
        for btn in (btn_inicio, btn_volver):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2d1f15;
                    font-size: 14px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    color: #FFEAC5;
                    background-color: #6C4E31;
                    border-radius: 8px;
                }
            """)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_volver.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        nav_layout.addStretch()
        nav_layout.addWidget(btn_inicio)
        nav_layout.addWidget(btn_volver)
        nav_layout.addStretch()

        header_layout.addWidget(titulo)
        header_layout.addLayout(nav_layout)

        main_layout.addWidget(header_frame)

        # ================= CUERPO PRINCIPAL =================
        body_layout = QHBoxLayout()

        # --- IZQUIERDA: Grafo ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(self.view.renderHints())
        self.view.setStyleSheet("background-color: #FFF3E0; border-radius: 8px;")

        self.view.resetTransform()
        self.view.scale(1.5, 1.5)
        body_layout.addWidget(self.view, stretch=2)

        # --- DERECHA: Controles ---
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #FFDBB5;
                border-radius: 12px;
            }
        """)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(15)
        controls_layout.setAlignment(Qt.AlignTop)

        # === INSERTAR ===
        lbl_insertar = QLabel("Insertar Palabra:")
        lbl_insertar.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")

        self.input_insertar = QLineEdit()
        self.input_insertar.setPlaceholderText("Ingrese palabra (A-Z)")
        self.input_insertar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bf8f62;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                color: #2d1f15;
            }
        """)

        btn_insertar = QPushButton("Insertar")
        btn_insertar.clicked.connect(self.insertar_palabra)

        # === BUSCAR ===
        lbl_buscar = QLabel("Buscar Letra:")
        lbl_buscar.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Ingrese letra (A-Z)")
        self.input_buscar.setMaxLength(1)
        self.input_buscar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bf8f62;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                color: #2d1f15;
            }
        """)

        btn_buscar = QPushButton("Buscar")
        btn_buscar.clicked.connect(self.buscar_letra)

        # === ELIMINAR ===
        lbl_eliminar = QLabel("Eliminar Letra:")
        lbl_eliminar.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")

        self.input_eliminar = QLineEdit()
        self.input_eliminar.setPlaceholderText("Ingrese letra (A-Z)")
        self.input_eliminar.setMaxLength(1)
        self.input_eliminar.setStyleSheet("""
            QLineEdit {
                border: 2px solid #bf8f62;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                color: #2d1f15;
            }
        """)

        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.eliminar_letra)

        # === LIMPIAR ===
        btn_limpiar = QPushButton("Limpiar Trie")
        btn_limpiar.clicked.connect(self.limpiar_trie)

        # Estilos para botones
        for btn in (btn_insertar, btn_buscar, btn_eliminar, btn_limpiar):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6C4E31;
                    color: #FFEAC5;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 10px 14px;
                }
                QPushButton:hover {
                    background-color: #9c724a;
                }
            """)

        # Agregar widgets al layout
        controls_layout.addWidget(lbl_insertar)
        controls_layout.addWidget(self.input_insertar)
        controls_layout.addWidget(btn_insertar)

        controls_layout.addSpacing(10)
        controls_layout.addWidget(lbl_buscar)
        controls_layout.addWidget(self.input_buscar)
        controls_layout.addWidget(btn_buscar)

        controls_layout.addSpacing(10)
        controls_layout.addWidget(lbl_eliminar)
        controls_layout.addWidget(self.input_eliminar)
        controls_layout.addWidget(btn_eliminar)

        controls_layout.addSpacing(15)
        controls_layout.addWidget(btn_limpiar)

        body_layout.addWidget(controls_frame, stretch=1)

        main_layout.addLayout(body_layout)

        self.setCentralWidget(central)

    # ================= MÉTODOS =================
    def insertar_palabra(self):
        palabra = self.input_insertar.text().strip()
        if palabra:
            try:
                self.controller.insertar(palabra)
                self.input_insertar.clear()
                self.nodo_resaltado = None
                self.dibujar_trie()

                # Mostrar mensaje de éxito con DialogoClave
                msg_dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    mensaje=f"Palabra '{palabra}' insertada correctamente.",
                    parent=self
                )
                msg_dialogo.exec()
            except ValueError as e:
                msg_dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    mensaje=str(e),
                    parent=self
                )
                msg_dialogo.exec()
        else:
            msg_dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                mensaje="Debe ingresar una palabra para insertar.",
                parent=self
            )
            msg_dialogo.exec()

    def buscar_letra(self):
        letra = self.input_buscar.text().strip().upper()
        if letra:
            try:
                encontrada, posicion, nodo = self.controller.buscar(letra)
                if encontrada:
                    self.nodo_resaltado = letra
                    self.dibujar_trie()
                    mensaje = (
                        f"✓ La letra '{letra}' SÍ está en el Trie.\n\n"
                        f"Posición (secuencia de bits): {posicion}\n"
                        f"Código binario completo: {self.controller.codigos[letra]}"
                    )
                else:
                    self.nodo_resaltado = None
                    self.dibujar_trie()
                    mensaje = f"✗ La letra '{letra}' NO está en el Trie."

                self.input_buscar.clear()
                msg_dialogo = DialogoClave(
                    longitud=0,
                    titulo="Resultado de Búsqueda",
                    modo="mensaje",
                    mensaje=mensaje,
                    parent=self
                )
                msg_dialogo.exec()
            except Exception as e:
                msg_dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    mensaje=str(e),
                    parent=self
                )
                msg_dialogo.exec()
        else:
            msg_dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                mensaje="Debe ingresar una letra para buscar.",
                parent=self
            )
            msg_dialogo.exec()

    def eliminar_letra(self):
        letra = self.input_eliminar.text().strip().upper()
        if letra:
            try:
                self.controller.eliminar(letra)
                self.input_eliminar.clear()
                self.nodo_resaltado = None
                self.dibujar_trie()

                msg_dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    mensaje=f"Letra '{letra}' eliminada. Árbol reconstruido.",
                    parent=self
                )
                msg_dialogo.exec()
            except ValueError as e:
                msg_dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    mensaje=str(e),
                    parent=self
                )
                msg_dialogo.exec()
        else:
            msg_dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                mensaje="Debe ingresar una letra para eliminar.",
                parent=self
            )
            msg_dialogo.exec()

    def limpiar_trie(self):
        """Reinicia el trie"""
        # Usar diálogo de confirmación
        dialogo = DialogoClave(
            longitud=0,
            titulo="Confirmar",
            modo="confirmar",
            mensaje="¿Está seguro de que desea limpiar el Trie completo?",
            parent=self
        )

        if dialogo.exec():
            self.controller = MultiplesResiduosController()
            self.nodo_resaltado = None
            self.scene.clear()

            # Resetear completamente la vista
            self.view.resetTransform()
            self.view.scale(1.5, 1.5)

            # Dibujar solo el nodo raíz vacío
            node_radius = 26
            brush_root = QBrush(QColor("#9c724a"))
            pen_node = QPen(QColor("#2d1f15"), 2)

            circle = QGraphicsEllipseItem(-node_radius, -node_radius, 2 * node_radius, 2 * node_radius)
            circle.setBrush(brush_root)
            circle.setPen(pen_node)
            self.scene.addItem(circle)

            text_item = QGraphicsTextItem("root")
            text_item.setDefaultTextColor(QColor("#FFEAC5"))
            text_item.setScale(1.1)
            text_rect = text_item.boundingRect()
            text_item.setPos(-text_rect.width() / 2, -text_rect.height() / 2)
            self.scene.addItem(text_item)

            # Ajustar vista
            brect = self.scene.itemsBoundingRect()
            margin = 80
            brect.adjust(-margin, -margin, margin, margin)
            self.view.setSceneRect(brect)
            self.view.centerOn(0, 0)

            msg_dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                mensaje="Trie limpiado correctamente.",
                parent=self
            )
            msg_dialogo.exec()

    def dibujar_trie(self):
        self.scene.clear()
        root = self.controller.root

        # Parámetros visuales
        level_gap = 120
        node_radius = 26
        horizontal_gap = 70  # espacio base entre nodos hermanos

        pen_line = QPen(QColor("#6C4E31"), 2)
        brush_root = QBrush(QColor("#9c724a"))
        brush_internal = QBrush(QColor("#bf8f62"))
        brush_leaf = QBrush(QColor("#6C4E31"))
        pen_node = QPen(QColor("#2d1f15"), 2)
        edge_color = QColor("#6C4E31")

        def calcular_ancho(node):
            """Devuelve el ancho total (en px) que ocupa el subárbol."""
            if not node.children:
                return horizontal_gap
            total = 0
            for child in node.children.values():
                total += calcular_ancho(child)
            return total

        def draw(node, x, y, is_root=False):
            """Dibuja recursivamente cada nodo del trie."""
            circle = QGraphicsEllipseItem(x - node_radius, y - node_radius, 2 * node_radius, 2 * node_radius)

            # Color según tipo
            if is_root:
                circle.setBrush(brush_root)
            elif node.letra:
                circle.setBrush(brush_leaf)
            else:
                circle.setBrush(brush_internal)

            circle.setPen(pen_node)
            self.scene.addItem(circle)

            # Texto centrado
            text = "root" if is_root else (node.letra.upper() if node.letra else "*")
            text_item = QGraphicsTextItem(text)
            text_item.setDefaultTextColor(QColor("#FFEAC5"))
            text_item.setScale(1.1)
            text_rect = text_item.boundingRect()
            text_item.setPos(x - text_rect.width() / 2, y - text_rect.height() / 2)
            self.scene.addItem(text_item)

            # Dibujar hijos
            children = list(node.children.items())
            if not children:
                return

            total_width = sum(calcular_ancho(child) for _, child in children)
            start_x = x - total_width / 2
            for key, child in children:
                ancho_child = calcular_ancho(child)
                child_x = start_x + ancho_child / 2
                child_y = y + level_gap

                # Línea padre-hijo
                self.scene.addLine(x, y + node_radius, child_x, child_y - node_radius, pen_line)

                # Etiqueta de arista
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 14
                label = QGraphicsTextItem(key)
                label.setDefaultTextColor(edge_color)
                label.setScale(0.9)
                label.setPos(mid_x - 8, mid_y)
                self.scene.addItem(label)

                draw(child, child_x, child_y)
                start_x += ancho_child

        draw(root, 0, 0, is_root=True)

        # Ajuste de vista
        brect = self.scene.itemsBoundingRect()
        margin = 80
        brect.adjust(-margin, -margin, margin, margin)
        self.view.setSceneRect(brect)
        self.view.fitInView(brect, Qt.KeepAspectRatio)
        self.view.scale(1.1, 1.1)