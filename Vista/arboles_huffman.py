from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QPushButton, QLineEdit, QMessageBox,
    QGraphicsScene, QGraphicsView, QGraphicsEllipseItem, QGraphicsTextItem,
    QHBoxLayout, QTextEdit
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen, QBrush, QColor
from Controlador.Internas.ArbolesHuffmanController import ArbolesHuffmanController
from Vista.dialogo_clave import DialogoClave
from fractions import Fraction


class ArbolesHuffman(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = ArbolesHuffmanController()

        self.setWindowTitle("Ciencias de la Computación II - Árboles de Huffman")
        self.resize(1100, 700)

        # --- Widget central con layout vertical (encabezado arriba, resto abajo)
        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        main_layout = QVBoxLayout(central)

        # ================= ENCABEZADO (ARRIBA) =================
        header_frame = QFrame()
        header_layout = QVBoxLayout(header_frame)
        header_layout.setContentsMargins(10, 10, 10, 10)

        # Fondo degradado y bordes redondeados
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

        # Título grande
        titulo = QLabel("Ciencias de la Computación II - Árboles de Huffman")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 22px; font-weight: bold;")

        # Menú de navegación centrado abajo
        nav_layout = QHBoxLayout()
        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")
        for btn in (btn_inicio, btn_busqueda):
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
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        nav_layout.addStretch()
        nav_layout.addWidget(btn_inicio)
        nav_layout.addWidget(btn_busqueda)
        nav_layout.addStretch()

        # Armado del encabezado
        header_layout.addWidget(titulo)
        header_layout.addLayout(nav_layout)

        main_layout.addWidget(header_frame)

        # ================= CUERPO (Árbol + Controles) =================
        body_layout = QHBoxLayout()

        # --- Panel izquierdo: Árbol ---
        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHints(self.view.renderHints())
        self.view.setStyleSheet("background-color: #FFF3E0; border-radius: 8px;")
        body_layout.addWidget(self.view, stretch=2)

        # --- Panel derecho: Controles ---
        controls_frame = QFrame()
        controls_frame.setStyleSheet("""
            QFrame {
                background-color: #FFDBB5;
                border-radius: 12px;
            }
        """)
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setSpacing(20)
        controls_layout.setAlignment(Qt.AlignTop)

        # Insertar texto
        lbl_insertar = QLabel("Insertar Texto:")
        lbl_insertar.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")
        self.input_insertar = QTextEdit()
        self.input_insertar.setPlaceholderText("Ingrese el texto a comprimir")
        self.input_insertar.setMaximumHeight(100)
        self.input_insertar.setStyleSheet("""
            QTextEdit {
                border: 2px solid #bf8f62;
                border-radius: 6px;
                padding: 5px;
                background-color: white;
                color: #2d1f15;
            }
        """)

        # Botón insertar
        btn_insertar = QPushButton("Generar Árbol de Huffman")
        btn_insertar.clicked.connect(self.generar_arbol)

        # === BUSCAR LETRA ===
        lbl_buscar = QLabel("Buscar Letra:")
        lbl_buscar.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")

        self.input_buscar = QLineEdit()
        self.input_buscar.setPlaceholderText("Ingrese letra a buscar")
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

        btn_buscar = QPushButton("Buscar Letra")
        btn_buscar.clicked.connect(self.buscar_letra)

        # === ELIMINAR LETRA ===
        lbl_eliminar = QLabel("Eliminar Letra:")
        lbl_eliminar.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")

        self.input_eliminar = QLineEdit()
        self.input_eliminar.setPlaceholderText("Ingrese letra a eliminar")
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

        btn_eliminar = QPushButton("Eliminar Letra")
        btn_eliminar.clicked.connect(self.eliminar_letra)

        # Botón limpiar
        btn_limpiar = QPushButton("Limpiar Todo")
        btn_limpiar.clicked.connect(self.limpiar_todo)

        # Estilos botones café
        for btn in (btn_insertar, btn_buscar, btn_eliminar, btn_limpiar):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #6C4E31;
                    color: #FFEAC5;
                    font-size: 14px;
                    font-weight: bold;
                    border-radius: 8px;
                    padding: 8px 14px;
                }
                QPushButton:hover {
                    background-color: #9c724a;
                }
            """)

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

        controls_layout.addSpacing(10)
        controls_layout.addWidget(btn_limpiar)

        # ================= TABLA DE FRECUENCIAS Y CÓDIGOS =================
        lbl_tabla = QLabel("Frecuencias y Códigos:")
        lbl_tabla.setStyleSheet("font-size: 14px; color: #2d1f15; font-weight: bold;")

        self.tabla_codigos = QTextEdit()
        self.tabla_codigos.setReadOnly(True)
        self.tabla_codigos.setMaximumHeight(200)
        self.tabla_codigos.setStyleSheet("""
            QTextEdit {
                font-family: Consolas, monospace;
                font-size: 12px;
                background-color: #FFF3E0;
                border: 1px solid #bf8f62;
                border-radius: 8px;
                padding: 6px;
                color: #2d1f15;
            }
        """)

        controls_layout.addWidget(lbl_tabla)
        controls_layout.addWidget(self.tabla_codigos)

        body_layout.addWidget(controls_frame, stretch=1)

        # Agregar el cuerpo al layout principal
        main_layout.addLayout(body_layout)

        self.setCentralWidget(central)

        # Variable para resaltar nodo buscado
        self.nodo_resaltado = None

    # --- Lógica ---
    def generar_arbol(self):
        texto = self.input_insertar.toPlainText().strip()
        if texto:
            try:
                self.controller.construir_arbol(texto)
                self.input_insertar.setReadOnly(True)
                self.input_insertar.setStyleSheet("""
                    QTextEdit {
                        background-color: #FFDBB5;
                        color: #2d1f15;
                        font-weight: bold;
                        border: 2px solid #bf8f62;
                        border-radius: 6px;
                        padding: 5px;
                    }
                """)
                self.nodo_resaltado = None
                self.dibujar_arbol()
                self.mostrar_tabla_codigos()

                # Usar DialogoClave para mensaje de éxito
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    mensaje="Árbol de Huffman generado correctamente.",
                    parent=self
                )
                dialogo.exec()
            except Exception as e:
                # Usar DialogoClave para mensaje de error
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    mensaje=f"Error al generar el árbol: {str(e)}",
                    parent=self
                )
                dialogo.exec()
        else:
            # Usar DialogoClave para advertencia
            dialogo = DialogoClave(
                longitud=0,
                titulo="Advertencia",
                modo="mensaje",
                mensaje="Debe ingresar un texto para generar el árbol.",
                parent=self
            )
            dialogo.exec()

    def buscar_letra(self):
        """Busca una letra en el árbol de Huffman y muestra su código."""
        letra = self.input_buscar.text().strip()

        if not letra:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Advertencia",
                modo="mensaje",
                mensaje="Debe ingresar una letra para buscar.",
                parent=self
            )
            dialogo.exec()
            return

        if not self.controller.root:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Advertencia",
                modo="mensaje",
                mensaje="Primero debe generar un árbol de Huffman.",
                parent=self
            )
            dialogo.exec()
            return

        try:
            codigos = self.controller.obtener_codigos()
            frecuencias = self.controller.obtener_frecuencias()

            if letra in codigos:
                codigo = codigos[letra]
                frecuencia = frecuencias.get(letra, 0)

                # Resaltar el nodo en el árbol
                self.nodo_resaltado = letra
                self.dibujar_arbol()

                char_display = letra if letra != ' ' else '[espacio]'
                mensaje = (
                    f"✓ Letra '{char_display}' encontrada en el árbol.\n\n"
                    f"Código Huffman: {codigo}\n"
                    f"Frecuencia: {frecuencia}\n"
                    f"Longitud del código: {len(codigo)} bits"
                )

                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Búsqueda Exitosa",
                    modo="mensaje",
                    mensaje=mensaje,
                    parent=self
                )
                dialogo.exec()
            else:
                self.nodo_resaltado = None
                self.dibujar_arbol()

                dialogo = DialogoClave(
                    longitud=0,
                    titulo="No Encontrada",
                    modo="mensaje",
                    mensaje=f"✗ La letra '{letra}' no existe en el árbol de Huffman.",
                    parent=self
                )
                dialogo.exec()

            self.input_buscar.clear()

        except Exception as e:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                mensaje=f"Error al buscar la letra: {str(e)}",
                parent=self
            )
            dialogo.exec()

    def eliminar_letra(self):
        """Elimina una letra del texto y regenera el árbol de Huffman."""
        letra = self.input_eliminar.text().strip()

        if not letra:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Advertencia",
                modo="mensaje",
                mensaje="Debe ingresar una letra para eliminar.",
                parent=self
            )
            dialogo.exec()
            return

        if not self.controller.root:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Advertencia",
                modo="mensaje",
                mensaje="Primero debe generar un árbol de Huffman.",
                parent=self
            )
            dialogo.exec()
            return

        try:
            frecuencias = self.controller.obtener_frecuencias()

            if letra not in frecuencias:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="No Encontrada",
                    modo="mensaje",
                    mensaje=f"La letra '{letra}' no existe en el árbol actual.",
                    parent=self
                )
                dialogo.exec()
                return

            # Confirmación antes de eliminar
            char_display = letra if letra != ' ' else '[espacio]'
            dialogo_confirmar = DialogoClave(
                longitud=0,
                titulo="Confirmar Eliminación",
                modo="confirmar",
                mensaje=f"¿Está seguro de eliminar la letra '{char_display}'?\nSe regenerará el árbol sin esta letra.",
                parent=self
            )

            if dialogo_confirmar.exec() == DialogoClave.Rejected:
                return

            # Obtener el texto actual y eliminar la letra
            texto_actual = self.input_insertar.toPlainText()
            texto_nuevo = texto_actual.replace(letra, '')

            if not texto_nuevo.strip():
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    mensaje="No se puede eliminar la letra porque quedaría un texto vacío.",
                    parent=self
                )
                dialogo.exec()
                return

            # Actualizar el texto y regenerar el árbol
            self.input_insertar.clear()
            self.input_insertar.setPlainText(texto_nuevo)
            self.input_insertar.setReadOnly(False)
            self.input_insertar.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #bf8f62;
                    border-radius: 6px;
                    padding: 5px;
                    background-color: white;
                    color: #2d1f15;
                }
            """)

            # Reconstruir el árbol
            self.controller.construir_arbol(texto_nuevo)
            self.input_insertar.setReadOnly(True)
            self.input_insertar.setStyleSheet("""
                QTextEdit {
                    background-color: #FFDBB5;
                    color: #2d1f15;
                    font-weight: bold;
                    border: 2px solid #bf8f62;
                    border-radius: 6px;
                    padding: 5px;
                }
            """)

            self.nodo_resaltado = None
            self.dibujar_arbol()
            self.mostrar_tabla_codigos()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Eliminación Exitosa",
                modo="mensaje",
                mensaje=f"Letra '{char_display}' eliminada correctamente.\nÁrbol regenerado.",
                parent=self
            )
            dialogo.exec()

            self.input_eliminar.clear()

        except Exception as e:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                mensaje=f"Error al eliminar la letra: {str(e)}",
                parent=self
            )
            dialogo.exec()

    def dibujar_arbol(self):
        """Dibuja el árbol de Huffman en la escena."""
        self.scene.clear()
        self.view.setScene(self.scene)
        root = self.controller.root

        if not root:
            text_item = QGraphicsTextItem("Árbol vacío")
            text_item.setDefaultTextColor(QColor("#6C4E31"))
            text_item.setScale(1.5)
            text_item.setPos(-60, -20)
            self.scene.addItem(text_item)
            self.view.setSceneRect(self.scene.itemsBoundingRect())
            return

        level_gap = 90
        start_offset = 280

        pen_line = QPen(QColor("#6C4E31"), 2)
        brush_node = QBrush(QColor("#6C4E31"))
        brush_leaf = QBrush(QColor("#bf8f62"))
        text_color = QColor("#FFEAC5")

        def draw(node, x, y, offset, depth):
            radio = 22
            circle = QGraphicsEllipseItem(x - radio, y - radio, 2 * radio, 2 * radio)

            # Si es hoja (tiene carácter), usar color diferente
            # Resaltar si es el nodo buscado
            if node.char is not None:
                if node.char == self.nodo_resaltado:
                    # Color especial para nodo resaltado
                    circle.setBrush(QBrush(QColor("#82531a")))  # Dorado
                    circle.setPen(QPen(QColor("#82531a"), 3))  # Borde naranja grueso
                else:
                    circle.setBrush(brush_leaf)
            else:
                circle.setBrush(brush_node)

            if node.char != self.nodo_resaltado:
                circle.setPen(QPen(QColor("#2d1f15"), 2))

            self.scene.addItem(circle)

            # Texto del nodo (carácter y frecuencia)
            try:
                freq_frac = str(Fraction(node.freq).limit_denominator())
            except Exception:
                freq_frac = str(node.freq)

            # Mostrar fracción y carácter (si lo tiene)
            if node.char is not None:
                txt = f"{node.char}\n{freq_frac}"
            else:
                # Si es raíz, mostrar '1' si la suma total es 1.0
                if abs(node.freq - 1.0) < 1e-6:
                    txt = "1"
                else:
                    txt = freq_frac

            text_item = QGraphicsTextItem(txt)
            # Cambiar color del texto si es el nodo resaltado
            if node.char == self.nodo_resaltado:
                text_item.setDefaultTextColor(QColor("#2d1f15"))  # Texto oscuro para contraste
            else:
                text_item.setDefaultTextColor(text_color)
            text_item.setPos(x - radio / 1.3, y - 8)
            self.scene.addItem(text_item)

            # Dibujar hijo izquierdo (0)
            if node.left:
                child_x = x - offset
                child_y = y + level_gap
                self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                # Etiqueta "0"
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 10
                bit_label = QGraphicsTextItem("0")
                bit_label.setDefaultTextColor(QColor("#6C4E31"))
                bit_label.setPos(mid_x, mid_y)
                self.scene.addItem(bit_label)

                draw(node.left, child_x, child_y, max(40, offset / 2), depth + 1)

            # Dibujar hijo derecho (1)
            if node.right:
                child_x = x + offset
                child_y = y + level_gap
                self.scene.addLine(x, y + radio, child_x, child_y - radio, pen_line)

                # Etiqueta "1"
                mid_x = (x + child_x) / 2
                mid_y = (y + child_y) / 2 - 10
                bit_label = QGraphicsTextItem("1")
                bit_label.setDefaultTextColor(QColor("#6C4E31"))
                bit_label.setPos(mid_x, mid_y)
                self.scene.addItem(bit_label)

                draw(node.right, child_x, child_y, max(40, offset / 2), depth + 1)

        draw(root, 0, 0, start_offset, 1)
        self.view.setSceneRect(self.scene.itemsBoundingRect())

    def mostrar_tabla_codigos(self):
        """Muestra la tabla de frecuencias y códigos Huffman."""
        frecuencias = self.controller.obtener_frecuencias()
        codigos = self.controller.obtener_codigos()

        if not frecuencias or not codigos:
            self.tabla_codigos.setText("No hay datos para mostrar")
            return

        texto = "Carácter | Frecuencia | Código\n"
        texto += "-" * 40 + "\n"

        for char in frecuencias.keys():
            char_display = char if char != ' ' else '[espacio]'
            freq = frecuencias[char]
            codigo = codigos.get(char, "N/A")
            texto += f"   {char_display:^8} | {freq:^10} | {codigo}\n"

        self.tabla_codigos.setText(texto)

    def limpiar_todo(self):
        """Elimina completamente el árbol y reinicia los campos."""
        # Usar DialogoClave para confirmación
        dialogo = DialogoClave(
            longitud=0,
            titulo="Confirmar limpieza",
            modo="confirmar",
            mensaje="¿Seguro que deseas limpiar todo?\nEsta acción no se puede deshacer.",
            parent=self
        )

        if dialogo.exec() == DialogoClave.Rejected:
            return

        try:
            # Reiniciar estructura del árbol
            self.controller.limpiar()

            # Limpiar campo y desbloquearlo
            self.input_insertar.clear()
            self.input_insertar.setReadOnly(False)
            self.input_insertar.setStyleSheet("""
                QTextEdit {
                    border: 2px solid #bf8f62;
                    border-radius: 6px;
                    padding: 5px;
                    background-color: white;
                    color: #2d1f15;
                }
            """)

            # Limpiar tabla de códigos
            self.tabla_codigos.clear()

            # Resetear nodo resaltado
            self.nodo_resaltado = None

            # Limpiar escena del árbol
            self.scene.clear()

            # Mostrar mensaje visual
            text_item = QGraphicsTextItem("Árbol vacío")
            text_item.setDefaultTextColor(QColor("#6C4E31"))
            text_item.setScale(1.5)
            text_item.setPos(-60, -20)
            self.scene.addItem(text_item)
            self.view.setScene(self.scene)
            self.view.setSceneRect(self.scene.itemsBoundingRect())

            # Usar DialogoClave para mensaje de éxito
            dialogo = DialogoClave(
                longitud=0,
                titulo="Limpieza completada",
                modo="mensaje",
                mensaje="Se ha limpiado el árbol y puedes insertar nuevo texto.",
                parent=self
            )
            dialogo.exec()

        except Exception as e:
            # Usar DialogoClave para mensaje de error
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                mensaje=f"Ocurrió un problema al limpiar: {str(e)}",
                parent=self
            )
            dialogo.exec()