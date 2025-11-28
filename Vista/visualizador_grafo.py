from PySide6.QtWidgets import QWidget, QInputDialog
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QFont
import math


class VisualizadorGrafo(QWidget):
    """Widget para visualizar un grafo con interacción para cambiar etiquetas y ponderaciones"""

    # Señales para comunicar cambios
    etiqueta_cambiada = Signal(int, str)  # (indice_vertice, nueva_etiqueta)
    ponderacion_cambiada = Signal(tuple, str)  # (arista, ponderacion)

    def __init__(self, titulo="Grafo", parent=None, es_editable=True):
        super().__init__(parent)
        self.titulo = titulo
        self.vertices = []
        self.aristas = []
        self.num_vertices = 0
        self.etiquetas = {}  # Diccionario para almacenar etiquetas personalizadas {indice: etiqueta}
        self.ponderaciones = {}  # Diccionario para almacenar ponderaciones de aristas {(origen, destino): peso}
        self.es_editable = es_editable  # Si se puede editar al hacer clic
        self.parent_window = parent
        self.setMinimumSize(350, 350)
        self.setMaximumSize(350, 350)

    def set_grafo(self, num_vertices, aristas, etiquetas=None, ponderaciones=None):
        """Configura el grafo con sus vértices, aristas, etiquetas y ponderaciones"""
        self.num_vertices = num_vertices
        self.aristas = aristas

        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            self.etiquetas = {i: str(i + 1) for i in range(num_vertices)}

        # CAMBIO IMPORTANTE: Almacenar ponderaciones como LISTA, no como diccionario
        if ponderaciones:
            if isinstance(ponderaciones, list):
                # Ya es una lista, usarla directamente
                self.ponderaciones_lista = ponderaciones.copy()
                # Mantener también diccionario para compatibilidad (solo para aristas únicas)
                self.ponderaciones = {}
                for i, arista in enumerate(aristas):
                    if i < len(ponderaciones) and ponderaciones[i]:
                        # Solo agregar al dict si no existe o para última aparición
                        self.ponderaciones[arista] = ponderaciones[i]
            else:
                # Es un diccionario, convertir a lista
                self.ponderaciones = ponderaciones.copy()
                self.ponderaciones_lista = []
                for arista in aristas:
                    self.ponderaciones_lista.append(ponderaciones.get(arista, ""))
        else:
            self.ponderaciones = {}
            self.ponderaciones_lista = [""] * len(aristas)

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
        """Maneja el clic sobre los vértices y aristas"""
        if not self.es_editable:
            return

        if event.button() == Qt.LeftButton:
            click_pos = event.pos()

            # Primero verificar si se hizo clic en algún vértice
            for i, pos in enumerate(self.vertices):
                distancia = math.sqrt((click_pos.x() - pos.x()) ** 2 +
                                      (click_pos.y() - pos.y()) ** 2)
                if distancia <= 20:  # Radio del vértice
                    self.cambiar_etiqueta_vertice(i)
                    return

            # Si no se clickeó un vértice, verificar si se clickeó una arista
            for arista in self.aristas:
                origen, destino = arista
                if origen < len(self.vertices) and destino < len(self.vertices):
                    if self.punto_cerca_de_linea(click_pos, self.vertices[origen], self.vertices[destino]):
                        self.cambiar_ponderacion_arista(arista)
                        return

    def punto_cerca_de_linea(self, punto, p1, p2, tolerancia=10):
        """Verifica si un punto está cerca de una línea entre p1 y p2"""
        # Calcular la distancia del punto a la línea
        x0, y0 = punto.x(), punto.y()
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()

        # Longitud del segmento
        longitud_cuadrado = (x2 - x1) ** 2 + (y2 - y1) ** 2

        if longitud_cuadrado == 0:
            # p1 y p2 son el mismo punto
            return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2) <= tolerancia

        # Proyección del punto sobre la línea
        t = max(0, min(1, ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / longitud_cuadrado))

        # Punto más cercano en el segmento
        proyeccion_x = x1 + t * (x2 - x1)
        proyeccion_y = y1 + t * (y2 - y1)

        # Distancia del punto al punto más cercano
        distancia = math.sqrt((x0 - proyeccion_x) ** 2 + (y0 - proyeccion_y) ** 2)

        return distancia <= tolerancia

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
            nueva_etiqueta = nueva_etiqueta.strip()[:3]  # Máximo 3 caracteres
            self.etiquetas[indice] = nueva_etiqueta
            self.update()

            # Emitir señal de cambio
            self.etiqueta_cambiada.emit(indice, nueva_etiqueta)

    def cambiar_ponderacion_arista(self, arista):
        """Muestra un diálogo para cambiar la ponderación de una arista"""
        origen, destino = arista
        etiq_origen = self.etiquetas.get(origen, str(origen + 1))
        etiq_destino = self.etiquetas.get(destino, str(destino + 1))

        ponderacion_actual = self.ponderaciones.get(arista, "")

        nueva_ponderacion, ok = QInputDialog.getText(
            self,
            "Ponderación de Arista",
            f"Ponderación para la arista ({etiq_origen} - {etiq_destino}):",
            text=str(ponderacion_actual)
        )

        if ok:
            nueva_ponderacion = nueva_ponderacion.strip()
            if nueva_ponderacion:
                # Limitar a 4 caracteres
                nueva_ponderacion = nueva_ponderacion[:4]
                self.ponderaciones[arista] = nueva_ponderacion
            else:
                # Si está vacío, eliminar la ponderación
                if arista in self.ponderaciones:
                    del self.ponderaciones[arista]
                nueva_ponderacion = ""

            self.update()

            # Emitir señal de cambio
            self.ponderacion_cambiada.emit(arista, nueva_ponderacion)

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

        # Agrupar aristas por par de vértices (sin importar ponderación para contar)
        aristas_por_par = {}
        for i, arista in enumerate(self.aristas):
            origen, destino = arista
            par = tuple(sorted([origen, destino]))
            if par not in aristas_por_par:
                aristas_por_par[par] = []
            aristas_por_par[par].append(i)  # Guardar ÍNDICE en lugar de arista

        # Dibujar aristas
        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 9))

        for i, arista in enumerate(self.aristas):
            if arista[0] < len(self.vertices) and arista[1] < len(self.vertices):
                origen, destino = arista
                p1 = self.vertices[origen]
                p2 = self.vertices[destino]

                # Determinar si hay múltiples aristas entre estos vértices
                par = tuple(sorted([origen, destino]))
                indices_aristas = aristas_por_par[par]
                num_aristas = len(indices_aristas)

                # Obtener ponderación usando el ÍNDICE
                ponderacion = ""
                if hasattr(self, 'ponderaciones_lista') and i < len(self.ponderaciones_lista):
                    ponderacion = self.ponderaciones_lista[i]
                elif arista in self.ponderaciones:
                    ponderacion = self.ponderaciones[arista]

                # Si hay múltiples aristas, calcular desplazamiento
                if num_aristas > 1:
                    indice_en_grupo = indices_aristas.index(i)
                    self.dibujar_arista_curva(painter, p1, p2, ponderacion, indice_en_grupo, num_aristas)
                else:
                    # Dibujar línea recta normal
                    painter.setPen(pen)
                    painter.drawLine(p1, p2)

                    # Dibujar ponderación si existe
                    if ponderacion:
                        self.dibujar_ponderacion(painter, p1, p2, ponderacion)

                    painter.setPen(pen)

        # Dibujar vértices (resto del código sin cambios)
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

    def dibujar_arista_curva(self, painter, p1, p2, ponderacion, indice, total):
        """Dibuja una arista curva cuando hay múltiples aristas entre los mismos vértices"""
        import math
        from PySide6.QtGui import QPainterPath

        # Calcular el desplazamiento perpendicular
        offset_base = 30
        offset = offset_base * (indice - (total - 1) / 2)

        if abs(offset) < 5 and offset != 0:
            offset = 15 if offset > 0 else -15

        # Vector perpendicular a la línea
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        longitud = math.sqrt(dx * dx + dy * dy)

        if longitud == 0:
            return

        perp_x = -dy / longitud
        perp_y = dx / longitud

        # Punto de control para la curva
        medio_x = (p1.x() + p2.x()) / 2 + perp_x * offset
        medio_y = (p1.y() + p2.y()) / 2 + perp_y * offset
        control = QPointF(medio_x, medio_y)

        # Dibujar curva
        path = QPainterPath()
        path.moveTo(p1)
        path.quadTo(control, p2)

        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.drawPath(path)

        # Dibujar ponderación si existe
        if ponderacion:
            t = 0.5
            punto_curva_x = (1 - t) * (1 - t) * p1.x() + 2 * (1 - t) * t * control.x() + t * t * p2.x()
            punto_curva_y = (1 - t) * (1 - t) * p1.y() + 2 * (1 - t) * t * control.y() + t * t * p2.y()
            punto_medio = QPointF(punto_curva_x, punto_curva_y)

            rect_pond = painter.fontMetrics().boundingRect(ponderacion)
            rect_pond.moveCenter(punto_medio.toPoint())
            rect_pond.adjust(-3, -2, 3, 2)

            painter.fillRect(rect_pond, QColor("#FFF3E0"))
            painter.setPen(QColor("#d9534f"))
            painter.setFont(QFont("Arial", 9, QFont.Bold))
            painter.drawText(rect_pond, Qt.AlignCenter, ponderacion)

    def dibujar_ponderacion(self, painter, p1, p2, ponderacion):
        """Dibuja la ponderación en el punto medio de una arista recta"""
        medio_x = (p1.x() + p2.x()) / 2
        medio_y = (p1.y() + p2.y()) / 2

        rect_pond = painter.fontMetrics().boundingRect(ponderacion)
        rect_pond.moveCenter(QPointF(medio_x, medio_y).toPoint())
        rect_pond.adjust(-3, -2, 3, 2)

        painter.fillRect(rect_pond, QColor("#FFF3E0"))
        painter.setPen(QColor("#d9534f"))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(rect_pond, Qt.AlignCenter, ponderacion)

    def get_datos_grafo(self):
        """Retorna los datos del grafo para guardar"""
        return {
            'vertices': self.num_vertices,
            'aristas': self.aristas.copy(),
            'etiquetas': self.etiquetas.copy(),
            'ponderaciones': {str(k): v for k, v in self.ponderaciones.items()}
        }