from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,QDialog,
    QMessageBox,QSpinBox, QComboBox, QPushButton, QGridLayout, QHBoxLayout, QScrollArea
)
from PySide6.QtCore import Qt
from Vista.dialogo_clave import DialogoClave

class CubetaTotal(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana

        self.setWindowTitle("Ciencias de la Computación II - Cubetas (Expansión y Reducción Total)")

        # Inicializar variables
        self.cubetas = []
        self.n = 0  # Número de cubetas
        self.R = 0  # Registros por cubeta
        self.num_digitos = 4
        self.estructura_creada = False
        self.historial = []

        # --- Widget central ---
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(20)

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

        titulo = QLabel("Ciencias de la Computación II - Cubetas (Expansión y Reducción Total)")
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
        self.spin_cubetas.setSingleStep(2)  # Incrementar de 2 en 2
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
                padding: 10px 20px;
                font-size: 16px;
                border-radius: 10px;
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
        fila_controles.setSpacing(20)
        fila_controles.setAlignment(Qt.AlignCenter)

        lbl_cubetas = QLabel("Número de cubetas:")
        lbl_cubetas.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_registros = QLabel("Registros por cubeta:")
        lbl_registros.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_digitos = QLabel("Tamaño de claves:")
        lbl_digitos.setStyleSheet("font-size: 16px; font-weight: bold;")

        lbl_accion = QLabel("Acción:")
        lbl_accion.setStyleSheet("font-size: 16px; font-weight: bold;")

        fila_controles.addWidget(lbl_cubetas)
        fila_controles.addWidget(self.spin_cubetas)
        fila_controles.addWidget(lbl_registros)
        fila_controles.addWidget(self.spin_registros)
        fila_controles.addWidget(lbl_digitos)
        fila_controles.addWidget(self.spin_digitos)
        fila_controles.addWidget(lbl_accion)
        fila_controles.addWidget(self.combo_accion)

        controles.addLayout(fila_controles)

        # --- Grid de botones ---
        grid_botones = QGridLayout()
        grid_botones.addWidget(self.btn_crear, 0, 0)
        grid_botones.addWidget(self.btn_insertar, 0, 1)
        grid_botones.addWidget(self.btn_buscar_clave, 0, 2)
        grid_botones.addWidget(self.btn_eliminar_clave, 0, 3)
        grid_botones.addWidget(self.btn_deshacer, 1, 0)
        grid_botones.addWidget(self.btn_guardar, 1, 1)
        grid_botones.addWidget(self.btn_eliminar, 1, 2)
        grid_botones.addWidget(self.btn_cargar, 1, 3)

        controles.addLayout(grid_botones)
        layout.addLayout(controles)

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
        self.lbl_info = QLabel("Aquí se mostrará la simulación de la expansión o reducción total de cubetas.")
        self.lbl_info.setAlignment(Qt.AlignCenter)
        self.lbl_info.setStyleSheet("font-size: 18px; color: #2c3e50; margin: 20px;")
        self.contenedor_layout.addWidget(self.lbl_info)

        # --- Conectar eventos ---
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_insertar.clicked.connect(self.insertar_clave)
        self.btn_buscar_clave.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)

    def crear_estructura(self):
        """Crear la estructura de cubetas"""
        n = self.spin_cubetas.value()

        # Validar que sea par
        if n % 2 != 0:
            QMessageBox.warning(self, "Error", "El número de cubetas debe ser par.")
            return

        self.n = n
        self.R = self.spin_registros.value()
        self.num_digitos = self.spin_digitos.value()

        # Inicializar cubetas vacías
        self.cubetas = [[] for _ in range(self.n)]
        self.estructura_creada = True
        self.historial = []

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
        """Calcular ocupación = registros ocupados / registros disponibles"""
        ocupados = sum(len(cubeta) for cubeta in self.cubetas)
        disponibles = self.n * self.R
        return ocupados / disponibles if disponibles > 0 else 0

    def insertar_clave(self):
        """Insertar una nueva clave"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dialogo = DialogoClave(self, "Insertar Clave", self.num_digitos)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()

            if len(clave) != self.num_digitos or not clave.isdigit():
                QMessageBox.warning(self, "Error",
                                    f"La clave debe tener exactamente {self.num_digitos} dígitos.")
                return

            # Guardar estado para deshacer
            self.guardar_estado()

            # Calcular posición
            posicion = self.calcular_posicion(clave)

            # Verificar si la clave ya existe
            for cubeta in self.cubetas:
                if clave in cubeta:
                    QMessageBox.warning(self, "Error", "La clave ya existe.")
                    return

            # Insertar en la cubeta correspondiente
            if len(self.cubetas[posicion]) < self.R:
                self.cubetas[posicion].append(clave)
                self.actualizar_visualizacion()

                # Verificar si se debe expandir
                ocupacion = self.calcular_ocupacion()
                if ocupacion >= 0.75:
                    self.expandir()
            else:
                QMessageBox.warning(self, "Error",
                                    f"La cubeta {posicion} está llena. Se requiere expansión manual.")

    def expandir(self):
        """Expandir la estructura (duplicar número de cubetas)"""
        msg = f"Ocupación: {self.calcular_ocupacion() * 100:.1f}%\n"
        msg += f"Se expandirá de {self.n}x{self.R} a {self.n * 2}x{self.R}"

        respuesta = QMessageBox.question(self, "Expansión", msg,
                                         QMessageBox.Yes | QMessageBox.No)

        if respuesta == QMessageBox.Yes:
            # Guardar todas las claves
            todas_claves = []
            for cubeta in self.cubetas:
                todas_claves.extend(cubeta)

            # Duplicar número de cubetas
            self.n = self.n * 2
            self.cubetas = [[] for _ in range(self.n)]

            # Re-insertar todas las claves
            for clave in todas_claves:
                posicion = self.calcular_posicion(clave)
                self.cubetas[posicion].append(clave)

            self.actualizar_visualizacion()
            QMessageBox.information(self, "Éxito",
                                    f"Estructura expandida a {self.n} cubetas")

    def buscar_clave(self):
        """Buscar una clave"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dialogo = DialogoClave(self, "Buscar Clave", self.num_digitos)
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
        """Eliminar una clave"""
        if not self.estructura_creada:
            QMessageBox.warning(self, "Error", "Primero debe crear la estructura.")
            return

        dialogo = DialogoClave(self, "Eliminar Clave", self.num_digitos)
        if dialogo.exec() == QDialog.Accepted:
            clave = dialogo.get_clave()

            self.guardar_estado()

            posicion = self.calcular_posicion(clave)

            if clave in self.cubetas[posicion]:
                self.cubetas[posicion].remove(clave)
                self.actualizar_visualizacion()
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
            'R': self.R
        }
        self.historial.append(estado)

    def deshacer(self):
        """Deshacer último movimiento"""
        if not self.historial:
            QMessageBox.information(self, "Info", "No hay acciones para deshacer.")
            return

        estado = self.historial.pop()
        self.cubetas = estado['cubetas']
        self.n = estado['n']
        self.R = estado['R']

        self.actualizar_visualizacion()
        QMessageBox.information(self, "Éxito", "Acción deshecha.")

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
        """Actualizar la visualización de las cubetas"""
        # Limpiar contenedor
        while self.contenedor_layout.count():
            item = self.contenedor_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

        # Título con ocupación
        ocupacion = self.calcular_ocupacion()
        info_layout = QHBoxLayout()
        info_layout.setAlignment(Qt.AlignCenter)

        titulo = QLabel(f"Estructura: {self.n} cubetas x {self.R} registros")
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #4C1D95;")

        ocupacion_lbl = QLabel(f"Ocupación: {ocupacion * 100:.1f}%")
        color = "#059669" if ocupacion < 0.75 else "#DC2626"
        ocupacion_lbl.setStyleSheet(f"font-size: 18px; font-weight: bold; color: {color};")

        info_layout.addWidget(titulo)
        info_layout.addWidget(QLabel(" | "))
        info_layout.addWidget(ocupacion_lbl)

        self.contenedor_layout.addLayout(info_layout)

        # Crear grid de cubetas
        for i, cubeta in enumerate(self.cubetas):
            frame = QFrame()
            frame.setStyleSheet("""
                QFrame {
                    background-color: #F3F4F6;
                    border: 2px solid #7C3AED;
                    border-radius: 8px;
                    padding: 10px;
                }
            """)

            layout = QVBoxLayout(frame)

            # Título de cubeta
            titulo_cubeta = QLabel(f"Cubeta {i}")
            titulo_cubeta.setStyleSheet("font-size: 16px; font-weight: bold; color: #7C3AED;")
            titulo_cubeta.setAlignment(Qt.AlignCenter)
            layout.addWidget(titulo_cubeta)

            # Registros
            for j in range(self.R):
                if j < len(cubeta):
                    lbl = QLabel(f"R{j + 1}: {cubeta[j]}")
                    lbl.setStyleSheet("font-size: 14px; color: #1F2937; padding: 5px;")
                else:
                    lbl = QLabel(f"R{j + 1}: ---")
                    lbl.setStyleSheet("font-size: 14px; color: #9CA3AF; padding: 5px;")
                layout.addWidget(lbl)

            self.contenedor_layout.addWidget(frame)

