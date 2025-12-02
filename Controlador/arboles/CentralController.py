#Controlador.arboles.CentralControllerv

from collections import deque


class CentralController:
    """Controlador para el algoritmo de centro de árbol"""

    def __init__(self):
        self.num_vertices = 0
        self.aristas = []
        self.etiquetas = {}

    def set_grafo(self, num_vertices, aristas, etiquetas=None):
        """Configura el grafo/árbol"""
        self.num_vertices = num_vertices
        self.aristas = aristas.copy()

        if etiquetas:
            self.etiquetas = etiquetas.copy()
        else:
            self.etiquetas = {i: chr(97 + i) for i in range(num_vertices)}

    def es_arbol(self):
        """Verifica si el grafo es un árbol"""
        if not self.aristas:
            return self.num_vertices == 1

        # Un árbol debe tener n-1 aristas
        if len(self.aristas) != self.num_vertices - 1:
            return False

        # Debe ser conexo
        return self.es_conexo()

    def es_conexo(self):
        """Verifica si el grafo es conexo usando BFS"""
        if self.num_vertices == 0:
            return True

        # Crear lista de adyacencia
        adyacencia = [[] for _ in range(self.num_vertices)]
        for origen, destino in self.aristas:
            adyacencia[origen].append(destino)
            adyacencia[destino].append(origen)

        # BFS desde el vértice 0
        visitados = [False] * self.num_vertices
        cola = deque([0])
        visitados[0] = True
        count = 1

        while cola:
            actual = cola.popleft()
            for vecino in adyacencia[actual]:
                if not visitados[vecino]:
                    visitados[vecino] = True
                    cola.append(vecino)
                    count += 1

        return count == self.num_vertices

    def calcular_distancias_desde(self, inicio):
        """Calcula las distancias desde un vértice a todos los demás usando BFS"""
        # Crear lista de adyacencia
        adyacencia = [[] for _ in range(self.num_vertices)]
        for origen, destino in self.aristas:
            adyacencia[origen].append(destino)
            adyacencia[destino].append(origen)

        # BFS
        distancias = [-1] * self.num_vertices
        distancias[inicio] = 0
        cola = deque([inicio])

        while cola:
            actual = cola.popleft()
            for vecino in adyacencia[actual]:
                if distancias[vecino] == -1:
                    distancias[vecino] = distancias[actual] + 1
                    cola.append(vecino)

        return distancias

    def calcular_excentricidades(self):
        """Calcula la excentricidad de cada vértice"""
        excentricidades = {}

        for vertice in range(self.num_vertices):
            distancias = self.calcular_distancias_desde(vertice)
            # La excentricidad es la máxima distancia desde este vértice
            excentricidad = max(distancias)
            excentricidades[vertice] = excentricidad

        return excentricidades

    def calcular_centro(self):
        """
        Calcula el centro del árbol
        Retorna: (centro, excentricidades, radio, diametro, detalles)
        """
        # Validar que sea un árbol
        if not self.es_arbol():
            return None, None, None, None, "Error: El grafo no es un árbol válido"

        # Calcular excentricidades
        excentricidades = self.calcular_excentricidades()

        # El radio es la mínima excentricidad
        radio = min(excentricidades.values())

        # El diámetro es la máxima excentricidad
        diametro = max(excentricidades.values())

        # El centro son los vértices con excentricidad igual al radio
        centro = [v for v, e in excentricidades.items() if e == radio]

        # Crear detalles
        detalles = self.generar_detalles(excentricidades, centro, radio, diametro)

        return centro, excentricidades, radio, diametro, detalles

    def generar_pasos_algoritmo(self):
        """
        Genera los pasos del algoritmo de encontrar el centro
        eliminando hojas (vértices de grado 1) iterativamente
        """
        pasos = []

        # Crear conjuntos y listas mutables
        vertices_activos = set(range(self.num_vertices))
        aristas_activas = self.aristas.copy()
        etiquetas_activas = self.etiquetas.copy()

        iteracion = 0

        # Paso inicial: Árbol original
        pasos.append({
            'titulo': f'Paso 0: Árbol Original',
            'descripcion': f' Árbol con {len(vertices_activos)} vértices y {len(aristas_activas)} aristas',
            'vertices_activos': sorted(list(vertices_activos)),
            'aristas': aristas_activas.copy(),
            'etiquetas': etiquetas_activas.copy(),
            'vertices_eliminados': []
        })

        # Iterar eliminando hojas hasta que queden 1 o 2 vértices
        while len(vertices_activos) > 2:
            iteracion += 1

            # Calcular grados solo para vértices activos
            grados = {v: 0 for v in vertices_activos}
            for origen, destino in aristas_activas:
                if origen in vertices_activos and destino in vertices_activos:
                    grados[origen] += 1
                    grados[destino] += 1

            # Encontrar hojas (vértices con grado 1)
            hojas = [v for v in vertices_activos if grados[v] == 1]

            if not hojas:
                # No hay más hojas, pero quedan más de 2 vértices
                # Esto no debería pasar en un árbol válido
                break

            # Crear descripción de las hojas encontradas
            hojas_etiquetas = [self.etiquetas[h] for h in sorted(hojas)]
            grados_texto = ", ".join([f"{self.etiquetas[h]}(grado={grados[h]})" for h in sorted(hojas)])

            # Paso: Mostrar hojas identificadas
            pasos.append({
                'titulo': f'Iteración {iteracion}a: Identificar Hojas',
                'descripcion': f' Hojas encontradas (grado 1): {", ".join(hojas_etiquetas)}\n   Detalles: {grados_texto}',
                'vertices_activos': sorted(list(vertices_activos)),
                'aristas': aristas_activas.copy(),
                'etiquetas': etiquetas_activas.copy(),
                'vertices_eliminados': []
            })

            # Eliminar hojas del conjunto de vértices activos
            for hoja in hojas:
                vertices_activos.remove(hoja)

            # Eliminar todas las aristas conectadas a las hojas
            nuevas_aristas = []
            for origen, destino in aristas_activas:
                # Solo mantener aristas que NO tocan ninguna hoja
                if origen not in hojas and destino not in hojas:
                    nuevas_aristas.append((origen, destino))

            aristas_activas = nuevas_aristas

            # Paso: Mostrar resultado después de eliminar hojas
            vertices_restantes = [self.etiquetas[v] for v in sorted(vertices_activos)]
            pasos.append({
                'titulo': f'Iteración {iteracion}b: Después de Eliminar Hojas',
                'descripcion': f'Eliminadas: {", ".join(hojas_etiquetas)}\n'
                               f'Quedan {len(vertices_activos)} vértices: {", ".join(vertices_restantes)}\n'
                               f' Aristas restantes: {len(aristas_activas)}',
                'vertices_activos': sorted(list(vertices_activos)),
                'aristas': aristas_activas.copy(),
                'etiquetas': etiquetas_activas.copy(),
                'vertices_eliminados': hojas
            })

        # Paso final: Centro encontrado
        centro_vertices = sorted(list(vertices_activos))
        centro_etiquetas = [self.etiquetas[v] for v in centro_vertices]

        if len(vertices_activos) == 1:
            desc = f'¡Centro encontrado!\n   Vértice central: {centro_etiquetas[0]}'
        else:
            desc = f' ¡Centro encontrado!\n   Vértices centrales: {", ".join(centro_etiquetas)}'

        pasos.append({
            'titulo': f'Resultado Final: Centro del Árbol',
            'descripcion': desc,
            'vertices_activos': sorted(list(vertices_activos)),
            'aristas': aristas_activas.copy(),
            'etiquetas': etiquetas_activas.copy(),
            'vertices_eliminados': []
        })

        return pasos

    def generar_detalles(self, excentricidades, centro, radio, diametro):
        """Genera un reporte detallado del análisis"""
        detalles = "=== RESULTADO FINAL ===\n\n"

        detalles += "EXCENTRICIDADES:\n"
        for vertice in sorted(excentricidades.keys()):
            etiqueta = self.etiquetas.get(vertice, str(vertice))
            exc = excentricidades[vertice]
            es_centro = " ← CENTRO ⭐" if vertice in centro else ""
            detalles += f"  Vértice {etiqueta}: e({etiqueta}) = {exc}{es_centro}\n"

        detalles += f"\n📏 RADIO del árbol: {radio}\n"
        detalles += f"📐 DIÁMETRO del árbol: {diametro}\n"

        detalles += f"\n🎯 CENTRO del árbol: "
        centro_etiquetas = [self.etiquetas.get(v, str(v)) for v in centro]
        if len(centro) == 1:
            detalles += f"{centro_etiquetas[0]}\n"
        else:
            detalles += f"{{{', '.join(centro_etiquetas)}}}\n"

        detalles += "\n💡 INTERPRETACIÓN:\n"
        if len(centro) == 1:
            etiq = centro_etiquetas[0]
            detalles += f"El vértice {etiq} es el centro del árbol.\n"
            detalles += f"Su excentricidad es {radio}, la menor de todos los vértices.\n"
        else:
            detalles += f"Los vértices {{{', '.join(centro_etiquetas)}}} forman el centro.\n"
            detalles += f"Ambos tienen excentricidad {radio}.\n"

        return detalles

    def obtener_matriz_distancias(self):
        """Genera la matriz de distancias completa"""
        matriz = []
        for i in range(self.num_vertices):
            distancias = self.calcular_distancias_desde(i)
            matriz.append(distancias)
        return matriz

    def generar_tabla_distancias_html(self):
        """Genera una tabla HTML con las distancias"""
        matriz = self.obtener_matriz_distancias()
        excentricidades = self.calcular_excentricidades()
        centro, _, _, _, _ = self.calcular_centro()

        html = '<table border="1" cellpadding="8" cellspacing="0" style="border-collapse: collapse; margin: 10px; font-family: Arial;">'

        # Encabezado - CAMBIO DE COLOR
        html += '<tr style="background-color: #9c724a; color: #FFEAC5; font-weight: bold;">'
        html += '<th></th>'
        for j in range(self.num_vertices):
            etiq = self.etiquetas.get(j, str(j))
            html += f'<th>{etiq}</th>'
        html += '<th>Exc.</th></tr>'

        # Filas
        for i in range(self.num_vertices):
            etiq_i = self.etiquetas.get(i, str(i))

            # Resaltar fila si es centro - CAMBIO DE VERDE A CAFÉ
            if i in centro:
                html += f'<tr style="background-color: #E8D4B8; font-weight: bold;">'
            else:
                html += '<tr>'

            html += f'<th style="background-color: #D3C1A8; color: #2d1f15;">{etiq_i}</th>'

            for j in range(self.num_vertices):
                dist = matriz[i][j]
                html += f'<td style="text-align: center;">{dist}</td>'

            # Excentricidad - resaltar si es centro - CAMBIO DE COLORES
            if i in centro:
                html += f'<td style="text-align: center; font-weight: bold; background-color: #8B6342; color: #FFEAC5;">{excentricidades[i]} </td>'
            else:
                html += f'<td style="text-align: center; font-weight: bold;">{excentricidades[i]}</td>'

            html += '</tr>'

        html += '</table>'
        return html