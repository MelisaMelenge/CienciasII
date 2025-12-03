from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton,
    QComboBox, QSpinBox, QGridLayout, QScrollArea,
    QFileDialog, QFrame, QDialog
)
from PySide6.QtCore import Qt
from Controlador.Internas.cuadrado_controller import CuadradoController
from Vista.dialogo_clave import DialogoClave
from Vista.dialogo_colision import DialogoColisiones
from Controlador.arreglo_anidado_controller import ArregloAnidadoController
from Vista.vista_arreglo_anidado import VistaArregloAnidado
from Controlador.lista_encadenada_controller import ListaEncadenadaController
from Vista.vista_lista_encadenada import VistaListaEncadenada


class CuadradoInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = CuadradoController()
        self.estrategia_actual = None  # Para recordar la estrategia seleccionada
        self.setWindowTitle("Ciencias de la Computación II - Función Hash (Cuadrado)")

        # --- Layout principal ---
        central = QWidget()
        central.setStyleSheet("background-color: #FFEAC5;")
        layout = QVBoxLayout(central)
        layout.setSpacing(20)
        layout.setContentsMargins(20, 20, 20, 20)

        # --- Encabezado con colores café ---
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

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Cuadrado)")
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

        # --- Controles superiores (misma línea) ---
        controles_layout = QHBoxLayout()
        controles_layout.setAlignment(Qt.AlignCenter)

        lbl_rango = QLabel("Rango (10^n):")
        lbl_rango.setStyleSheet("font-weight: bold; color: #2d1f15;")
        self.rango = QComboBox()
        self.rango.addItems([f"10^{i}" for i in range(1, 6)])
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
        lbl_digitos.setStyleSheet("font-weight: bold; color: #2d1f15;")
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

        controles_layout.addWidget(lbl_rango)
        controles_layout.addWidget(self.rango)
        controles_layout.addSpacing(20)
        controles_layout.addWidget(lbl_digitos)
        controles_layout.addWidget(self.digitos)
        layout.addLayout(controles_layout)

        # --- Botones con colores café ---
        botones_layout = QGridLayout()
        botones_layout.setSpacing(15)

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

        # --- Misma distribución que en ModInterna ---
        botones_layout.addWidget(self.btn_crear, 0, 0)
        botones_layout.addWidget(self.btn_agregar, 0, 1)
        botones_layout.addWidget(self.btn_buscar, 0, 2)
        botones_layout.addWidget(self.btn_eliminar_clave, 0, 3)
        botones_layout.addWidget(self.btn_deshacer, 1, 0)
        botones_layout.addWidget(self.btn_guardar, 1, 1)
        botones_layout.addWidget(self.btn_eliminar, 1, 2)
        botones_layout.addWidget(self.btn_cargar, 1, 3)

        layout.addLayout(botones_layout)

        # --- Área de scroll (visualización de estructura) ---
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.contenedor = QWidget()
        self.contenedor.setStyleSheet("background-color: transparent;")
        self.grid = QGridLayout(self.contenedor)
        self.grid.setAlignment(Qt.AlignCenter)
        self.scroll.setWidget(self.contenedor)
        layout.addWidget(self.scroll)

        self.setCentralWidget(central)

        # --- Conexiones ---
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_agregar.clicked.connect(self.adicionar_claves)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)

        self.labels = []
        self.capacidad = 0

    # --- Métodos funcionales ---
    def crear_estructura(self):
        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.setParent(None)
        self.labels.clear()
        self.estrategia_actual = None  # Resetear estrategia

        n = int(self.rango.currentText().split("^")[1])
        self.capacidad = 10 ** n
        self.controller.crear_estructura(self.capacidad, self.digitos.value())

        for i in range(min(self.capacidad, 100)):
            self._agregar_cuadro(i + 1, i + 1)

    def _agregar_cuadro(self, idx_visual, idx_real):
        fila = ((idx_visual - 1) // 10) * 2
        col = (idx_visual - 1) % 10

        cuadro = QLabel("")
        cuadro.setAlignment(Qt.AlignCenter)
        cuadro.setFixedSize(60, 60)
        cuadro.setStyleSheet("""
            QLabel {
                background-color: #FFDBB5;
                border: 2px solid #9c724a;
                border-radius: 12px;
                font-size: 16px;
                color: #2d1f15;
            }
        """)
        self.grid.addWidget(cuadro, fila, col, alignment=Qt.AlignCenter)

        numero = QLabel(str(idx_real))
        numero.setAlignment(Qt.AlignCenter)
        numero.setStyleSheet("font-size: 14px; color: #6C4E31; margin-top: 5px;")
        self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)

        self.labels.append(cuadro)

    def adicionar_claves(self):
        if self.capacidad == 0:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="Primero cree la estructura."
            )
            dialogo.exec()
            return

        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo=f"Clave de {self.digitos.value()} dígitos",
            modo="insertar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()

        # Si ya hay una estrategia definida, usarla directamente
        if self.estrategia_actual:
            resultado = self.controller.adicionar_clave(clave, self.estrategia_actual)

            if resultado == "OK":
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    parent=self,
                    mensaje=f"Clave {clave} insertada correctamente."
                )
                dialogo.exec()
                self.actualizar_vista_segun_estrategia()
            elif resultado == "LONGITUD":
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    parent=self,
                    mensaje="Longitud de clave incorrecta."
                )
                dialogo.exec()
            elif resultado == "REPETIDA":
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    parent=self,
                    mensaje="La clave ya existe."
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
            return

        # Primera inserción o sin estrategia definida
        resultado = self.controller.adicionar_clave(clave)

        if resultado == "COLISION":
            dlg_col = DialogoColisiones(self)
            if dlg_col.exec() == QDialog.Accepted:
                estrategia = dlg_col.get_estrategia()
                self.estrategia_actual = estrategia.lower()

                resultado = self.controller.adicionar_clave(clave, self.estrategia_actual)

                if resultado == "OK":
                    dialogo = DialogoClave(
                        longitud=0,
                        titulo="Éxito",
                        modo="mensaje",
                        parent=self,
                        mensaje=f"Clave {clave} insertada con estrategia: {estrategia}"
                    )
                    dialogo.exec()
                    self.actualizar_vista_segun_estrategia()
                elif resultado == "LONGITUD":
                    dialogo = DialogoClave(
                        longitud=0,
                        titulo="Error",
                        modo="mensaje",
                        parent=self,
                        mensaje="Longitud de clave incorrecta."
                    )
                    dialogo.exec()
                elif resultado == "REPETIDA":
                    dialogo = DialogoClave(
                        longitud=0,
                        titulo="Error",
                        modo="mensaje",
                        parent=self,
                        mensaje="La clave ya existe."
                    )
                    dialogo.exec()
            else:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Cancelado",
                    modo="mensaje",
                    parent=self,
                    mensaje="Inserción cancelada."
                )
                dialogo.exec()
                return

        elif resultado == "OK":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} insertada correctamente."
            )
            dialogo.exec()
            self.actualizar_tabla()
        elif resultado == "LONGITUD":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="Longitud de clave incorrecta."
            )
            dialogo.exec()
        elif resultado == "REPETIDA":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje="La clave ya existe."
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

    def actualizar_vista_segun_estrategia(self):
        """Actualiza la vista según la estrategia de colisión seleccionada"""
        if self.estrategia_actual == "arreglo anidado":
            anidado_ctrl = ArregloAnidadoController(self.controller)
            vista_anidada = VistaArregloAnidado(self.grid, anidado_ctrl)
            vista_anidada.dibujar()
        elif self.estrategia_actual == "lista encadenada":
            encadenada_ctrl = ListaEncadenadaController(self.controller)
            vista_encadenada = VistaListaEncadenada(self.grid, encadenada_ctrl)
            vista_encadenada.dibujar()
        else:
            # Estrategias de direccionamiento abierto (lineal, cuadrática, doble hash)
            self.actualizar_tabla()

    def cargar_estructura(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                self.capacidad = self.controller.capacidad

                # Detectar estrategia del archivo cargado
                if hasattr(self.controller, 'estrategia_fija') and self.controller.estrategia_fija:
                    self.estrategia_actual = self.controller.estrategia_fija.lower()

                # Si tiene estructura_anidada, es arreglo anidado o lista encadenada
                if hasattr(self.controller, 'estructura_anidada') and self.controller.estructura_anidada:
                    if not self.estrategia_actual:
                        self.estrategia_actual = "lista encadenada"

                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Éxito",
                    modo="mensaje",
                    parent=self,
                    mensaje=f"Estructura cargada correctamente.\nEstrategia: {self.estrategia_actual or 'direccionamiento abierto'}"
                )
                dialogo.exec()
                self.actualizar_vista_segun_estrategia()
            else:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Error",
                    modo="mensaje",
                    parent=self,
                    mensaje="No se pudo cargar el archivo."
                )
                dialogo.exec()

    def eliminar_estructura(self):
        dialogo = DialogoClave(
            longitud=0,
            titulo="Eliminar estructura",
            modo="confirmar",
            parent=self,
            mensaje="¿Desea eliminar la estructura actual?"
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        self.controller.estructura = {}
        self.controller.capacidad = 0
        self.controller.digitos = 0
        self.controller.historial.clear()
        self.estrategia_actual = None
        if hasattr(self.controller, 'estructura_anidada'):
            self.controller.estructura_anidada = []
        self.actualizar_tabla()

        dialogo = DialogoClave(
            longitud=0,
            titulo="Éxito",
            modo="mensaje",
            parent=self,
            mensaje="Estructura eliminada correctamente."
        )
        dialogo.exec()

    def buscar_clave(self):
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo="Buscar clave",
            modo="buscar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        if clave:
            datos = self.controller.obtener_datos_vista()
            encontrado = None
            posicion_detallada = None

            # Buscar en estructura principal
            for pos, valor in datos["estructura"].items():
                if str(valor) == clave:
                    encontrado = pos
                    posicion_detallada = f"posición {pos} (arreglo principal)"
                    break

            # Si no se encontró y hay estructura anidada, buscar ahí también
            if not encontrado and hasattr(self.controller, 'estructura_anidada'):
                for idx, sublista in enumerate(self.controller.estructura_anidada):
                    if sublista and isinstance(sublista, list):
                        for sub_idx, item in enumerate(sublista):
                            if str(item) == clave:
                                encontrado = idx + 1
                                posicion_detallada = f"posición {idx + 1} (lista encadenada {sub_idx + 1})"
                                break
                        if encontrado:
                            break

            if encontrado:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Resultado",
                    modo="mensaje",
                    parent=self,
                    mensaje=f"Clave {clave} encontrada en {posicion_detallada}"
                )
                dialogo.exec()
                self.resaltar_clave(encontrado, posicion_detallada)
            else:
                dialogo = DialogoClave(
                    longitud=0,
                    titulo="Resultado",
                    modo="mensaje",
                    parent=self,
                    mensaje=f"Clave {clave} no encontrada"
                )
                dialogo.exec()

    def resaltar_clave(self, posicion, detalle):
        """Resalta visualmente la clave encontrada"""
        if self.estrategia_actual in ["arreglo anidado", "lista encadenada"]:
            if self.estrategia_actual == "arreglo anidado":
                anidado_ctrl = ArregloAnidadoController(self.controller)
                vista_anidada = VistaArregloAnidado(self.grid, anidado_ctrl, resaltar=(posicion, detalle))
                vista_anidada.dibujar()
            elif self.estrategia_actual == "lista encadenada":
                encadenada_ctrl = ListaEncadenadaController(self.controller)
                vista_encadenada = VistaListaEncadenada(self.grid, encadenada_ctrl, resaltar=(posicion, detalle))
                vista_encadenada.dibujar()

    def eliminar_clave(self):
        dialogo = DialogoClave(
            longitud=self.digitos.value(),
            titulo="Eliminar clave",
            modo="eliminar",
            parent=self
        )
        if dialogo.exec() != QDialog.Accepted:
            return

        clave = dialogo.get_clave()
        if not clave.strip():
            return

        resultado = self.controller.eliminar_clave(clave.strip())
        if resultado == "OK":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje=f"Clave {clave} eliminada."
            )
            dialogo.exec()
            self.actualizar_vista_segun_estrategia()
        elif resultado == "NO_EXISTE":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"La clave {clave} no existe."
            )
            dialogo.exec()
        else:
            dialogo = DialogoClave(
                longitud=0,
                titulo="Error",
                modo="mensaje",
                parent=self,
                mensaje=f"Ocurrió un problema: {resultado}"
            )
            dialogo.exec()

    def deshacer(self):
        resultado = self.controller.deshacer()
        if resultado == "OK":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Éxito",
                modo="mensaje",
                parent=self,
                mensaje="Se deshizo el último movimiento."
            )
            dialogo.exec()
            self.actualizar_vista_segun_estrategia()
        elif resultado == "VACIO":
            dialogo = DialogoClave(
                longitud=0,
                titulo="Aviso",
                modo="mensaje",
                parent=self,
                mensaje="No hay movimientos para deshacer."
            )
            dialogo.exec()

    def guardar_estructura(self):
        ruta, _ = QFileDialog.getSaveFileName(
            self, "Guardar estructura", "cuadrado_interna.json", "Archivos JSON (*.json)"
        )
        if not ruta:
            return
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
                mensaje=f"No se pudo guardar:\n{e}"
            )
            dialogo.exec()

    def actualizar_tabla(self):
        """Actualiza la vista para estrategias de direccionamiento abierto"""
        datos = self.controller.obtener_datos_vista()
        estructura = datos.get("estructura", {})

        for i in reversed(range(self.grid.count())):
            widget = self.grid.itemAt(i).widget()
            if widget:
                widget.deleteLater()

        for i in range(self.controller.capacidad):
            fila = (i // 10) * 2
            col = i % 10
            celda = QLabel(str(estructura.get(i + 1, "")) or "")
            celda.setAlignment(Qt.AlignCenter)
            celda.setFixedSize(60, 60)
            celda.setStyleSheet("""
                QLabel {
                    background-color: #FFDBB5;
                    border: 2px solid #9c724a;
                    border-radius: 12px;
                    font-size: 16px;
                    color: #2d1f15;
                }
            """)
            self.grid.addWidget(celda, fila, col, alignment=Qt.AlignCenter)

            numero = QLabel(str(i + 1))
            numero.setAlignment(Qt.AlignCenter)
            numero.setStyleSheet("font-size: 14px; color: #6C4E31; margin-top: 5px;")
            self.grid.addWidget(numero, fila + 1, col, alignment=Qt.AlignCenter)

        self.labels = [
            self.grid.itemAt(j).widget()
            for j in range(0, self.grid.count(), 2)
        ]