from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame, QDialog, QFileDialog,
    QMessageBox, QSpinBox, QComboBox, QPushButton, QGridLayout, QHBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt
from Vista.dialogo_clave import DialogoClave
import json
import os


class CubetaParcial(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setWindowTitle("Ciencias de la Computación II - Cubetas (Expansión y Reducción Parcial)")

        # Inicializar variables
        self.cubetas = []
        self.n = 0  # Número de cubetas
        self.R = 0  # Registros por cubeta
        self.num_digitos = 4
        self.estructura_creada = False
        self.historial = []
        self.hubo_expansion = False
        self.nivel_expansion = 0  # Para controlar el nivel en la secuencia

        # --- Widget central ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(8)

        # --- Encabezado ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #D8B4FE, stop:1 #A78BFA
            );
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)

        titulo = QLabel("Ciencias de la Computación II - Cubetas (Expansión y Reducción Parcial)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: white; margin: 10px;")
        header_layout.addWidget(titulo)

        # --- Menú de navegación ---
        menu_layout = QHBoxLayout()
        menu_layout.setSpacing(40)
        menu_layout.setAlignment(Qt.AlignCenter)

        btn_inicio = QPushButton("Inicio")
        btn_busqueda = QPushButton("Menú de Búsqueda")

        for btn in (btn_inicio, btn_busqueda):
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    color: #2E1065;
                    font-size: 16px;
                    font-weight: bold;
                    border: none;
                }
                QPushButton:hover {
                    color: #6D28D9;
                    text-decoration: underline;
                }
            """)
            menu_layout.addWidget(btn)

        header_layout.addLayout(menu_layout)
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))
        layout.addWidget(header)

        # --- Controles de parámetros ---
        self.spin_cubetas = QSpinBox()
        self.spin_cubetas.setRange(2, 100)
        self.spin_cubetas.setValue(2)
        self.spin_cubetas.setFixedWidth(100)

        self.spin_registros = QSpinBox()
        self.spin_registros.setRange(1, 50)
        self.spin_registros.setValue(2)
        self.spin_registros.setFixedWidth(100)

        self.spin_digitos = QSpinBox()
        self.spin_digitos.setRange(1, 10)
        self.spin_digitos.setValue(4)
        self.spin_digitos.setFixedWidth(100)

        self.combo_accion = QComboBox()
        self.combo_accion.addItems(["Expandir", "Reducir"])
        self.combo_accion.setFixedWidth(150)

        # Estilo para los controles
        estilo_control = "font-size: 16px; padding: 5px;"
        self.spin_cubetas.setStyleSheet(estilo_control)
        self.spin_registros.setStyleSheet(estilo_control)
        self.spin_digitos.setStyleSheet(estilo_control)
        self.combo_accion.setStyleSheet(estilo_control)
        self.combo_accion.currentTextChanged.connect(self.actualizar_botones_accion)

        # --- Botones principales ---
        self.btn_crear = QPushButton("Crear estructura")
        self.btn_insertar = QPushButton("Insertar claves")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_buscar_clave = QPushButton("Buscar clave")

        estilo_boton = """
            QPushButton {
                background-color: #7C3AED;
                color: white;
                padding: 6px 14px;
                font-size: 14px;
                border-radius: 8px;
                min-width: 150px;
            }
            QPushButton:hover {
                background-color: #6D28D9;
            }
        """

        botones = (
            self.btn_crear, self.btn_insertar, self.btn_guardar,
            self.btn_cargar, self.btn_eliminar, self.btn_deshacer,
            self.btn_eliminar_clave, self.btn_buscar_clave
        )
        for btn in botones:
            btn.setStyleSheet(estilo_boton)

        # --- Layout de controles ---
        controles = QVBoxLayout()

        fila_controles = QHBoxLayout()
        fila_controles.setSpacing(10)
        fila_controles.setAlignment(Qt.AlignCenter)

        lbl_cubetas = QLabel("Número de cubetas:")
        lbl_cubetas.setStyleSheet("font-size: 14px; font-weight: bold;")

        lbl_registros = QLabel("Registros por cubeta:")
        lbl_registros.setStyleSheet("font-size: 14px; font-weight: bold;")

        lbl_digitos = QLabel("Tamaño de claves:")
        lbl_digitos.setStyleSheet("font-size: 14px; font-weight: bold;")

        lbl_accion = QLabel("Acción:")
        lbl_accion.setStyleSheet("font-size: 14px; font-weight: bold;")

        fila_controles.addWidget(lbl_cubetas)
        fila_controles.addWidget(self.spin_cubetas)
        fila_controles.addWidget(lbl_registros)
        fila_controles.addWidget(self.spin_registros)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.spin_digitos)
        fila_controles.addWidget(lbl_accion)
        fila_controles.addWidget(self.combo_accion)

        controles.addLayout(fila_controles)
        controles.setContentsMargins(0, 0, 0, 0)

        # --- Grid de botones ---
        self.grid_botones = QGridLayout()
        self.grid_botones.setHorizontalSpacing(15)
        self.grid_botones.setVerticalSpacing(6)
        self.grid_botones.setAlignment(Qt.AlignCenter)

        # Grid fijo (2 filas x 3 columnas)
        self.grid_botones.addWidget(self.btn_crear, 0, 0)
        self.grid_botones.addWidget(self.btn_insertar, 0, 1)
        self.grid_botones.addWidget(self.btn_eliminar_clave, 0, 1)
        self.grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        self.grid_botones.addWidget(self.btn_guardar, 1, 0)
        self.grid_botones.addWidget(self.btn_eliminar, 1, 1)
        self.grid_botones.addWidget(self.btn_cargar, 1, 2)

        self.grid_botones.setAlignment(Qt.AlignCenter)

        controles.addLayout(self.grid_botones)
        layout.addLayout(controles)

        # Inicializar visibilidad según acción actual
        self.actualizar_botones_accion()

        # --- Área de visualización (scroll) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.contenedor = QWidget()
        self.contenedor_layout = QVBoxLayout(self.contenedor)
        self.contenedor_layout.setSpacing(10)
        self.contenedor_layout.setContentsMargins(20, 20, 20, 20)
        self.contenedor_layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        # --- Mensaje inicial ---
        self.lbl_info = QLabel("Aquí se mostrará la simulación de la expansión o reducción parcial de cubetas.")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 18px; color: #2c3e50; margin: 20px;")
        self.contenedor_layout.addWidget(self.lbl_info)

        # --- Conectar eventos ---
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_insertar.clicked.connect(self.insertar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_guardar.clicked.connect(self.guardar_estructura)
        self.btn_cargar.clicked.connect(self.cargar_estructura)

    def obtener_secuencia_expansion(self):
        """Retorna la secuencia de expansión parcial: 2, 3, 4, 6, 8, 12, 16, 24, 32..."""
        secuencia = [2, 3, 4, 6, 8, 12, 16, 24, 32, 48, 64, 96]
        return secuencia

    def obtener_siguiente_n(self, n_actual):
        """Obtiene el siguiente número de cubetas en la secuencia de expansión"""
        secuencia = self.obtener_secuencia_expansion()
        try:
            idx = secuencia.index(n_actual)
            if idx < len(secuencia) - 1:
                return secuencia[idx + 1]
            else:
                # Si se pasa de la secuencia, seguir el patrón (multiplicar por 1.5)
                return int(n_actual * 1.5)
        except ValueError:
            # Si no está en la secuencia, buscar el siguiente mayor
            for n in secuencia:
                if n > n_actual:
                    return n
            return int(n_actual * 1.5)

    def obtener_anterior_n(self, n_actual):
        """Obtiene el anterior número de cubetas en la secuencia de reducción"""
        secuencia = self.obtener_secuencia_expansion()
        try:
            idx = secuencia.index(n_actual)
            if idx > 0:
                return secuencia[idx - 1]
            else:
                return 2  # Mínimo
        except ValueError:
            # Si no está en la secuencia, buscar el anterior menor
            for i in range(len(secuencia) - 1, -1, -1):
                if secuencia[i] < n_actual:
                    return secuencia[i]
            return 2

    def crear_estructura(self):
        """Crear la estructura de cubetas"""
        n = self.spin_cubetas.value()

        # Validar que esté en la secuencia
        secuencia = self.obtener_secuencia_expansion()
        if n not in secuencia and n < 100:
            QMessageBox.warning(
                self, "Error",
                f"El número de cubetas debe estar en la secuencia: {', '.join(map(str, secuencia[:8]))}..."
            )
            return

        self.n = n
        self.R = self.spin_registros.value()
        self.num_digitos = self.spin_digitos.value()

        # Inicializar cubetas vacías
        self.cubetas = [[] for _ in range(self.n)]
        self.estructura_creada = True
        self.historial = []
        self.nivel_expansion = 0

        self.actualizar_visualizacion()
        QMessageBox.information(self, "Éxito",
                                f"Estructura creada: {self.n} cubetas x {self.R} registros")

    def calcular_posicion(self, clave):
        """Calcular posición: clave mod n"""
        try:
            clave_num = int(clave)
            return clave_num % self.n
        except:
            return -1

    def calcular_ocupacion(self):
        """Calcular ocupación para EXPANSIÓN = registros ocupados / espacios disponibles"""
        ocupados_reales = sum(min(len(cubeta), self.R) for cubeta in self.cubetas)
        disponibles = self.n * self.R
        return ocupados_reales / disponibles if disponibles > 0 else 0

    def insertar_clave(self):
        """Insertar una nueva clave con desbordamiento visible antes de expandir"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dialogo = DialogoClave(self.num_digitos, "Insertar Clave", "insertar", self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()

            # Validar clave
            if len(clave) != self.num_digitos or not clave.isdigit():
                QMessageBox.warning(self, "Error",
                                    f"La clave debe tener exactamente {self.num_digitos} dígitos.")
                return

            # Verificar duplicados
            for cubeta in self.cubetas:
                if clave in cubeta:
                    QMessageBox.warning(self, "Error", "La clave ya existe.")
                    return

            # Guardar estado para deshacer
            self.guardar_estado()

            # Calcular posición
            posicion = self.calcular_posicion(clave)

            # SIEMPRE insertar en la cubeta correspondiente (permitir desbordamiento)
            self.cubetas[posicion].append(clave)

            # Actualizar visualización para mostrar el desbordamiento
            self.actualizar_visualizacion()

            # Calcular ocupación REAL
            ocupados_reales = sum(min(len(cubeta), self.R) for cubeta in self.cubetas)
            disponibles = self.n * self.R
            ocupacion_real = ocupados_reales / disponibles if disponibles > 0 else 0

            # Si la cubeta desbordó o la ocupación >= 75%, expandir
            if len(self.cubetas[posicion]) > self.R or ocupacion_real >= 0.75:
                QMessageBox.information(
                    self, "Desbordamiento detectado",
                    f"La clave {clave} fue insertada en la cubeta {posicion}.\n"
                    f"Ocupación real: {ocupacion_real * 100:.1f}%\n"
                    f"Se procederá a expandir la estructura."
                )
                self.expandir_parcial()

    def expandir_parcial(self):
        """Expansión parcial: expande según la secuencia 2→3→4→6→8→12→16..."""
        self.hubo_expansion = True

        ocupacion = self.calcular_ocupacion()
        if ocupacion < 0.75:
            return

        antiguo_n = self.n
        nuevo_n = self.obtener_siguiente_n(self.n)

        # Guardar todas las claves actuales
        todas_claves = [clave for cubeta in self.cubetas for clave in cubeta]

        # Reasignar estructura
        self.n = nuevo_n
        self.cubetas = [[] for _ in range(self.n)]
        self.nivel_expansion += 1

        # Reinsertar claves con nuevo módulo
        for clave in todas_claves:
            pos = self.calcular_posicion(clave)
            self.cubetas[pos].append(clave)

        self.actualizar_visualizacion()

        # Verificar si completó una expansión total (cada 2 parciales)
        mensaje_extra = ""
        if self.nivel_expansion % 2 == 0:
            mensaje_extra = f"\n¡Se completó una expansión TOTAL! (Nivel {self.nivel_expansion // 2})"

        QMessageBox.information(
            self, "Expansión parcial",
            f"Ocupación: {ocupacion * 100:.1f}%\n"
            f"Estructura expandida de {antiguo_n} a {nuevo_n} cubetas."
            f"{mensaje_extra}"
        )

    def buscar_clave(self):
        """Buscar una clave"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dialogo = DialogoClave(self.num_digitos, "Buscar Clave", "buscar", self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()

            posicion = self.calcular_posicion(clave)

            if clave in self.cubetas[posicion]:
                registro = self.cubetas[posicion].index(clave) + 1
                QMessageBox.information(self, "Encontrada",
                                        f"Clave {clave} encontrada en:\nCubeta {posicion}, Registro {registro}")
            else:
                QMessageBox.information(self, "No encontrada",
                                        f"La clave {clave} no existe en la estructura.")

    def eliminar_clave(self):
        """Eliminar una clave con reducción automática"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dialogo = DialogoClave(self.num_digitos, "Eliminar Clave", "eliminar", self)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()

            # Guardar estado para deshacer
            self.guardar_estado()

            posicion = self.calcular_posicion(clave)

            if clave in self.cubetas[posicion]:
                self.cubetas[posicion].remove(clave)
                self.actualizar_visualizacion()

                # Calcular ocupación para reducción
                ocupacion_reduccion = self.calcular_ocupacion_reduccion()

                # Verificar si se puede reducir (ocupación <= 80% y n > 2)
                if ocupacion_reduccion <= 0.80 and self.n > 2:
                    QMessageBox.information(
                        self, "Reducción detectada",
                        f"La clave {clave} fue eliminada de la cubeta {posicion}.\n"
                        f"Espacios ocupados / cubetas: {ocupacion_reduccion * 100:.1f}%\n"
                        f"Se procederá a reducir la estructura."
                    )
                    self.reducir_parcial()
                else:
                    QMessageBox.information(self, "Éxito",
                                            f"Clave {clave} eliminada de la cubeta {posicion}")
            else:
                QMessageBox.warning(self, "Error",
                                    f"La clave {clave} no existe.")

    def guardar_estado(self):
        """Guardar estado actual para deshacer"""
        estado = {
            'cubetas': [cubeta.copy() for cubeta in self.cubetas],
            'n': self.n,
            'R': self.R,
            'nivel_expansion': self.nivel_expansion
        }
        self.historial.append(estado)

    def eliminar_estructura(self):
        """Eliminar la estructura completa"""
        respuesta = QMessageBox.question(self, "Confirmar",
                                         "¿Está seguro de eliminar la estructura?",
                                         QMessageBox.Yes | QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            self.cubetas = []
            self.n = 0
            self.R = 0
            self.estructura_creada = False
            self.historial = []
            self.nivel_expansion = 0

            # Limpiar visualización
            while self.contenedor_layout.count():
                item = self.contenedor_layout.takeAt(0)
                if item.widget():
                    item.widget().deleteLater()

            self.lbl_info = QLabel("Estructura eliminada. Cree una nueva estructura.")
            self.lbl_info.setAlignment(Qt.AlignCenter)
            self.lbl_info.setStyleSheet("font-size: 18px; color: #2c3e50; margin: 20px;")
            self.contenedor_layout.addWidget(self.lbl_info)

    def actualizar_visualizacion(self):
        """Actualizar la visualización: cubetas horizontales, registros verticales"""
        # Limpiar contenedor
        while self.contenedor_layout.count():
            item = self.contenedor_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Título con ocupación
        ocupacion = self.calcular_ocupacion()
        color = "#059669" if ocupacion < 0.75 else "#DC2626"

        lbl_info = QLabel(
            f"<b>Estructura:</b> {self.n} cubetas x {self.R} registros "
            f"<span style='color:{color}; font-weight:bold;'>| Ocupación: {ocupacion * 100:.1f}%</span> "
            f"<span style='color:#7C3AED; font-weight:bold;'>| Nivel: {self.nivel_expansion}</span>"
        )
        lbl_info.setAlignment(Qt.AlignCenter)
        lbl_info.setStyleSheet("font-size: 14px; margin-bottom: 10px;")
        self.contenedor_layout.addWidget(lbl_info)

        # Crear tabla usando QGridLayout
        tabla_widget = QWidget()
        grid = QGridLayout(tabla_widget)
        grid.setSpacing(2)
        grid.setContentsMargins(0, 0, 0, 0)

        # Encabezado (cubetas)
        lbl_esquina = QLabel("")
        lbl_esquina.setStyleSheet("""
            background-color: #7C3AED;
            border: 1px solid #6D28D9;
        """)
        lbl_esquina.setFixedWidth(55)
        lbl_esquina.setFixedHeight(28)
        grid.addWidget(lbl_esquina, 0, 0)

        # Headers de cubetas
        for i in range(self.n):
            lbl_cubeta = QLabel(f"C{i}")
            lbl_cubeta.setAlignment(Qt.AlignCenter)
            lbl_cubeta.setStyleSheet("""
                background-color: #7C3AED;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 6px 8px;
                border: 1px solid #6D28D9;
            """)
            lbl_cubeta.setMinimumWidth(60)
            lbl_cubeta.setMaximumWidth(80)
            lbl_cubeta.setFixedHeight(28)
            grid.addWidget(lbl_cubeta, 0, i + 1)

        # Filas de registros
        for j in range(self.R):
            # Header de registro
            lbl_registro = QLabel(f"R{j + 1}")
            lbl_registro.setAlignment(Qt.AlignCenter)
            lbl_registro.setStyleSheet("""
                background-color: #7C3AED;
                color: white;
                font-size: 12px;
                font-weight: bold;
                padding: 6px 8px;
                border: 1px solid #6D28D9;
            """)
            lbl_registro.setFixedWidth(55)
            lbl_registro.setFixedHeight(30)
            grid.addWidget(lbl_registro, j + 1, 0)

            # Celdas de datos
            for i in range(self.n):
                cubeta = self.cubetas[i]
                bg_color = "#F3F4F6" if i % 2 == 0 else "#FFFFFF"

                if j < len(cubeta):
                    lbl_val = QLabel(cubeta[j])
                    lbl_val.setStyleSheet(f"""
                        background-color: {bg_color};
                        color: #1F2937;
                        font-size: 12px;
                        font-weight: 500;
                        padding: 6px 8px;
                        border: 1px solid #E5E7EB;
                    """)
                else:
                    lbl_val = QLabel("---")
                    lbl_val.setStyleSheet(f"""
                        background-color: {bg_color};
                        color: #9CA3AF;
                        font-size: 11px;
                        padding: 6px 8px;
                        border: 1px solid #E5E7EB;
                    """)

                lbl_val.setAlignment(Qt.AlignCenter)
                lbl_val.setMinimumWidth(60)
                lbl_val.setMaximumWidth(80)
                lbl_val.setFixedHeight(30)
                grid.addWidget(lbl_val, j + 1, i + 1)

        # Desbordamientos
        fila_desborde = self.R + 1
        hay_desbordamientos = False

        for i in range(self.n):
            cubeta = self.cubetas[i]
            if len(cubeta) > self.R:
                hay_desbordamientos = True
                extras = cubeta[self.R:]
                texto_extras = ", ".join(extras)

                lbl_extra = QLabel(texto_extras)
                lbl_extra.setAlignment(Qt.AlignCenter)
                lbl_extra.setStyleSheet("""
                    color: #DC2626;
                    font-size: 11px;
                    font-weight: bold;
                    padding: 4px;
                    background-color: #FEE2E2;
                """)
                lbl_extra.setMinimumWidth(60)
                lbl_extra.setMaximumWidth(80)
                grid.addWidget(lbl_extra, fila_desborde, i + 1)

        if hay_desbordamientos:
            lbl_desborde_txt = QLabel("Desborde")
            lbl_desborde_txt.setAlignment(Qt.AlignCenter)
            lbl_desborde_txt.setStyleSheet("""
                background-color: #FEE2E2;
                color: #DC2626;
                font-size: 10px;
                font-weight: bold;
                padding: 4px;
                border: 1px solid #FCA5A5;
            """)
            lbl_desborde_txt.setFixedWidth(55)
            grid.addWidget(lbl_desborde_txt, fila_desborde, 0)

        grid.setColumnStretch(0, 0)
        for i in range(1, self.n + 1):
            grid.setColumnStretch(i, 0)

        self.contenedor_layout.addWidget(tabla_widget, alignment=Qt.AlignTop | Qt.AlignHCenter)
        self.contenedor_layout.addStretch()

    def actualizar_botones_accion(self):
        """Mostrar los botones según la acción seleccionada"""
        accion = self.combo_accion.currentText()

        self.btn_insertar.hide()
        self.btn_eliminar_clave.hide()

        if accion == "Expandir":
            self.btn_insertar.show()
        elif accion == "Reducir":
            if self.hubo_expansion:
                self.btn_eliminar_clave.show()
            else:
                QMessageBox.warning(
                    self, "Aviso",
                    "No puede reducir porque no ha habido ninguna expansión todavía."
                )
                self.combo_accion.setCurrentText("Expandir")
                self.actualizar_botones_accion()
                return

        self.btn_crear.show()
        self.btn_buscar_clave.show()
        self.btn_guardar.show()
        self.btn_eliminar.show()
        self.btn_cargar.show()

    def calcular_ocupacion_reduccion(self):
        """Calcular ocupación para REDUCCIÓN = espacios ocupados / número de cubetas"""
        espacios_ocupados = sum(len(cubeta) for cubeta in self.cubetas)
        return espacios_ocupados / self.n if self.n > 0 else 0

    def reducir_parcial(self):
        """Reducción parcial: reduce según la secuencia inversa"""
        if self.n <= 2:
            QMessageBox.warning(
                self, "No se puede reducir",
                "La estructura tiene 2 cubetas (mínimo). No se puede reducir más."
            )
            return

        ocupacion_reduccion = self.calcular_ocupacion_reduccion()

        if ocupacion_reduccion > 0.80:
            QMessageBox.warning(
                self, "No se puede reducir",
                f"La ocupación ({ocupacion_reduccion * 100:.1f}%) es mayor a 80%.\n"
                "No se puede reducir la estructura."
            )
            return

        antiguo_n = self.n
        nuevo_n = self.obtener_anterior_n(self.n)

        # Guardar todas las claves actuales
        todas_claves = [clave for cubeta in self.cubetas for clave in cubeta]

        # Reasignar estructura
        self.n = nuevo_n
        self.cubetas = [[] for _ in range(self.n)]
        self.nivel_expansion = max(0, self.nivel_expansion - 1)

        # Reinsertar claves con nuevo módulo
        for clave in todas_claves:
            pos = self.calcular_posicion(clave)
            self.cubetas[pos].append(clave)

        self.actualizar_visualizacion()

        # Verificar si completó una reducción total (cada 2 parciales)
        mensaje_extra = ""
        if self.nivel_expansion % 2 == 0 and self.nivel_expansion >= 0:
            mensaje_extra = f"\n¡Se completó una reducción TOTAL!"

        QMessageBox.information(
            self, "Reducción parcial",
            f"Ocupación: {ocupacion_reduccion * 100:.1f}%\n"
            f"Estructura reducida de {antiguo_n} a {nuevo_n} cubetas."
            f"{mensaje_extra}"
        )

    def guardar_estructura(self):
        """Guardar la estructura actual en un archivo JSON"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "No hay estructura para guardar.")
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar estructura",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )

        if not archivo:
            return

        if not archivo.endswith('.json'):
            archivo += '.json'

        try:
            datos = {
                "n": self.n,
                "R": self.R,
                "num_digitos": self.num_digitos,
                "cubetas": self.cubetas,
                "hubo_expansion": self.hubo_expansion,
                "nivel_expansion": self.nivel_expansion
            }

            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            QMessageBox.information(
                self, "Éxito",
                f"Estructura guardada correctamente en:\n{archivo}"
            )

        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Error al guardar la estructura:\n{str(e)}"
            )

    def cargar_estructura(self):
        """Cargar una estructura desde un archivo JSON"""
        archivo, _ = QFileDialog.getOpenFileName(
            self,
            "Cargar estructura",
            "",
            "Archivos JSON (*.json);;Todos los archivos (*)"
        )

        if not archivo:
            return

        if not os.path.exists(archivo):
            QMessageBox.warning(self, "Error", f"El archivo no existe:\n{archivo}")
            return

        try:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            if not all(k in datos for k in ["n", "R", "num_digitos", "cubetas"]):
                QMessageBox.warning(
                    self, "Error",
                    "El archivo no contiene una estructura válida."
                )
                return

            self.n = datos["n"]
            self.R = datos["R"]
            self.num_digitos = datos["num_digitos"]
            self.cubetas = datos["cubetas"]
            self.hubo_expansion = datos.get("hubo_expansion", False)
            self.nivel_expansion = datos.get("nivel_expansion", 0)
            self.estructura_creada = True
            self.historial = []

            self.spin_cubetas.setValue(self.n)
            self.spin_registros.setValue(self.R)
            self.spin_digitos.setValue(self.num_digitos)

            self.actualizar_visualizacion()

            QMessageBox.information(
                self, "Éxito",
                f"Estructura cargada correctamente desde:\n{archivo}\n\n"
                f"{self.n} cubetas x {self.R} registros\n"
                f"Nivel de expansión: {self.nivel_expansion}"
            )

        except json.JSONDecodeError:
            QMessageBox.critical(
                self, "Error",
                "El archivo no es un JSON válido."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Error",
                f"Error al cargar la estructura:\n{str(e)}"
            )