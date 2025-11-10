import sys
from PySide6.QtWidgets import QMainWindow, QStackedWidget
from Vista.inicio import Inicio
from Vista.busqueda import Busqueda
from Vista.grafos import Grafos
from Vista.lineal_interna import LinealInterna
from Vista.binaria_interna import BinariaInterna
from Vista.mod_interna import ModInterna
from Vista.cuadrado_interna import CuadradoInterna
from Vista.truncamiento_interna import TruncamientoInterna
from Vista.plegamiento_interna import PlegamientoInterna
from Vista.busqueda_residuos import BusquedaResiduos
from Vista.arboles_digitales import ArbolesDigitales
from Vista.tries_residuos import TriesResiduos
from Vista.multiples_residuos import MultiplesResiduos
from Vista.arboles_huffman import ArbolesHuffman

# ✅ Importa también las vistas de búsquedas externas
from Vista.lineal_externa import LinealExterna
from Vista.binaria_externa import BinariaExterna
from Vista.mod_externa import ModExterna
from Vista.cuadrado_externa import CuadradoExterna
from Vista.truncamiento_externa import TruncamientoExterna
from Vista.plegamiento_externa import PlegamientoExterna
from Vista.cambio_base import CambioBase
from Vista.CubetaTotal import CubetaTotal
from Vista.CubetaParcial import CubetaParcial
from Vista.Indices import Indices

#grafos
from Vista.interseccion_grafos import InterseccionGrafos
from Vista.union_grafos import UnionGrafos
from Vista.suma_anillo_grafos import SumaAnilloGrafos

class MainWindow(QMainWindow):
    def __init__(self, cambiar_pagina_callback):
        super().__init__()
        self.setWindowTitle("Ciencias de la Computación II")
        self.setGeometry(300, 200, 900, 600)

        self.stacked = QStackedWidget()
        self.setCentralWidget(self.stacked)

        # ----- Páginas -----
        self.inicio = Inicio(cambiar_pagina_callback)
        self.busqueda = Busqueda(cambiar_pagina_callback)
        self.grafos = Grafos(cambiar_pagina_callback)
        # Operaciones entre grafos
        self.interseccion_grafos = InterseccionGrafos(cambiar_pagina_callback)
        self.union_grafos = UnionGrafos(cambiar_pagina_callback)
        self.suma_anillo_grafos = SumaAnilloGrafos(cambiar_pagina_callback)

        # Internas
        self.lineal_interna = LinealInterna(cambiar_pagina_callback)
        self.binaria_interna = BinariaInterna(cambiar_pagina_callback)
        self.mod_interna = ModInterna(cambiar_pagina_callback)
        self.cuadrado_interna = CuadradoInterna(cambiar_pagina_callback)
        self.truncamiento_interna = TruncamientoInterna(cambiar_pagina_callback)
        self.plegamiento_interna = PlegamientoInterna(cambiar_pagina_callback)

        # Externas ✅
        self.lineal_externa = LinealExterna(cambiar_pagina_callback)
        self.binaria_externa = BinariaExterna(cambiar_pagina_callback)
        self.mod_externa = ModExterna(cambiar_pagina_callback)
        self.cuadrado_externa = CuadradoExterna(cambiar_pagina_callback)
        self.truncamiento_externa = TruncamientoExterna(cambiar_pagina_callback)
        self.plegamiento_externa = PlegamientoExterna(cambiar_pagina_callback)
        self.cambio_base = CambioBase(cambiar_pagina_callback)

        # Otros
        self.busqueda_residuos = BusquedaResiduos(cambiar_pagina_callback)
        self.arboles_digitales = ArbolesDigitales(cambiar_pagina_callback)
        self.tries_residuos = TriesResiduos(cambiar_pagina_callback)
        self.multiples_residuos = MultiplesResiduos(cambiar_pagina_callback)
        self.arboles_huffman = ArbolesHuffman(cambiar_pagina_callback)
        self.cubeta_total = CubetaTotal(cambiar_pagina_callback)
        self.cubeta_parcial = CubetaParcial(cambiar_pagina_callback)
        self.indices = Indices(cambiar_pagina_callback)

        # ----- Añadir al stack -----
        self.stacked.addWidget(self.inicio)                # 0
        self.stacked.addWidget(self.busqueda)              # 1
        self.stacked.addWidget(self.grafos)                # 2

        # Internas
        self.stacked.addWidget(self.lineal_interna)        # 3
        self.stacked.addWidget(self.binaria_interna)       # 4
        self.stacked.addWidget(self.mod_interna)           # 5
        self.stacked.addWidget(self.cuadrado_interna)      # 6
        self.stacked.addWidget(self.truncamiento_interna)  # 7
        self.stacked.addWidget(self.plegamiento_interna)   # 8

        # Externas
        self.stacked.addWidget(self.lineal_externa)        # 9
        self.stacked.addWidget(self.binaria_externa)       # 10
        self.stacked.addWidget(self.mod_externa)           # 11
        self.stacked.addWidget(self.cuadrado_externa)      # 12
        self.stacked.addWidget(self.truncamiento_externa)  # 13
        self.stacked.addWidget(self.plegamiento_externa)   # 14

        # Otros
        self.stacked.addWidget(self.busqueda_residuos)     # 15
        self.stacked.addWidget(self.arboles_digitales)     # 16
        self.stacked.addWidget(self.tries_residuos)        # 17
        self.stacked.addWidget(self.multiples_residuos)    # 18
        self.stacked.addWidget(self.arboles_huffman)       # 19
        self.stacked.addWidget(self.cambio_base)  # 20
        self.stacked.addWidget(self.cubeta_total)  # 21
        self.stacked.addWidget(self.cubeta_parcial)  # 22
        self.stacked.addWidget(self.indices)  # 23

        #Grafos
        self.stacked.addWidget(self.interseccion_grafos)  # 24
        self.stacked.addWidget(self.union_grafos)  # 25
        self.stacked.addWidget(self.suma_anillo_grafos)  # 26

        # Página inicial
        self.stacked.setCurrentIndex(0)

    def cambiar_pagina(self, nombre):
        paginas = {
            # Inicio
            "inicio": 0,
            "busqueda": 1,
            "grafos": 2,

            # Internas
            "lineal_interna": 3,
            "binaria_interna": 4,
            "mod_interna": 5,
            "cuadrado_interna": 6,
            "truncamiento_interna": 7,
            "plegamiento_interna": 8,

            # Externas ✅
            "lineal_externa": 9,
            "binaria_externa": 10,
            "mod_externa": 11,
            "cuadrado_externa": 12,
            "truncamiento_externa": 13,
            "plegamiento_externa": 14,

            # Otros
            "busqueda_residuos": 15,
            "arboles_digitales": 16,
            "tries_residuos": 17,
            "multiples_residuos": 18,
            "arboles_huffman": 19,
            "cambio_base": 20,
            "cubeta_total": 21,
            "cubeta_parcial": 22,
            "indices": 23,

            #grafos
            "interseccion_grafos": 24,
            "union_grafos": 25,
            "suma_anillo_grafos": 26,
        }

        if nombre in paginas:
            self.stacked.setCurrentIndex(paginas[nombre])
