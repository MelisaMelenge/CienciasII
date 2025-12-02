import math
from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QLineEdit, QTableWidget, QTableWidgetItem,
    QScrollArea, QGroupBox, QMessageBox, QFrame
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPaintEvent


class IndiceCanvas(QWidget):
    """Canvas para dibujar estructuras de índices"""

    def __init__(self, parent: QWidget = None):
        super().__init__(parent)

        self.setMinimumHeight(500)
        self.setMinimumWidth(720)
        self.setStyleSheet("background-color: #FAF5EB;")  # Café muy claro

        # Variables para el dibujo de la gráfica
        self.resTabla = []
        self.activo = False
        self.Tipo = ""
        self.cantNivel = ""
        self.tamaBloque = 0
        self.cantRegistro = 0
        self.tamaRegistro = 0
        self.tamaRegistroIndice = 0
        self.cantIndices = 0
        self.cantEstructuras = 0

        self.regisXbloq = 0
        self.cantBloqRegis = 0
        self.indicXbloq = 0
        self.cantBloqIndic = 0

    def dibujarGrafico(self, T: str, cN: str, tB: int, cR: int, tR: int, tRI: int):
        """Dibuja el gráfico de índices con los parámetros dados"""
        self.setGeometry(0, 0, 720, 500)
        self.activo = True
        self.resTabla = []

        self.Tipo = T
        self.cantNivel = cN
        self.tamaBloque = tB
        self.cantRegistro = cR
        self.tamaRegistro = tR
        self.tamaRegistroIndice = tRI

        # Cálculos
        self.resTabla.append(["1", "Cant.registros", str(self.cantRegistro)])
        self.regisXbloq = self.tamaBloque // self.tamaRegistro
        self.resTabla.append(["1", "Reg. x Bloque", str(self.regisXbloq)])
        self.cantBloqRegis = math.ceil(self.cantRegistro / self.regisXbloq)
        self.resTabla.append(["1", "Bloques", str(self.cantBloqRegis)])
        self.indicXbloq = self.tamaBloque // self.tamaRegistroIndice

        if self.Tipo == "Primario":
            self.cantIndices = self.cantBloqRegis
            self.cantBloqIndic = math.ceil(self.cantBloqRegis / self.indicXbloq)
        elif self.Tipo == "Secundario":
            self.cantIndices = self.cantRegistro
            self.cantBloqIndic = math.ceil(self.cantRegistro / self.indicXbloq)

        self.resTabla.append(["2", "Cant. registros Indice", str(self.cantIndices)])
        self.resTabla.append(["2", "Ind x Bloque", str(self.indicXbloq)])
        self.resTabla.append(["2", "Cant. Bloques Indice", str(self.cantBloqIndic)])

        row = 2
        if self.cantNivel == "Multinivel":
            while self.cantBloqIndic != 1:
                row += 1
                self.cantBloqRegis = self.cantBloqIndic
                self.resTabla.append([str(row), "Cant. registros Indice", str(self.cantBloqRegis)])
                self.resTabla.append([str(row), "Ind x Bloque", str(self.indicXbloq)])
                self.cantBloqIndic = math.ceil(self.cantBloqRegis / self.indicXbloq)
                self.resTabla.append([str(row), "Cant. Bloques Indice", str(self.cantBloqIndic)])

        self.cantEstructuras = row
        self.update()
        return self.resTabla

    def paintEvent(self, event: QPaintEvent) -> None:
        """Dibuja las estructuras de índices"""
        super().paintEvent(event)

        painter = QPainter(self)
        # Fondo color café claro
        painter.fillRect(self.rect(), QColor(250, 245, 235))
        # Líneas color café oscuro
        painter.setPen(QPen(QColor(101, 67, 33), 3))

        if not self.activo:
            painter.end()
            return

        separacion = 100
        diffEstructura = 30
        borde = 50
        anchoCanvas = self.rect().width()
        altoCanvas = self.rect().height()

        if self.cantEstructuras <= 3:
            anchoEstructura = (anchoCanvas - (separacion * (self.cantEstructuras - 1)) - (
                        2 * borde)) // self.cantEstructuras
        else:
            anchoEstructura = 140
            self.resize(
                (borde * 2 + (self.cantEstructuras * anchoEstructura) + ((self.cantEstructuras - 1) * separacion)),
                altoCanvas)
            anchoCanvas = self.rect().width()

        # Estructura principal
        estX = anchoCanvas - borde - anchoEstructura
        estY = borde
        painter.drawText(estX + (anchoEstructura // 2) - 30, estY - 20, "Principal")
        painter.drawRect(estX, estY, anchoEstructura, altoCanvas - (2 * borde))

        # Borde superior
        painter.drawLine(estX, estY + 10, estX + anchoEstructura, estY + 10)
        painter.drawText(estX - 12, estY, "1")
        painter.drawText(estX + (anchoEstructura // 2) - 10, estY + 35, "B1")
        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.drawLine(estX, estY + 60, estX + anchoEstructura, estY + 60)
        painter.drawText(estX - ((len(str(self.resTabla[1][2])) * 6)) - 12, estY + 60, str(self.resTabla[1][2]))
        painter.setPen(QPen(QColor(0, 0, 0), 3))
        painter.drawLine(estX, estY + 50, estX + anchoEstructura, estY + 50)

        # Borde inferior
        painter.setPen(QPen(QColor(0, 0, 0), 5))
        painter.drawLine(estX, estY + (altoCanvas - (2 * borde)) - 60, estX + anchoEstructura,
                         estY + (altoCanvas - (2 * borde)) - 60)
        painter.drawText(estX - ((len(str(int(self.resTabla[0][2]) - int(self.resTabla[1][2]))) * 6)) - 12,
                         estY + (altoCanvas - (2 * borde)) - 60,
                         str(int(self.resTabla[0][2]) - int(self.resTabla[1][2])))
        painter.setPen(QPen(QColor(0, 0, 0), 3))
        painter.drawText(estX + (anchoEstructura // 2) - 10, estY + (altoCanvas - (2 * borde)) - 30,
                         "B" + self.resTabla[2][2])
        painter.drawLine(estX, estY + (altoCanvas - (2 * borde)) - 10, estX + anchoEstructura,
                         estY + (altoCanvas - (2 * borde)) - 10)
        painter.drawText(estX - ((len(str(self.resTabla[0][2])) * 6)) - 12, estY + (altoCanvas - (2 * borde)) - 10,
                         self.resTabla[0][2])

        # Estructura de índice primario
        if self.Tipo == "Primario":
            estX = anchoCanvas - borde - (2 * anchoEstructura) - separacion
            estY = borde + (diffEstructura // 2)
            painter.drawText(estX + (anchoEstructura // 2) - 30, estY - 20, "Est. Indice")
            painter.drawRect(estX, estY, anchoEstructura, altoCanvas - (2 * borde) - diffEstructura)

            painter.drawLine(estX, estY + 10, estX + anchoEstructura, estY + 10)
            painter.drawText(estX - 10, estY + 7, "1")
            painter.drawText(estX + (anchoEstructura // 2) - 10, estY + 35, "B1")

            if self.cantBloqIndic != 1 or self.cantEstructuras != 2:
                painter.setPen(QPen(QColor(0, 0, 0), 5))
                painter.drawLine(estX, estY + 60, estX + anchoEstructura, estY + 60)
                painter.drawText(estX - ((len(str(self.resTabla[4][2])) * 6)) - 12, estY + 60, str(self.resTabla[4][2]))
                painter.setPen(QPen(QColor(0, 0, 0), 3))
                painter.drawLine(estX, estY + 50, estX + anchoEstructura, estY + 50)

                painter.setPen(QPen(QColor(0, 0, 0), 5))
                painter.drawLine(estX, estY + (altoCanvas - (2 * borde) - diffEstructura) - 60, estX + anchoEstructura,
                                 estY + (altoCanvas - (2 * borde) - diffEstructura) - 60)
                painter.drawText(estX - ((len(str(int(self.resTabla[3][2]) - int(self.resTabla[4][2]))) * 6)) - 12,
                                 estY + (altoCanvas - (2 * borde) - diffEstructura) - 60,
                                 str(int(self.resTabla[3][2]) - int(self.resTabla[4][2])))
                painter.setPen(QPen(QColor(0, 0, 0), 3))
                painter.drawText(estX + (anchoEstructura // 2) - 10,
                                 estY + (altoCanvas - (2 * borde) - diffEstructura) - 30,
                                 "B" + self.resTabla[5][2])

            painter.drawLine(estX, estY + (altoCanvas - (2 * borde) - diffEstructura) - 10, estX + anchoEstructura,
                             estY + (altoCanvas - (2 * borde) - diffEstructura) - 10)
            painter.drawLine(estX + anchoEstructura, estY + 5, estX + anchoEstructura + separacion, estY + 15)
            painter.drawLine(estX + anchoEstructura, estY + (altoCanvas - (2 * borde) - diffEstructura) - 5,
                             estX + anchoEstructura + separacion,
                             estY + (altoCanvas - (2 * borde) - diffEstructura) - 15)
            painter.drawText(estX - ((len(str(self.resTabla[3][2])) * 6)) - 12,
                             estY + (altoCanvas - (2 * borde) - diffEstructura) - 3, self.resTabla[3][2])

        # Estructura de índice secundario
        elif self.Tipo == "Secundario":
            estX = anchoCanvas - borde - (2 * anchoEstructura) - separacion
            estY = borde

            painter.setPen(QPen(QColor(101, 67, 33), 2))
            painter.drawText(estX + (anchoEstructura // 2) - 30, estY - 20, "Est. Indice")

            painter.setBrush(QColor(245, 235, 220))
            painter.setPen(QPen(QColor(101, 67, 33), 3))
            painter.drawRect(estX, estY, anchoEstructura, altoCanvas - (2 * borde))
            painter.setBrush(Qt.NoBrush)

            painter.setPen(QPen(QColor(101, 67, 33), 2))
            painter.drawLine(estX, estY + 10, estX + anchoEstructura, estY + 10)
            painter.drawText(estX - 10, estY + 7, "1")
            painter.drawText(estX + (anchoEstructura // 2) - 10, estY + 35, "B1")

            if self.cantBloqIndic != 1 or self.cantEstructuras != 2:
                painter.setPen(QPen(QColor(139, 90, 43), 5))
                painter.drawLine(estX, estY + 60, estX + anchoEstructura, estY + 60)
                painter.drawText(estX - ((len(str(self.resTabla[4][2])) * 6)) - 12, estY + 60, str(self.resTabla[4][2]))
                painter.setPen(QPen(QColor(101, 67, 33), 2))
                painter.drawLine(estX, estY + 50, estX + anchoEstructura, estY + 50)

                painter.setPen(QPen(QColor(139, 90, 43), 5))
                painter.drawLine(estX, estY + (altoCanvas - (2 * borde)) - 60, estX + anchoEstructura,
                                 estY + (altoCanvas - (2 * borde)) - 60)
                painter.drawText(estX - ((len(str(int(self.resTabla[3][2]) - int(self.resTabla[4][2]))) * 6)) - 12,
                                 estY + (altoCanvas - (2 * borde)) - 60,
                                 str(int(self.resTabla[3][2]) - int(self.resTabla[4][2])))
                painter.setPen(QPen(QColor(101, 67, 33), 2))
                painter.drawText(estX + (anchoEstructura // 2) - 10, estY + (altoCanvas - (2 * borde)) - 30,
                                 "B" + self.resTabla[5][2])

            painter.drawLine(estX, estY + (altoCanvas - (2 * borde)) - 10, estX + anchoEstructura,
                             estY + (altoCanvas - (2 * borde)) - 10)

            # Líneas de conexión en café
            painter.setPen(QPen(QColor(139, 90, 43), 3))
            painter.drawLine(estX + anchoEstructura, estY + 5, estX + anchoEstructura + separacion, estY + 5)
            painter.drawLine(estX + anchoEstructura, estY + (altoCanvas - (2 * borde)) - 5,
                             estX + anchoEstructura + separacion, estY + (altoCanvas - (2 * borde)) - 5)
            painter.setPen(QPen(QColor(101, 67, 33), 2))
            painter.drawText(estX - ((len(str(self.resTabla[3][2])) * 6)) - 12,
                             estY + (altoCanvas - (2 * borde)) - 3, self.resTabla[3][2])

        # Estructuras índices multinivel
        if self.cantNivel == "Multinivel":
            row = 3
            for i in range(2, self.cantEstructuras):
                estX = anchoCanvas - borde - (row * anchoEstructura) - ((row - 1) * separacion)
                estY = borde + (((row - 1) * diffEstructura) // 2) if altoCanvas - (2 * borde) - (
                            (row - 1) * diffEstructura) > 160 else 170
                altura = altoCanvas - (2 * borde) - ((row - 1) * diffEstructura) if altoCanvas - (2 * borde) - (
                            (row - 1) * diffEstructura) > 160 else 160
                inclinacion = 15 if altoCanvas - (2 * borde) - ((row - 1) * diffEstructura) > 160 else 25

                painter.drawText(estX + (anchoEstructura // 2) - 40, estY - 20, "Est. Indice " + str(row - 1))
                painter.drawRect(estX, estY, anchoEstructura, altura)

                painter.drawLine(estX, estY + 10, estX + anchoEstructura, estY + 10)
                painter.drawText(estX - 15, estY + 7, "1")
                painter.drawText(estX + (anchoEstructura // 2) - 10, estY + 35, "B1")

                if row != self.cantEstructuras:
                    painter.setPen(QPen(QColor(0, 0, 0), 5))
                    painter.drawLine(estX, estY + 60, estX + anchoEstructura, estY + 60)
                    painter.drawText(estX - ((len(str(self.resTabla[(3 * row) - 2][2])) * 6)) - 12, estY + 60,
                                     str(self.resTabla[(3 * row) - 2][2]))
                    painter.setPen(QPen(QColor(0, 0, 0), 3))
                    painter.drawLine(estX, estY + 50, estX + anchoEstructura, estY + 50)

                    painter.setPen(QPen(QColor(0, 0, 0), 5))
                    painter.drawLine(estX, estY + altura - 60, estX + anchoEstructura, estY + altura - 60)
                    dato = int(self.resTabla[(3 * row) - 3][2]) - int(self.resTabla[(3 * row) - 2][2])
                    dato = dato if dato >= int(self.resTabla[(3 * row) - 2][2]) else int(
                        self.resTabla[(3 * row) - 2][2]) + 1
                    painter.drawText(estX - ((len(str(dato)) * 6)) - 12, estY + altura - 60, str(dato))
                    painter.setPen(QPen(QColor(0, 0, 0), 3))
                    painter.drawText(estX + (anchoEstructura // 2) - 10, estY + altura - 30,
                                     "B" + self.resTabla[(3 * row) - 1][2])

                painter.drawLine(estX, estY + altura - 10, estX + anchoEstructura, estY + altura - 10)
                painter.drawLine(estX + anchoEstructura, estY + 5, estX + anchoEstructura + separacion,
                                 estY + inclinacion)
                painter.drawLine(estX + anchoEstructura, estY + altura - 5, estX + anchoEstructura + separacion,
                                 estY + altura - inclinacion)
                painter.drawText(estX - ((len(str(self.resTabla[(3 * row) - 3][2])) * 6)) - 12, estY + altura - 3,
                                 self.resTabla[(3 * row) - 3][2])
                row += 1

        painter.end()


class Indices(QWidget):
    """Vista de índices - Se integra con tu MainWindow existente"""

    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setStyleSheet("background-color: #FFEAC5;")

        # Layout principal
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62
            );
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Ciencias de la Computación II - Índices")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2d1f15; margin: 10px;")
        header_layout.addWidget(titulo)

        # --- Menú de navegación ---
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)
        menu_layout.setAlignment(Qt.AlignCenter)

        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")

        for btn in (btn_inicio, btn_busqueda):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2d1f15;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                    padding: 8px 16px;
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
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        main_layout.addWidget(header)

        # --- Contenedor del contenido ---
        content_widget = QWidget()
        content_widget.setStyleSheet("background-color: #DECCA6;")
        content_layout = QVBoxLayout(content_widget)
        content_layout.setContentsMargins(20, 20, 20, 20)
        content_layout.setSpacing(10)

        # Layout horizontal para canvas y tabla
        content_layout_hz = QHBoxLayout()

        # Canvas con scroll
        self.canvas = IndiceCanvas()
        self.canvas.setGeometry(0, 0, 720, 500)

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidget(self.canvas)
        self.scroll_area.setMinimumSize(722, 502)
        self.scroll_area.setMaximumHeight(502)
        self.scroll_area.verticalScrollBar().setVisible(False)
        self.scroll_area.verticalScrollBar().setEnabled(False)
        self.scroll_area.setStyleSheet("background-color: #FAF5EB; border: 2px solid #8B5A2B;")
        self.scroll_area.setFrameStyle(1)
        content_layout_hz.addWidget(self.scroll_area)

        # Tabla de resultados
        self.tabla = QTableWidget()
        self.tabla.setColumnCount(3)
        self.tabla.verticalHeader().setVisible(False)
        self.tabla.setHorizontalHeaderLabels(["N. Est", "Variable", "Valor"])
        self.tabla.setMinimumSize(290, 500)
        self.tabla.setMaximumSize(290, 500)
        self.tabla.setFont(QFont("Arial", 8))
        self.tabla.horizontalScrollBar().setVisible(False)
        self.tabla.setColumnWidth(0, 40)
        self.tabla.setColumnWidth(1, 140)
        self.tabla.setColumnWidth(2, 100)
        self.tabla.setStyleSheet("""
            QTableWidget {
                border: 2px solid #8B5A2B; 
                background-color: #FAF5EB;
                color: #2d1f15;
                gridline-color: #C19A6B;
            }
            QHeaderView::section {
                background-color: #C19A6B;
                color: #2d1f15;
                font-weight: bold;
                border: 1px solid #8B5A2B;
                padding: 4px;
            }
            QTableWidget::item {
                border-bottom: 1px solid #D4C4A8;
                padding: 3px;
            }
            QTableWidget::item:selected {
                background-color: #D4C4A8;
                color: #2d1f15;
            }
        """)
        content_layout_hz.addWidget(self.tabla)

        content_layout.addLayout(content_layout_hz)

        # Panel de controles
        controls_widget = QWidget()
        controls_widget.setStyleSheet("background-color: #DECCA6;")
        controls_layout = QVBoxLayout(controls_widget)
        controls_layout.setSpacing(15)

        # Primera fila de controles
        row1 = QHBoxLayout()
        row1.setSpacing(20)

        # Tipo de índice
        tipo_layout = QHBoxLayout()
        label_tipo = QLabel("Tipo de Índice:")
        label_tipo.setFont(QFont("Arial", 10, QFont.Bold))
        label_tipo.setStyleSheet("color: #2d1f15;")
        self.opcionTipoIndice = QComboBox()
        self.opcionTipoIndice.addItems(["Primario", "Secundario"])
        self.opcionTipoIndice.setMinimumWidth(140)
        self.opcionTipoIndice.setFont(QFont("Arial", 10))
        self.opcionTipoIndice.setStyleSheet("""
            QComboBox {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                border-radius: 4px;
                padding: 5px;
                color: #2d1f15;
            }
            QComboBox:hover {
                border: 2px solid #654321;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                selection-background-color: #C19A6B;
                color: #2d1f15;
            }
        """)
        tipo_layout.addWidget(label_tipo)
        tipo_layout.addWidget(self.opcionTipoIndice)
        row1.addLayout(tipo_layout)

        # Cantidad de niveles
        nivel_layout = QHBoxLayout()
        label_nivel = QLabel("Cantidad de Niveles:")
        label_nivel.setFont(QFont("Arial", 10, QFont.Bold))
        label_nivel.setStyleSheet("color: #2d1f15;")
        self.opcionNiveles = QComboBox()
        self.opcionNiveles.addItems(["Un Nivel", "Multinivel"])
        self.opcionNiveles.setMinimumWidth(140)
        self.opcionNiveles.setFont(QFont("Arial", 10))
        self.opcionNiveles.setStyleSheet("""
            QComboBox {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                border-radius: 4px;
                padding: 5px;
                color: #2d1f15;
            }
            QComboBox:hover {
                border: 2px solid #654321;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox QAbstractItemView {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                selection-background-color: #C19A6B;
                color: #2d1f15;
            }
        """)
        nivel_layout.addWidget(label_nivel)
        nivel_layout.addWidget(self.opcionNiveles)
        row1.addLayout(nivel_layout)

        # Tamaño de bloque
        tambloque_layout = QHBoxLayout()
        label_tambloque = QLabel("Tamaño Bloque (b):")
        label_tambloque.setFont(QFont("Arial", 10, QFont.Bold))
        label_tambloque.setStyleSheet("color: #2d1f15;")
        self.campoTamBloque = QLineEdit("1024")
        self.campoTamBloque.setMinimumWidth(140)
        self.campoTamBloque.setFont(QFont("Arial", 10))
        self.campoTamBloque.setStyleSheet("""
            QLineEdit {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                border-radius: 4px;
                padding: 5px;
                color: #2d1f15;
            }
            QLineEdit:focus {
                border: 2px solid #654321;
            }
        """)
        tambloque_layout.addWidget(label_tambloque)
        tambloque_layout.addWidget(self.campoTamBloque)
        row1.addLayout(tambloque_layout)

        controls_layout.addLayout(row1)

        # Segunda fila de controles
        row2 = QHBoxLayout()
        row2.setSpacing(20)

        # Cantidad de registros
        cantreg_layout = QHBoxLayout()
        label_cantreg = QLabel("Cant. Registros:")
        label_cantreg.setFont(QFont("Arial", 10, QFont.Bold))
        label_cantreg.setStyleSheet("color: #2d1f15;")
        self.campoCantReg = QLineEdit("700000")
        self.campoCantReg.setMinimumWidth(140)
        self.campoCantReg.setFont(QFont("Arial", 10))
        self.campoCantReg.setStyleSheet("""
            QLineEdit {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                border-radius: 4px;
                padding: 5px;
                color: #2d1f15;
            }
            QLineEdit:focus {
                border: 2px solid #654321;
            }
        """)
        cantreg_layout.addWidget(label_cantreg)
        cantreg_layout.addWidget(self.campoCantReg)
        row2.addLayout(cantreg_layout)

        # Tamaño de registro
        tamreg_layout = QHBoxLayout()
        label_tamreg = QLabel("Tamaño Registro (b):")
        label_tamreg.setFont(QFont("Arial", 10, QFont.Bold))
        label_tamreg.setStyleSheet("color: #2d1f15;")
        self.campoTamReg = QLineEdit("20")
        self.campoTamReg.setMinimumWidth(140)
        self.campoTamReg.setFont(QFont("Arial", 10))
        self.campoTamReg.setStyleSheet("""
            QLineEdit {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                border-radius: 4px;
                padding: 5px;
                color: #2d1f15;
            }
            QLineEdit:focus {
                border: 2px solid #654321;
            }
        """)
        tamreg_layout.addWidget(label_tamreg)
        tamreg_layout.addWidget(self.campoTamReg)
        row2.addLayout(tamreg_layout)

        # Tamaño registro índice
        tamregind_layout = QHBoxLayout()
        label_tamregind = QLabel("Tamaño Regi. Índice (b):")
        label_tamregind.setFont(QFont("Arial", 10, QFont.Bold))
        label_tamregind.setStyleSheet("color: #2d1f15;")
        self.campoTamRegIn = QLineEdit("12")
        self.campoTamRegIn.setMinimumWidth(140)
        self.campoTamRegIn.setFont(QFont("Arial", 10))
        self.campoTamRegIn.setStyleSheet("""
            QLineEdit {
                background-color: #FAF5EB;
                border: 2px solid #8B5A2B;
                border-radius: 4px;
                padding: 5px;
                color: #2d1f15;
            }
            QLineEdit:focus {
                border: 2px solid #654321;
            }
        """)
        tamregind_layout.addWidget(label_tamregind)
        tamregind_layout.addWidget(self.campoTamRegIn)
        row2.addLayout(tamregind_layout)

        controls_layout.addLayout(row2)

        # Botón generar
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.botonGenerar = QPushButton("Generar Índices")
        self.botonGenerar.setMinimumSize(150, 40)
        self.botonGenerar.setFont(QFont("Arial", 11, QFont.Bold))
        self.botonGenerar.setStyleSheet("""
            QPushButton {
                background-color: #8B7355; 
                border: 2px solid #654321;
                border-radius: 6px;
                color: #FAF5EB;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #A0826D;
                border: 2px solid #8B5A2B;
            }
            QPushButton:pressed {
                background-color: #6F5739;
            }
        """)
        self.botonGenerar.clicked.connect(self.generarGrafica)
        btn_layout.addWidget(self.botonGenerar)
        btn_layout.addStretch()
        controls_layout.addLayout(btn_layout)

        content_layout.addWidget(controls_widget)

        main_layout.addWidget(content_widget)

    def generarGrafica(self):
        """Genera la gráfica con los datos ingresados"""
        try:
            self.tabla.setRowCount(0)
            tablaRes = self.canvas.dibujarGrafico(
                self.opcionTipoIndice.currentText(),
                self.opcionNiveles.currentText(),
                int(self.campoTamBloque.text()),
                int(self.campoCantReg.text()),
                int(self.campoTamReg.text()),
                int(self.campoTamRegIn.text())
            )

            for row, datos in enumerate(tablaRes):
                self.tabla.insertRow(row)
                for column, valor in enumerate(datos):
                    self.tabla.setItem(row, column, QTableWidgetItem(valor))

        except Exception as e:
            error = QMessageBox(self)
            error.setIcon(QMessageBox.Icon.Warning)
            error.setText(f"Datos Mal Ingresados\n{str(e)}")
            error.exec()