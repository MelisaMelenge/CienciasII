import os
from Modelo.manejador_archivos import ManejadorArchivos


class PlegamientoController:
    def __init__(self, ruta_archivo="data/plegamiento.json"):
        self.ruta_archivo = ruta_archivo
        self.estructura = {}
        self.arreglo_anidado = []
        self.lista_encadenada = []
        self.estructura_anidada = []  # Alias para compatibilidad
        self.capacidad = 0
        self.digitos = 0
        self.historial = []
        self.estrategia_fija = None

        os.makedirs(os.path.dirname(self.ruta_archivo), exist_ok=True)

    # -------------------------------
    # GUARDAR ESTADO (para deshacer)
    # -------------------------------
    def _guardar_estado(self):
        self.historial.append({
            'estructura': self.estructura.copy(),
            'arreglo_anidado': [sub.copy() for sub in self.arreglo_anidado],
            'lista_encadenada': [sub.copy() for sub in self.lista_encadenada]
        })

    # -------------------------------
    # CREAR ESTRUCTURA
    # -------------------------------
    def crear_estructura(self, capacidad, digitos):
        self.capacidad = capacidad
        self.digitos = digitos
        self.estructura = {i: "" for i in range(1, capacidad + 1)}
        self.arreglo_anidado = [[] for _ in range(capacidad)]
        self.lista_encadenada = [[] for _ in range(capacidad)]
        self.estructura_anidada = []
        self.estrategia_fija = None
        self.historial.clear()
        self.guardar()

    # -------------------------------
    # FUNCIÓN HASH (Plegamiento)
    # -------------------------------
    def funcion_hash(self, clave: int) -> int:
        clave_str = str(clave)
        partes = [int(clave_str[i:i + 2]) for i in range(0, len(clave_str), 2)]
        suma = sum(partes)
        pos = (suma % self.capacidad) + 1
        return pos

    # -------------------------------
    # VERIFICAR CLAVE REPETIDA
    # -------------------------------
    def _clave_existe(self, clave: str) -> bool:
        if clave in self.estructura.values():
            return True
        for sub in self.arreglo_anidado:
            if clave in sub:
                return True
        for sub in self.lista_encadenada:
            if clave in sub:
                return True
        return False

    # -------------------------------
    # ADICIONAR CLAVE
    # -------------------------------
    def adicionar_clave(self, clave: str, estrategia: str = None) -> str:
        if len(clave) != self.digitos:
            return "LONGITUD"

        if self._clave_existe(clave):
            return "REPETIDA"

        # Verificar si está llena
        total = sum(1 for v in self.estructura.values() if v != "")
        total += sum(len(sub) for sub in self.arreglo_anidado)
        total += sum(len(sub) for sub in self.lista_encadenada)
        if total >= self.capacidad * 10:  # Permitir más elementos con colisiones
            return "LLENO"

        try:
            clave_int = int(clave)
            pos = self.funcion_hash(clave_int)

            # --- Sin colisión ---
            if self.estructura[pos] == "":
                self._guardar_estado()
                self.estructura[pos] = clave
                self.guardar()
                return "OK"

            # --- Colisión ---
            if not estrategia and not self.estrategia_fija:
                return "COLISION"

            # Usar estrategia fija si existe
            estrategia_usar = estrategia or self.estrategia_fija
            if not self.estrategia_fija and estrategia:
                self.estrategia_fija = estrategia

            self._guardar_estado()
            estrategia_usar = estrategia_usar.lower()

            # Sondeo lineal
            if estrategia_usar in ["lineal", "sondeo lineal"]:
                for i in range(1, self.capacidad + 1):
                    nueva_pos = ((pos - 1 + i) % self.capacidad) + 1
                    if self.estructura[nueva_pos] == "":
                        self.estructura[nueva_pos] = clave
                        self.guardar()
                        return "OK"
                self.historial.pop()
                return "LLENO"

            # Arreglo anidado
            elif estrategia_usar == "arreglo anidado":
                idx = pos - 1
                self.arreglo_anidado[idx].append(clave)
                self.estructura_anidada = self.arreglo_anidado  # Sincronizar
                self.guardar()
                return "OK"

            # Lista encadenada
            elif estrategia_usar == "lista encadenada":
                idx = pos - 1
                self.lista_encadenada[idx].append(clave)
                self.estructura_anidada = self.lista_encadenada  # Sincronizar
                self.guardar()
                return "OK"

            else:
                self.historial.pop()
                return f"ERROR: Estrategia desconocida '{estrategia_usar}'"

        except ValueError:
            return "ERROR: La clave debe ser numérica"
        except Exception as e:
            return f"ERROR: {e}"

    # -------------------------------
    # BUSCAR CLAVE
    # -------------------------------
    def buscar_clave(self, clave: str) -> dict:
        """
        Busca una clave en toda la estructura.
        Retorna un diccionario con información de la búsqueda.
        """
        clave = str(clave)

        # Buscar en estructura principal
        for pos, valor in self.estructura.items():
            if valor == clave:
                return {
                    'encontrado': True,
                    'posicion': pos,
                    'tipo': 'principal',
                    'mensaje': f"Clave {clave} encontrada en posición {pos}"
                }

        # Buscar en arreglo anidado
        for idx, sub in enumerate(self.arreglo_anidado):
            if clave in sub:
                sub_idx = sub.index(clave)
                return {
                    'encontrado': True,
                    'posicion': idx + 1,
                    'sub_posicion': sub_idx,
                    'tipo': 'arreglo_anidado',
                    'mensaje': f"Clave {clave} encontrada en posición {idx + 1}, índice {sub_idx + 1} del arreglo anidado"
                }

        # Buscar en lista encadenada
        for idx, sub in enumerate(self.lista_encadenada):
            if clave in sub:
                sub_idx = sub.index(clave)
                return {
                    'encontrado': True,
                    'posicion': idx + 1,
                    'sub_posicion': sub_idx,
                    'tipo': 'lista_encadenada',
                    'mensaje': f"Clave {clave} encontrada en posición {idx + 1}, nodo {sub_idx + 1} de la lista encadenada"
                }

        return {
            'encontrado': False,
            'mensaje': f"Clave {clave} no encontrada"
        }

    # -------------------------------
    # ELIMINAR CLAVE
    # -------------------------------
    def eliminar_clave(self, clave: str) -> str:
        clave = str(clave)

        # Estructura principal
        for k, v in self.estructura.items():
            if v == clave:
                self._guardar_estado()
                self.estructura[k] = ""
                self.guardar()
                return "OK"

        # Arreglo anidado
        for idx, sub in enumerate(self.arreglo_anidado):
            if clave in sub:
                self._guardar_estado()
                sub.remove(clave)
                self.guardar()
                return "OK"

        # Lista encadenada
        for idx, sub in enumerate(self.lista_encadenada):
            if clave in sub:
                self._guardar_estado()
                sub.remove(clave)
                self.guardar()
                return "OK"

        return "NO_EXISTE"

    # -------------------------------
    # DESHACER
    # -------------------------------
    def deshacer(self):
        if not self.historial:
            return "VACIO"
        estado_anterior = self.historial.pop()
        self.estructura = estado_anterior['estructura']
        self.arreglo_anidado = estado_anterior['arreglo_anidado']
        self.lista_encadenada = estado_anterior['lista_encadenada']
        self.guardar()
        return "OK"

    # -------------------------------
    # GUARDAR / CARGAR
    # -------------------------------
    def guardar(self):
        datos = {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
            "arreglo_anidado": self.arreglo_anidado,
            "lista_encadenada": self.lista_encadenada,
            "estrategia_fija": self.estrategia_fija
        }
        ManejadorArchivos.guardar_json(self.ruta_archivo, datos)

    def cargar(self):
        datos = ManejadorArchivos.leer_json(self.ruta_archivo)
        if datos:
            self.capacidad = datos.get("capacidad", 0)
            self.digitos = datos.get("digitos", 0)
            self.estructura = {int(k): v for k, v in datos.get("estructura", {}).items()}
            self.arreglo_anidado = datos.get("arreglo_anidado", [[] for _ in range(self.capacidad)])
            self.lista_encadenada = datos.get("lista_encadenada", [[] for _ in range(self.capacidad)])
            self.estrategia_fija = datos.get("estrategia_fija")

            # Sincronizar estructura_anidada
            if self.arreglo_anidado and any(self.arreglo_anidado):
                self.estructura_anidada = self.arreglo_anidado
            elif self.lista_encadenada and any(self.lista_encadenada):
                self.estructura_anidada = self.lista_encadenada

            return True
        return False

    # -------------------------------
    # OBTENER DATOS PARA LA VISTA
    # -------------------------------
    def obtener_datos_vista(self):
        return {
            "capacidad": self.capacidad,
            "digitos": self.digitos,
            "estructura": self.estructura,
            "arreglo_anidado": self.arreglo_anidado,
            "lista_encadenada": self.lista_encadenada,
            "estructura_anidada": self.estructura_anidada,
            "estrategia_fija": self.estrategia_fija
        }

    def get_claves(self):
        claves = [v for v in self.estructura.values() if v != ""]
        for sub in self.arreglo_anidado:
            claves.extend(sub)
        for sub in self.lista_encadenada:
            claves.extend(sub)
        return claves