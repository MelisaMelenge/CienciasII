from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QInputDialog, QHBoxLayout, QDialog, QFileDialog
)
from PySide6.QtCore import Qt
from .dialogo_clave import DialogoClave
from Controlador.Internas.mod_controller import ModController
from .dialogo_colision import DialogoColisiones


class ModInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = ModController()
        self.setWindowTitle("Ciencias de la Computación II - Función Hash (Módulo)")

        # --- Layout principal ---
        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Encabezado con gradiente café ---
        header = QFrame()
        header.setStyleSheet("""
            background: qlineargradient(
                spread:pad, x1:0, y1:0, x2:1, y2:0,
                stop:0 #9c724a, stop:1 #bf8f62
            );
            border-radius: 12px;
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setSpacing(5)
        header_layout.setContentsMargins(10, 10, 10, 10)

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Módulo)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
            font-size: 26px;
            font-weight: bold;
            color: #2d1f15;
            margin-top: 10px;
        """)
        header_layout.addWidget(titulo)

        # Menú con colores café
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
        layout.addWidget(header)

        # Conexiones del menú
        btn_inicio.clicked.connect(lambda: self.cambiar_ventana("inicio"))
        btn_busqueda.clicked.connect(lambda: self.cambiar_ventana("busqueda"))

        # --- Controles superiores alineados horizontalmente ---
        controles_superiores = QHBoxLayout()
        controles_superiores.setSpacing(15)
        controles_superiores.setAlignment(Qt.AlignCenter)

        lbl_rango = QLabel("Rango (10^n):")
        lbl_rango.setStyleSheet("font-weight: bold; font-size: 14px; color: #2d1f15;")
        self.rango = QComboBox()
        self.rango.addItems([str(i) for i in range(1, 7)])  # Solo números 1-6
        self.rango.setFixedWidth(100)
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
        self.digitos.setFixedWidth(60)
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

        controles_superiores.addWidget(lbl_rango)
        controles_superiores.addWidget(self.rango)
        controles_superiores.addWidget(lbl_digitos)
        controles_superiores.addWidget(self.digitos)

        layout.addLayout(controles_superiores)

        # --- Botones principales con colores café ---
        botones_layout = QGridLayout()
        botones_layout.setSpacing(12)
        botones_layout.setAlignment(Qt.AlignCenter)

        self.btn_crear = QPushButton("Crear estructura")
        self.btn_agregar = QPushButton("Adicionar claves")
        self.btn_buscar = QPushButton("Buscar clave")
        self.btn_eliminar_clave = QPushButton("Eliminar clave")
        self.btn_deshacer = QPushButton("Deshacer último movimiento")
        self.btn_guardar = QPushButton("Guardar estructura")
        self.btn_eliminar = QPushButton("Eliminar estructura")
        self.btn_cargar = QPushButton("Cargar estructura")

        botones = [
            self.btn_crear, self.btn_agregar, self.btn_buscar, self.btn_eliminar_clave,
            self.btn_deshacer, self.btn_guardar, self.btn_eliminar, self.btn_cargar
        ]

        for i, btn in enumerate(botones):
            btn.setFixedHeight(45)
            btn.setFixedWidth(240)

            btn.setStyleSheet("""
                QPushButton {
                    background-color: #9c724a;
                    color: #2d1f15;
                    font-size: 15px;
                    font-weight: bold;
                    border-radius: 10px;
                    padding: 8px 20px;
                }
                QPushButton:hover {
                    background-color: #bf8f62;
                }
            """)
            fila = i // 4
            col = i % 4
            botones_layout.addWidget(btn, fila, col, alignment=Qt.AlignCenter)

        layout.addLayout(botones_layout)

        # --- Contenedor con scroll para la estructura ---
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

        # --- Conexiones ---
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_agregar.clicked.connect(self.adicionar_claves)
        self.btn_cargar.clicked.connect(self.crear_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)

        # Estado
        self.labels = []
        self.indices_labels = []
        self.indices_reales = []
        self.capacidad = 0
        self.filas_info = []

    def crear_estructura(self):
        """Crea la estructura con vista dinámica similar a LinealInterna"""
        self._limpiar_vista()

        # Calcular capacidad desde el exponente
        n = int(self.rango.currentText())
        self.capacidad = 10 ** n

        # Crear estructura en el controlador
        self.controller.crear_estructura(self.capacidad, self.digitos.value())

        # Bloquear controles
        self.rango.setEnabled(False)
        self.digitos.setEnabled(False)

        # Reconstruir vista dinámica
        self._reconstruir_vista()

        self.controller.ultima_estrategia = None

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
        """Reconstruye la vista dinámicamente según las posiciones ocupadas"""
        self._limpiar_vista()

        if self.capacidad <= 10:
            self._crear_fila(0, self.capacidad, completa=True)
            return

        # Contar posiciones ocupadas (principales y anidadas)
        total_ocupadas = self._contar_ocupadas()

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
                            if self._posicion_ocupada(i)
                        )
                        if ocupadas_hasta_aqui <= fila_actual + 8:
                            self._crear_fila(fila_actual, 8, completa=False)
                            break
                        else:
                            self._crear_fila(fila_actual, 10, completa=True)
                            fila_actual += 10

    def _contar_ocupadas(self):
        """Cuenta todas las posiciones ocupadas (principales + anidadas)"""
        count = 0
        estructura = self.controller.estructura
        anidados = getattr(self.controller, "estructura_anidada", [])

        for i in range(self.capacidad):
            if self._posicion_ocupada(i):
                count += 1

        return count

    def _posicion_ocupada(self, idx):
        """Verifica si una posición tiene datos (principal o anidados)"""
        estructura = self.controller.estructura
        anidados = getattr(self.controller, "estructura_anidada", [])

        # Verificar posición principal (idx+1 porque estructura usa base 1)
        if estructura.get(idx + 1, "") != "":
            return True

        # Verificar si tiene elementos anidados
        if isinstance(anidados, list) and idx < len(anidados):
            sublista = anidados[idx]
            if sublista and len(sublista) > 0:
                return True

        return False

    def _crear_fila(self, inicio, cantidad, completa):
        """Crea una fila de bloques visuales"""
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
        """Agrega un bloque individual a la vista"""
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
        """Agrega un bloque especial (puntos suspensivos)"""
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
        self.indices_reales.append(-1)

    def _repintar(self):
        """Repinta los bloques según el estado actual"""
        for i, idx_real in enumerate(self.indices_reales):
            if idx_real == -1:
                continue

            lbl = self.labels[i]
            idx_lbl = self.indices_labels[i]

            # Obtener valor (recordar que estructura usa base 1)
            val = str(self.controller.estructura.get(idx_real + 1, ""))

            if val and val != "":
                lbl.setText(val)
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #bf8f62;
                        border: 2px solid #6C4E31;
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
                        font-size: 16px;
                        color: #2d1f15;
                    }
                """)

            idx_lbl.setText(str(idx_real + 1))

    def adicionar_claves(self):
        """Adiciona claves con manejo dinámico de la vista"""
        # Obtener cantidad total actual de claves (principales + anidadas)
        total_actual = len([v for v in self.controller.estructura.values() if v])
        anidados = getattr(self.controller, "estructura_anidada", [])
        if isinstance(anidados, list):
            total_actual += sum(len(sublista) for sublista in anidados if sublista)

        # Si ya se alcanzó el límite (capacidad total)
        if total_actual >= self.controller.capacidad:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Capacidad alcanzada",
                modo="mensaje",
                parent=self,
                mensaje=f"No se pueden agregar más claves.\nLa estructura ya contiene {total_actual} claves de un máximo de {self.controller.capacidad}."
            )
            dialogo.exec()
            return

        if self.capacidad == 0 or self.controller is None:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="Primero cree la estructura."
            )
            dialogo.exec()
            return

        # Obtener clave del usuario
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo=f"Clave de {self.digitos.value()} dígitos",
            modo="insertar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()

        # Intentar insertar
        resultado = self.controller.adicionar_clave(clave)

        # Si hubo colisión
        if resultado == "COLISION":
            if getattr(self.controller, "ultima_estrategia", None):
                estrategia = self.controller.ultima_estrategia
                resultado = self.controller.adicionar_clave(clave, estrategia)
            else:
                dlg_col = DialogoColisiones(self)
                if dlg_col.exec() == QDialog.Accepted:
                    estrategia = dlg_col.get_estrategia()
                    self.controller.ultima_estrategia = estrategia
                    resultado = self.controller.adicionar_clave(clave, estrategia)
                else:
                    dialogo = DialogoClave(
                        longitud=0,
                        titulo="Cancelado",
                        modo="mensaje",
                        parent=self,
                        mensaje="Inserción cancelada por el usuario."
                    )
                    dialogo.exec()
                    return

        # Manejar resultados
        if resultado == "OK":
            # Actualizar vista según estrategia
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                # Vista dinámica normal - reconstruir para mostrar la nueva posición
                self._reconstruir_vista_inteligente()
                self._repintar()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} insertada correctamente."
            )
            dialogo.exec()

        elif resultado == "LONGITUD":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave debe tener exactamente {self.digitos.value()} dígitos."
            )
            dialogo.exec()

        elif resultado == "REPETIDA":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="La clave ya existe en la estructura."
            )
            dialogo.exec()

        elif isinstance(resultado, str) and resultado.startswith("ERROR:"):
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=resultado
            )
            dialogo.exec()

        else:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"Resultado inesperado: {resultado}"
            )
            dialogo.exec()

    def _reconstruir_vista_inteligente(self):
        """Reconstruye la vista mostrando grupos de 10 según posiciones ocupadas"""
        self._limpiar_vista()

        if self.capacidad <= 10:
            self._crear_fila(0, self.capacidad, completa=True)
            return

        # Encontrar todos los grupos de 10 que tienen al menos una posición ocupada
        grupos_ocupados = set()
        for i in range(self.capacidad):
            if self._posicion_ocupada(i):
                grupo = (i // 10) * 10
                grupos_ocupados.add(grupo)

        # Convertir a lista ordenada
        grupos_ocupados = sorted(grupos_ocupados)

        if not grupos_ocupados:
            # Si no hay nada ocupado, mostrar solo las primeras 8 posiciones
            self._crear_fila(0, 8, completa=False)
            return

        # Mostrar cada grupo ocupado
        for i, grupo in enumerate(grupos_ocupados):
            self._crear_fila(grupo, 10, completa=True)

            # Si hay más grupos después, agregar puntos suspensivos
            if i < len(grupos_ocupados) - 1:
                # Verificar si el siguiente grupo NO es consecutivo
                if grupos_ocupados[i + 1] != grupo + 10:
                    fila_container = QWidget()
                    fila_container.setStyleSheet("background: transparent;")
                    fila_layout = QHBoxLayout(fila_container)
                    fila_layout.setSpacing(0)
                    fila_layout.setContentsMargins(0, 0, 0, 0)
                    fila_layout.setAlignment(Qt.AlignHCenter)

                    self._agregar_bloque_especial(fila_layout, "...", "...")
                    fila_layout.addStretch()

                    self.contenedor_layout.addWidget(fila_container, 0, Qt.AlignHCenter)

    def _reconstruir_vista_con_posicion(self, posicion_objetivo):
        """Reconstruye la vista asegurándose de incluir una posición específica (en grupos de 10)"""
        self._limpiar_vista()

        if self.capacidad <= 10:
            self._crear_fila(0, self.capacidad, completa=True)
            return

        # Calcular en qué grupo de 10 está la posición objetivo
        grupo_objetivo = (posicion_objetivo // 10) * 10

        # Encontrar todos los grupos ocupados
        grupos_ocupados = set()
        grupos_ocupados.add(grupo_objetivo)  # Agregar el grupo objetivo

        for i in range(self.capacidad):
            if self._posicion_ocupada(i):
                grupo = (i // 10) * 10
                grupos_ocupados.add(grupo)

        # Convertir a lista ordenada
        grupos_ocupados = sorted(grupos_ocupados)

        # Mostrar cada grupo
        for i, grupo in enumerate(grupos_ocupados):
            self._crear_fila(grupo, 10, completa=True)

            # Si hay más grupos después y no son consecutivos, agregar puntos
            if i < len(grupos_ocupados) - 1:
                if grupos_ocupados[i + 1] != grupo + 10:
                    fila_container = QWidget()
                    fila_container.setStyleSheet("background: transparent;")
                    fila_layout = QHBoxLayout(fila_container)
                    fila_layout.setSpacing(0)
                    fila_layout.setContentsMargins(0, 0, 0, 0)
                    fila_layout.setAlignment(Qt.AlignHCenter)

                    self._agregar_bloque_especial(fila_layout, "...", "...")
                    fila_layout.addStretch()

                    self.contenedor_layout.addWidget(fila_container, 0, Qt.AlignHCenter)


        # Seleccionar archivo
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                self.capacidad = self.controller.capacidad

                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    parent=self,
                    mensaje="Estructura cargada correctamente."
                )
                dialogo.exec()

                # Mostrar según la última estrategia usada
                estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

                if estrategia_actual == "Arreglo anidado":
                    self.actualizar_vista_anidada()
                elif estrategia_actual == "Lista encadenada":
                    self.actualizar_vista_encadenada()
                else:
                    self._reconstruir_vista_inteligente()
                    self._repintar()

            else:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    parent=self,
                    mensaje="No se pudo cargar la estructura."
                )
                dialogo.exec()

    def eliminar_estructura(self):
        dialogo = DialogoClave(
            longitud=0,
            titulo="Eliminar estructura",
            modo="confirmar",
            parent=self,
            mensaje="¿Está seguro de que desea eliminar la estructura actual?"
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        # Limpiar datos
        self.controller.estructura = {}
        self.controller.capacidad = 0
        self.controller.digitos = 0
        self.controller.historial.clear()

        if hasattr(self.controller, "estructura_anidada"):
            self.controller.estructura_anidada = []

        if hasattr(self.controller, "colisiones_controller"):
            cc = self.controller.colisiones_controller
            cc.estructura = [None] * getattr(cc, "tamaño", 0)
            cc.estructura_anidada = [None] * getattr(cc, "tamaño", 0)
            cc.ultima_estrategia = None
            cc.estrategia_fijada = False

        self.controller.ultima_estrategia = None

        # Limpiar vista
        self._limpiar_vista()
        self.capacidad = 0

        # Desbloquear controles
        self.rango.setEnabled(True)
        self.digitos.setEnabled(True)

        dialogo = DialogoClave(
            longitud=0,
            titulo="Éxito",
            modo="mensaje",
            parent=self,
            mensaje="Estructura eliminada correctamente."
        )
        dialogo.exec()

    def buscar_clave(self):
        """Busca una clave en la estructura (principal y anidada) y la muestra visualmente."""
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo="Buscar clave",
            modo="buscar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        estructura = self.controller.estructura
        anidados = self.controller.estructura_anidada

        encontrado = None
        detalle = ""
        posicion_real = None

        # Buscar en el arreglo principal
        for pos, valor in estructura.items():
            if str(valor).strip() == clave:
                encontrado = pos
                posicion_real = pos - 1  # Índice base 0
                detalle = f"en el arreglo principal (posición {pos})"
                break

        # Buscar en los arreglos/listas anidadas
        if not encontrado and isinstance(anidados, list):
            for i, sublista in enumerate(anidados):
                if not sublista:
                    continue

                sublista_str = [str(x).strip() for x in sublista if x is not None]

                if clave in sublista_str:
                    encontrado = i + 1
                    posicion_real = i  # Índice base 0
                    indice_anidado = sublista_str.index(clave)

                    estrategia_actual = getattr(self.controller, "ultima_estrategia", "")
                    if estrategia_actual == "Lista encadenada":
                        detalle = f"en la lista encadenada de la posición {i + 1}, nodo #{indice_anidado + 1}"
                    else:
                        detalle = f"en el arreglo anidado de la posición {i + 1}, índice interno {indice_anidado + 1}"
                    break

        # Resultado final
        if encontrado:
            # Verificar si la posición está visible en la vista actual
            if posicion_real not in self.indices_reales:
                # Si no está visible, reconstruir la vista para mostrarla
                dialogo_aviso = DialogoClave(
                    longitud=0,
                    titulo="Clave encontrada",
                    modo="mensaje",
                    parent=self,
                    mensaje=f"Clave {clave} encontrada {detalle}.\n\nLa vista se actualizará para mostrar esta posición."
                )
                dialogo_aviso.exec()

                # Forzar la reconstrucción incluyendo esta posición
                self._reconstruir_vista_con_posicion(posicion_real)
                self._repintar()

                # Resaltar la posición encontrada
                self._resaltar_posicion(posicion_real)
            else:
                # Si está visible, solo resaltarla
                self._resaltar_posicion(posicion_real)

            dialogo_resultado = DialogoClave(
                longitud=0,
                titulo="Resultado",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} encontrada {detalle}."
            )
            dialogo_resultado.exec()
        else:
            dialogo_resultado = DialogoClave(
                longitud=0,
                titulo="Resultado",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} no encontrada en la estructura."
            )
            dialogo_resultado.exec()

    def _reconstruir_vista_con_posicion(self, posicion_objetivo):
        """Reconstruye la vista asegurándose de incluir una posición específica"""
        self._limpiar_vista()

        if self.capacidad <= 10:
            self._crear_fila(0, self.capacidad, completa=True)
            return

        # Calcular en qué grupo de 10 está la posición objetivo
        grupo_objetivo = (posicion_objetivo // 10) * 10

        # Siempre mostrar las primeras 10 posiciones
        self._crear_fila(0, 10, completa=True)

        if grupo_objetivo > 0 and grupo_objetivo < self.capacidad - 10:
            # Mostrar el grupo donde está la posición buscada
            self._crear_fila(grupo_objetivo, 10, completa=True)

            # Puntos suspensivos si hay más datos después
            if grupo_objetivo + 10 < self.capacidad - 1:
                # Crear una fila especial con solo puntos
                fila_container = QWidget()
                fila_layout = QHBoxLayout(fila_container)
                fila_layout.setAlignment(Qt.AlignHCenter)
                self._agregar_bloque_especial(fila_layout, "...", "...")
                self.contenedor_layout.addWidget(fila_container, 0, Qt.AlignHCenter)

        # Siempre mostrar la última posición si no está ya visible
        if self.capacidad - 1 > grupo_objetivo + 9:
            fila_container = QWidget()
            fila_layout = QHBoxLayout(fila_container)
            fila_layout.setAlignment(Qt.AlignHCenter)
            self._agregar_bloque(fila_layout, self.capacidad - 1)
            self.contenedor_layout.addWidget(fila_container, 0, Qt.AlignHCenter)

    def _resaltar_posicion(self, posicion):
        """Resalta visualmente una posición específica"""
        try:
            pos_label = self.indices_reales.index(posicion)

            # Resetear estilos de todos los labels primero
            self._reset_label_styles()

            # Resaltar la posición encontrada
            self.labels[pos_label].setStyleSheet("""
                QLabel {
                    background-color: #9c724a;
                    border: 3px solid #603F26;
                    font-size: 18px;
                    font-weight: bold;
                    color: #FFEAC5;
                }
            """)
        except ValueError:
            # Si no se encuentra en la lista visible, no hay nada que resaltar
            pass

    def _reset_label_styles(self):
        """Resetea los estilos de todos los labels a su estado normal"""
        for i, lbl in enumerate(self.labels):
            if self.indices_reales[i] == -1:
                continue

            idx_real = self.indices_reales[i]
            val = str(self.controller.estructura.get(idx_real + 1, ""))

            if val and val != "":
                lbl.setStyleSheet("""
                    QLabel {
                        background-color: #bf8f62;
                        border: 2px solid #6C4E31;
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
                        font-size: 16px;
                        color: #2d1f15;
                    }
                """)

    def eliminar_clave(self):
        """Elimina una clave de la estructura con actualización dinámica."""
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo="Eliminar clave",
            modo="eliminar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        eliminada = False

        # Guardar estado antes de eliminar
        self.controller._guardar_estado()

        # Intentar eliminar del arreglo principal
        estructura = self.controller.estructura
        posiciones_a_borrar = [pos for pos, val in estructura.items() if str(val).strip() == clave]

        if posiciones_a_borrar:
            for pos in posiciones_a_borrar:
                estructura[pos] = ""

                if self.controller.colisiones_controller:
                    idx = pos - 1
                    self.controller.colisiones_controller.estructura[idx] = None

            eliminada = True

        # Intentar eliminar de los arreglos/listas anidadas
        anidados = self.controller.estructura_anidada
        if isinstance(anidados, list):
            for i, sublista in enumerate(anidados):
                if not sublista:
                    continue

                sublista_str = [str(x).strip() for x in sublista if x is not None]

                if clave in sublista_str:
                    for j, elem in enumerate(sublista):
                        if elem is not None and str(elem).strip() == clave:
                            del sublista[j]
                            eliminada = True

                            if self.controller.colisiones_controller:
                                self.controller.colisiones_controller.estructura_anidada[i] = sublista.copy()

                            break
                    break

        # Resultado final
        if eliminada:
            self.controller.estructura = estructura
            self.controller.estructura_anidada = anidados
            self.controller.guardar()

            # Actualizar vista según estrategia
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self._reconstruir_vista_inteligente()
                self._repintar()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave {clave} fue eliminada correctamente."
            )
            dialogo.exec()
        else:
            # Si no se eliminó nada, remover el estado guardado del historial
            if self.controller.historial:
                self.controller.historial.pop()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave {clave} no existe en la estructura."
            )
            dialogo.exec()

    def deshacer(self):
        """Deshace el último movimiento con actualización dinámica."""
        resultado = self.controller.deshacer()

        if isinstance(resultado, dict):
            # Caso extendido: el controlador devolvió un estado completo
            self.controller.estructura = resultado.get("estructura", self.controller.estructura)
            self.controller.estructura_anidada = resultado.get("estructura_anidada",
                                                               getattr(self.controller, "estructura_anidada", []))

            # Restaurar en el controlador de colisiones también
            if self.controller.colisiones_controller:
                self.controller.colisiones_controller.estructura = [None] * self.controller.capacidad
                for pos, valor in self.controller.estructura.items():
                    if valor and valor != "":
                        idx = pos - 1
                        try:
                            self.controller.colisiones_controller.estructura[idx] = int(valor)
                        except ValueError:
                            self.controller.colisiones_controller.estructura[idx] = valor

                self.controller.colisiones_controller.estructura_anidada = [
                    lst.copy() if lst else [] for lst in self.controller.estructura_anidada
                ]

            # Refrescar la vista según la estrategia activa
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self._reconstruir_vista_inteligente()
                self._repintar()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje="Se deshizo el último movimiento."
            )
            dialogo.exec()

        elif resultado == "OK":
            # Versión simple (antiguo comportamiento)
            estrategia_actual = getattr(self.controller, "ultima_estrategia", "")

            if estrategia_actual == "Arreglo anidado":
                self.actualizar_vista_anidada()
            elif estrategia_actual == "Lista encadenada":
                self.actualizar_vista_encadenada()
            else:
                self._reconstruir_vista_inteligente()
                self._repintar()

            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje="Se deshizo el último movimiento."
            )
            dialogo.exec()

        elif resultado == "VACIO":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Aviso",
                modo="mensaje",
                parent=self,
                mensaje="No hay movimientos para deshacer."
            )
            dialogo.exec()

        else:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"Ocurrió un error: {resultado}"
            )
            dialogo.exec()

    def guardar_estructura(self):
        # sugerimos nombre por defecto
        nombre_defecto = "interna_mod.json"
        ruta, _ = QFileDialog.getSaveFileName(
            self,
            "Guardar estructura",
            nombre_defecto,
            "Archivos JSON (*.json)"
        )
        if not ruta:
            return  # usuario canceló

        try:
            self.controller.ruta_archivo = ruta
            self.controller.guardar()
            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"Estructura guardada en:\n{ruta}"
            )
            dialogo.exec()
        except Exception as e:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"No se pudo guardar la estructura:\n{e}"
            )
            dialogo.exec()

    def actualizar_vista_anidada(self, modo="vertical"):
        """Dibuja el arreglo principal con sus arreglos anidados pegados visualmente."""
        # Limpiar grid (mantenemos compatibilidad con el método original)
        self._limpiar_vista()

        # Crear un nuevo grid para esta vista especial
        grid_especial = QGridLayout()
        grid_especial.setHorizontalSpacing(0)
        grid_especial.setVerticalSpacing(5)
        grid_especial.setContentsMargins(0, 0, 0, 0)

        # Datos
        estructura = self.controller.estructura or {}
        anidados = getattr(self.controller, "estructura_anidada", [])
        if not isinstance(anidados, list):
            anidados = []

        if len(anidados) != self.controller.capacidad:
            anidados = (anidados + [[]] * self.controller.capacidad)[:self.controller.capacidad]

        # Calcular el máximo global de colisiones
        max_colisiones_global = max((len(sublista) for sublista in anidados), default=0)

        # Título
        titulo = QLabel("Arreglo principal  |  Arreglos anidados (colisiones)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 18px; font-weight: bold; color: #6C4E31; margin-bottom: 15px;")
        grid_especial.addWidget(titulo, 0, 0, alignment=Qt.AlignCenter)

        # Construcción visual fila por fila
        fila_actual = 1
        for fila in range(1, self.controller.capacidad + 1):
            fila_layout = QHBoxLayout()
            fila_layout.setSpacing(0)
            fila_layout.setContentsMargins(0, 0, 0, 0)

            # Celda principal
            val = estructura.get(fila, "")
            texto = str(val).zfill(self.controller.digitos) if val else ""
            celda = QLabel(texto)
            celda.setFixedSize(70, 70)
            celda.setAlignment(Qt.AlignCenter)
            celda.setStyleSheet("""
                        background-color: #FFDBB5;
                        border: 2px solid #9c724a;
                        border-radius: 10px;
                        font-size: 16px;
                        color: #2d1f15;
                    """)
            fila_layout.addWidget(celda)

            # Arreglos anidados
            sublista = anidados[fila - 1] if fila - 1 < len(anidados) else []

            for j in range(max_colisiones_global):
                if j < len(sublista):
                    texto = str(sublista[j]).zfill(self.controller.digitos)
                    estilo = """
                                background-color: #EDCCAA;
                                border: 2px solid #9c724a;
                                border-left: none;
                                border-radius: 10px;
                                font-size: 16px;
                                color: #2d1f15;
                            """
                else:
                    texto = ""
                    estilo = """
                                border: 2px dashed #bf8f62;
                                border-left: none;
                                background-color: #FFF5EB;
                                border-radius: 10px;
                            """

                lbl = QLabel(texto)
                lbl.setFixedSize(70, 70)
                lbl.setAlignment(Qt.AlignCenter)
                lbl.setStyleSheet(estilo)
                fila_layout.addWidget(lbl)

            # Índice a la izquierda
            fila_layout_con_indice = QHBoxLayout()
            fila_layout_con_indice.setSpacing(10)
            fila_layout_con_indice.setContentsMargins(0, 0, 0, 0)

            idx = QLabel(str(fila))
            idx.setAlignment(Qt.AlignCenter)
            idx.setFixedWidth(30)
            idx.setStyleSheet("""
                        color: #9c724a;
                        font-size: 13px;
                        font-weight: bold;
                    """)
            fila_layout_con_indice.addWidget(idx)
            fila_layout_con_indice.addLayout(fila_layout)

            # Contenedor final de toda la fila
            fila_contenedor = QWidget()
            fila_contenedor.setLayout(fila_layout_con_indice)
            grid_especial.addWidget(fila_contenedor, fila_actual, 0, alignment=Qt.AlignLeft)

            fila_actual += 1

        # Agregar el grid especial al contenedor principal
        widget_especial = QWidget()
        widget_especial.setLayout(grid_especial)
        self.contenedor_layout.addWidget(widget_especial, 0, Qt.AlignHCenter)

    def actualizar_vista_encadenada(self):
        """Dibuja visualmente la estructura con listas encadenadas."""
        # Limpiar vista
        self._limpiar_vista()

        # Crear un nuevo grid para esta vista especial
        grid_especial = QGridLayout()
        grid_especial.setHorizontalSpacing(10)
        grid_especial.setVerticalSpacing(5)
        grid_especial.setContentsMargins(0, 0, 0, 0)

        # Título
        titulo = QLabel("Visualización: Lista Encadenada (colisiones con punteros)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("""
                    font-size: 18px;
                    font-weight: bold;
                    color: #6C4E31;
                    margin-bottom: 15px;
                """)
        grid_especial.addWidget(titulo, 0, 0, alignment=Qt.AlignCenter)

        fila_actual = 1

        for fila in range(1, self.controller.capacidad + 1):
            # Obtener valor principal
            val = self.controller.estructura.get(fila, "")

            # Obtener sublista
            sublista = self.controller.estructura_anidada[fila - 1] if fila - 1 < len(
                self.controller.estructura_anidada) else []

            # Asegurar que sublista sea una lista
            if sublista is None:
                sublista = []
            elif not isinstance(sublista, list):
                sublista = []

            fila_layout = QHBoxLayout()
            fila_layout.setSpacing(10)
            fila_layout.setContentsMargins(0, 0, 0, 0)

            # Nodo principal
            nodo = QLabel(str(val).zfill(self.controller.digitos) if val != "" else "")
            nodo.setFixedSize(70, 70)
            nodo.setAlignment(Qt.AlignCenter)
            nodo.setStyleSheet("""
                        background-color: #FFDBB5;
                        border: 2px solid #9c724a;
                        border-radius: 10px;
                        font-size: 16px;
                        color: #2d1f15;
                    """)
            fila_layout.addWidget(nodo)

            # Dibujar flechas y nodos encadenados
            for clave in sublista:
                flecha = QLabel("→")
                flecha.setAlignment(Qt.AlignCenter)
                flecha.setStyleSheet("font-size: 20px; color: #9c724a;")
                fila_layout.addWidget(flecha)

                nodo_col = QLabel(str(clave).zfill(self.controller.digitos))
                nodo_col.setFixedSize(70, 70)
                nodo_col.setAlignment(Qt.AlignCenter)
                nodo_col.setStyleSheet("""
                            background-color: #EDCCAA;
                            border: 2px solid #9c724a;
                            border-radius: 10px;
                            font-size: 16px;
                            color: #2d1f15;
                        """)
                fila_layout.addWidget(nodo_col)

            # Índice a la izquierda
            idx = QLabel(str(fila))
            idx.setAlignment(Qt.AlignCenter)
            idx.setFixedWidth(30)
            idx.setStyleSheet("color: #9c724a; font-size: 13px; font-weight: bold;")

            fila_layout_final = QHBoxLayout()
            fila_layout_final.addWidget(idx)
            fila_layout_final.addLayout(fila_layout)

            contenedor_fila = QWidget()
            contenedor_fila.setLayout(fila_layout_final)
            grid_especial.addWidget(contenedor_fila, fila_actual, 0, alignment=Qt.AlignLeft)

            fila_actual += 1

        # Agregar el grid especial al contenedor principal
        widget_especial = QWidget()
        widget_especial.setLayout(grid_especial)
        self.contenedor_layout.addWidget(widget_especial, 0, Qt.AlignHCenter)