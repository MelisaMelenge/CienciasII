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
        self.etiquetas = {}
        self.ponderaciones = {}
        self.es_editable = es_editable
        self.parent_window = parent
        self.setMinimumSize(350, 350)
        self.setMaximumSize(350, 350)

        # Para mover aristas
        self.arista_seleccionada = None
        self.desplazamientos_aristas = {}

    def set_grafo(self, num_vertices, aristas, etiquetas=None, ponderaciones=None):
        """Configura el grafo con sus vértices, aristas, etiquetas y ponderaciones"""
        self.num_vertices = num_vertices
        self.aristas = aristas
        self.desplazamientos_aristas = {}

        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            self.etiquetas = {i: str(i + 1) for i in range(num_vertices)}

        # Almacenar ponderaciones como LISTA
        if ponderaciones:
            if isinstance(ponderaciones, list):
                self.ponderaciones_lista = ponderaciones.copy()
                self.ponderaciones = {}
                for i, arista in enumerate(aristas):
                    if i < len(ponderaciones) and ponderaciones[i]:
                        self.ponderaciones[arista] = ponderaciones[i]
            else:
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
        if event.button() == Qt.LeftButton:
            click_pos = event.pos()

            # Verificar clic en vértice
            for i, pos in enumerate(self.vertices):
                distancia = math.sqrt((click_pos.x() - pos.x()) ** 2 +
                                      (click_pos.y() - pos.y()) ** 2)
                if distancia <= 20:
                    if self.es_editable:
                        self.cambiar_etiqueta_vertice(i)
                    return

            # Verificar clic en arista
            for idx, arista in enumerate(self.aristas):
                origen, destino = arista
                if origen < len(self.vertices) and destino < len(self.vertices):
                    if self.punto_cerca_de_arista(click_pos, origen, destino, idx):
                        if self.es_editable:
                            self.cambiar_ponderacion_arista(arista)
                        return

        elif event.button() == Qt.RightButton:
            # Clic derecho para mover aristas (SIEMPRE habilitado)
            click_pos = event.pos()
            for idx, arista in enumerate(self.aristas):
                origen, destino = arista
                if origen < len(self.vertices) and destino < len(self.vertices):
                    if self.punto_cerca_de_arista(click_pos, origen, destino, idx):
                        self.arista_seleccionada = idx
                        self.ultimo_pos = event.pos()
                        self.setCursor(Qt.ClosedHandCursor)
                        return

    def mouseMoveEvent(self, event):
        """Mueve la arista seleccionada"""
        if self.arista_seleccionada is not None:
            delta_y = event.pos().y() - self.ultimo_pos.y()
            offset_actual = self.desplazamientos_aristas.get(self.arista_seleccionada, 0)
            self.desplazamientos_aristas[self.arista_seleccionada] = offset_actual + delta_y * 0.5
            self.ultimo_pos = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        """Suelta la arista"""
        if event.button() == Qt.RightButton and self.arista_seleccionada is not None:
            self.arista_seleccionada = None
            self.setCursor(Qt.ArrowCursor)

    def punto_cerca_de_arista(self, punto, origen, destino, idx_arista):
        """Verifica si un punto está cerca de una arista específica"""
        if origen == destino:
            p = self.vertices[origen]
            desplazamiento = 35
            centro = QPointF(p.x(), p.y() - desplazamiento)
            radio_externo = 40
            dist_centro = math.sqrt((punto.x() - centro.x()) ** 2 + (punto.y() - centro.y()) ** 2)
            return abs(dist_centro - radio_externo) < 15

        p1 = self.vertices[origen]
        p2 = self.vertices[destino]

        par = tuple(sorted([origen, destino]))
        conteo_pares = {}
        for a in self.aristas:
            o, d = a
            par_temp = tuple(sorted([o, d]))
            conteo_pares[par_temp] = conteo_pares.get(par_temp, 0) + 1

        total_aristas = conteo_pares.get(par, 1)

        if total_aristas == 1:
            return self.punto_cerca_de_linea(punto, p1, p2)
        else:
            indices_por_par = {}
            for i, arista in enumerate(self.aristas):
                o, d = arista
                par_temp = tuple(sorted([o, d]))
                if par_temp not in indices_por_par:
                    indices_por_par[par_temp] = []
                indices_por_par[par_temp].append(i)

            indice_actual = indices_por_par[par].index(idx_arista)
            offset_base = 70
            offset = offset_base * (indice_actual - (total_aristas - 1) / 2)
            offset += self.desplazamientos_aristas.get(idx_arista, 0)

            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            longitud = math.sqrt(dx * dx + dy * dy)

            if longitud == 0:
                return False

            perp_x = -dy / longitud
            perp_y = dx / longitud
            medio_x = (p1.x() + p2.x()) / 2 + perp_x * offset
            medio_y = (p1.y() + p2.y()) / 2 + perp_y * offset

            for t in [0.2, 0.4, 0.5, 0.6, 0.8]:
                punto_curva_x = (1 - t) * (1 - t) * p1.x() + 2 * (1 - t) * t * medio_x + t * t * p2.x()
                punto_curva_y = (1 - t) * (1 - t) * p1.y() + 2 * (1 - t) * t * medio_y + t * t * p2.y()
                dist = math.sqrt((punto.x() - punto_curva_x) ** 2 + (punto.y() - punto_curva_y) ** 2)
                if dist < 15:
                    return True
            return False

    def punto_cerca_de_linea(self, punto, p1, p2, tolerancia=15):
        """Verifica si un punto está cerca de una línea"""
        x0, y0 = punto.x(), punto.y()
        x1, y1 = p1.x(), p1.y()
        x2, y2 = p2.x(), p2.y()

        longitud_cuadrado = (x2 - x1) ** 2 + (y2 - y1) ** 2

        if longitud_cuadrado == 0:
            return math.sqrt((x0 - x1) ** 2 + (y0 - y1) ** 2) <= tolerancia

        t = max(0, min(1, ((x0 - x1) * (x2 - x1) + (y0 - y1) * (y2 - y1)) / longitud_cuadrado))
        proyeccion_x = x1 + t * (x2 - x1)
        proyeccion_y = y1 + t * (y2 - y1)
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
            nueva_etiqueta = nueva_etiqueta.strip()[:3]
            self.etiquetas[indice] = nueva_etiqueta
            self.update()
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
                nueva_ponderacion = nueva_ponderacion[:4]
                self.ponderaciones[arista] = nueva_ponderacion
            else:
                if arista in self.ponderaciones:
                    del self.ponderaciones[arista]
                nueva_ponderacion = ""

            if hasattr(self, 'ponderaciones_lista'):
                try:
                    indice_arista = self.aristas.index(arista)
                    if indice_arista < len(self.ponderaciones_lista):
                        self.ponderaciones_lista[indice_arista] = nueva_ponderacion
                except ValueError:
                    pass

            self.update()
            self.ponderacion_cambiada.emit(arista, nueva_ponderacion)

    def paintEvent(self, event):
        """Dibuja el grafo"""
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor("#FFF3E0"))

        painter.setFont(QFont("Arial", 12, QFont.Bold))
        painter.setPen(QColor("#6C4E31"))
        painter.drawText(self.rect().adjusted(0, 5, 0, 0), Qt.AlignTop | Qt.AlignHCenter, self.titulo)

        if self.num_vertices == 0:
            painter.setFont(QFont("Arial", 10))
            painter.setPen(QColor("#9c724a"))
            painter.drawText(self.rect(), Qt.AlignCenter, "Sin grafo")
            return

        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.setFont(QFont("Arial", 9))

        conteo_pares = {}
        for arista in self.aristas:
            origen, destino = arista
            par = tuple(sorted([origen, destino]))
            conteo_pares[par] = conteo_pares.get(par, 0) + 1

        indices_por_par = {}
        for i, arista in enumerate(self.aristas):
            origen, destino = arista
            par = tuple(sorted([origen, destino]))
            if par not in indices_por_par:
                indices_por_par[par] = []
            indices_por_par[par].append(i)

        for i, arista in enumerate(self.aristas):
            if arista[0] >= len(self.vertices) or arista[1] >= len(self.vertices):
                continue

            origen, destino = arista
            p1 = self.vertices[origen]
            p2 = self.vertices[destino]

            ponderacion = ""
            if hasattr(self, 'ponderaciones_lista') and i < len(self.ponderaciones_lista):
                ponderacion = self.ponderaciones_lista[i]
            elif arista in self.ponderaciones:
                ponderacion = self.ponderaciones[arista]

            if origen == destino:
                self.dibujar_bucle(painter, p1, ponderacion, i)
                continue

            par = tuple(sorted([origen, destino]))
            total_aristas = conteo_pares[par]
            indice_actual = indices_por_par[par].index(i)

            if total_aristas > 1:
                self.dibujar_arista_curva(painter, p1, p2, ponderacion, indice_actual, total_aristas, i)
            else:
                painter.setPen(pen)
                painter.drawLine(p1, p2)
                if ponderacion:
                    self.dibujar_ponderacion(painter, p1, p2, ponderacion)

        for i, pos in enumerate(self.vertices):
            painter.setBrush(QColor("#6C4E31"))
            painter.setPen(QPen(QColor("#2d1f15"), 2))
            painter.drawEllipse(pos, 20, 20)

            painter.setPen(QColor("#FFEAC5"))
            painter.setFont(QFont("Arial", 10, QFont.Bold))
            texto = self.etiquetas.get(i, str(i + 1))
            rect = painter.fontMetrics().boundingRect(texto)
            painter.drawText(
                int(pos.x() - rect.width() / 2),
                int(pos.y() + rect.height() / 4),
                texto
            )

    def dibujar_arista_curva(self, painter, p1, p2, ponderacion, indice, total, idx_arista):
        """Dibuja una arista curva"""
        from PySide6.QtGui import QPainterPath

        offset_base = 70
        offset = offset_base * (indice - (total - 1) / 2)
        offset += self.desplazamientos_aristas.get(idx_arista, 0)

        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        longitud = math.sqrt(dx * dx + dy * dy)

        if longitud == 0:
            return

        perp_x = -dy / longitud
        perp_y = dx / longitud

        medio_x = (p1.x() + p2.x()) / 2 + perp_x * offset
        medio_y = (p1.y() + p2.y()) / 2 + perp_y * offset
        control = QPointF(medio_x, medio_y)

        path = QPainterPath()
        path.moveTo(p1)
        path.quadTo(control, p2)

        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.drawPath(path)

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
        """Dibuja la ponderación en el punto medio"""
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
        """Retorna los datos del grafo"""
        return {
            'vertices': self.num_vertices,
            'aristas': self.aristas.copy(),
            'etiquetas': self.etiquetas.copy(),
            'ponderaciones': {str(k): v for k, v in self.ponderaciones.items()}
        }

    def dibujar_bucle(self, painter, p, ponderacion, indice):
        """Dibuja un bucle"""
        from PySide6.QtGui import QPainterPath

        radio_externo = 40
        desplazamiento = 35

        centro = QPointF(p.x(), p.y() - desplazamiento)

        path = QPainterPath()
        inicio = QPointF(p.x() + radio_externo, centro.y())
        path.moveTo(inicio)

        path.arcTo(
            centro.x() - radio_externo,
            centro.y() - radio_externo,
            radio_externo * 2,
            radio_externo * 2,
            0, 300
        )

        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.drawPath(path)

        if ponderacion:
            painter.setFont(QFont("Arial", 10, QFont.Bold))

            rect_pond = painter.fontMetrics().boundingRect(ponderacion)
            rect_pond.moveCenter(QPointF(
                p.x(),
                centro.y() - radio_externo - 10
            ).toPoint())
            rect_pond.adjust(-4, -3, 4, 3)

            painter.fillRect(rect_pond, QColor("#FFF3E0"))
            painter.setPen(QColor("#d9534f"))
            painter.drawText(rect_pond, Qt.AlignCenter, ponderacion)
