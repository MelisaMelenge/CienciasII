from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QHBoxLayout, QFileDialog
)
from PySide6.QtCore import Qt
import os
import json
from Vista.dialogo_clave import DialogoClave
from Controlador.Externas.LinealController import LinealExternaController


class LinealExterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = LinealExternaController()

        # Variables para la estructura
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0

        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Lineal Externa")

        # ================== LAYOUT PRINCIPAL ==================
        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # ======= ENCABEZADO =======
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

        titulo = QLabel("Ciencias de la Computación II - Búsqueda Lineal Externa")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2d1f15; margin: 10px;")
        header_layout.addWidget(titulo)

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
                }
                QPushButton:hover {
                    color: #FFEAC5;
                    background-color: #6C4E31;
                    border-radius: 8px;
                }
            """)
            menu_layout.addWidget(btn)

        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        header_layout.addLayout(menu_layout)
        layout.addWidget(header)

        # ======= CONTROLES SUPERIORES =======
        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)

        lbl_claves = QLabel("Número de claves (N):")
        lbl_digitos = QLabel("Número de dígitos:")

        for lbl in (lbl_claves, lbl_digitos):
            lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #2d1f15;")

        self.num_claves_input = QSpinBox()
        self.num_claves_input.setRange(2, 100)
        self.num_claves_input.setValue(10)
        self.num_claves_input.setFixedWidth(100)
        self.num_claves_input.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                color: #2d1f15;
            }
            QSpinBox:hover {
                border: 2px solid #6C4E31;
            }
        """)

        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(100)
        self.digitos.setStyleSheet("""
            QSpinBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                color: #2d1f15;
            }
            QSpinBox:hover {
                border: 2px solid #6C4E31;
            }
        """)

        fila_controles.addWidget(lbl_claves)
        fila_controles.addWidget(self.num_claves_input)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.digitos)

        layout.addLayout(fila_controles)

        # ======= BOTONES =======
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_insertar = QPushButton("Insertar claves")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_buscar_clave = QPushButton("Buscar clave")

        botones = (
            self.btn_crear, self.btn_insertar, self.btn_guardar,
            self.btn_cargar, self.btn_eliminar, self.btn_deshacer,
            self.btn_eliminar_clave, self.btn_buscar_clave
        )
        for btn in botones:
            btn.setFixedHeight(50)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9c724a;
                    color: #2d1f15;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #bf8f62;
                }
            """)

        grid_botones = QGridLayout()
        grid_botones.setSpacing(15)
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_insertar, 0, 1)
        grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)
        layout.addLayout(grid_botones)

        # ======= VISUALIZACIÓN =======
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("background-color: transparent;")
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(10)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        self.setCentralWidget(central)

        # ======= CONEXIONES =======
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_insertar.clicked.connect(self.insertar_clave)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)

    # ================== FUNCIONALIDAD ==================

    def crear_estructura(self):
        """Crea la estructura de bloques según N claves"""
        try:
            num_claves = self.num_claves_input.value()
            datos = self.controller.crear_estructura(num_claves)
            self.bloques = datos['bloques']
            self.num_claves = datos['num_claves']
            self.tamanio_bloque = datos['tamanio_bloque']
            self.actualizar_visualizacion()

            DialogoClave(0, "Estructura Creada", "mensaje", self,
                         f"Estructura creada exitosamente:\n\n"
                         f"• N (claves totales): {self.num_claves}\n"
                         f"• B (tamaño de bloque): {self.tamanio_bloque}\n"
                         f"• Número de bloques: {len(self.bloques)}").exec()
        except Exception as e:
            DialogoClave(0, "Error", "mensaje", self,
                         f"Error al crear estructura: {str(e)}").exec()

    def actualizar_visualizacion(self):
        """Actualiza la visualización de los bloques"""
        while self.contenedor_layout.count():
            child = self.contenedor_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.bloques:
            label = QLabel("No hay estructura creada.")
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-size: 16px; color: #6C4E31; padding: 40px;")
            self.contenedor_layout.addWidget(label)
            return

        info_label = QLabel(
            f"Estructura lineal externa | Claves: {self.num_claves} | "
            f"Tamaño de bloque: {self.tamanio_bloque} | Bloques: {len(self.bloques)}"
        )
        info_label.setAlignment(Qt.AlignCenter)
        info_label.setStyleSheet("""
            font-size: 18px;
            font-weight: bold;
            color: #2d1f15;
            background-color: #FFDBB5;
            padding: 10px;
            border: 2px solid #bf8f62;
            border-radius: 8px;
            margin-bottom: 20px;
        """)
        self.contenedor_layout.addWidget(info_label)

        bloques_container = QWidget()
        bloques_layout = QHBoxLayout(bloques_container)
        bloques_layout.setSpacing(30)
        bloques_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        bloques_layout.setContentsMargins(20, 20, 20, 20)

        bloques_dibujados = 0
        for i, bloque in enumerate(self.bloques):
            if any(c is not None for c in bloque):
                bloque_widget = self.crear_bloque_visual(i, bloque)
                bloques_layout.addWidget(bloque_widget)
                bloques_dibujados += 1

        if bloques_dibujados == 0:
            ejemplo = self.crear_bloque_visual(0, [None] * self.tamanio_bloque)
            bloques_layout.addWidget(ejemplo)

        bloques_layout.addStretch()
        self.contenedor_layout.addWidget(bloques_container)

    def crear_bloque_visual(self, indice, bloque):
        """Crea la representación visual de un bloque"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(3)
        container_layout.setContentsMargins(0, 0, 0, 0)

        frame = QFrame()
        layout = QHBoxLayout(frame)
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        for i in range(self.tamanio_bloque):
            celda = QFrame()
            celda_layout = QVBoxLayout(celda)
            celda_layout.setContentsMargins(0, 0, 0, 0)

            if i < len(bloque) and bloque[i] is not None:
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #FFDBB5;
                        border: 2px solid #9c724a;
                        min-width: 50px; max-width: 50px;
                        min-height: 50px; max-height: 50px;
                    }
                """)
                label_clave = QLabel(str(bloque[i]))
                label_clave.setAlignment(Qt.AlignCenter)
                label_clave.setStyleSheet("font-size: 12px; font-weight: bold; color: #2d1f15;")
                celda_layout.addWidget(label_clave)
            else:
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #FFF3E0;
                        border: 2px solid #bf8f62;
                        min-width: 50px; max-width: 50px;
                        min-height: 50px; max-height: 50px;
                    }
                """)

            layout.addWidget(celda)

        container_layout.addWidget(frame)

        num_bloque = QLabel(f"Bloque {indice + 1}")
        num_bloque.setAlignment(Qt.AlignCenter)
        num_bloque.setStyleSheet("font-size: 11px; font-weight: bold; color: #6C4E31;")
        container_layout.addWidget(num_bloque)

        return container

    def insertar_clave(self):
        """Inserta una nueva clave en la estructura"""
        if not self.bloques:
            DialogoClave(0, "Advertencia", "mensaje", self,
                         "Primero debes crear la estructura.").exec()
            return

        # Validar que no se supere el número máximo de claves
        claves_actuales = sum(1 for bloque in self.bloques for c in bloque if c is not None and c != "")
        if claves_actuales >= self.num_claves:
            DialogoClave(0, "Error", "mensaje", self,
                         f"No se pueden insertar más claves.\nLímite: {self.num_claves} claves.").exec()
            return

        dlg = DialogoClave(self.digitos.value(), "Insertar clave", "insertar", self)
        if dlg.exec():
            clave = int(dlg.input.text())
            resultado = self.controller.insertar_clave(clave)

            if resultado["exito"]:
                self.bloques = self.controller.bloques
                self.actualizar_visualizacion()

            DialogoClave(0, "Resultado", "mensaje", self, resultado["mensaje"]).exec()

    def guardar_estructura(self):
        """Guarda la estructura actual en un archivo JSON"""
        if not self.bloques:
            DialogoClave(0, "Advertencia", "mensaje", self,
                         "No hay estructura para guardar.").exec()
            return

        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar estructura", os.getcwd(), "Archivos JSON (*.json)"
        )

        if not ruta:
            return

        try:
            datos = self.controller.exportar_estructura()
            with open(ruta, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4)

            DialogoClave(0, "Éxito", "mensaje", self,
                         f"Estructura guardada en:\n{ruta}").exec()
        except Exception as e:
            DialogoClave(0, "Error", "mensaje", self,
                         f"No se pudo guardar: {str(e)}").exec()

    def cargar_estructura(self):
        """Carga una estructura guardada desde un archivo JSON"""
        ruta, _ = QFileDialog.getOpenFileName(
            self, "Cargar estructura", os.getcwd(), "Archivos JSON (*.json)"
        )

        if not ruta:
            return

        try:
            with open(ruta, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            resultado = self.controller.importar_estructura(datos)

            if resultado["exito"]:
                self.bloques = self.controller.bloques
                self.num_claves = self.controller.num_claves
                self.tamanio_bloque = self.controller.tamanio_bloque
                self.actualizar_visualizacion()
                DialogoClave(0, "Éxito", "mensaje", self, resultado["mensaje"]).exec()
            else:
                DialogoClave(0, "Advertencia", "mensaje", self, resultado["mensaje"]).exec()
        except Exception as e:
            DialogoClave(0, "Error", "mensaje", self,
                         f"No se pudo cargar: {str(e)}").exec()

    def eliminar_estructura(self):
        """Elimina la estructura actual"""
        if not self.bloques:
            DialogoClave(0, "Advertencia", "mensaje", self,
                         "No hay estructura para eliminar.").exec()
            return

        dlg = DialogoClave(0, "Confirmar eliminación", "confirmar", self,
                           "¿Estás seguro de que deseas eliminar la estructura actual?")
        if dlg.exec():
            self.bloques = []
            self.num_claves = 0
            self.tamanio_bloque = 0
            self.actualizar_visualizacion()
            DialogoClave(0, "Éxito", "mensaje", self,
                         "Estructura eliminada correctamente.").exec()

    def buscar_clave(self):
        """Buscar una clave existente"""
        if not self.bloques:
            DialogoClave(0, "Advertencia", "mensaje", self,
                         "Primero debes crear la estructura.").exec()
            return

        dlg = DialogoClave(self.digitos.value(), "Buscar clave", "buscar", self)
        if dlg.exec():
            clave = int(dlg.input.text())
            resultado = self.controller.buscar_clave(clave)
            DialogoClave(0, "Resultado de búsqueda", "mensaje", self,
                         resultado["mensaje"]).exec()

    def eliminar_clave(self):
        """Elimina una clave solicitándola por diálogo y actualiza la vista"""
        if not self.bloques:
            DialogoClave(0, "Advertencia", "mensaje", self,
                         "Primero debes crear la estructura.").exec()
            return

        dlg = DialogoClave(self.digitos.value(), "Eliminar clave", "eliminar", self)
        if dlg.exec():
            try:
                clave = int(dlg.input.text())
            except Exception:
                DialogoClave(0, "Error", "mensaje", self, "Clave inválida.").exec()
                return

            resultado = self.controller.eliminar_clave(clave)

            if resultado.get("exito"):
                self.bloques = self.controller.bloques
                self.num_claves = self.controller.num_claves
                self.tamanio_bloque = self.controller.tamanio_bloque
                self.actualizar_visualizacion()

            DialogoClave(0, "Resultado", "mensaje", self, resultado["mensaje"]).exec()

    def deshacer(self):
        """Deshace la última operación"""
        resultado = self.controller.deshacer()
        if resultado["exito"]:
            self.bloques = resultado["bloques"]
            self.actualizar_visualizacion()
        DialogoClave(0, "Deshacer", "mensaje", self, resultado["mensaje"]).exec()

    def compactar_bloques(self):
        """Reacomoda las claves en los bloques para eliminar huecos"""
        todas = [x for bloque in self.bloques for x in bloque if x is not None]

        for bloque in self.bloques:
            bloque.clear()

        idx = 0
        for bloque in self.bloques:
            for _ in range(self.tamanio_bloque):
                if idx < len(todas):
                    bloque.append(todas[idx])
                    idx += 1
                else:
                    bloque.append(None)