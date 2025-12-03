import os
from Modelo.manejador_archivos import ManejadorArchivos


class TruncamientoController:
    def __init__(self, ruta_archivo="data/truncamiento.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.capacidad = 0
        self.digitos = 0
        self.posiciones = []  # posiciones elegidas por el usuario (1-based)
        self.historial = []
        self.estrategia_fija = None  # Para estrategias de colisión
        self.estructura_anidada = []  # Para arreglo anidado o lista encadenada
        # Alias para compatibilidad con los controladores de vista
        self.arreglo_anidado = []
        self.lista_encadenada = []

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    # -------------------------------
    # ESTADO / HISTORIAL
    # -------------------------------
    def _guardar_estado(self):
        """Guarda una copia del estado actual para poder deshacer."""
        estructura_copia = [lista.copy() if isinstance(lista, list) else lista
                            for lista in self.estructura_anidada] if self.estructura_anidada else []
        estado = {
            'estructura': self.estructura.copy(),
            'estructura_anidada': estructura_copia
        }
        self.historial.append(estado)

    # -------------------------------
    # CREACIÓN / CONFIGURACIÓN
    # -------------------------------
    def crear_estructura(self, capacidad: int, digitos: int, posiciones: list[int]):
        """Crea una nueva estructura vacía de truncamiento."""
        self.capacidad = int(capacidad)
        self.digitos = int(digitos)
        self.posiciones = list(posiciones)
        self.estructura = {i: "" for i in range(1, self.capacidad + 1)}
        self.estructura_anidada = []
        self.estrategia_fija = None
        self.historial.clear()
        self.guardar()
        return "OK"

    def _digitos_necesarios(self) -> int:
        """Determina cuántos dígitos se necesitan según la capacidad (mínimo 2)."""
        if self.capacidad <= 1:
            return 2
        return max(2, len(str(self.capacidad - 1)))

    # -------------------------------
    # FUNCIÓN HASH (TRUNCAMIENTO)
    # -------------------------------
    def funcion_hash(self, clave: str) -> int:
        """Calcula la posición hash usando truncamiento en las posiciones elegidas."""
        if not self.posiciones:
            raise ValueError("No se han definido posiciones para truncamiento.")
        if not clave.isdigit():
            raise ValueError("La clave debe ser numérica.")
        if len(clave) < max(self.posiciones):
            raise ValueError("Las posiciones elegidas superan la longitud de la clave.")

        seleccionados = [clave[p - 1] for p in self.posiciones[:self._digitos_necesarios()]]
        valor = int("".join(seleccionados))
        return (valor % self.capacidad) + 1 if self.capacidad > 0 else 1

    # -------------------------------
    # INSERCIÓN / ELIMINACIÓN / DESHACER
    # -------------------------------
    def agregar_clave(self, clave: str, estrategia: str = None) -> str:
        """Inserta una clave con manejo de colisiones."""
        if not clave.isdigit():
            return "NO_NUMERICA"
        if len(clave) != self.digitos:
            return "LONGITUD"

        # Verificar si ya existe en estructura principal
        if clave in self.estructura.values():
            return "REPETIDA"

        # Verificar si ya existe en estructura anidada
        if self.estructura_anidada:
            for sublista in self.estructura_anidada:
                if sublista and clave in sublista:
                    return "REPETIDA"

        try:
            pos = self.funcion_hash(clave)
        except Exception as e:
            return f"ERROR: {e}"

        if pos not in self.estructura:
            return "FUERA_RANGO"

        # Si no hay estrategia definida y la posición está ocupada -> COLISION
        if not estrategia and not self.estrategia_fija:
            if self.estructura[pos] != "":
                return "COLISION"

        # Usar estrategia fija si existe
        estrategia_a_usar = estrategia or self.estrategia_fija

        # Si no hay colisión, insertar directamente
        if self.estructura[pos] == "":
            self._guardar_estado()
            self.estructura[pos] = clave
            self.guardar()
            return "OK"

        # Hay colisión, aplicar estrategia
        if not estrategia_a_usar:
            return "COLISION"

        # Guardar estrategia para futuras inserciones
        if not self.estrategia_fija:
            self.estrategia_fija = estrategia_a_usar

        # Aplicar estrategias de colisión
        if estrategia_a_usar.lower() == "arreglo anidado":
            return self._insertar_arreglo_anidado(pos, clave)
        elif estrategia_a_usar.lower() == "lista encadenada":
            return self._insertar_lista_encadenada(pos, clave)
        elif estrategia_a_usar.lower() == "lineal":
            return self._insertar_lineal(pos, clave)
        elif estrategia_a_usar.lower() == "cuadrática":
            return self._insertar_cuadratica(pos, clave)
        elif estrategia_a_usar.lower() == "doble hash":
            return self._insertar_doble_hash(pos, clave)
        else:
            return f"ESTRATEGIA_DESCONOCIDA: {estrategia_a_usar}"

    def _insertar_arreglo_anidado(self, pos: int, clave: str) -> str:
        """Inserta usando arreglo anidado."""
        if not self.estructura_anidada:
            self.estructura_anidada = [[] for _ in range(self.capacidad)]

        self._guardar_estado()
        if not self.estructura_anidada[pos - 1]:
            self.estructura_anidada[pos - 1] = []
        self.estructura_anidada[pos - 1].append(clave)

        # Sincronizar con alias
        self.arreglo_anidado = self.estructura_anidada
        self.guardar()
        return "OK"

    def _insertar_lista_encadenada(self, pos: int, clave: str) -> str:
        """Inserta usando lista encadenada."""
        if not self.estructura_anidada:
            self.estructura_anidada = [[] for _ in range(self.capacidad)]

        self._guardar_estado()
        if not self.estructura_anidada[pos - 1]:
            self.estructura_anidada[pos - 1] = []
        self.estructura_anidada[pos - 1].append(clave)

        # Sincronizar con alias
        self.lista_encadenada = self.estructura_anidada
        self.guardar()
        return "OK"

    def _insertar_lineal(self, pos: int, clave: str) -> str:
        """Inserta usando sondeo lineal."""
        self._guardar_estado()
        intentos = 0
        pos_actual = pos

        while intentos < self.capacidad:
            if self.estructura[pos_actual] == "":
                self.estructura[pos_actual] = clave
                self.guardar()
                return "OK"
            pos_actual = (pos_actual % self.capacidad) + 1
            intentos += 1

        return "TABLA_LLENA"

    def _insertar_cuadratica(self, pos: int, clave: str) -> str:
        """Inserta usando sondeo cuadrático."""
        self._guardar_estado()
        intentos = 0

        while intentos < self.capacidad:
            offset = intentos ** 2
            pos_actual = ((pos - 1 + offset) % self.capacidad) + 1

            if self.estructura[pos_actual] == "":
                self.estructura[pos_actual] = clave
                self.guardar()
                return "OK"
            intentos += 1

        return "TABLA_LLENA"

    def _insertar_doble_hash(self, pos: int, clave: str) -> str:
        """Inserta usando doble hash."""
        self._guardar_estado()

        # Segunda función hash: 7 - (valor % 7)
        valor_clave = int(clave)
        hash2 = 7 - (valor_clave % 7)

        intentos = 0
        while intentos < self.capacidad:
            pos_actual = ((pos - 1 + intentos * hash2) % self.capacidad) + 1

            if self.estructura[pos_actual] == "":
                self.estructura[pos_actual] = clave
                self.guardar()
                return "OK"
            intentos += 1

        return "TABLA_LLENA"

    def eliminar_clave(self, clave: str) -> str:
        """Elimina una clave existente."""
        if not clave.isdigit():
            return "NO_NUMERICA"

        # Buscar en estructura principal
        for pos, valor in list(self.estructura.items()):
            if valor == clave:
                self._guardar_estado()
                self.estructura[pos] = ""
                self.guardar()
                return "OK"

        # Buscar en estructura anidada
        if self.estructura_anidada:
            for sublista in self.estructura_anidada:
                if sublista and clave in sublista:
                    self._guardar_estado()
                    sublista.remove(clave)
                    self.guardar()
                    return "OK"

        return "NO_EXISTE"

    def deshacer(self) -> str:
        """Revierte al último estado guardado."""
        if not self.historial:
            return "VACIO"

        estado_anterior = self.historial.pop()
        self.estructura = estado_anterior['estructura']
        self.estructura_anidada = estado_anterior.get('estructura_anidada', [])

        # Sincronizar con alias
        self.arreglo_anidado = self.estructura_anidada
        self.lista_encadenada = self.estructura_anidada

        self.guardar()
        return "OK"

    # -------------------------------
    # PERSISTENCIA
    # -------------------------------
    def guardar(self):
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "posiciones": self.posiciones,
            "estructura": self.estructura,
            "estrategia_fija": self.estrategia_fija,
            "estructura_anidada": self.estructura_anidada
        }
        try:
            ManejadorArchivos.guardar_json(self.ruta_archivo, datos)
        except Exception as e:
            print("Error guardando truncamiento:", e)

    def cargar(self) -> bool:
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if not datos:
            return False
        self.capacidad = int(datos.get("capacidad", 0))
        self.digitos = int(datos.get("digitos", 0))
        self.posiciones = list(datos.get("posiciones", []))
        self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
        self.estrategia_fija = datos.get("estrategia_fija")
        self.estructura_anidada = datos.get("estructura_anidada", [])

        # Sincronizar con alias
        self.arreglo_anidado = self.estructura_anidada
        self.lista_encadenada = self.estructura_anidada

        return True

    # -------------------------------
    # UTILIDADES
    # -------------------------------
    def obtener_datos_vista(self):
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "posiciones": self.posiciones,
            "estructura": self.estructura,
            "estrategia_fija": self.estrategia_fija,
            "estructura_anidada": self.estructura_anidada
        }

    def get_claves(self):
        claves = [v for v in self.estructura.values() if v != ""]
        if self.estructura_anidada:
            for sublista in self.estructura_anidada:
                if sublista:
                    claves.extend(sublista)
        return claves