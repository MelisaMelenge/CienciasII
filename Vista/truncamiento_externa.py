from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QHBoxLayout, QFileDialog, QMessageBox
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Externas.TruncamientoController import TruncamientoController
from .dialogo_posiciones import DialogoPosiciones

class TruncamientoExterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = TruncamientoController()
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.posiciones_fijas = None

        self.setWindowTitle("Ciencias de la Computación II - Método Módulo (Externa)")

        central = QWidget()
        layout = QVBoxLayout(central)
        layout.setSpacing(20)

        # ======= HEADER =======
        header = QFrame()
        header.setStyleSheet("""
               background: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0,
                   stop:0 #C4B5FD, stop:1 #7C3AED);
               border-radius: 12px;
           """)
        header_layout = QVBoxLayout(header)
        titulo = QLabel("Ciencias de la Computación II - Método Truncamiento (Externa)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
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
                       color: white;
                       font-size: 16px;
                       font-weight: bold;
                       border: none;
                   }
                   QPushButton:hover { color: #EDE9FF; text-decoration: underline; }
               """)
            menu_layout.addWidget(btn)
        header_layout.addLayout(menu_layout)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        layout.addWidget(header)

        # ======= CONTROLES =======
        self.num_claves_input = QSpinBox()
        self.num_claves_input.setRange(2, 1000)
        self.num_claves_input.setValue(20)
        self.num_claves_input.setFixedWidth(120)

        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(100)

        lbl_claves = QLabel("Número de claves (N):")
        lbl_digitos = QLabel("Número de dígitos:")
        for lbl in (lbl_claves, lbl_digitos):
            lbl.setStyleSheet("font-size: 16px; font-weight: bold; color: #4C1D95;")

        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)
        fila_controles.addWidget(lbl_claves)
        fila_controles.addWidget(self.num_claves_input)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.digitos)
        layout.addLayout(fila_controles)

        # ======= BOTONES =======
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_insertar = QPushButton("Insertar clave")
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
            btn.setStyleSheet("""
                   QPushButton {
                       background-color: #7C3AED;
                       color: white;
                       padding: 8px 16px;
                       font-size: 14px;
                       border-radius: 8px;
                   }
                   QPushButton:hover { background-color: #6D28D9; }
               """)

        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_insertar, 0, 1)
        grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)
        layout.addLayout(grid_botones)

        # ======= AREA DE VISUALIZACION =======
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(12)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
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

        # ==================== FUNCIONES ====================

    def crear_estructura(self):
        """Crea la estructura de bloques según N claves"""
        try:
            num_claves = self.num_claves_input.value()
            datos = self.controller.crear_estructura(num_claves)
            self.bloques = datos['bloques']
            self.num_claves = datos['num_claves']
            self.tamanio_bloque = datos['tamanio_bloque']
            self.posiciones_fijas = None

            self.actualizar_visualizacion()
            QMessageBox.information(
                self,
                "Estructura Creada",
                f"Estructura creada exitosamente:\n\n"
                f"• N (claves totales): {self.num_claves}\n"
                f"• B (tamaño de bloque): {self.tamanio_bloque}\n"
                f"• Número de bloques: {len(self.bloques)}"
            )
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Error al crear estructura: {str(e)}")

    def insertar_clave(self):
        # 1️⃣ Pedir la clave completa
        dlg = DialogoClave(self.digitos.value(), "Insertar clave", "insertar", self)
        if not dlg.exec():
            return
        clave = dlg.get_clave()  # Ejemplo: "2835"

        # 2️⃣ Usar las posiciones fijas si ya existen, si no, pedirlas una vez
        if self.posiciones_fijas is None:
            dlg_pos = DialogoPosiciones(len(clave), 2, self)
            if not dlg_pos.exec():
                return
            self.posiciones_fijas = dlg_pos.get_posiciones(2)
            QMessageBox.information(
                self,
                "Posiciones fijas establecidas",
                f"Posiciones seleccionadas: {self.posiciones_fijas}\n\n"
                "Estas posiciones se usarán para todas las claves "
                "hasta que se cree una nueva estructura."
            )

        posiciones = self.posiciones_fijas

        # 3️⃣ Crear versión truncada (solo para mostrar)
        clave_s = str(clave).zfill(self.digitos.value())
        truncada = "".join(clave_s[i - 1] for i in posiciones)
        truncada_int = int(truncada)

        # 4️⃣ Insertar pasando la clave original y las posiciones fijas
        res = self.controller.insertar_clave(clave, posiciones)

        # 5️⃣ Manejo de colisiones y mensajes
        if isinstance(res, tuple) and len(res) == 3 and res[1] == "collision":
            info = res[2]
            detalle = (
                f"Colisión detectada para la clave {info['clave']}.\n\n"
                f"Hash bloque: {info['hash_bloque']} (bloque {info['bloque_objetivo']})\n"
                f"Hash posición: {info['hash_pos']} (posición {info['pos_objetivo']})\n\n"
                "¿Deseas insertar la clave en la Zona de Colisiones?"
            )
            reply = QMessageBox.question(self, "Colisión detectada", detalle, QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                ok, msg = self.controller.insertar_en_zona_colisiones(info["clave"])
                if ok:
                    QMessageBox.information(self, "Zona de colisiones", msg)
                else:
                    QMessageBox.warning(self, "Zona de colisiones", msg)
        else:
            ok, msg = res
            if ok:
                QMessageBox.information(self, "Insertar clave", msg)
            else:
                QMessageBox.warning(self, "Insertar clave", msg)

        # 6️⃣ Actualizar visualización
        self.bloques = self.controller.bloques
        self.actualizar_visualizacion()

    def buscar_clave(self):
        dlg = DialogoClave(self.digitos.value(), "Buscar clave", "buscar", self)
        if dlg.exec():
            clave = dlg.get_clave()
            res = self.controller.buscar_clave(clave)

            if res is None:
                QMessageBox.information(self, "Buscar", "La clave no se encontró.")
                return

            tipo = res[0]
            if tipo == "estructura":
                _, bloque_idx, offset = res
                self.actualizar_visualizacion()
                self._resaltar(bloque_idx, offset)
                QMessageBox.information(
                    self,
                    "Buscar",
                    f"✅ Clave encontrada en el bloque {bloque_idx + 1}, posición {offset + 1}."
                )

            elif tipo == "colision":
                _, idx = res
                self.actualizar_visualizacion()
                # Si tienes método para resaltar en la zona de colisiones:
                if hasattr(self, "_resaltar_colision"):
                    self._resaltar_colision(idx)
                QMessageBox.information(
                    self,
                    "Buscar",
                    f"⚠️ Clave encontrada en la zona de colisiones, posición {idx + 1}."
                )

    def eliminar_clave(self):
        dlg = DialogoClave(self.digitos.value(), "Eliminar clave", "eliminar", self)
        if dlg.exec():
            clave = dlg.get_clave()
            ok, msg = self.controller.eliminar_clave(clave)
            if not ok:
                QMessageBox.warning(self, "Eliminar", msg)
            self.bloques = self.controller.bloques
            self.actualizar_visualizacion()

    def guardar_estructura(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar estructura", "truncamiento_externa.json", "JSON (*.json)")
        if ruta:
            try:
                self.controller.guardar_estructura(ruta)
                QMessageBox.information(self, "Guardar", "Estructura guardada correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo guardar: {e}")

    def cargar_estructura(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "JSON (*.json)")
        if ruta:
            try:
                self.controller.cargar_estructura(ruta)
                datos = {
                    'bloques': self.controller.bloques,
                    'num_claves': self.controller.num_claves,
                    'tamanio_bloque': self.controller.tamanio_bloque
                }
                self.bloques = datos['bloques']
                self.num_claves = datos['num_claves']
                self.tamanio_bloque = datos['tamanio_bloque']
                self.actualizar_visualizacion()
                QMessageBox.information(self, "Cargar", "Estructura cargada correctamente.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"No se pudo cargar: {e}")

    def eliminar_estructura(self):
        self.controller.eliminar_estructura()
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.actualizar_visualizacion()

    def deshacer(self):
        self.controller.deshacer()
        self.bloques = self.controller.bloques
        self.actualizar_visualizacion()

        # ==================== VISUALIZACION ====================

    def actualizar_visualizacion(self):
        """Actualiza la visualización de los bloques"""
        # Limpiar contenedor
        while self.contenedor_layout.count():
            child = self.contenedor_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.bloques:
            label = QLabel("No hay estructura creada. Presiona 'Crear estructura' para comenzar.")
            label.setStyleSheet("font-size: 16px; color: #6B7280; padding: 40px;")
            label.setAlignment(Qt.AlignCenter)
            self.contenedor_layout.addWidget(label)
            return

        # Título de información
        info_label = QLabel(
            f"Estructura: {self.num_claves} claves | "
            f"Tamaño de bloque: {self.tamanio_bloque} | "
            f"Bloques: {len(self.bloques)}"
        )
        info_label.setStyleSheet("""
               font-size: 18px;
               font-weight: bold;
               color: #7C3AED;
               padding: 10px;
               background-color: #F3E8FF;
               border-radius: 8px;
               margin-bottom: 20px;
           """)
        info_label.setAlignment(Qt.AlignCenter)
        self.contenedor_layout.addWidget(info_label)

        # Contenedor para los bloques en disposición horizontal
        bloques_container = QWidget()
        bloques_layout = QHBoxLayout(bloques_container)
        bloques_layout.setSpacing(8)
        bloques_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        bloques_layout.setContentsMargins(20, 10, 20, 10)

        # Dibujar solo los bloques que ya tienen al menos una clave insertada
        bloques_dibujados = 0
        for i, bloque in enumerate(self.bloques):
            if any(c is not None for c in bloque):  # solo dibujar si tiene al menos una clave
                bloque_widget = self.crear_bloque_visual(i, bloque)
                bloques_layout.addWidget(bloque_widget)
                bloques_dibujados += 1

        # Si aún no hay bloques usados, mostrar solo un bloque de ejemplo
        if bloques_dibujados == 0:
            ejemplo = self.crear_bloque_visual(0, [None] * self.tamanio_bloque)
            bloques_layout.addWidget(ejemplo)

        bloques_layout.addStretch()
        self.contenedor_layout.addWidget(bloques_container)

        # --- Zona de Colisiones ---
        if self.controller.zona_colisiones.zona:
            zona_label = QLabel("Zona de Colisiones:")
            zona_label.setStyleSheet("""
                   font-size: 18px;
                   font-weight: bold;
                   color: #6D28D9;
                   margin-top: 20px;
                   margin-bottom: 10px;
               """)
            self.contenedor_layout.addWidget(zona_label)

            zona_widget = QWidget()
            zona_layout = QHBoxLayout(zona_widget)
            zona_layout.setSpacing(8)
            zona_layout.setContentsMargins(0, 0, 0, 0)
            zona_layout.setAlignment(Qt.AlignLeft)  # o Qt.AlignCenter si prefieres centrado

            for clave in self.controller.zona_colisiones.zona:
                celda = QLabel(str(clave))
                celda.setAlignment(Qt.AlignCenter)
                celda.setStyleSheet("""
                       background-color: #E9D5FF;
                       border: 2px solid #6D28D9;
                       border-radius: 8px;
                       min-width: 60px; max-width: 60px;
                       min-height: 60px; max-height: 60px;
                       font-weight: bold;
                       font-size: 14px;
                   """)
                zona_layout.addWidget(celda)

            self.contenedor_layout.addWidget(zona_widget)

    def crear_bloque_visual(self, indice, bloque):
        """Crea la representación visual de un bloque con sus posiciones numeradas"""
        container = QWidget()
        container_layout = QVBoxLayout(container)
        container_layout.setSpacing(6)
        container_layout.setContentsMargins(0, 0, 0, 0)

        # Frame que contiene las celdas
        frame = QFrame()
        frame.setStyleSheet("QFrame { background-color: transparent; border: none; }")
        layout = QHBoxLayout(frame)
        layout.setSpacing(4)
        layout.setContentsMargins(0, 0, 0, 0)

        # Crear cada celda del bloque
        for i in range(self.tamanio_bloque):
            celda = QFrame()
            celda_layout = QVBoxLayout(celda)
            celda_layout.setContentsMargins(0, 0, 0, 0)
            celda_layout.setSpacing(0)

            if i < len(bloque) and bloque[i] is not None:
                # Celda ocupada
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #E9D5FF;
                        border: 2px solid #A78BFA;
                        min-width: 50px; max-width: 50px;
                        min-height: 50px; max-height: 50px;
                        border-radius: 6px;
                    }
                """)
                label_clave = QLabel(str(bloque[i]))
                label_clave.setStyleSheet("font-size: 12px; font-weight: bold; color: #5B21B6;")
                label_clave.setAlignment(Qt.AlignCenter)
                celda_layout.addWidget(label_clave)
            else:
                # Celda vacía
                celda.setStyleSheet("""
                    QFrame {
                        background-color: #F3E8FF;
                        border: 2px solid #A78BFA;
                        min-width: 50px; max-width: 50px;
                        min-height: 50px; max-height: 50px;
                        border-radius: 6px;
                    }
                """)

            layout.addWidget(celda)

        container_layout.addWidget(frame)

        # 🔢 Fila de números debajo de las celdas
        numeros_frame = QFrame()
        numeros_layout = QHBoxLayout(numeros_frame)
        numeros_layout.setSpacing(4)
        numeros_layout.setContentsMargins(0, 0, 0, 0)

        for i in range(self.tamanio_bloque):
            lbl_num = QLabel(str(i + 1))
            lbl_num.setAlignment(Qt.AlignCenter)
            lbl_num.setStyleSheet("font-size: 11px; color: #6B7280; font-weight: bold; min-width: 50px;")
            numeros_layout.addWidget(lbl_num)

        container_layout.addWidget(numeros_frame)

        # Número del bloque debajo (centrado)
        num_bloque = QLabel(f"Bloque {indice + 1}")
        num_bloque.setStyleSheet("font-size: 11px; font-weight: bold; color: #6B7280;")
        num_bloque.setAlignment(Qt.AlignCenter)
        container_layout.addWidget(num_bloque)

        return container

    def _resaltar(self, bloque_idx, offset):
        """Resalta una celda encontrada; reconstruye y colorea la celda encontrada."""
        # Reconstruir vista y aplicar un estilo de resaltado simple:
        # (para simplicidad volvemos a construir y coloreamos el bloque objetivo)
        self.actualizar_visualizacion()
        # localizar el widget del bloque en el layout:
        bloques_container = self.contenedor_layout.itemAt(1).widget()  # índice 1: info_label=0, bloques_container=1
        if not bloques_container:
            return
        bloques_layout = bloques_container.layout()
        if bloque_idx < 0 or bloque_idx >= bloques_layout.count():
            return
        bloque_widget = bloques_layout.itemAt(bloque_idx).widget()
        if not bloque_widget:
            return
        # Dentro del bloque, el primer child es frame con las celdas
        frame = bloque_widget.findChild(QFrame)
        if not frame:
            return
        # Encontrar la celda (QFrame) correspondiente y aplicar estilo de resaltado.
        cells = frame.findChildren(QFrame)
        # The first frame is the container itself, so we pick the cell by order:
        if 0 <= offset < len(cells):
            target = cells[offset]
            target.setStyleSheet("""
                   QFrame {
                       background-color: #C4B5FD;
                       border: 3px solid #5B21B6;
                       min-width: 50px; max-width: 50px;
                       min-height: 50px; max-height: 50px;
                       border-radius: 6px;
                   }
               """)
