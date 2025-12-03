#Controlador.Externas.Cambio_baseController

from Controlador.Externas.ZonaColisionesController import ZonaColisionesController
import copy, json, math, os

class CambioBaseController:
    def __init__(self):
        self.bloques = []
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.historial = []
        self.zona_colisiones = ZonaColisionesController()
        self.base = None

    # ==================== CREACIÓN ====================
    def crear_estructura(self, num_claves, base):
        """Crea la estructura principal y define la base elegida por el usuario."""
        if num_claves < 1:
            raise ValueError("num_claves debe ser >= 1")
        if base < 2:
            raise ValueError("la base debe ser >= 2")

        self.base = base

        self.num_claves = int(num_claves)
        b = max(1, int(math.floor(math.sqrt(self.num_claves))))
        num_bloques = int(math.ceil(self.num_claves / b))

        self.tamanio_bloque = b
        self.bloques = [[None for _ in range(b)] for _ in range(num_bloques)]

        self.historial.clear()
        self.zona_colisiones = ZonaColisionesController()
        return {
            "bloques": copy.deepcopy(self.bloques),
            "num_claves": self.num_claves,
            "tamanio_bloque": self.tamanio_bloque,
            "base": self.base
        }

    # ==================== INSERCIÓN ====================
    def insertar_clave(self, clave):
        if self.base is None:
            return False, "Debes definir la base antes de insertar claves."

        clave_s = str(clave)
        if not clave_s.isdigit():
            return False, "La clave debe ser numérica."

        # Asegurar 4 dígitos
        k_digitos = [int(d) for d in clave_s.zfill(4)]

        # Cambio de base: digMenSig(k)base r
        nuevo_valor = sum(k_digitos[i] * (self.base ** (3 - i)) for i in range(4))
        hash_val = nuevo_valor % 100
        if hash_val == 0:
            hash_val = 1

        pos_inicial = hash_val
        total_pos = self.num_claves

        # Recorrido lineal circular
        for intento in range(total_pos):
            pos_global = ((pos_inicial - 1 + intento) % total_pos) + 1
            bloque_idx = (pos_global - 1) // self.tamanio_bloque
            pos_idx = (pos_global - 1) % self.tamanio_bloque

            if self.bloques[bloque_idx][pos_idx] is None:
                self._guardar_historial()
                self.bloques[bloque_idx][pos_idx] = clave_s
                return True, (
                    f"Clave {clave_s} insertada en bloque {bloque_idx + 1}, "
                    f"posición {pos_idx + 1} )."
                )

        return (None, "collision", {
            "clave": clave_s,
            "hash_bloque": None,
            "bloque_objetivo": None,
            "hash_pos": None,
            "pos_objetivo": None
        })

    def insertar_en_zona_colisiones(self, clave):
        """Maneja la inserción en la zona de colisiones (controlador dedicado)."""
        ok, msg = self.zona_colisiones.insertar(clave)
        if ok:
            self._guardar_historial()
        return ok, msg

    # ==================== BÚSQUEDA / ELIMINACIÓN ====================
    def buscar_clave(self, clave):
        clave = str(clave)
        for i, bloque in enumerate(self.bloques):
            for j, val in enumerate(bloque):
                if val == clave:
                    return ("estructura", i, j)
        idx = self.zona_colisiones.buscar(clave)
        if idx is not None:
            return ("colision", idx)
        return None

    def eliminar_clave(self, clave):
        clave = str(clave)
        # Buscar en los bloques principales
        for i, bloque in enumerate(self.bloques):
            for j, val in enumerate(bloque):
                if val == clave:
                    self._guardar_historial()
                    bloque[j] = None
                    return True, f"Clave {clave} eliminada del bloque {i + 1}"

        # Buscar en la zona de colisiones
        idx = self.zona_colisiones.buscar(clave)
        if idx is not None:
            ok, msg = self.zona_colisiones.eliminar(clave)
            if ok:
                self._guardar_historial()
            return ok, msg

        return False, f"La clave {clave} no se encontró en la estructura ni en la zona de colisiones."

    # ==================== HISTORIAL / DESHACER ====================
    def _guardar_historial(self):
        self.historial.append({
            "bloques": copy.deepcopy(self.bloques),
            "zona": copy.deepcopy(self.zona_colisiones.zona)
        })

    def deshacer(self):
        if not self.historial:
            return False
        estado = self.historial.pop()
        self.bloques = estado["bloques"]
        self.zona_colisiones.zona = estado["zona"]
        return True

    # ==================== GUARDAR / CARGAR / ELIMINAR ====================
    def guardar_estructura(self, ruta):
        """Guarda toda la estructura (bloques + zona de colisiones) en un archivo JSON."""
        datos = {
            "num_claves": self.num_claves,
            "tamanio_bloque": self.tamanio_bloque,
            "bloques": self.bloques,
            "zona_colisiones": self.zona_colisiones.zona
        }
        try:
            with open(ruta, "w", encoding="utf-8") as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)
            return True, f"Estructura guardada correctamente en {ruta}."
        except Exception as e:
            return False, f"Error al guardar la estructura: {e}"

    def cargar_estructura(self, ruta):
        """Carga la estructura completa desde un archivo JSON, incluyendo zona de colisiones."""
        if not os.path.exists(ruta):
            return False, f"No se encontró el archivo: {ruta}"

        try:
            with open(ruta, "r", encoding="utf-8") as f:
                datos = json.load(f)

            self.num_claves = datos.get("num_claves", 0)
            self.tamanio_bloque = datos.get("tamanio_bloque", 0)
            self.bloques = datos.get("bloques", [])
            self.zona_colisiones = ZonaColisionesController()
            self.zona_colisiones.zona = datos.get("zona_colisiones", [])
            self.historial.clear()

            return True, "Estructura cargada correctamente."
        except Exception as e:
            return False, f"Error al cargar la estructura: {e}"

    def eliminar_estructura(self):
        """Borra la estructura completa (bloques, zona y registros)."""
        self.bloques = []
        self.zona_colisiones = ZonaColisionesController()
        self.num_claves = 0
        self.tamanio_bloque = 0
        self.historial.clear()
        return True, "Estructura eliminada correctamente."
