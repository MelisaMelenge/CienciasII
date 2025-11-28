from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel, QFrame,
    QComboBox, QSpinBox, QPushButton, QGridLayout, QScrollArea,
    QHBoxLayout, QDialog, QFileDialog
)
from PySide6.QtCore import Qt

from Controlador.Internas.truncamiento_controller import TruncamientoController
from Vista.dialogo_clave import DialogoClave
from Vista.dialogo_posiciones import DialogoPosiciones


class TruncamientoInterna(QMainWindow):
    def __init__(self, cambiar_ventana):
        super().__init__()
        self.cambiar_ventana = cambiar_ventana
        self.controller = TruncamientoController()
        self.setWindowTitle("Ciencias de la Computación II - Función Hash (Truncamiento)")

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

        titulo = QLabel("Ciencias de la Computación II - Función Hash (Truncamiento)")
        titulo.setAlignment(Qt.AlignCenter)
        titulo.setStyleSheet("font-size: 26px; font-weight: bold; color: #2d1f15; margin: 10px;")
        header_layout.addWidget(titulo)

        # --- Menú superior ---
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

        # --- Controles superiores ---
        controles_superiores = QHBoxLayout()
        controles_superiores.setSpacing(20)
        controles_superiores.setAlignment(Qt.AlignCenter)

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

        controles_superiores.addWidget(lbl_rango)
        controles_superiores.addWidget(self.rango)
        controles_superiores.addWidget(lbl_digitos)
        controles_superiores.addWidget(self.digitos)
        layout.addLayout(controles_superiores)

        # --- Botones principales con colores café ---
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

        botones_layout.addWidget(self.btn_crear, 0, 0)
        botones_layout.addWidget(self.btn_agregar, 0, 1)
        botones_layout.addWidget(self.btn_buscar, 0, 2)
        botones_layout.addWidget(self.btn_eliminar_clave, 0, 3)
        botones_layout.addWidget(self.btn_deshacer, 1, 0)
        botones_layout.addWidget(self.btn_guardar, 1, 1)
        botones_layout.addWidget(self.btn_eliminar, 1, 2)
        botones_layout.addWidget(self.btn_cargar, 1, 3)

        layout.addLayout(botones_layout)

        # --- Contenedor con scroll ---
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

        # Conexiones
        self.btn_crear.clicked.connect(self.crear_estructura)
        self.btn_agregar.clicked.connect(self.adicionar_claves)
        self.btn_cargar.clicked.connect(self.cargar_estructura)
        self.btn_eliminar.clicked.connect(self.eliminar_estructura)
        self.btn_buscar.clicked.connect(self.buscar_clave)
        self.btn_eliminar_clave.clicked.connect(self.eliminar_clave)
        self.btn_deshacer.clicked.connect(self.deshacer)
        self.btn_guardar.clicked.connect(self.guardar_estructura)

        # Estado
        self.labels = []
        self.capacidad = 0

    # ==============================================================
    # MÉTODOS FUNCIONALES
    # ==============================================================

    def crear_estructura(self):
        # Limpia la vista
        for i in reversed(range(self.grid.count())):
            w = self.grid.itemAt(i).widget()
            if w:
                w.setParent(None)
        self.labels.clear()

        n = int(self.rango.currentText().split("^")[1])
        self.capacidad = 10 ** n
        dig = self.digitos.value()
        self.controller.crear_estructura(self.capacidad, dig, [])

        try:
            digitos_req = self.controller._digitos_necesarios()
        except AttributeError:
            DialogoClave(0, titulo="Error", modo="mensaje", mensaje="El controlador no tiene el método '_digitos_necesarios'.", parent=self).exec()
            return

        dlg = DialogoPosiciones(dig, digitos_req, parent=self)
        if dlg.exec() == QDialog.Accepted:
            posiciones = dlg.get_posiciones(digitos_req)
            if posiciones and len(posiciones) == digitos_req:
                self.controller.posiciones = posiciones
                DialogoClave(0, titulo="OK", modo="mensaje", mensaje=f"Posiciones seleccionadas: {posiciones}", parent=self).exec()
            else:
                DialogoClave(0, titulo="Error", modo="mensaje", mensaje="Número incorrecto de posiciones.", parent=self).exec()
        else:
            DialogoClave(0, titulo="Cancelado", modo="mensaje", mensaje="Debes seleccionar posiciones.", parent=self).exec()

        # Dibujar estructura visual
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
            DialogoClave(0, titulo="Error", modo="mensaje", mensaje="Primero cree la estructura.", parent=self).exec()
            return

        if not self.controller.posiciones:
            DialogoClave(0, titulo="Error", modo="mensaje", mensaje="Seleccione las posiciones primero.", parent=self).exec()
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
        resultado = self.controller.agregar_clave(clave)

        if resultado == "OK":
            DialogoClave(0, titulo="Éxito", modo="mensaje", mensaje=f"Clave {clave} insertada correctamente.", parent=self).exec()
            self.actualizar_tabla()
        else:
            DialogoClave(0, titulo="Error", modo="mensaje", mensaje=f"Resultado: {resultado}", parent=self).exec()

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
        if not clave:
            return

        resultado = self.controller.eliminar_clave(clave)
        DialogoClave(0, titulo="Resultado", modo="mensaje", mensaje=resultado, parent=self).exec()
        self.actualizar_tabla()

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
        if not clave:
            return

        encontrado = None
        for pos, valor in self.controller.estructura.items():
            if str(valor) == clave:
                encontrado = pos
                break

        if encontrado:
            DialogoClave(0, titulo="Resultado", modo="mensaje", mensaje=f"Clave {clave} encontrada en posición {encontrado}", parent=self).exec()
        else:
            DialogoClave(0, titulo="Resultado", modo="mensaje", mensaje="Clave no encontrada.", parent=self).exec()

    def deshacer(self):
        res = self.controller.deshacer()
        DialogoClave(0, titulo="Deshacer", modo="mensaje", mensaje=res, parent=self).exec()
        self.actualizar_tabla()

    def eliminar_estructura(self):
        dialogo_confirmar = DialogoClave(
            0,
            titulo="Eliminar estructura",
            modo="confirmar",
            mensaje="¿Desea eliminar la estructura actual?",
            parent=self
        )
        if dialogo_confirmar.exec() == QDialog.Accepted:
            self.controller.estructura = {}
            self.controller.posiciones = []
            self.actualizar_tabla()
            DialogoClave(0, titulo="Éxito", modo="mensaje", mensaje="Estructura eliminada correctamente.", parent=self).exec()

    def guardar_estructura(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar estructura", "truncamiento_interna.json", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            self.controller.guardar()
            DialogoClave(0, titulo="Éxito", modo="mensaje", mensaje=f"Estructura guardada en:\n{ruta}", parent=self).exec()

    def cargar_estructura(self):
        ruta, _ = QFileDialog.getOpenFileName(self, "Cargar estructura", "", "Archivos JSON (*.json)")
        if ruta:
            self.controller.ruta_archivo = ruta
            if self.controller.cargar():
                DialogoClave(0, titulo="Éxito", modo="mensaje", mensaje="Estructura cargada correctamente.", parent=self).exec()
                self.actualizar_tabla()
            else:
                DialogoClave(0, titulo="Error", modo="mensaje", mensaje="No se pudo cargar el archivo.", parent=self).exec()

    def actualizar_tabla(self):
        for i, lbl in enumerate(self.labels, start=1):
            valor = self.controller.estructura.get(i, "")
            lbl.setText(str(valor) if valor else "")