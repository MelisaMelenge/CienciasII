from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea, QHBoxLayout, QDialog, QFileDialog
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.binaria_controller import BinariaController


class BinariaInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = BinariaController()
        self.cuadro_resaltado = None
        self.setWindowTitle("Ciencias de la Computación II - Búsqueda Binaria")

        # --- Layout principal ---
        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Encabezado ---
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

        titulo = QLabel("Ciencias de la Computación II - Búsqueda Binaria")
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

        header_layout.addLayout(menu_layout)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        layout.addWidget(header)

        # --- Controles superiores (Rango y Dígitos) ---
        controles_layout = QHBoxLayout()
        controles_layout.setAlignment(Qt.AlignCenter)
        controles_layout.setSpacing(20)

        lbl_rango = QLabel("Rango (10^n):")
        lbl_rango.setStyleSheet("font-weight: bold; font-size: 14px; color: #2d1f15;")

        self.rango = QComboBox()
        self.rango.addItems([str(i) for i in range(1, 7)])
        self.rango.setFixedWidth(80)
        self.rango.setStyleSheet("""
            QComboBox {
                background-color: white;
                border: 2px solid #bf8f62;
                border-radius: 5px;
                padding: 5px;
                color: #2d1f15;
            }
            QComboBox:hover {
                border: 2px solid #6C4E31;
            }
        """)

        lbl_digitos = QLabel("Número de dígitos:")
        lbl_digitos.setStyleSheet("font-weight: bold; font-size: 14px; color: #2d1f15;")

        self.digitos = QSpinBox()
        self.digitos.setRange(1, 10)
        self.digitos.setValue(4)
        self.digitos.setFixedWidth(80)
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

        controles_layout.addWidget(lbl_rango)
        controles_layout.addWidget(self.rango)
        controles_layout.addWidget(lbl_digitos)
        controles_layout.addWidget(self.digitos)

        layout.addLayout(controles_layout)

        # --- Botones principales ---
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_agregar = QPushButton("Insertar claves")
        self.btn_buscar = QPushButton("Buscar clave")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")

        for btn in (
                self.btn_crear, self.btn_agregar, self.btn_buscar, self.btn_eliminar_clave,
                self.btn_deshacer, self.btn_guardar, self.btn_eliminar, self.btn_cargar
        ):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9c724a;
                    color: #2d1f15;
                    padding: 10px 20px;
                    font-size: 16px;
                    font-weight: bold;
                    border-radius: 10px;
                }
                QPushButton:hover {
                    background-color: #bf8f62;
                }
            """)

        grid_botones = QGridLayout()
        grid_botones.setSpacing(20)
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_agregar, 0, 1)
        grid_botones.addWidget(self.btn_buscar, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)

        layout.addLayout(grid_botones)

        # --- Contenedor con scroll (ahora con VBoxLayout como en lineal) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("background-color: transparent;")

        # 🔄 Cambio clave: usar VBoxLayout en lugar de QGridLayout
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(10)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)

        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        self.setCentralWidget(central)

        # --- Conexiones ---
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_agregar.clicked.connect(self.adicionar_claves)
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)

        # Estado (ahora similar a lineal)
        self.filas_info = []
        self.labels = []
        self.indices_labels = []
        self.indices_reales = []
        self.capacidad = 0

    def crear_estructura(self):
        """Crea la estructura con vista inicial mínima"""
        self._limpiar_vista()

        n = int(self.rango.currentText())
        capacidad = 10 ** n
        self.capacidad = capacidad

        self.controller.crear_estructura(capacidad, self.digitos.value())

        # Crear vista dinámica inicial
        self._reconstruir_vista()

        # Bloquear los controles
        self.rango.setEnabled(False)
        self.digitos.setEnabled(False)

    def _limpiar_vista(self):
        """Limpia completamente la vista"""
        while self.contenedor_layout.count():
            item = self.contenedor_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        self.filas_info.clear()
        self.labels.clear()
        self.indices_labels.clear()
        self.indices_reales.clear()

    def _reconstruir_vista(self):
        """Reconstruye la vista dinámicamente según claves ocupadas"""
        self._limpiar_vista()

        if self.capacidad == 0:
            return

        # Si la capacidad es pequeña (≤10), mostrar todo
        if self.capacidad <= 10:
            self._crear_fila(0, self.capacidad, completa=True)
            return

        # Contar posiciones ocupadas
        total_ocupadas = sum(
            1 for i in range(self.capacidad)
            if self.controller.estructura.get(i, "") != ""
        )

        # Lógica progresiva igual que en lineal
        if total_ocupadas <= 8:
            self._crear_fila(0, 8, completa=False)
        else:
            self._crear_fila(0, 10, completa=True)

            if total_ocupadas <= 18:
                self._crear_fila(10, 8, completa=False)
            else:
                self._crear_fila(10, 10, completa=True)

                if total_ocupadas <= 28:
                    self._crear_fila(20, 8, completa=False)
                else:
                    fila_actual = 20
                    while fila_actual < self.capacidad:
                        ocupadas_hasta_aqui = sum(
                            1 for i in range(fila_actual + 10)
                            if self.controller.estructura.get(i, "") != ""
                        )
                        if ocupadas_hasta_aqui <= fila_actual + 8:
                            self._crear_fila(fila_actual, 8, completa=False)
                            break
                        else:
                            self._crear_fila(fila_actual, 10, completa=True)
                            fila_actual += 10

    def _crear_fila(self, inicio, cantidad, completa):
        """Crea una fila de cuadros"""
        fila_container = QWidget()
        fila_container.setStyleSheet("background: transparent;")
        fila_layout = QHBoxLayout(fila_container)
        fila_layout.setSpacing(0)
        fila_layout.setContentsMargins(0, 0, 0, 0)
        fila_layout.setAlignment(Qt.AlignHCenter)

        if completa:
            for i in range(cantidad):
                idx_real = inicio + i
                if idx_real < self.capacidad:
                    self._agregar_bloque(fila_layout, idx_real)
        else:
            for i in range(cantidad):
                idx_real = inicio + i
                if idx_real < self.capacidad:
                    self._agregar_bloque(fila_layout, idx_real)

            self._agregar_bloque_especial(fila_layout, "...", "...")
            self._agregar_bloque(fila_layout, self.capacidad - 1)

        fila_layout.addStretch()

        self.contenedor_layout.addWidget(fila_container, 0, Qt.AlignHCenter)
        self.filas_info.append({
            'widget': fila_container,
            'inicio': inicio,
            'cantidad': cantidad,
            'completa': completa
        })

    def _agregar_bloque(self, layout, idx_real):
        """Agrega un cuadro individual con su número de índice"""
        contenedor = QWidget()
        contenedor.setFixedWidth(80)
        layout_vert = QVBoxLayout(contenedor)
        layout_vert.setSpacing(2)
        layout_vert.setContentsMargins(0, 0, 0, 0)

        cuadro = QLabel("")
        cuadro.setAlignment(Qt.AlignCenter)
        cuadro.setFixedSize(80, 80)
        cuadro.setStyleSheet("""
            QLabel {
                background-color: #FFDBB5;
                border: 2px solid #9c724a;
                border-radius: 12px;
                font-size: 16px;
                color: #2d1f15;
            }
        """)

        numero = QLabel(str(idx_real + 1))
        numero.setAlignment(Qt.AlignCenter)
        numero.setFixedHeight(20)
        numero.setStyleSheet("font-size: 12px; color: #6C4E31; background: transparent;")

        layout_vert.addWidget(cuadro)
        layout_vert.addWidget(numero)

        layout.addWidget(contenedor)
        self.labels.append(cuadro)
        self.indices_labels.append(numero)
        self.indices_reales.append(idx_real)

    def _agregar_bloque_especial(self, layout, texto_valor, texto_indice):
        """Agrega el bloque de puntos suspensivos '...'"""
        contenedor = QWidget()
        contenedor.setFixedWidth(80)
        layout_vert = QVBoxLayout(contenedor)
        layout_vert.setSpacing(2)
        layout_vert.setContentsMargins(0, 0, 0, 0)

        cuadro = QLabel(texto_valor)
        cuadro.setAlignment(Qt.AlignCenter)
        cuadro.setFixedSize(80, 80)
        cuadro.setStyleSheet("""
            QLabel {
                background-color: #FFEAC5;
                border: 2px solid #bf8f62;
                border-radius: 12px;
                font-size: 24px;
                color: #6C4E31;
            }
        """)

        numero = QLabel(texto_indice)
        numero.setAlignment(Qt.AlignCenter)
        numero.setFixedHeight(20)
        numero.setStyleSheet("font-size: 12px; color: #6C4E31; background: transparent;")

        layout_vert.addWidget(cuadro)
        layout_vert.addWidget(numero)

        layout.addWidget(contenedor)
        self.labels.append(cuadro)
        self.indices_labels.append(numero)
        self.indices_reales.append(-1)  # Marcador especial

    def _repintar(self):
        """Actualiza el contenido visual de todos los cuadros"""
        for i, idx_real in enumerate(self.indices_reales):
            if idx_real == -1:  # Bloque especial "..."
                continue

            lbl = self.labels[i]
            val = str(self.controller.estructura.get(idx_real, ""))

            if val:
                lbl.setText(val)
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #bf8f62;
                        border: 2px solid #6C4E31;
                        border-radius: 12px;
                        font-size: 16px;
                        font-weight: bold;
                        color: #2d1f15;
                    }
                """)
            else:
                lbl.setText("")
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #FFDBB5;
                        border: 2px solid #9c724a;
                        border-radius: 12px;
                        font-size: 16px;
                        color: #2d1f15;
                    }
                """)

    def adicionar_claves(self):
        """Inserta una nueva clave y actualiza la vista dinámicamente"""
        self.limpiar_resaltado()

        if self.capacidad == 0:
            DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                         mensaje="Primero cree la estructura.").exec()
            return

        dialogo = DialogoClave(self.digitos.value(), "Insertar clave", parent=self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            resultado = self.controller.adicionar_clave(clave)

            if resultado == "OK":
                # 🔄 Reconstruir vista dinámicamente
                self._reconstruir_vista()
                self._repintar()

                DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                             mensaje=f"La clave {clave} fue insertada correctamente.").exec()

            elif resultado == "LONGITUD":
                DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                             mensaje="La clave no cumple con la longitud definida.").exec()
            elif resultado == "REPETIDA":
                DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                             mensaje="La clave ya existe en la estructura.").exec()
            elif resultado == "LLENO":
                DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                             mensaje="La estructura ya está llena.").exec()

    def buscar_clave(self):
        """Busca una clave y resalta su posición"""
        self.limpiar_resaltado()

        if self.capacidad == 0:
            DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                         mensaje="Primero cree la estructura.").exec()
            return

        dialogo = DialogoClave(self.digitos.value(), self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            pos = self.controller.buscar(clave)

            if pos != -1:
                # Buscar el label correspondiente
                try:
                    pos_label = self.indices_reales.index(pos)

                    # Resaltar el cuadro encontrado
                    self.labels[pos_label].setStyleSheet("""
                        QLabel {
                            background-color: #9c724a;
                            border: 3px solid #603F26;
                            border-radius: 12px;
                            font-size: 18px;
                            font-weight: bold;
                            color: #FFEAC5;
                        }
                    """)
                    self.cuadro_resaltado = self.labels[pos_label]

                    DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                                 mensaje=f"Clave encontrada en posición {pos + 1}").exec()
                except ValueError:
                    DialogoClave(0, titulo="Encontrada (no visible)", modo="mensaje", parent=self,
                                 mensaje=f"La clave está en la posición {pos + 1}, pero no es visible actualmente.").exec()
            else:
                DialogoClave(0, titulo="No encontrado", modo="mensaje", parent=self,
                             mensaje="La clave no está en la estructura.").exec()
                self.cuadro_resaltado = None

    def eliminar_clave(self):
        """Elimina una clave y actualiza la vista"""
        self.limpiar_resaltado()

        if self.capacidad == 0:
            DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                         mensaje="Primero cree la estructura.").exec()
            return

        dialogo = DialogoClave(self.digitos.value(), self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()
            resultado = self.controller.eliminar_clave(clave)

            if resultado == "OK":
                # 🔄 Reconstruir y repintar
                self._reconstruir_vista()
                self._repintar()

                if self.cuadro_resaltado:
                    self.cuadro_resaltado = None

                DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                             mensaje="Clave eliminada correctamente.").exec()
            else:
                DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                             mensaje=f"No se pudo eliminar: {resultado}").exec()

    def deshacer(self):
        """Revierte la última acción"""
        self.limpiar_resaltado()
        resultado = self.controller.deshacer()

        if resultado == "OK":
            # 🔄 Reconstruir y repintar
            self._reconstruir_vista()
            self._repintar()

            DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                         mensaje="Se deshizo el último movimiento.").exec()
        else:
            DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                         mensaje="No hay movimientos para deshacer.").exec()

    def eliminar_estructura(self):
        """Elimina completamente la estructura"""
        confirmar = DialogoClave(
            0, titulo="Confirmar eliminación", modo="confirmar", parent=self,
            mensaje="¿Está seguro de que desea eliminar la estructura actual?"
        )
        if confirmar.exec() != QDialog.Accepted:
            return

        self.limpiar_resaltado()
        self.controller = BinariaController()
        self.capacidad = 0

        self._limpiar_vista()

        DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                     mensaje="La estructura ha sido eliminada correctamente.").exec()

        # Volver a habilitar controles
        self.rango.setEnabled(True)
        self.digitos.setEnabled(True)

    def guardar_estructura(self):
        """Guarda la estructura en archivo JSON"""
        self.limpiar_resaltado()
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar estructura", "interna_binaria.json", "Archivos JSON (*.json)"
        )
        if not ruta:
            return

        resultado = self.controller.guardar(ruta)
        if resultado == "OK":
            DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                         mensaje=f"Estructura guardada en:\n{ruta}").exec()
        else:
            DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                         mensaje=f"No se pudo guardar la estructura:\n{resultado}").exec()

    def cargar_estructura(self):
        """Carga estructura desde archivo JSON"""
        self.limpiar_resaltado()

        if self.controller.estructura:
            dialogo = DialogoClave(0, titulo="Advertencia", modo="confirmar", parent=self,
                                   mensaje="Se sobrescribirá la estructura actual.\n\n¿Desea continuar?")
            if dialogo.exec() != QDialog.Accepted:
                return

        ruta, _ = QFileDialog.getOpenFileName(
            self, "Cargar estructura", "", "Archivos JSON (*.json)"
        )
        if not ruta:
            return

        resultado = self.controller.cargar(ruta)
        if resultado == "OK":
            datos = self.controller.obtener_datos_vista()
            self.capacidad = datos["capacidad"]

            # 🔄 Reconstruir vista y repintar
            self._reconstruir_vista()
            self._repintar()

            DialogoClave(0, titulo="Éxito", modo="mensaje", parent=self,
                         mensaje="Estructura cargada correctamente.").exec()
        else:
            DialogoClave(0, titulo="Error", modo="mensaje", parent=self,
                         mensaje=f"No se pudo cargar la estructura:\n{resultado}").exec()

    def limpiar_resaltado(self):
        """Restaura el color normal de todos los cuadros"""
        for i, lbl in enumerate(self.labels):
            if self.indices_reales[i] == -1:  # Saltar bloques especiales
                continue

            text = lbl.text()
            if text:
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #bf8f62;
                        border: 2px solid #6C4E31;
                        border-radius: 12px;
                        font-size: 16px;
                        font-weight: bold;
                        color: #2d1f15;
                    }
                """)
            else:
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #FFDBB5;
                        border: 2px solid #9c724a;
                        border-radius: 12px;
                        font-size: 16px;
                        color: #2d1f15;
                    }
                """)