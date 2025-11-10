from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, QPointF
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import math


class VisualizadorGrafo(QWidget):
    """Widget para visualizar un grafo"""

    def __init__(self, titulo="Grafo", parent=None):
        super().__init__(parent)
        self.titulo = titulo
        self.vertices = []
        self.aristas = []
        self.num_vertices = 0
        self.setMinimumSize(350, 350)
        self.setMaximumSize(350, 350)

    def set_grafo(self, num_vertices, aristas):
        self.num_vertices = num_vertices
        self.aristas = aristas
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

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Fondo
        painter.fillRect(self.rect(), QColor("#F9FAFB"))

        # Título
        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.setPen(QColor("#7C3AED"))
        painter.drawText(self.rect().adjusted(0, 5, 0, 0), Qt.AlignTop | Qt.AlignHCenter, self.titulo)

        if self.num_vertices == 0:
            painter.setFont(QFont("Arial", 10))
            painter.setPen(QColor("#6B7280"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Sin grafo")
            return

        # Dibujar aristas
        pen = QPen(QColor("#A78BFA"), 2)
        painter.setPen(pen)
        for origen, destino in self.aristas:
            if origen < len(self.vertices) and destino < len(self.vertices):
                painter.drawLine(self.vertices[origen], self.vertices[destino])

        # Dibujar vértices
        for i, pos in enumerate(self.vertices):
            # Círculo del vértice
            painter.setBrush(QColor("#7C3AED"))
            painter.setPen(QPen(QColor("#5B21B6"), 2))
            painter.drawEllipse(pos, 20, 20)

            # Número del vértice
            painter.setPen(QColor("white"))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            texto = str(i + 1)
            rect = painter.fontMetrics().boundingRect(texto)
            painter.drawText(
                int(pos.x() - rect.width() / 2),
                int(pos.y() + rect.height() / 4),
                texto
            )