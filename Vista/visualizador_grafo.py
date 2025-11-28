from PySide6.QtWidgets import QWidget, QInputDialog
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import math


class VisualizadorGrafo(QWidget):
    """Widget para visualizar un grafo con interacción para cambiar etiquetas"""

    def __init__(self, titulo="Grafo", parent=None, es_editable=True):
        super().__init__(parent)
        self.titulo = titulo
        self.vertices = []
        self.aristas = []
        self.num_vertices = 0
        self.etiquetas = {}  # Diccionario para almacenar etiquetas personalizadas {indice: etiqueta}
        self.es_editable = es_editable  # Si se puede editar al hacer clic
        self.parent_window = parent
        self.setMinimumSize(350, 350)
        self.setMaximumSize(350, 350)

    def set_grafo(self, num_vertices, aristas, etiquetas=None):
        """Configura el grafo con sus vértices, aristas y etiquetas"""
        self.num_vertices = num_vertices
        self.aristas = aristas

        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            # Inicializar etiquetas por defecto (números del 1 al n)
            self.etiquetas = {i: str(i + 1) for i in range(num_vertices)}

        self.calcular_posiciones()
        self.update()

    def calcular_posiciones(self):
        """Calcula las posiciones de los vértices en círculo"""
        self.vertices = []
        if self.num_vertices == 0:
            return

        centro_x = self.width() / 2
        centro_y = self.height() / 2
        radio = min(centro_x, centro_y) - 40

        for i in range(self.num_vertices):
            angulo = 2 * math.pi * i / self.num_vertices - math.pi / 2
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            self.vertices.append(QPointF(x, y))

    def mousePressEvent(self, event):
        """Maneja el clic sobre los vértices para cambiar etiquetas"""
        if not self.es_editable:
            return

        if event.button() == Qt.LeftButton:
            # Verificar si se hizo clic en algún vértice
            for i, pos in enumerate(self.vertices):
                distancia = math.sqrt((event.pos().x() - pos.x()) ** 2 +
                                      (event.pos().y() - pos.y()) ** 2)
                if distancia <= 20:  # Radio del vértice
                    self.cambiar_etiqueta_vertice(i)
                    break

    def cambiar_etiqueta_vertice(self, indice):
        """Muestra un diálogo para cambiar la etiqueta de un vértice"""
        etiqueta_actual = self.etiquetas.get(indice, str(indice + 1))

        nueva_etiqueta, ok = QInputDialog.getText(
            self,
            "Cambiar Etiqueta",
            f"Nueva etiqueta para el vértice {indice + 1}:",
            text=etiqueta_actual
        )

        if ok and nueva_etiqueta.strip():
            self.etiquetas[indice] = nueva_etiqueta.strip()[:3]  # Máximo 3 caracteres
            self.update()

            # Actualizar en la ventana padre si existe
            if self.parent_window and hasattr(self.parent_window, 'actualizar_etiquetas'):
                self.parent_window.actualizar_etiquetas(self.titulo, self.etiquetas)

    def paintEvent(self, event):
        """Dibuja el grafo"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fondo
        painter.fillRect(self.rect(), QColor("#FFF3E0"))

        # Título
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.setPen(QColor("#6C4E31"))
        painter.drawText(self.rect().adjusted(0, 5, 0, 0), Qt.AlignTop | Qt.AlignHCenter, self.titulo)

        if self.num_vertices == 0:
            painter.setFont(QFont("Arial", 10))
            painter.setPen(QColor("#9c724a"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Sin grafo")
            return

        # Dibujar aristas
        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        for origen, destino in self.aristas:
            if origen < len(self.vertices) and destino < len(self.vertices):
                painter.drawLine(self.vertices[origen], self.vertices[destino])

        # Dibujar vértices
        for i, pos in enumerate(self.vertices):
            # Círculo del vértice
            painter.setBrush(QColor("#6C4E31"))
            painter.setPen(QPen(QColor("#2d1f15"), 2))
            painter.drawEllipse(pos, 20, 20)

            # Etiqueta del vértice
            painter.setPen(QColor("#FFEAC5"))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            texto = self.etiquetas.get(i, str(i + 1))
            rect = painter.fontMetrics().boundingRect(texto)
            painter.drawText(
                int(pos.x() - rect.width() / 2),
                int(pos.y() + rect.height() / 4),
                texto
            )

    def get_datos_grafo(self):
        """Retorna los datos del grafo para guardar"""
        return {
            'vertices': self.num_vertices,
            'aristas': self.aristas.copy(),
            'etiquetas': self.etiquetas.copy()
        }