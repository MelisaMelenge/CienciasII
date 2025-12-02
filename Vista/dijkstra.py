from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QSpinBox, QMessageBox, QFileDialog
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo_dirigido import VisualizadorGrafoDirigido
from Controlador.Algoritmos.DijkstraController import DijkstraController
import json


class ModeloGrafoInterno:
    """Modelo interno simple para el grafo"""

    def __init__(self):
        self.num_vertices = 0
        self.aristas = []
        self.etiquetas = {}
        self.ponderaciones_lista = []

    def crear_grafo(self, num_vertices):
        """Crea un grafo vacío con n vértices"""
        self.num_vertices = num_vertices
        self.aristas = []
        self.etiquetas = {i: str(i + 1) for i in range(num_vertices)}
        self.ponderaciones_lista = []

    def agregar_arista(self, origen, destino):
        """Agrega una arista al grafo"""
        if origen < 0 or origen >= self.num_vertices or destino < 0 or destino >= self.num_vertices:
            return False

        arista = (origen, destino)
        if arista not in self.aristas:
            self.aristas.append(arista)
            self.ponderaciones_lista.append("")  # Sin peso por defecto
            return True
        return False

    def obtener_num_vertices(self):
        """Retorna el número de vértices"""
        return self.num_vertices

    def obtener_aristas(self):
        """Retorna la lista de aristas"""
        return self.aristas.copy()

    def obtener_etiquetas(self):
        """Retorna el diccionario de etiquetas"""
        return self.etiquetas.copy()

    def obtener_ponderaciones_como_lista(self):
        """Retorna las ponderaciones como lista"""
        return self.ponderaciones_lista.copy()

    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        """Actualiza la etiqueta de un vértice"""
        if 0 <= indice < self.num_vertices:
            self.etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion(self, arista, nueva_ponderacion):
        """Actualiza la ponderación de una arista"""
        try:
            idx = self.aristas.index(arista)
            if idx < len(self.ponderaciones_lista):
                self.ponderaciones_lista[idx] = nueva_ponderacion
        except ValueError:
            pass

    def guardar_grafo(self, archivo):
        """Guarda el grafo en un archivo JSON"""
        try:
            datos = {
                'num_vertices': self.num_vertices,
                'aristas': self.aristas,
                'etiquetas': self.etiquetas,
                'ponderaciones': self.ponderaciones_lista
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=2)
            return True
        except Exception as e:
            print(f"Error al guardar: {e}")
            return False

    def cargar_grafo(self, archivo):
        """Carga el grafo desde un archivo JSON"""
        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            self.num_vertices = datos.get('num_vertices', 0)
            self.aristas = [tuple(a) for a in datos.get('aristas', [])]
            self.etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}
            self.ponderaciones_lista = datos.get('ponderaciones', [])

            return True
        except Exception as e:
            print(f"Error al cargar: {e}")
            return False


class VisualizadorDijkstra(VisualizadorGrafoDirigido):
    """Visualizador especial para Dijkstra que muestra todos los caminos"""

    def __init__(self, titulo="Dijkstra", parent=None):
        super().__init__(titulo, parent, es_editable=True, ancho=500, alto=500)
        self.todos_caminos = {}
        self.distancias_minimas = {}
        self.vertice_origen = None
        self.ponderaciones_lista = []  # Almacenar ponderaciones como lista

    def set_grafo(self, num_vertices, aristas, etiquetas, ponderaciones):
        """Override para guardar también las ponderaciones"""
        super().set_grafo(num_vertices, aristas, etiquetas, ponderaciones)
        self.ponderaciones_lista = ponderaciones if isinstance(ponderaciones, list) else []

    def set_resultado_dijkstra(self, distancias, todos_caminos, origen):
        """Configura los resultados de Dijkstra para visualizar"""
        self.distancias_minimas = distancias
        self.todos_caminos = todos_caminos
        self.vertice_origen = origen
        self.update()

    def limpiar_resultados(self):
        """Limpia los resultados de Dijkstra"""
        self.todos_caminos = {}
        self.distancias_minimas = {}
        self.vertice_origen = None
        self.update()

    def paintEvent(self, event):
        """Dibuja el grafo con los caminos encontrados"""
        # Primero dibuja el grafo normal
        super().paintEvent(event)

        if not self.todos_caminos:
            return

        from PySide6.QtGui import QPainter, QFont, QColor
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # Dibujar información de caminos al lado de cada vértice
        for i, pos in enumerate(self.vertices):
            if i == self.vertice_origen:
                continue

            # Posición para el texto (a la derecha del vértice)
            texto_x = pos.x() + 35
            texto_y = pos.y() - 20

            if i in self.todos_caminos and self.todos_caminos[i]:
                # Ordenar caminos por distancia
                caminos_ordenados = sorted(self.todos_caminos[i], key=lambda x: x[0])

                # Mostrar hasta 3 caminos
                for idx, (distancia, camino) in enumerate(caminos_ordenados[:3]):
                    if distancia == float('inf'):
                        continue

                    # Marcar el camino más corto
                    es_minimo = (distancia == self.distancias_minimas.get(i, float('inf')))

                    # Calcular distancia total y vértice de donde viene (último antes del actual)
                    if len(camino) >= 2:
                        vertice_previo = camino[-2]
                        # Formatear distancia: mostrar como entero si es .0, sino como float
                        dist_str = str(int(distancia)) if distancia % 1 == 0 else str(distancia)
                        info_corchetes = f"[{dist_str}, {vertice_previo + 1}]"
                    else:
                        info_corchetes = f"[0, {i + 1}]"  # Es el origen

                    camino_str = '→'.join(str(v + 1) for v in camino)
                    texto = f"{info_corchetes} {camino_str}"

                    if es_minimo:
                        # Camino más corto en rojo/destacado
                        painter.setPen(QColor("#d9534f"))
                        painter.setFont(QFont("Arial", 9, QFont.Bold))
                        texto += " ✓"
                    else:
                        # Caminos alternativos en gris
                        painter.setPen(QColor("#6C4E31"))
                        painter.setFont(QFont("Arial", 8))

                    # Fondo semi-transparente
                    rect = painter.fontMetrics().boundingRect(texto)
                    rect.moveTo(int(texto_x), int(texto_y + idx * 18))
                    rect.adjust(-3, -2, 3, 2)

                    painter.fillRect(rect, QColor(255, 243, 224, 220))
                    painter.drawText(rect, Qt.AlignLeft | Qt.AlignVCenter, texto)

                # Si hay más caminos, mostrar indicador
                if len(self.todos_caminos[i]) > 3:
                    painter.setPen(QColor("#9c724a"))
                    painter.setFont(QFont("Arial", 7))
                    texto_mas = f"... +{len(self.todos_caminos[i]) - 3} más"
                    painter.drawText(int(texto_x), int(texto_y + 3 * 18 + 5), texto_mas)

    def _obtener_peso_arista(self, origen, destino):
        """Obtiene el peso de una arista específica"""
        # Buscar la arista en la lista
        for idx, (u, v) in enumerate(self.aristas):
            if u == origen and v == destino:
                # Obtener peso desde la lista de ponderaciones
                if idx < len(self.ponderaciones_lista) and self.ponderaciones_lista[idx]:
                    try:
                        peso = self.ponderaciones_lista[idx]
                        # Si es string, convertir a float
                        return float(peso) if peso else 1.0
                    except (ValueError, TypeError):
                        return 1.0
                return 1.0

        return 1.0  # Peso por defecto si no se encuentra

class Dijkstra(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Crear modelo interno
        self.model = ModeloGrafoInterno()
        self.controller = DijkstraController(self.model)

        self.setWindowTitle("Algoritmo de Dijkstra")
        self.setGeometry(150, 80, 1300, 750)

        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Header
        header = self._crear_header()
        layout.addWidget(header)

        # Contenido principal
        contenido_layout = QHBoxLayout()

        # Panel izquierdo - Visualización
        panel_visual = self._crear_panel_visual()
        contenido_layout.addWidget(panel_visual, 2)

        # Panel central - Controles del Grafo
        panel_grafo = self._crear_panel_grafo()
        contenido_layout.addWidget(panel_grafo, 1)

        # Panel derecho - Dijkstra
        panel_dijkstra = self._crear_panel_dijkstra()
        contenido_layout.addWidget(panel_dijkstra, 2)

        layout.addLayout(contenido_layout)

    def _crear_header(self):
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62);
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Algoritmo de Dijkstra")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d1f15; margin: 10px;")
        header_layout.addWidget(titulo)

        # Menú de navegación
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
                           padding: 5px 15px;
                       }
                       QPushButton:hover { 
                           color: #FFEAC5; 
                           background-color: #6C4E31;
                           border-radius: 8px;
                       }
                   """)
            menu_layout.addWidget(btn)

        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_grafos.clicked.connect(lambda: self.cambiar_ventana("grafos"))

        header_layout.addLayout(menu_layout)

        return header

    def _crear_panel_visual(self):
        panel = QFrame()
        panel.setStyleSheet("""
            background-color: #FFF3E0;
            border: 2px solid #bf8f62;
            border-radius: 10px;
            padding: 10px;
        """)
        layout = QVBoxLayout(panel)

        titulo = QLabel("Visualización del Grafo")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #6C4E31;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Visualizador
        self.visualizador = VisualizadorDijkstra("Grafo Dirigido", self)
        self.visualizador.etiqueta_cambiada.connect(self.actualizar_etiqueta)
        self.visualizador.ponderacion_cambiada.connect(self.actualizar_ponderacion)
        layout.addWidget(self.visualizador, alignment=Qt.AlignCenter)

        # Leyenda
        leyenda = QLabel("""
            <p style='font-size: 11px; color: #6C4E31;'>
            <b>Leyenda:</b><br>
            <span style='color: #d9534f; font-weight: bold;'>[peso] camino ✓</span> = Camino más corto<br>
            <span style='color: #6C4E31;'>[peso] camino</span> = Camino alternativo<br>
            <i>Click en vértices para cambiar etiquetas<br>
            Click en aristas para cambiar ponderaciones</i>
            </p>
        """)
        leyenda.setStyleSheet("background-color: #FFEAC5; padding: 8px; border-radius: 5px;")
        layout.addWidget(leyenda)

        return panel

    def _crear_panel_grafo(self):
        panel = QFrame()
        panel.setStyleSheet("""
            background-color: #FFF3E0;
            border: 2px solid #bf8f62;
            border-radius: 10px;
            padding: 15px;
        """)
        layout = QVBoxLayout(panel)

        # Título
        titulo = QLabel("Construcción del Grafo")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #6C4E31;")
        titulo.setAlignment(Qt.AlignCenter)
        layout.addWidget(titulo)

        # Número de vértices
        vertices_layout = QHBoxLayout()
        label_vertices = QLabel("Nº Vértices:")
        label_vertices.setStyleSheet("font-weight: bold; color: #6C4E31;")
        vertices_layout.addWidget(label_vertices)

        self.spin_vertices = QSpinBox()
        self.spin_vertices.setMinimum(2)
        self.spin_vertices.setMaximum(10)
        self.spin_vertices.setValue(6)
        self.spin_vertices.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        vertices_layout.addWidget(self.spin_vertices)
        layout.addLayout(vertices_layout)

        # Botón crear grafo
        btn_crear = QPushButton("Crear Grafo")
        btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_crear.clicked.connect(self.crear_grafo)
        layout.addWidget(btn_crear)

        layout.addWidget(QLabel("─" * 20))

        # Agregar arista
        titulo_arista = QLabel("Agregar Arista")
        titulo_arista.setStyleSheet("font-weight: bold; color: #6C4E31; font-size: 13px;")
        layout.addWidget(titulo_arista)

        arista_layout = QHBoxLayout()

        self.spin_origen_arista = QSpinBox()
        self.spin_origen_arista.setMinimum(1)
        self.spin_origen_arista.setMaximum(10)
        self.spin_origen_arista.setPrefix("De: ")
        arista_layout.addWidget(self.spin_origen_arista)

        self.spin_destino_arista = QSpinBox()
        self.spin_destino_arista.setMinimum(1)
        self.spin_destino_arista.setMaximum(10)
        self.spin_destino_arista.setPrefix("A: ")
        arista_layout.addWidget(self.spin_destino_arista)

        layout.addLayout(arista_layout)

        btn_agregar_arista = QPushButton("Agregar")
        btn_agregar_arista.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_agregar_arista.clicked.connect(self.agregar_arista)
        layout.addWidget(btn_agregar_arista)

        layout.addWidget(QLabel("─" * 20))

        # Botones de archivo
        btn_guardar = QPushButton("Guardar Grafo")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_grafo)
        layout.addWidget(btn_guardar)

        btn_cargar = QPushButton("Cargar Grafo")
        btn_cargar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_cargar.clicked.connect(self.cargar_grafo)
        layout.addWidget(btn_cargar)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 8px;
                border-radius: 6px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_limpiar.clicked.connect(self.limpiar_grafo)
        layout.addWidget(btn_limpiar)

        layout.addStretch()

        return panel

    def _crear_panel_dijkstra(self):
        panel = QFrame()
        panel.setStyleSheet("""
            background-color: #FFF3E0;
            border: 2px solid #bf8f62;
            border-radius: 10px;
            padding: 15px;
        """)
        layout = QVBoxLayout(panel)

        # Título
        titulo = QLabel("Ejecutar Dijkstra")
        titulo.setStyleSheet("font-size: 16px; font-weight: bold; color: #6C4E31;")
        layout.addWidget(titulo)

        # Selector de vértice origen
        origen_layout = QHBoxLayout()
        label_origen = QLabel("Vértice origen:")
        label_origen.setStyleSheet("font-weight: bold; color: #6C4E31;")
        origen_layout.addWidget(label_origen)

        self.spin_origen = QSpinBox()
        self.spin_origen.setMinimum(1)
        self.spin_origen.setMaximum(10)
        self.spin_origen.setValue(1)
        self.spin_origen.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                font-size: 14px;
            }
        """)
        origen_layout.addWidget(self.spin_origen)
        origen_layout.addStretch()
        layout.addLayout(origen_layout)

        # Botón ejecutar
        btn_ejecutar = QPushButton("Ejecutar Dijkstra")
        btn_ejecutar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 12px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_ejecutar.clicked.connect(self.ejecutar_dijkstra)
        layout.addWidget(btn_ejecutar)

        # Área de proceso
        titulo_proceso = QLabel("Proceso paso a paso")
        titulo_proceso.setStyleSheet("font-size: 14px; font-weight: bold; color: #6C4E31; margin-top: 15px;")
        layout.addWidget(titulo_proceso)

        self.texto_proceso = QTextEdit()
        self.texto_proceso.setReadOnly(True)
        self.texto_proceso.setStyleSheet("""
            background-color: white;
            border: 2px solid #bf8f62;
            border-radius: 8px;
            padding: 10px;
            font-family: 'Courier New';
            font-size: 11px;
            color: #2d1f15;
        """)
        self.texto_proceso.setPlaceholderText("Los pasos del algoritmo aparecerán aquí...")
        layout.addWidget(self.texto_proceso)

        return panel

    def crear_grafo(self):
        """Crea un nuevo grafo"""
        num_vertices = self.spin_vertices.value()
        self.model.crear_grafo(num_vertices)
        self.visualizador.limpiar_resultados()
        self.texto_proceso.clear()
        self._actualizar_visualizacion()
        QMessageBox.information(self, "Éxito", f"Grafo creado con {num_vertices} vértices")

    def _actualizar_visualizacion(self):
        """Actualiza la visualización del grafo"""
        num_vertices = self.model.obtener_num_vertices()

        # Actualizar límites de spin boxes
        self.spin_origen.setMaximum(max(1, num_vertices))
        self.spin_origen_arista.setMaximum(max(1, num_vertices))
        self.spin_destino_arista.setMaximum(max(1, num_vertices))

        # Cargar grafo en visualizador
        if num_vertices > 0:
            self.visualizador.set_grafo(
                num_vertices,
                self.model.obtener_aristas(),
                self.model.obtener_etiquetas(),
                self.model.obtener_ponderaciones_como_lista()
            )
        else:
            self.visualizador.set_grafo(0, [], {}, [])

    def agregar_arista(self):
        """Agrega una arista al grafo"""
        if self.model.obtener_num_vertices() == 0:
            QMessageBox.warning(self, "Error", "Primero crea un grafo")
            return

        origen = self.spin_origen_arista.value() - 1
        destino = self.spin_destino_arista.value() - 1

        if self.model.agregar_arista(origen, destino):
            self.visualizador.limpiar_resultados()
            self._actualizar_visualizacion()
            QMessageBox.information(self, "Éxito", f"Arista agregada: {origen + 1} → {destino + 1}")
        else:
            QMessageBox.warning(self, "Error", "No se pudo agregar la arista")

    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        """Actualiza la etiqueta de un vértice"""
        self.model.actualizar_etiqueta(indice, nueva_etiqueta)

    def actualizar_ponderacion(self, arista, nueva_ponderacion):
        """Actualiza la ponderación de una arista"""
        self.model.actualizar_ponderacion(arista, nueva_ponderacion)

    def guardar_grafo(self):
        """Guarda el grafo en un archivo"""
        if self.model.obtener_num_vertices() == 0:
            QMessageBox.warning(self, "Error", "No hay grafo para guardar")
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Grafo", "", "Archivos de Grafo (*.json)"
        )
        if archivo:
            if self.model.guardar_grafo(archivo):
                QMessageBox.information(self, "Éxito", "Grafo guardado correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se pudo guardar el grafo")

    def cargar_grafo(self):
        """Carga un grafo desde un archivo"""
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Cargar Grafo", "", "Archivos de Grafo (*.json)"
        )
        if archivo:
            if self.model.cargar_grafo(archivo):
                self.visualizador.limpiar_resultados()
                self.texto_proceso.clear()
                self._actualizar_visualizacion()
                QMessageBox.information(self, "Éxito", "Grafo cargado correctamente")
            else:
                QMessageBox.warning(self, "Error", "No se pudo cargar el grafo")

    def limpiar_grafo(self):
        """Limpia el grafo actual"""
        self.model.crear_grafo(0)
        self.visualizador.limpiar_resultados()
        self.texto_proceso.clear()
        self._actualizar_visualizacion()

    def ejecutar_dijkstra(self):
        """Ejecuta el algoritmo de Dijkstra"""
        num_vertices = self.model.obtener_num_vertices()
        if num_vertices == 0:
            QMessageBox.warning(self, "Error", "Primero crea un grafo")
            return

        # Verificar pesos
        valido, mensaje = self.controller.verificar_pesos_validos()
        if not valido:
            QMessageBox.warning(self, "Error", mensaje)
            return

        # Obtener vértice origen
        origen = self.spin_origen.value() - 1

        # Ejecutar algoritmo
        distancias, predecesores, todos_caminos, proceso = self.controller.ejecutar_dijkstra(origen)

        if distancias is None:
            QMessageBox.warning(self, "Error", "Error al ejecutar Dijkstra")
            return

        # Actualizar visualización con resultados
        self.visualizador.set_resultado_dijkstra(distancias, todos_caminos, origen)

        # Mostrar proceso
        self.texto_proceso.setPlainText('\n'.join(proceso))

    def showEvent(self, event):
        """Se llama cuando se muestra la ventana"""
        super().showEvent(event)
        self._actualizar_visualizacion()


