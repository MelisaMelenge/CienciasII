from PySide6.QtWidgets import QWidget, QInputDialog
from PySide6.QtCore import Qt, QPointF, Signal
from PySide6.QtGui import QPainter, QPen, QColor, QFont, QPainterPath, QPolygonF
import math


class VisualizadorGrafoDirigido(QWidget):
    """Widget para visualizar un grafo DIRIGIDO con flechas"""

    # Señales para comunicar cambios
    etiqueta_cambiada = Signal(int, str)
    ponderacion_cambiada = Signal(tuple, str)

    def __init__(self, titulo="Grafo", parent=None, es_editable=True, ancho=350, alto=350):
        super().__init__(parent)
        self.titulo = titulo
        self.vertices = []
        self.aristas = []
        self.num_vertices = 0
        self.etiquetas = {}
        self.ponderaciones = {}
        self.es_editable = es_editable
        self.parent_window = parent
        self.ancho_fijo = ancho
        self.alto_fijo = alto
        self.setMinimumSize(ancho, alto)
        self.setMaximumSize(ancho, alto)

        self.desplazamientos_aristas = {}
        self.desplazamientos_ponderaciones = {}
        self.arista_seleccionada = None
        self.ponderacion_seleccionada = None

    def set_grafo(self, num_vertices, aristas, etiquetas=None, ponderaciones=None):
        """Configura el grafo dirigido"""
        self.num_vertices = num_vertices
        self.aristas = aristas
        self.desplazamientos_aristas = {}
        self.desplazamientos_ponderaciones = {}

        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            self.etiquetas = {i: str(i + 1) for i in range(num_vertices)}

        # Almacenar ponderaciones
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

        centro_x = self.ancho_fijo / 2
        centro_y = self.alto_fijo / 2
        radio = min(centro_x, centro_y) - 60

        for i in range(self.num_vertices):
            angulo = 2 * math.pi * i / self.num_vertices - math.pi / 2
            x = centro_x + radio * math.cos(angulo)
            y = centro_y + radio * math.sin(angulo)
            self.vertices.append(QPointF(x, y))

    def mousePressEvent(self, event):
        """Maneja el clic sobre vértices y aristas"""
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

            # Verificar clic en arista para cambiar ponderación
            for idx, arista in enumerate(self.aristas):
                origen, destino = arista
                if origen < len(self.vertices) and destino < len(self.vertices):
                    if self.punto_cerca_de_arista(click_pos, origen, destino, idx):
                        if self.es_editable:
                            self.cambiar_ponderacion_arista(arista)
                        return

    def cambiar_etiqueta_vertice(self, indice):
        """Muestra diálogo para cambiar etiqueta"""
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
        """Muestra diálogo para cambiar ponderación"""
        origen, destino = arista
        etiq_origen = self.etiquetas.get(origen, str(origen + 1))
        etiq_destino = self.etiquetas.get(destino, str(destino + 1))

        ponderacion_actual = self.ponderaciones.get(arista, "")

        nueva_ponderacion, ok = QInputDialog.getText(
            self,
            "Ponderación de Arista",
            f"Ponderación para la arista ({etiq_origen} → {etiq_destino}):",
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

    def punto_cerca_de_arista(self, punto, origen, destino, idx):
        """Verifica si un punto está cerca de una arista"""
        if origen == destino:
            # Bucle
            p = self.vertices[origen]
            centro = QPointF(p.x(), p.y() - 35)
            radio = 40
            dist = math.sqrt((punto.x() - centro.x()) ** 2 + (punto.y() - centro.y()) ** 2)
            return abs(dist - radio) < 15

        p1 = self.vertices[origen]
        p2 = self.vertices[destino]

        # Contar aristas entre mismo par (dirigidas)
        aristas_entre_par = [a for a in self.aristas if
                             (a[0] == origen and a[1] == destino) or
                             (a[0] == destino and a[1] == origen)]

        if len(aristas_entre_par) == 1:
            # Arista simple
            return self.punto_cerca_de_linea(punto, p1, p2)
        else:
            # Arista curva
            idx_en_grupo = aristas_entre_par.index((origen, destino))
            offset = 50 * (idx_en_grupo - (len(aristas_entre_par) - 1) / 2)

            dx = p2.x() - p1.x()
            dy = p2.y() - p1.y()
            longitud = math.sqrt(dx * dx + dy * dy)
            if longitud == 0:
                return False

            perp_x = -dy / longitud
            perp_y = dx / longitud
            medio_x = (p1.x() + p2.x()) / 2 + perp_x * offset
            medio_y = (p1.y() + p2.y()) / 2 + perp_y * offset

            # Verificar puntos en la curva
            for t in [0.2, 0.4, 0.5, 0.6, 0.8]:
                punto_x = (1 - t) ** 2 * p1.x() + 2 * (1 - t) * t * medio_x + t ** 2 * p2.x()
                punto_y = (1 - t) ** 2 * p1.y() + 2 * (1 - t) * t * medio_y + t ** 2 * p2.y()
                dist = math.sqrt((punto.x() - punto_x) ** 2 + (punto.y() - punto_y) ** 2)
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

    def paintEvent(self, event):
        """Dibuja el grafo dirigido"""
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

        # Dibujar aristas
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
            else:
                # Contar aristas entre el mismo par
                aristas_entre_par = [a for a in self.aristas if
                                     (a[0] == origen and a[1] == destino) or
                                     (a[0] == destino and a[1] == origen)]

                if len(aristas_entre_par) == 1:
                    self.dibujar_arista_simple(painter, p1, p2, ponderacion, origen, destino)
                else:
                    idx_en_grupo = aristas_entre_par.index(arista)
                    self.dibujar_arista_curva(painter, p1, p2, ponderacion, origen, destino,
                                              idx_en_grupo, len(aristas_entre_par))

        # Dibujar vértices
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

    def dibujar_arista_simple(self, painter, p1, p2, ponderacion, origen, destino):
        """Dibuja una arista dirigida simple con flecha"""
        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)

        # Calcular punto de inicio y fin (descontando el radio del círculo)
        dx = p2.x() - p1.x()
        dy = p2.y() - p1.y()
        longitud = math.sqrt(dx * dx + dy * dy)

        if longitud < 40:
            return

        # Normalizar
        dx /= longitud
        dy /= longitud

        # Puntos ajustados
        p1_adj = QPointF(p1.x() + dx * 20, p1.y() + dy * 20)
        p2_adj = QPointF(p2.x() - dx * 20, p2.y() - dy * 20)

        # Dibujar línea
        painter.drawLine(p1_adj, p2_adj)

        # Dibujar flecha
        self.dibujar_flecha(painter, p2_adj, dx, dy)

        # Dibujar ponderación
        if ponderacion:
            medio_x = (p1.x() + p2.x()) / 2
            medio_y = (p1.y() + p2.y()) / 2
            self.dibujar_ponderacion(painter, QPointF(medio_x, medio_y), str(ponderacion))

    def dibujar_arista_curva(self, painter, p1, p2, ponderacion, origen, destino, idx, total):
        """Dibuja una arista dirigida curva con flecha"""
        offset = 50 * (idx - (total - 1) / 2)

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

        # Ajustar inicio y fin
        t_inicio = 0.1
        t_fin = 0.9

        p1_adj_x = (1 - t_inicio) ** 2 * p1.x() + 2 * (1 - t_inicio) * t_inicio * control.x() + t_inicio ** 2 * p2.x()
        p1_adj_y = (1 - t_inicio) ** 2 * p1.y() + 2 * (1 - t_inicio) * t_inicio * control.y() + t_inicio ** 2 * p2.y()
        p1_adj = QPointF(p1_adj_x, p1_adj_y)

        p2_adj_x = (1 - t_fin) ** 2 * p1.x() + 2 * (1 - t_fin) * t_fin * control.x() + t_fin ** 2 * p2.x()
        p2_adj_y = (1 - t_fin) ** 2 * p1.y() + 2 * (1 - t_fin) * t_fin * control.y() + t_fin ** 2 * p2.y()
        p2_adj = QPointF(p2_adj_x, p2_adj_y)

        # Dibujar curva
        path = QPainterPath()
        path.moveTo(p1_adj)
        path.quadTo(control, p2_adj)

        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.drawPath(path)

        # Calcular dirección en el punto final
        dx_fin = p2_adj.x() - control.x()
        dy_fin = p2_adj.y() - control.y()
        longitud_fin = math.sqrt(dx_fin * dx_fin + dy_fin * dy_fin)
        if longitud_fin > 0:
            dx_fin /= longitud_fin
            dy_fin /= longitud_fin
            self.dibujar_flecha(painter, p2_adj, dx_fin, dy_fin)

        # Dibujar ponderación
        if ponderacion:
            punto_medio_x = (1 - 0.5) ** 2 * p1.x() + 2 * (1 - 0.5) * 0.5 * control.x() + 0.5 ** 2 * p2.x()
            punto_medio_y = (1 - 0.5) ** 2 * p1.y() + 2 * (1 - 0.5) * 0.5 * control.y() + 0.5 ** 2 * p2.y()
            self.dibujar_ponderacion(painter, QPointF(punto_medio_x, punto_medio_y), str(ponderacion))

    def dibujar_bucle(self, painter, p, ponderacion, indice):
        """Dibuja un bucle (arista de un vértice a sí mismo) con flecha"""
        radio_externo = 40
        desplazamiento = 35
        centro = QPointF(p.x(), p.y() - desplazamiento)

        # Dibujar arco (no círculo completo)
        path = QPainterPath()
        angulo_inicio = 30
        angulo_barrido = 300

        rect_x = centro.x() - radio_externo
        rect_y = centro.y() - radio_externo
        rect_ancho = 2 * radio_externo
        rect_alto = 2 * radio_externo

        path.arcMoveTo(rect_x, rect_y, rect_ancho, rect_alto, angulo_inicio)
        inicio = path.currentPosition()
        path.arcTo(rect_x, rect_y, rect_ancho, rect_alto, angulo_inicio, angulo_barrido)

        pen = QPen(QColor("#bf8f62"), 2)
        painter.setPen(pen)
        painter.drawPath(path)

        # Dibujar flecha al final del arco
        angulo_fin = math.radians(angulo_inicio + angulo_barrido)
        punto_fin_x = centro.x() + radio_externo * math.cos(angulo_fin)
        punto_fin_y = centro.y() - radio_externo * math.sin(angulo_fin)

        # Dirección tangente
        dx = -math.sin(angulo_fin)
        dy = math.cos(angulo_fin)

        self.dibujar_flecha(painter, QPointF(punto_fin_x, punto_fin_y), dx, dy)

        # Dibujar ponderación
        if ponderacion:
            pos_x = p.x()
            pos_y = centro.y() - radio_externo - 10
            self.dibujar_ponderacion(painter, QPointF(pos_x, pos_y), str(ponderacion))

    def dibujar_flecha(self, painter, punto, dx, dy):
        """Dibuja una flecha en la dirección indicada"""
        tamaño_flecha = 10
        angulo_flecha = 25  # grados

        # Calcular puntos de la flecha
        angulo = math.atan2(dy, dx)

        angulo1 = angulo + math.radians(180 - angulo_flecha)
        angulo2 = angulo + math.radians(180 + angulo_flecha)

        p1 = QPointF(
            punto.x() + tamaño_flecha * math.cos(angulo1),
            punto.y() + tamaño_flecha * math.sin(angulo1)
        )
        p2 = QPointF(
            punto.x() + tamaño_flecha * math.cos(angulo2),
            punto.y() + tamaño_flecha * math.sin(angulo2)
        )

        # Dibujar triángulo de flecha
        flecha = QPolygonF([punto, p1, p2])
        painter.setBrush(QColor("#bf8f62"))
        painter.drawPolygon(flecha)

    def dibujar_ponderacion(self, painter, punto, ponderacion):
        """Dibuja la ponderación en un punto"""
        rect_pond = painter.fontMetrics().boundingRect(ponderacion)
        rect_pond.moveCenter(punto.toPoint())
        rect_pond.adjust(-3, -2, 3, 2)

        painter.fillRect(rect_pond, QColor("#FFF3E0"))
        painter.setPen(QColor("#d9534f"))
        painter.setFont(QFont("Arial", 9, QFont.Bold))
        painter.drawText(rect_pond, Qt.AlignCenter, ponderacion)

