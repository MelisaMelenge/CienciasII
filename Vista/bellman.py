from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QTextEdit, QComboBox, QSpinBox, QMessageBox,
    QFileDialog, QInputDialog
)
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
import sys
import os
import json

sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from Vista.visualizador_grafo_dirigido import VisualizadorGrafoDirigido
from Controlador.Algoritmos.BellmanController import BellmanController


class Bellman(QMainWindow):
    """Ventana principal del algoritmo de Bellman"""

    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        # Inicializar el controlador
        self.controller = BellmanController(self)

        self.setWindowTitle("Algoritmo de Bellman")
        self.setGeometry(200, 100, 1400, 750)

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
        header.setMaximumHeight(120)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Algoritmo de Bellman")
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

        layout.addWidget(header)

        # Contenedor principal
        contenedor_principal = QHBoxLayout()

        # Panel izquierdo - Grafos y Controles
        panel_izquierdo = QVBoxLayout()

        # Controles de creación del grafo
        controles_frame = QFrame()
        controles_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF3E0;
                border: 2px solid #bf8f62;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        controles_layout = QVBoxLayout(controles_frame)

        # Fila 1: Crear grafo
        fila1 = QHBoxLayout()

        label_vertices = QLabel("Vértices:")
        label_vertices.setStyleSheet("color: #6C4E31; font-weight: bold; font-size: 12px;")
        fila1.addWidget(label_vertices)

        self.spin_vertices = QSpinBox()
        self.spin_vertices.setMinimum(1)
        self.spin_vertices.setMaximum(20)
        self.spin_vertices.setValue(6)
        self.spin_vertices.setStyleSheet("""
            QSpinBox {
                background-color: #FFEAC5;
                border: 2px solid #9c724a;
                border-radius: 6px;
                padding: 5px;
                font-size: 12px;
            }
        """)
        fila1.addWidget(self.spin_vertices)

        btn_crear = QPushButton("Crear Grafo")
        btn_crear.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_crear.clicked.connect(self.crear_grafo)
        fila1.addWidget(btn_crear)

        controles_layout.addLayout(fila1)

        # Fila 2: Conectar vértices
        fila2 = QHBoxLayout()

        label_origen_arista = QLabel("Origen:")
        label_origen_arista.setStyleSheet("color: #6C4E31; font-weight: bold; font-size: 12px;")
        fila2.addWidget(label_origen_arista)

        self.combo_origen_arista = QComboBox()
        self.combo_origen_arista.setStyleSheet("""
            QComboBox {
                background-color: #FFEAC5;
                border: 2px solid #9c724a;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
            }
        """)
        fila2.addWidget(self.combo_origen_arista)

        label_destino_arista = QLabel("Destino:")
        label_destino_arista.setStyleSheet("color: #6C4E31; font-weight: bold; font-size: 12px;")
        fila2.addWidget(label_destino_arista)

        self.combo_destino_arista = QComboBox()
        self.combo_destino_arista.setStyleSheet("""
            QComboBox {
                background-color: #FFEAC5;
                border: 2px solid #9c724a;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
            }
        """)
        fila2.addWidget(self.combo_destino_arista)

        label_peso = QLabel("Peso:")
        label_peso.setStyleSheet("color: #6C4E31; font-weight: bold; font-size: 12px;")
        fila2.addWidget(label_peso)

        self.spin_peso = QSpinBox()
        self.spin_peso.setMinimum(-99)
        self.spin_peso.setMaximum(99)
        self.spin_peso.setValue(1)
        self.spin_peso.setStyleSheet("""
            QSpinBox {
                background-color: #FFEAC5;
                border: 2px solid #9c724a;
                border-radius: 6px;
                padding: 4px;
                font-size: 12px;
            }
        """)
        fila2.addWidget(self.spin_peso)

        btn_agregar_arista = QPushButton("Agregar Arista")
        btn_agregar_arista.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
        """)
        btn_agregar_arista.clicked.connect(self.agregar_arista)
        fila2.addWidget(btn_agregar_arista)

        controles_layout.addLayout(fila2)

        # Fila 3: Botones de acción
        fila3 = QHBoxLayout()

        btn_eliminar = QPushButton("Eliminar Arista")
        btn_eliminar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_eliminar.clicked.connect(self.eliminar_arista)
        fila3.addWidget(btn_eliminar)

        btn_guardar = QPushButton(" Guardar")
        btn_guardar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_guardar.clicked.connect(self.guardar_grafo)
        fila3.addWidget(btn_guardar)

        btn_cargar = QPushButton("Cargar")
        btn_cargar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: white;
                font-weight: bold;
                padding: 6px 12px;
                border-radius: 6px;
                font-size: 12px;
            }
            QPushButton:hover {
                background-color: #6C4E31;
            }
        """)
        btn_cargar.clicked.connect(self.cargar_grafo)
        fila3.addWidget(btn_cargar)

        controles_layout.addLayout(fila3)

        panel_izquierdo.addWidget(controles_frame)

        # Frame de ejecución
        ejecutar_frame = QFrame()
        ejecutar_frame.setStyleSheet("""
            QFrame {
                background-color: #FFF3E0;
                border: 2px solid #bf8f62;
                border-radius: 8px;
                padding: 10px;
            }
        """)
        ejecutar_layout = QHBoxLayout(ejecutar_frame)

        label_info = QLabel("El algoritmo se ejecutará desde V1 del grafo enumerado:")
        label_info.setStyleSheet("color: #6C4E31; font-weight: bold; font-size: 13px;")
        ejecutar_layout.addWidget(label_info)

        # Botón ejecutar
        self.btn_ejecutar = QPushButton("▶ Ejecutar Bellman (desde V1)")
        self.btn_ejecutar.setStyleSheet("""
            QPushButton {
                background-color: #6C4E31;
                color: #FFEAC5;
                font-weight: bold;
                padding: 8px 16px;
                border-radius: 8px;
                font-size: 13px;
            }
            QPushButton:hover {
                background-color: #8B6342;
            }
            QPushButton:disabled {
                background-color: #cccccc;
                color: #666666;
            }
        """)
        self.btn_ejecutar.clicked.connect(self.ejecutar_algoritmo)
        ejecutar_layout.addWidget(self.btn_ejecutar)

        panel_izquierdo.addWidget(ejecutar_frame)

        # Visualizadores de grafo
        grafos_layout = QHBoxLayout()

        self.grafo_original = VisualizadorGrafoDirigido("Grafo Original", es_editable=True, ancho=380, alto=380)
        self.grafo_original.ponderacion_cambiada.connect(self.on_ponderacion_cambiada)
        grafos_layout.addWidget(self.grafo_original)

        self.grafo_enumerado = VisualizadorGrafoDirigido("Grafo Enumerado", es_editable=False, ancho=380, alto=380)
        grafos_layout.addWidget(self.grafo_enumerado)

        panel_izquierdo.addLayout(grafos_layout)

        contenedor_principal.addLayout(panel_izquierdo, stretch=60)

        # Panel derecho - Resultados
        panel_derecho = QVBoxLayout()

        # Área de iteraciones
        label_iter = QLabel("<b>Proceso de Iteraciones:</b>")
        label_iter.setStyleSheet("color: #6C4E31; font-size: 14px;")
        panel_derecho.addWidget(label_iter)

        self.texto_iteraciones = QTextEdit()
        self.texto_iteraciones.setReadOnly(True)
        self.texto_iteraciones.setStyleSheet("""
            QTextEdit {
                background-color: #FFF3E0;
                border: 2px solid #bf8f62;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                color: #2d1f15;
            }
        """)
        panel_derecho.addWidget(self.texto_iteraciones, stretch=50)

        # Resultado final
        label_resultado = QLabel("<b>Resultado Final:</b>")
        label_resultado.setStyleSheet("color: #6C4E31; font-size: 14px;")
        panel_derecho.addWidget(label_resultado)

        self.texto_resultado = QTextEdit()
        self.texto_resultado.setReadOnly(True)
        self.texto_resultado.setStyleSheet("""
            QTextEdit {
                background-color: #FFF3E0;
                border: 2px solid #bf8f62;
                border-radius: 8px;
                padding: 10px;
                font-family: 'Courier New', monospace;
                font-size: 11px;
                color: #2d1f15;
            }
        """)
        panel_derecho.addWidget(self.texto_resultado, stretch=50)

        contenedor_principal.addLayout(panel_derecho, stretch=40)

        layout.addLayout(contenedor_principal)

        # Crear un grafo inicial por defecto
        self.crear_grafo()

    def set_controller(self, controller):
        """Establece el controlador (ya no es necesario, pero se mantiene por compatibilidad)"""
        self.controller = controller

    def crear_grafo(self):
        """Crea un grafo vacío"""

        num_vertices = self.spin_vertices.value()
        self.controller.crear_grafo_vacio(num_vertices)
        self.actualizar_combos_aristas()


    def agregar_arista(self):
        """Agrega una arista al grafo"""
        print("🔧 Agregando arista...")

        origen = self.combo_origen_arista.currentData()
        destino = self.combo_destino_arista.currentData()
        peso = self.spin_peso.value()

        if origen is None or destino is None:
            QMessageBox.warning(self, "Error", "Seleccione origen y destino")
            return

        self.controller.agregar_arista(origen, destino, peso)
        print(f"✅ Arista agregada: {origen} -> {destino} (peso: {peso})")

    def eliminar_arista(self):
        """Elimina la última arista agregada"""
        print("🔧 Eliminando arista...")
        self.controller.eliminar_ultima_arista()

    def guardar_grafo(self):
        """Guarda el grafo en un archivo JSON"""
        archivo, _ = QFileDialog.getSaveFileName(
            self, "Guardar Grafo", "", "JSON Files (*.json)"
        )

        if archivo:
            self.controller.guardar_grafo(archivo)
            QMessageBox.information(self, "Éxito", "Grafo guardado correctamente")

    def cargar_grafo(self):
        """Carga un grafo desde un archivo JSON"""
        archivo, _ = QFileDialog.getOpenFileName(
            self, "Cargar Grafo", "", "JSON Files (*.json)"
        )

        if archivo:
            self.controller.cargar_grafo_desde_archivo(archivo)
            self.actualizar_combos_aristas()
            QMessageBox.information(self, "Éxito", "Grafo cargado correctamente")

    def actualizar_combos_aristas(self):
        """Actualiza los combos de origen y destino de aristas"""
        self.combo_origen_arista.clear()
        self.combo_destino_arista.clear()

        etiquetas = self.controller.etiquetas_originales
        for i in range(self.controller.num_vertices):
            etiqueta = etiquetas.get(i, chr(65 + i))
            self.combo_origen_arista.addItem(etiqueta, i)
            self.combo_destino_arista.addItem(etiqueta, i)

    def on_ponderacion_cambiada(self, arista, nueva_ponderacion):
        """Maneja el cambio de ponderación desde el visualizador"""
        if self.controller:
            self.controller.actualizar_ponderacion(arista, nueva_ponderacion)

    def ejecutar_algoritmo(self):
        """Ejecuta el algoritmo de Bellman desde V1 automáticamente"""
        if self.controller.num_vertices == 0 or len(self.controller.aristas) == 0:
            QMessageBox.warning(self, "Error", "Debe crear un grafo con aristas primero")
            return

        # CAMBIO: Ejecutar sin parámetros (automáticamente desde V1)
        resultado = self.controller.ejecutar_bellman()

        # Mostrar resultados
        self.mostrar_resultado(resultado)

    def mostrar_resultado(self, resultado):
        """Muestra el resultado del algoritmo"""
        iteraciones = resultado['iteraciones']
        final = resultado['resultado_final']
        ciclo_negativo = resultado['ciclo_negativo']

        # Mostrar iteraciones
        texto_iter = ""
        for iter_info in iteraciones:
            texto_iter += f"<b style='color: #6C4E31;'>λ{iter_info['iteracion']} (Iteración {iter_info['iteracion']}):</b><br>"
            texto_iter += f"<span style='font-family: Courier New;'>Distancias: {iter_info['distancias']}</span><br>"
            if iter_info['cambios']:
                texto_iter += f"<span style='color: #d9534f;'>Cambios: {', '.join(iter_info['cambios'])}</span><br>"
            texto_iter += "<br>"

        self.texto_iteraciones.setHtml(texto_iter)

        # Mostrar resultado final
        if ciclo_negativo:
            self.texto_resultado.setHtml(
                "<h3 style='color: #d9534f;'>⚠ Ciclo Negativo Detectado</h3>"
                "<p>El grafo contiene un ciclo negativo, no existe solución.</p>"
            )
        else:
            texto_final = "<h3 style='color: #6C4E31;'>Caminos Más Cortos desde V1:</h3>"
            texto_final += "<table style='width: 100%; border-collapse: collapse;'>"
            texto_final += "<tr style='background-color: #bf8f62; color: white;'>"
            texto_final += "<th style='padding: 5px; border: 1px solid #9c724a;'>Vértice</th>"
            texto_final += "<th style='padding: 5px; border: 1px solid #9c724a;'>Distancia</th>"
            texto_final += "<th style='padding: 5px; border: 1px solid #9c724a;'>Camino</th>"
            texto_final += "</tr>"

            for i, (v, info) in enumerate(final.items()):
                dist = info['distancia']
                camino = info['camino']

                color_fila = "#FFEAC5" if i % 2 == 0 else "#FFF3E0"
                texto_final += f"<tr style='background-color: {color_fila};'>"
                texto_final += f"<td style='padding: 5px; border: 1px solid #9c724a; text-align: center;'><b>V{v}</b></td>"

                if dist == float('inf'):
                    texto_final += "<td style='padding: 5px; border: 1px solid #9c724a; text-align: center;'>∞</td>"
                    texto_final += "<td style='padding: 5px; border: 1px solid #9c724a; text-align: center;'>-</td>"
                else:
                    texto_final += f"<td style='padding: 5px; border: 1px solid #9c724a; text-align: center;'>{dist}</td>"
                    texto_final += f"<td style='padding: 5px; border: 1px solid #9c724a;'>{camino}</td>"

                texto_final += "</tr>"

            texto_final += "</table>"

            # Mostrar el camino más corto desde V1 hasta el último vértice
            ultimo_v = str(len(final))
            if ultimo_v in final:
                camino_final = final[ultimo_v]['camino']
                distancia_final = resultado['camino_total']

                texto_final += f"<br><hr style='border: 1px solid #bf8f62;'><br>"
                texto_final += f"<h3 style='color: #6C4E31;'> Camino Más Corto (V1 → V{ultimo_v}):</h3>"
                texto_final += f"<p style='font-size: 14px;'><b>Ruta:</b> {camino_final}</p>"
                texto_final += f"<p style='font-size: 14px;'><b>Distancia Total:</b> {distancia_final}</p>"

            self.texto_resultado.setHtml(texto_final)