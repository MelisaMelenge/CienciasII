from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout, QSpinBox, QMessageBox,
    QDialog, QComboBox, QLineEdit, QFileDialog
)
from PySide6.QtCore import Qt
from Vista.visualizador_grafo_dirigido import VisualizadorGrafoDirigido
import json


class DialogoAgregarArista(QDialog):
    def __init__(self, num_vertices, etiquetas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Agregar Arista")
        self.setModal(True)
        self.resize(300, 180)

        layout = QVBoxLayout(self)

        # Origen
        layout.addWidget(QLabel("Vértice Origen:"))
        self.combo_origen = QComboBox()
        for i in range(num_vertices):
            etiqueta = etiquetas.get(i, str(i + 1))
            self.combo_origen.addItem(f"{etiqueta} ({i+1})", i)
        layout.addWidget(self.combo_origen)

        # Destino
        layout.addWidget(QLabel("Vértice Destino:"))
        self.combo_destino = QComboBox()
        for i in range(num_vertices):
            etiqueta = etiquetas.get(i, str(i + 1))
            self.combo_destino.addItem(f"{etiqueta} ({i+1})", i)
        layout.addWidget(self.combo_destino)

        # Ponderación
        layout.addWidget(QLabel("Ponderación (opcional):"))
        self.input_ponderacion = QLineEdit()
        self.input_ponderacion.setPlaceholderText("Dejar vacío o ingresar valor")
        layout.addWidget(self.input_ponderacion)

        # Botones
        botones = QHBoxLayout()
        btn_aceptar = QPushButton("Agregar")
        btn_aceptar.clicked.connect(self.accept)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)

        btn_aceptar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #bf8f62;
            }
        """)

        botones.addWidget(btn_aceptar)
        botones.addWidget(btn_cancelar)
        layout.addLayout(botones)

    def obtener_datos(self):
        origen = self.combo_origen.currentData()
        destino = self.combo_destino.currentData()
        ponderacion = self.input_ponderacion.text().strip()
        return origen, destino, ponderacion


class DialogoEliminarArista(QDialog):
    def __init__(self, aristas, etiquetas, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Eliminar Arista")
        self.setModal(True)
        self.resize(300, 150)

        layout = QVBoxLayout(self)

        layout.addWidget(QLabel("Selecciona la arista a eliminar:"))

        self.combo_aristas = QComboBox()
        for arista in aristas:
            origen, destino = arista
            etiq_origen = etiquetas.get(origen, str(origen + 1))
            etiq_destino = etiquetas.get(destino, str(destino + 1))
            self.combo_aristas.addItem(f"{etiq_origen} → {etiq_destino}", arista)
        layout.addWidget(self.combo_aristas)

        # Botones
        botones = QHBoxLayout()
        btn_eliminar = QPushButton("Eliminar")
        btn_eliminar.clicked.connect(self.accept)
        btn_cancelar = QPushButton("Cancelar")
        btn_cancelar.clicked.connect(self.reject)

        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #a0522d;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #8B4513;
            }
        """)
        btn_cancelar.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
            }
            QPushButton:hover {
                background-color: #bf8f62;
            }
        """)

        botones.addWidget(btn_eliminar)
        botones.addWidget(btn_cancelar)
        layout.addLayout(botones)

    def obtener_arista(self):
        return self.combo_aristas.currentData()


class Floyd(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.setWindowTitle("Algoritmo de Floyd")
        self.setGeometry(150, 80, 1300, 750)

        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)

        # Header
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62);
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Algoritmo de Floyd (Alcance)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 24px; font-weight: bold; color: #2d1f15; margin: 10px;")
        header_layout.addWidget(titulo)

        # Botón regresar
        btn_regresar = QPushButton("← Regresar a Grafos")
        btn_regresar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_regresar.clicked.connect(lambda: self.cambiar_ventana("grafos"))
        header_layout.addWidget(btn_regresar, alignment=Qt.AlignLeft)

        layout.addWidget(header)

        # Controles superiores - MÁS COMPACTO
        controles = QFrame()
        controles.setStyleSheet("""
            background-color: #FFF3E0;
            border: 2px solid #bf8f62;
            border-radius: 8px;
            padding: 8px;
        """)
        controles_layout = QHBoxLayout(controles)
        controles_layout.setSpacing(8)

        # Crear grafo
        label_vertices = QLabel("Vértices:")
        label_vertices.setStyleSheet("color: #2d1f15; font-weight: bold; font-size: 11px;")
        self.spin_vertices = QSpinBox()
        self.spin_vertices.setRange(2, 8)
        self.spin_vertices.setValue(4)
        self.spin_vertices.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 4px;
                padding: 4px;
                color: #2d1f15;
                min-width: 50px;
            }
        """)

        btn_crear = QPushButton("Crear")
        btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_crear.clicked.connect(self.crear_grafo)

        btn_agregar = QPushButton("+ Arista")
        btn_agregar.setStyleSheet("""
            QPushButton {
                background-color: #8B6342;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #9c724a;
            }
        """)
        btn_agregar.clicked.connect(self.agregar_arista)

        btn_eliminar = QPushButton("- Arista")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #a0522d;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #8B4513;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_arista)

        btn_limpiar = QPushButton("Limpiar")
        btn_limpiar.setStyleSheet("""
            QPushButton {
                background-color: #bf8f62;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #d4a574;
            }
        """)
        btn_limpiar.clicked.connect(self.limpiar_aristas)

        btn_guardar = QPushButton("Guardar")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #bf8f62;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_grafo)

        btn_cargar = QPushButton("Cargar")
        btn_cargar.setStyleSheet("""
            QPushButton {
                background-color: #9c724a;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 11px;
            }
            QPushButton:hover {
                background-color: #bf8f62;
            }
        """)
        btn_cargar.clicked.connect(self.cargar_grafo)

        # Separador vertical
        separador = QFrame()
        separador.setFrameShape(QFrame.VLine)
        separador.setStyleSheet("color: #bf8f62;")

        btn_ejecutar = QPushButton("Ejecutar Algoritmo")
        btn_ejecutar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_ejecutar.clicked.connect(self.ejecutar_algoritmo)

        controles_layout.addWidget(label_vertices)
        controles_layout.addWidget(self.spin_vertices)
        controles_layout.addWidget(btn_crear)
        controles_layout.addWidget(btn_agregar)
        controles_layout.addWidget(btn_eliminar)
        controles_layout.addWidget(btn_limpiar)
        controles_layout.addWidget(btn_guardar)
        controles_layout.addWidget(btn_cargar)
        controles_layout.addWidget(separador)
        controles_layout.addWidget(btn_ejecutar)
        controles_layout.addStretch()

        layout.addWidget(controles)

        # Área de contenido
        contenido = QWidget()
        contenido_layout = QHBoxLayout(contenido)

        # Columna izquierda - Grafo
        columna_izq = QWidget()
        columna_izq_layout = QVBoxLayout(columna_izq)

        self.visualizador = VisualizadorGrafoDirigido("Grafo Dirigido", es_editable=True, ancho=380, alto=380)
        columna_izq_layout.addWidget(self.visualizador)

        instrucciones = QLabel(
            "• Crea el grafo y agrega aristas\n"
            "• Clic en vértices para cambiar etiquetas\n"
            "• Clic en aristas para agregar ponderaciones\n"
            "• Ejecuta el algoritmo para ver resultados"
        )
        instrucciones.setStyleSheet("""
            color: #6C4E31;
            font-size: 10px;
            padding: 6px;
            background-color: #FFF3E0;
            border: 1px solid #bf8f62;
            border-radius: 4px;
        """)
        instrucciones.setAlignment(Qt.AlignLeft)
        columna_izq_layout.addWidget(instrucciones)

        contenido_layout.addWidget(columna_izq)

        # Columna derecha - Matrices
        self.scroll_matrices = QScrollArea()
        self.scroll_matrices.setWidgetResizable(True)
        self.scroll_matrices.setStyleSheet("""
            QScrollArea {
                background-color: #FFF3E0;
                border: 2px solid #bf8f62;
                border-radius: 8px;
            }
        """)

        self.widget_matrices = QWidget()
        self.layout_matrices = QVBoxLayout(self.widget_matrices)
        self.layout_matrices.setAlignment(Qt.AlignTop)

        self.scroll_matrices.setWidget(self.widget_matrices)
        contenido_layout.addWidget(self.scroll_matrices)

        contenido_layout.setStretch(0, 1)
        contenido_layout.setStretch(1, 2)

        layout.addWidget(contenido)

        # Mensaje inicial
        self.mostrar_mensaje_inicial()

    def mostrar_mensaje_inicial(self):
        self.limpiar_matrices()

        mensaje = QLabel(
            "Crea un grafo y ejecuta el algoritmo\n\n"
            "El algoritmo de Floyd calcula el alcance entre todos\n"
            "los pares de vértices y muestra las ponderaciones\n"
            "de los caminos encontrados"
        )
        mensaje.setStyleSheet("""
            color: #6C4E31;
            font-size: 14px;
            padding: 20px;
        """)
        mensaje.setAlignment(Qt.AlignCenter)
        self.layout_matrices.addWidget(mensaje)

    def crear_grafo(self):
        n = self.spin_vertices.value()
        self.visualizador.set_grafo(n, [])
        self.limpiar_matrices()
        self.mostrar_mensaje_inicial()

    def agregar_arista(self):
        if self.visualizador.num_vertices == 0:
            QMessageBox.warning(self, "Advertencia", "Primero crea un grafo")
            return

        dialogo = DialogoAgregarArista(
            self.visualizador.num_vertices,
            self.visualizador.etiquetas,
            self
        )

        if dialogo.exec() == QDialog.Accepted:
            origen, destino, ponderacion = dialogo.obtener_datos()

            # Verificar si la arista ya existe
            if (origen, destino) in self.visualizador.aristas:
                QMessageBox.warning(self, "Advertencia", "Esta arista ya existe")
                return

            # Agregar arista
            self.visualizador.aristas.append((origen, destino))

            # Agregar ponderación si existe
            if ponderacion:
                self.visualizador.ponderaciones[(origen, destino)] = ponderacion

            self.visualizador.update()
            QMessageBox.information(self, "Éxito", "Arista agregada correctamente")

    def eliminar_arista(self):
        if not self.visualizador.aristas:
            QMessageBox.warning(self, "Advertencia", "No hay aristas para eliminar")
            return

        dialogo = DialogoEliminarArista(
            self.visualizador.aristas,
            self.visualizador.etiquetas,
            self
        )

        if dialogo.exec() == QDialog.Accepted:
            arista = dialogo.obtener_arista()

            # Eliminar arista
            self.visualizador.aristas.remove(arista)

            # Eliminar ponderación si existe
            if arista in self.visualizador.ponderaciones:
                del self.visualizador.ponderaciones[arista]

            self.visualizador.update()
            QMessageBox.information(self, "Éxito", "Arista eliminada correctamente")

    def limpiar_aristas(self):
        if not self.visualizador.aristas:
            QMessageBox.information(self, "Información", "No hay aristas para limpiar")
            return

        respuesta = QMessageBox.question(
            self,
            "Confirmar",
            "¿Estás seguro de eliminar todas las aristas?",
            QMessageBox.Yes | QMessageBox.No
        )

        if respuesta == QMessageBox.Yes:
            self.visualizador.aristas = []
            self.visualizador.ponderaciones = {}
            self.visualizador.update()
            QMessageBox.information(self, "Éxito", "Todas las aristas han sido eliminadas")

    def guardar_grafo(self):
        if self.visualizador.num_vertices == 0:
            QMessageBox.warning(self, "Advertencia", "No hay grafo para guardar")
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar Grafo",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if archivo:
            try:
                datos = {
                    'num_vertices': self.visualizador.num_vertices,
                    'aristas': self.visualizador.aristas,
                    'etiquetas': self.visualizador.etiquetas,
                    'ponderaciones': {f"{k[0]},{k[1]}": v for k, v in self.visualizador.ponderaciones.items()}
                }

                with open(archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos, f, indent=2, ensure_ascii=False)

                QMessageBox.information(self, "Éxito", "Grafo guardado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al guardar: {str(e)}")

    def cargar_grafo(self):
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar Grafo",
            "",
            "JSON Files (*.json);;All Files (*)"
        )

        if archivo:
            try:
                with open(archivo, 'r', encoding='utf-8') as f:
                    datos = json.load(f)

                num_vertices = datos['num_vertices']
                aristas = [tuple(a) for a in datos['aristas']]
                etiquetas = {int(k): v for k, v in datos['etiquetas'].items()}
                ponderaciones_dict = datos.get('ponderaciones', {})
                ponderaciones = {tuple(map(int, k.split(','))): v for k, v in ponderaciones_dict.items()}

                self.spin_vertices.setValue(num_vertices)
                self.visualizador.set_grafo(num_vertices, aristas, etiquetas, ponderaciones)

                self.limpiar_matrices()
                self.mostrar_mensaje_inicial()

                QMessageBox.information(self, "Éxito", "Grafo cargado correctamente")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Error al cargar: {str(e)}")

    def limpiar_matrices(self):
        while self.layout_matrices.count():
            child = self.layout_matrices.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def ejecutar_algoritmo(self):
        if self.visualizador.num_vertices == 0:
            QMessageBox.warning(self, "Advertencia", "Primero crea un grafo")
            return

        if not self.visualizador.aristas:
            QMessageBox.warning(self, "Advertencia", "El grafo no tiene aristas")
            return

        from Controlador.Algoritmos.FloydController import FloydController

        controller = FloydController(
            self.visualizador.num_vertices,
            self.visualizador.aristas,
            self.visualizador.etiquetas,
            self.visualizador.ponderaciones
        )

        iteraciones = controller.ejecutar()
        self.mostrar_iteraciones(iteraciones)

    def mostrar_iteraciones(self, iteraciones):
        self.limpiar_matrices()

        for idx, iteracion in enumerate(iteraciones):
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: white;
                    border: 2px solid #bf8f62;
                    border-radius: 8px;
                    padding: 10px;
                    margin: 5px;
                }
            """)
            frame_layout = QVBoxLayout(frame)

            # Título de la iteración
            if idx == 0:
                titulo = QLabel("Matriz Inicial")
            else:
                titulo = QLabel(f"Iteración k = {idx}")

            titulo.setStyleSheet("color: #6C4E31; font-weight: bold; font-size: 14px;")
            titulo.setAlignment(Qt.AlignCenter)
            frame_layout.addWidget(titulo)

            # Información adicional
            if 'info' in iteracion:
                info_label = QLabel(iteracion['info'])
                info_label.setStyleSheet("color: #9c724a; font-size: 12px;")
                info_label.setAlignment(Qt.AlignCenter)
                info_label.setWordWrap(True)
                frame_layout.addWidget(info_label)

            # Matriz de ponderaciones
            matriz_widget = self.crear_matriz_widget(
                iteracion['matriz_distancias'],
                iteracion.get('etiquetas', {}),
                iteracion.get('cambios_distancias', [])
            )
            frame_layout.addWidget(matriz_widget)

            self.layout_matrices.addWidget(frame)

    def crear_matriz_widget(self, matriz, etiquetas, cambios):
        widget = QWidget()
        layout_principal = QVBoxLayout(widget)
        layout_principal.setContentsMargins(5, 5, 5, 5)

        grid = QGridLayout()
        grid.setSpacing(2)

        n = len(matriz)

        # Encabezados de columnas
        grid.addWidget(QLabel(""), 0, 0)
        for j in range(n):
            label = QLabel(etiquetas.get(j, str(j + 1)))
            label.setStyleSheet("""
                background-color: #bf8f62;
                color: white;
                font-weight: bold;
                padding: 5px;
                border-radius: 3px;
            """)
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, 0, j + 1)

        # Filas
        for i in range(n):
            # Encabezado de fila
            label = QLabel(etiquetas.get(i, str(i + 1)))
            label.setStyleSheet("""
                background-color: #bf8f62;
                color: white;
                font-weight: bold;
                padding: 5px;
                border-radius: 3px;
            """)
            label.setAlignment(Qt.AlignCenter)
            grid.addWidget(label, i + 1, 0)

            # Celdas
            for j in range(n):
                valor = matriz[i][j]

                if valor == float('inf'):
                    texto = "∞"
                elif isinstance(valor, float):
                    if valor == int(valor):
                        texto = str(int(valor))
                    else:
                        texto = str(valor)
                elif isinstance(valor, str):
                    texto = valor
                else:
                    texto = str(valor)

                cell = QLabel(texto)
                cell.setAlignment(Qt.AlignCenter)
                cell.setMinimumSize(40, 30)

                # Colorear cambios
                if (i, j) in cambios:
                    cell.setStyleSheet("""
                        background-color: #d4a574;
                        color: #2d1f15;
                        font-weight: bold;
                        padding: 5px;
                        border: 2px solid #a0522d;
                        border-radius: 3px;
                    """)
                elif i == j:
                    cell.setStyleSheet("""
                        background-color: #e8d4b8;
                        color: #2d1f15;
                        padding: 5px;
                        border: 1px solid #bf8f62;
                        border-radius: 3px;
                    """)
                else:
                    cell.setStyleSheet("""
                        background-color: #FFF3E0;
                        color: #2d1f15;
                        padding: 5px;
                        border: 1px solid #bf8f62;
                        border-radius: 3px;
                    """)

                grid.addWidget(cell, i + 1, j + 1)

        layout_principal.addLayout(grid)
        return widget
