#controlador.arboles.minimaController
from PySide6.QtWidgets import QFileDialog
from Vista.dialogo_arista import DialogoArista
from Vista.dialogo_clave import DialogoClave
import json


class MinimaController:
    def __init__(self, vista):
        self.vista = vista

        # Datos del grafo
        self.vertices = 0
        self.aristas = []
        self.etiquetas = {}
        self.ponderaciones = {}

        # Datos del árbol resultante
        self.arbol_aristas = []
        self.peso_total = 0

    # ==================== CALLBACKS ====================
    def actualizar_etiqueta(self, indice, nueva_etiqueta):
        """Actualiza la etiqueta de un vértice"""
        self.etiquetas[indice] = nueva_etiqueta

    def actualizar_ponderacion(self, arista, ponderacion):
        """Actualiza la ponderación de una arista"""
        if ponderacion.strip():
            try:
                # Intentar convertir a número
                valor = float(ponderacion)
                self.ponderaciones[arista] = valor
            except ValueError:
                # Si no es número, usar como string
                self.ponderaciones[arista] = ponderacion
        else:
            # Si está vacío, remover ponderación
            if arista in self.ponderaciones:
                del self.ponderaciones[arista]

    # ==================== GESTIÓN DEL GRAFO ====================
    def crear_grafo(self):
        """Crea un nuevo grafo con el número de vértices especificado"""
        self.vertices = self.vista.vertices_spin.value()
        self.aristas = []
        self.etiquetas = {i: str(i + 1) for i in range(self.vertices)}
        self.ponderaciones = {}

        self.vista.visual_grafo.set_grafo(
            self.vertices,
            self.aristas,
            self.etiquetas,
            self.ponderaciones
        )

        DialogoClave(0, "Grafo creado", "mensaje", self.vista,
                     f"Grafo creado con {self.vertices} vértices.").exec()

    def agregar_arista(self):
        """Agrega una arista al grafo"""
        if self.vertices == 0:
            DialogoClave(0, "Error", "mensaje", self.vista,
                         "Primero debes crear el grafo.").exec()
            return

        dlg = DialogoArista(self.vertices, self.vista, self.etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            self.aristas.append(arista)
            self.vista.visual_grafo.set_grafo(
                self.vertices,
                self.aristas,
                self.etiquetas,
                self.ponderaciones
            )

    def eliminar_arista(self):
        """Elimina una arista del grafo"""
        if not self.aristas:
            DialogoClave(0, "Error", "mensaje", self.vista,
                         "No hay aristas para eliminar.").exec()
            return

        dlg = DialogoArista(self.vertices, self.vista, self.etiquetas)
        if dlg.exec():
            arista = dlg.get_arista()
            if arista in self.aristas:
                self.aristas.remove(arista)
                if arista in self.ponderaciones:
                    del self.ponderaciones[arista]
                self.vista.visual_grafo.set_grafo(
                    self.vertices,
                    self.aristas,
                    self.etiquetas,
                    self.ponderaciones
                )
            else:
                DialogoClave(0, "Error", "mensaje", self.vista,
                             "La arista especificada no existe.").exec()

    def limpiar_grafo(self):
        """Limpia el grafo"""
        self.vertices = 0
        self.aristas = []
        self.etiquetas = {}
        self.ponderaciones = {}
        self.vista.visual_grafo.set_grafo(0, [], {}, {})
        self.vista.vertices_spin.setValue(4)
        self.limpiar_resultado()

    def guardar_grafo(self):
        """Guarda el grafo en un archivo JSON"""
        if self.vertices == 0:
            DialogoClave(0, "Error", "mensaje", self.vista,
                         "No hay grafo para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self.vista, "Guardar Grafo", "", "JSON Files (*.json)")
        if archivo:
            datos = {
                'vertices': self.vertices,
                'aristas': self.aristas,
                'etiquetas': self.etiquetas,
                'ponderaciones': {str(k): v for k, v in self.ponderaciones.items()}
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            DialogoClave(0, "Éxito", "mensaje", self.vista,
                         "Grafo guardado correctamente.").exec()

    def cargar_grafo(self):
        """Carga un grafo desde un archivo JSON"""
        archivo, _ = QFileDialog.getOpenFileName(
            self.vista, "Cargar Grafo", "", "JSON Files (*.json)")
        if archivo:
            with open(archivo, 'r', encoding='utf-8') as f:
                datos = json.load(f)

            self.vertices = datos['vertices']
            self.aristas = [tuple(a) for a in datos['aristas']]
            self.etiquetas = {int(k): v for k, v in datos.get('etiquetas', {}).items()}

            # Cargar ponderaciones
            self.ponderaciones = {}
            for k, v in datos.get('ponderaciones', {}).items():
                arista_tuple = tuple(map(int, k.strip('()').split(', ')))
                self.ponderaciones[arista_tuple] = v

            self.vista.vertices_spin.setValue(self.vertices)
            self.vista.visual_grafo.set_grafo(
                self.vertices,
                self.aristas,
                self.etiquetas,
                self.ponderaciones
            )

            DialogoClave(0, "Éxito", "mensaje", self.vista,
                         "Grafo cargado correctamente.").exec()

    # ==================== ALGORITMOS ====================
    def ejecutar_algoritmo(self):
        """Genera árbol eliminando aristas de mayor peso"""
        if self.vertices < 2:
            DialogoClave(0, "Error", "mensaje", self.vista,
                         "El grafo necesita al menos 2 vértices.").exec()
            return

        if not self.aristas:
            DialogoClave(0, "Error", "mensaje", self.vista,
                         "El grafo necesita al menos una arista.").exec()
            return

        # Obtener pesos de las aristas
        aristas_con_peso = []
        for arista in self.aristas:
            peso = self.ponderaciones.get(arista, 1)
            try:
                peso = float(peso)
            except (ValueError, TypeError):
                peso = 1
            aristas_con_peso.append((peso, arista))

        # Ordenar por peso (de menor a mayor)
        aristas_con_peso.sort()

        # Tomar las primeras n-1 aristas (árbol)
        self.arbol_aristas = []
        self.peso_total = 0

        for peso, arista in aristas_con_peso:
            if len(self.arbol_aristas) < self.vertices - 1:
                self.arbol_aristas.append(arista)
                self.peso_total += peso

        # Mostrar resultados
        self.mostrar_resultados()

    def mostrar_resultados(self):
        """Muestra los resultados del árbol generado"""
        # Visualizar árbol
        ponderaciones_arbol = {}
        for arista in self.arbol_aristas:
            if arista in self.ponderaciones:
                ponderaciones_arbol[arista] = self.ponderaciones[arista]

        self.vista.visual_arbol.set_grafo(
            self.vertices,
            self.arbol_aristas,
            self.etiquetas,
            ponderaciones_arbol
        )

        # Clasificar aristas
        ramas = self.arbol_aristas
        cuerdas = [a for a in self.aristas if a not in self.arbol_aristas]

        # Tab Información General - Mostrar Ramas y Cuerdas
        info_html = f"""
        <h3>Árbol de Expansión Mínima</h3>
        <p><b>Peso total del árbol:</b> {self.peso_total}</p>
        <p><b>Número de aristas en el árbol:</b> {len(self.arbol_aristas)}</p>

        <h4>Ramas (Aristas del Árbol):</h4>
        <ul>
        """

        for arista in ramas:
            u, v = arista
            etiq_u = self.etiquetas.get(u, str(u + 1))
            etiq_v = self.etiquetas.get(v, str(v + 1))
            peso = self.ponderaciones.get(arista, 1)
            info_html += f"<li>({etiq_u}, {etiq_v}) = {peso}</li>"

        info_html += "</ul>"

        if cuerdas:
            info_html += "<h4>Cuerdas (Aristas NO usadas):</h4><ul>"
            for arista in cuerdas:
                u, v = arista
                etiq_u = self.etiquetas.get(u, str(u + 1))
                etiq_v = self.etiquetas.get(v, str(v + 1))
                peso = self.ponderaciones.get(arista, 1)
                info_html += f"<li>({etiq_u}, {etiq_v}) = {peso}</li>"
            info_html += "</ul>"
        else:
            info_html += "<p><i>No hay cuerdas (todas las aristas están en el árbol)</i></p>"

        self.vista.info_text.setHtml(info_html)

        # Analizar circuitos, conjuntos de corte y matrices
        self.analizar_circuitos_grafo_original()
        self.analizar_circuitos_fundamentales()
        self.analizar_conjuntos_corte()
        self.generar_matrices()

        DialogoClave(0, "Árbol Generado", "mensaje", self.vista,
                     f"Árbol de expansión generado.\n"
                     f"Peso total: {self.peso_total}").exec()

    def analizar_circuitos_grafo_original(self):
        """Encuentra todos los circuitos del grafo ORIGINAL usando DFS"""
        circuitos_html = "<h3>Circuitos del Grafo Original</h3>"
        circuitos_html += "<p>Circuitos encontrados con sus ponderaciones:</p>"

        # Construir grafo de adyacencia
        grafo = {i: [] for i in range(self.vertices)}
        for u, v in self.aristas:
            grafo[u].append(v)
            grafo[v].append(u)

        circuitos_encontrados = []

        def dfs_ciclos(inicio, actual, visitados, camino, padre):
            """Busca ciclos usando DFS"""
            visitados.add(actual)
            camino.append(actual)

            for vecino in grafo[actual]:
                if vecino == padre:
                    continue

                if vecino == inicio and len(camino) >= 3:
                    # Encontramos un ciclo
                    ciclo = camino.copy()
                    ciclo_normalizado = tuple(sorted(ciclo))
                    if ciclo_normalizado not in circuitos_encontrados:
                        circuitos_encontrados.append(ciclo_normalizado)
                elif vecino not in visitados:
                    dfs_ciclos(inicio, vecino, visitados, camino, actual)

            camino.pop()
            visitados.remove(actual)

        # Buscar ciclos desde cada vértice
        for v in range(self.vertices):
            dfs_ciclos(v, v, set(), [], -1)

        if circuitos_encontrados:
            for idx, ciclo in enumerate(circuitos_encontrados, 1):
                # Obtener ponderaciones del ciclo
                ponderaciones_ciclo = []
                ciclo_list = list(ciclo)

                for i in range(len(ciclo_list)):
                    u = ciclo_list[i]
                    v = ciclo_list[(i + 1) % len(ciclo_list)]

                    arista1 = (u, v)
                    arista2 = (v, u)

                    peso = None
                    if arista1 in self.ponderaciones:
                        peso = self.ponderaciones[arista1]
                    elif arista2 in self.ponderaciones:
                        peso = self.ponderaciones[arista2]
                    else:
                        peso = 1

                    ponderaciones_ciclo.append(str(peso))

                # Crear representación del circuito
                etiquetas_ciclo = [self.etiquetas.get(v, str(v + 1)) for v in ciclo_list]
                circuito_str = " → ".join(etiquetas_ciclo) + f" → {etiquetas_ciclo[0]}"
                ponderaciones_str = f"({', '.join(ponderaciones_ciclo)})"

                circuitos_html += f"<p><b>Circuito {idx}:</b> {circuito_str}<br>"
                circuitos_html += f"<b>Ponderaciones:</b> {ponderaciones_str}</p>"
        else:
            circuitos_html += "<p><i>No se encontraron circuitos en el grafo original</i></p>"

        self.vista.circuitos_text.setHtml(circuitos_html)

    def analizar_circuitos_fundamentales(self):
        """Analiza circuitos fundamentales - uno por cada cuerda"""
        cuerdas = [a for a in self.aristas if a not in self.arbol_aristas]

        if not cuerdas:
            self.vista.circuitos_fund_text.setHtml("<p>No hay circuitos fundamentales (no hay cuerdas).</p>")
            return

        from collections import deque

        def encontrar_camino(u, v, aristas_arbol):
            """Encuentra el camino entre u y v usando BFS"""
            grafo = {i: [] for i in range(self.vertices)}
            for a, b in aristas_arbol:
                grafo[a].append(b)
                grafo[b].append(a)

            visitados = set()
            cola = deque([(u, [u])])
            visitados.add(u)

            while cola:
                actual, camino = cola.popleft()
                if actual == v:
                    return camino

                for vecino in grafo[actual]:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append((vecino, camino + [vecino]))

            return []

        # Tab Circuitos Fundamentales
        circuitos_fund_html = "<h3>Circuitos Fundamentales</h3>"
        circuitos_fund_html += f"<p>Cada cuerda genera un circuito fundamental único. Total: {len(cuerdas)} circuitos</p>"

        for idx, cuerda in enumerate(cuerdas, 1):
            u, v = cuerda
            camino = encontrar_camino(u, v, self.arbol_aristas)

            if camino:
                # Obtener ponderaciones del circuito
                ponderaciones_circuito = []

                # Ponderaciones de las ramas en el camino
                for i in range(len(camino) - 1):
                    origen = camino[i]
                    destino = camino[i + 1]

                    arista1 = (origen, destino)
                    arista2 = (destino, origen)

                    if arista1 in self.ponderaciones:
                        ponderaciones_circuito.append(str(self.ponderaciones[arista1]))
                    elif arista2 in self.ponderaciones:
                        ponderaciones_circuito.append(str(self.ponderaciones[arista2]))
                    else:
                        ponderaciones_circuito.append("1")

                # Ponderación de la cuerda
                peso_cuerda = self.ponderaciones.get(cuerda, self.ponderaciones.get((v, u), 1))
                ponderaciones_circuito.append(str(peso_cuerda))

                etiq_u = self.etiquetas.get(u, str(u + 1))
                etiq_v = self.etiquetas.get(v, str(v + 1))

                # Construir representación del circuito
                circuito = [self.etiquetas.get(n, str(n + 1)) for n in camino]
                circuito_str = " → ".join(circuito) + f" → {etiq_u}"

                ponderaciones_str = f"({', '.join(ponderaciones_circuito)})"

                circuitos_fund_html += f"<p><b>CF{idx}:</b> (con cuerda ({etiq_u}, {etiq_v}))<br>"
                circuitos_fund_html += f"<b>Camino:</b> {circuito_str}<br>"
                circuitos_fund_html += f"<b>Ponderaciones:</b> {ponderaciones_str}</p>"

        self.vista.circuitos_fund_text.setHtml(circuitos_fund_html)

    def generar_matrices(self):
        """Genera matrices de adyacencia e incidencia"""
        # Clasificar aristas
        ramas = self.arbol_aristas
        cuerdas = [a for a in self.aristas if a not in self.arbol_aristas]

        # Matriz de adyacencia del árbol
        matriz_ady = [[0] * self.vertices for _ in range(self.vertices)]
        for u, v in ramas:
            matriz_ady[u][v] = 1
            matriz_ady[v][u] = 1

        # Matriz de incidencia del árbol
        matriz_inc = [[0] * len(ramas) for _ in range(self.vertices)]
        for idx, (u, v) in enumerate(ramas):
            matriz_inc[u][idx] = 1
            matriz_inc[v][idx] = 1

        # Generar HTML
        matrices_html = "<div style='max-width: 100%; overflow-x: auto;'>"

        # Matriz de Adyacencia
        matrices_html += "<h3>Matriz de Adyacencia (del Árbol)</h3>"
        matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
        matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'></th>"
        for i in range(self.vertices):
            matrices_html += f"<th style='padding: 10px;'>{self.etiquetas.get(i, str(i + 1))}</th>"
        matrices_html += "</tr>"

        for i in range(self.vertices):
            matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>{self.etiquetas.get(i, str(i + 1))}</th>"
            for j in range(self.vertices):
                matrices_html += f"<td align='center' style='padding: 10px;'>{matriz_ady[i][j]}</td>"
            matrices_html += "</tr>"
        matrices_html += "</table><br>"

        # Matriz de Incidencia
        matrices_html += "<h3>Matriz de Incidencia (del Árbol)</h3>"
        matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
        matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'></th>"
        for idx, (u, v) in enumerate(ramas):
            etiq_u = self.etiquetas.get(u, str(u + 1))
            etiq_v = self.etiquetas.get(v, str(v + 1))
            matrices_html += f"<th style='padding: 10px;'>e{idx + 1}<br>({etiq_u},{etiq_v})</th>"
        matrices_html += "</tr>"

        for i in range(self.vertices):
            matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>{self.etiquetas.get(i, str(i + 1))}</th>"
            for j in range(len(ramas)):
                matrices_html += f"<td align='center' style='padding: 10px;'>{matriz_inc[i][j]}</td>"
            matrices_html += "</tr>"
        matrices_html += "</table><br>"

        # Matriz Circuitos vs Aristas (solo si hay cuerdas)
        if cuerdas:
            matrices_html += "<h3>Matriz Circuitos Fundamentales vs Aristas</h3>"
            matrices_html += "<p style='font-size: 11px; color: #6C4E31;'>Filas: Circuitos | Columnas: Ponderaciones de todas las aristas</p>"

            todas_aristas = ramas + cuerdas

            matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
            matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'>Circuito</th>"

            for arista in todas_aristas:
                u, v = arista
                etiq_u = self.etiquetas.get(u, str(u + 1))
                etiq_v = self.etiquetas.get(v, str(v + 1))
                peso = self.ponderaciones.get(arista, 1)
                matrices_html += f"<th style='padding: 10px;'>({etiq_u},{etiq_v})<br>p={peso}</th>"
            matrices_html += "</tr>"

            from collections import deque

            def encontrar_camino(u, v, aristas_arbol):
                grafo = {i: [] for i in range(self.vertices)}
                for a, b in aristas_arbol:
                    grafo[a].append(b)
                    grafo[b].append(a)

                visitados = set()
                cola = deque([(u, [u])])
                visitados.add(u)

                while cola:
                    actual, camino = cola.popleft()
                    if actual == v:
                        return camino

                    for vecino in grafo[actual]:
                        if vecino not in visitados:
                            visitados.add(vecino)
                            cola.append((vecino, camino + [vecino]))

                return []

            for idx_circuito, cuerda in enumerate(cuerdas, 1):
                u, v = cuerda
                camino = encontrar_camino(u, v, ramas)

                matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>C{idx_circuito}</th>"

                if camino:
                    aristas_en_circuito = set()

                    # Aristas del camino en el árbol
                    for i in range(len(camino) - 1):
                        arista1 = (camino[i], camino[i + 1])
                        arista2 = (camino[i + 1], camino[i])
                        aristas_en_circuito.add(arista1)
                        aristas_en_circuito.add(arista2)

                    # La cuerda que cierra el circuito
                    aristas_en_circuito.add(cuerda)
                    aristas_en_circuito.add((v, u))

                    for arista in todas_aristas:
                        if arista in aristas_en_circuito:
                            peso = self.ponderaciones.get(arista, 1)
                            matrices_html += f"<td align='center' style='padding: 10px; font-weight: bold; color: #d9534f;'>{peso}</td>"
                        else:
                            matrices_html += "<td align='center' style='padding: 10px;'>0</td>"
                else:
                    for _ in todas_aristas:
                        matrices_html += "<td align='center' style='padding: 10px;'>0</td>"

                matrices_html += "</tr>"

            matrices_html += "</table>"

        matrices_html += "</div>"
        self.vista.matrices_text.setHtml(matrices_html)

    def analizar_conjuntos_corte(self):
        """Analiza los conjuntos de corte del grafo original"""
        conjuntos_html = "<h3>Conjuntos de Corte</h3>"
        conjuntos_html += "<p>Conjuntos minimales de aristas que al eliminarlas hacen el grafo inconexo:</p>"

        from collections import deque
        from itertools import combinations

        def es_conexo(aristas_disponibles):
            """Verifica si el grafo es conexo con las aristas dadas"""
            if not aristas_disponibles:
                return False

            grafo = {i: [] for i in range(self.vertices)}
            for a, b in aristas_disponibles:
                grafo[a].append(b)
                grafo[b].append(a)

            # BFS desde el vértice 0
            visitados = set()
            cola = deque([0])
            visitados.add(0)

            while cola:
                actual = cola.popleft()
                for vecino in grafo[actual]:
                    if vecino not in visitados:
                        visitados.add(vecino)
                        cola.append(vecino)

            return len(visitados) == self.vertices

        def contiene_conjunto(conjunto_grande, conjunto_pequeno):
            """Verifica si conjunto_grande contiene a conjunto_pequeno"""
            return set(conjunto_pequeno).issubset(set(conjunto_grande))

        # Encontrar todos los conjuntos de corte minimales
        conjuntos_corte = []

        # Probar desde 1 arista hasta n aristas
        max_tamano = min(len(self.aristas), 4)  # Limitar búsqueda

        for tamano in range(1, max_tamano + 1):
            for combo in combinations(self.aristas, tamano):
                combo_list = list(combo)

                # Verificar que no contenga un conjunto de corte anterior
                contiene_anterior = False
                for cc_anterior in conjuntos_corte:
                    if contiene_conjunto(combo_list, cc_anterior):
                        contiene_anterior = True
                        break

                if contiene_anterior:
                    continue

                # Verificar si al quitar estas aristas el grafo queda inconexo
                aristas_sin_combo = [a for a in self.aristas if a not in combo]

                if not es_conexo(aristas_sin_combo):
                    # Verificar minimalidad: con una arista menos debe seguir conexo
                    es_minimal = True

                    if len(combo_list) > 1:
                        for arista in combo_list:
                            combo_sin_una = [a for a in combo_list if a != arista]
                            aristas_temp = [a for a in self.aristas if a not in combo_sin_una]
                            if not es_conexo(aristas_temp):
                                es_minimal = False
                                break

                    if es_minimal:
                        conjuntos_corte.append(combo_list)

        # Mostrar solo los conjuntos de corte
        if conjuntos_corte:
            for idx, conjunto in enumerate(conjuntos_corte, 1):
                # Mostrar el conjunto de corte
                aristas_corte_str = []
                for arista in conjunto:
                    u, v = arista
                    etiq_u = self.etiquetas.get(u, str(u + 1))
                    etiq_v = self.etiquetas.get(v, str(v + 1))
                    peso = self.ponderaciones.get(arista, self.ponderaciones.get((v, u), 1))
                    aristas_corte_str.append(f"({etiq_u},{etiq_v})={peso}")

                conjunto_str = "{" + ", ".join(aristas_corte_str) + "}"

                conjuntos_html += f"<p><b>CC{idx}:</b> {conjunto_str}</p>"
        else:
            conjuntos_html += "<p><i>No se encontraron conjuntos de corte</i></p>"

        self.vista.conjuntos_text.setHtml(conjuntos_html)


    def generar_matrices(self):
        """Genera matrices de adyacencia, incidencia y circuitos vs aristas"""
        # Clasificar aristas
        ramas = self.arbol_aristas
        cuerdas = [a for a in self.aristas if a not in self.arbol_aristas]

        # Matriz de adyacencia del árbol
        matriz_ady = [[0] * self.vertices for _ in range(self.vertices)]
        for u, v in ramas:
            matriz_ady[u][v] = 1
            matriz_ady[v][u] = 1

        # Matriz de incidencia del árbol
        matriz_inc = [[0] * len(ramas) for _ in range(self.vertices)]
        for idx, (u, v) in enumerate(ramas):
            matriz_inc[u][idx] = 1
            matriz_inc[v][idx] = 1

        # Generar HTML
        matrices_html = "<div style='max-width: 100%; overflow-x: auto;'>"

        # ========== MATRIZ DE ADYACENCIA ==========
        matrices_html += "<h3>Matriz de Adyacencia (del Árbol)</h3>"
        matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
        matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'></th>"
        for i in range(self.vertices):
            matrices_html += f"<th style='padding: 10px;'>{self.etiquetas.get(i, str(i + 1))}</th>"
        matrices_html += "</tr>"

        for i in range(self.vertices):
            matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>{self.etiquetas.get(i, str(i + 1))}</th>"
            for j in range(self.vertices):
                matrices_html += f"<td align='center' style='padding: 10px;'>{matriz_ady[i][j]}</td>"
            matrices_html += "</tr>"
        matrices_html += "</table><br><br>"

        # ========== MATRIZ DE INCIDENCIA ==========
        matrices_html += "<h3>Matriz de Incidencia (del Árbol)</h3>"
        matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
        matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'>Vértices</th>"
        for idx, (u, v) in enumerate(ramas):
            etiq_u = self.etiquetas.get(u, str(u + 1))
            etiq_v = self.etiquetas.get(v, str(v + 1))
            matrices_html += f"<th style='padding: 10px;'>e{idx + 1}<br>({etiq_u},{etiq_v})</th>"
        matrices_html += "</tr>"

        for i in range(self.vertices):
            matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>{self.etiquetas.get(i, str(i + 1))}</th>"
            for j in range(len(ramas)):
                matrices_html += f"<td align='center' style='padding: 10px;'>{matriz_inc[i][j]}</td>"
            matrices_html += "</tr>"
        matrices_html += "</table><br><br>"

        # ========== MATRIZ CIRCUITOS FUNDAMENTALES VS ARISTAS ==========
        if cuerdas:
            from collections import deque

            def encontrar_camino(u, v, aristas_arbol):
                grafo = {i: [] for i in range(self.vertices)}
                for a, b in aristas_arbol:
                    grafo[a].append(b)
                    grafo[b].append(a)

                visitados = set()
                cola = deque([(u, [u])])
                visitados.add(u)

                while cola:
                    actual, camino = cola.popleft()
                    if actual == v:
                        return camino

                    for vecino in grafo[actual]:
                        if vecino not in visitados:
                            visitados.add(vecino)
                            cola.append((vecino, camino + [vecino]))

                return []

            todas_aristas = list(self.aristas)

            # ========== PRIMERA MATRIZ: CIRCUITOS FUNDAMENTALES VS ARISTAS ==========
            matrices_html += "<h3>Matriz: Circuitos Fundamentales vs Aristas</h3>"
            matrices_html += "<p style='font-size: 11px; color: #6C4E31;'>Muestra qué aristas pertenecen a cada circuito fundamental (1 = pertenece, 0 = no pertenece)</p>"

            matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
            matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'>Circuito</th>"

            # Encabezados: nombre de aristas
            for arista in todas_aristas:
                u, v = arista
                etiq_u = self.etiquetas.get(u, str(u + 1))
                etiq_v = self.etiquetas.get(v, str(v + 1))
                matrices_html += f"<th style='padding: 10px;'>({etiq_u},{etiq_v})</th>"
            matrices_html += "</tr>"

            # Fila por cada circuito fundamental
            for idx_circuito, cuerda in enumerate(cuerdas, 1):
                u, v = cuerda
                camino = encontrar_camino(u, v, ramas)

                matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>CF{idx_circuito}</th>"

                if camino:
                    aristas_en_circuito = set()

                    for i in range(len(camino) - 1):
                        arista1 = (camino[i], camino[i + 1])
                        arista2 = (camino[i + 1], camino[i])
                        aristas_en_circuito.add(arista1)
                        aristas_en_circuito.add(arista2)

                    aristas_en_circuito.add(cuerda)
                    aristas_en_circuito.add((v, u))

                    for arista in todas_aristas:
                        if arista in aristas_en_circuito:
                            matrices_html += f"<td align='center' style='padding: 10px; font-weight: bold;'>1</td>"
                        else:
                            matrices_html += "<td align='center' style='padding: 10px;'>0</td>"
                else:
                    for _ in todas_aristas:
                        matrices_html += "<td align='center' style='padding: 10px;'>0</td>"

                matrices_html += "</tr>"

            matrices_html += "</table><br><br>"

            # ========== SEGUNDA MATRIZ: CIRCUITOS VS PONDERACIONES ==========
            matrices_html += "<h3>Matriz: Circuitos vs Ponderaciones de Aristas</h3>"
            matrices_html += "<p style='font-size: 11px; color: #6C4E31;'>Muestra las ponderaciones de las aristas en cada circuito</p>"

            matrices_html += "<table border='1' cellpadding='8' cellspacing='0' style='border-collapse: collapse; margin: 10px 0;'>"
            matrices_html += "<tr style='background-color: #FFDBB5;'><th style='padding: 10px;'>Circuito</th>"

            # Encabezados: ponderación
            for arista in todas_aristas:
                peso = self.ponderaciones.get(arista, self.ponderaciones.get((arista[1], arista[0]), 1))
                matrices_html += f"<th style='padding: 10px;'>{peso}</th>"
            matrices_html += "</tr>"

            # Fila por cada circuito
            for idx_circuito, cuerda in enumerate(cuerdas, 1):
                u, v = cuerda
                camino = encontrar_camino(u, v, ramas)

                matrices_html += f"<tr><th style='background-color: #FFDBB5; padding: 10px;'>C{idx_circuito}</th>"

                if camino:
                    aristas_en_circuito = set()

                    for i in range(len(camino) - 1):
                        arista1 = (camino[i], camino[i + 1])
                        arista2 = (camino[i + 1], camino[i])
                        aristas_en_circuito.add(arista1)
                        aristas_en_circuito.add(arista2)

                    aristas_en_circuito.add(cuerda)
                    aristas_en_circuito.add((v, u))

                    for arista in todas_aristas:
                        if arista in aristas_en_circuito:
                            peso = self.ponderaciones.get(arista, self.ponderaciones.get((arista[1], arista[0]), 1))
                            matrices_html += f"<td align='center' style='padding: 10px; font-weight: bold; color: #d9534f;'>{peso}</td>"
                        else:
                            matrices_html += "<td align='center' style='padding: 10px;'>0</td>"
                else:
                    for _ in todas_aristas:
                        matrices_html += "<td align='center' style='padding: 10px;'>0</td>"

                matrices_html += "</tr>"

            matrices_html += "</table>"
        else:
            matrices_html += "<p><i>No hay circuitos fundamentales (no hay cuerdas)</i></p>"

        matrices_html += "</div>"
        self.vista.matrices_text.setHtml(matrices_html)


    # ==================== ACCIONES ADICIONALES ====================
    def guardar_arbol(self):
        """Guarda el árbol resultante en un archivo JSON"""
        if not self.arbol_aristas:
            DialogoClave(0, "Error", "mensaje", self.vista,
                         "No hay árbol para guardar.").exec()
            return

        archivo, _ = QFileDialog.getSaveFileName(
            self.vista, "Guardar Árbol", "", "JSON Files (*.json)")
        if archivo:
            datos = {
                'vertices': self.vertices,
                'aristas': self.arbol_aristas,
                'etiquetas': self.etiquetas,
                'ponderaciones': {str(k): v for k, v in self.ponderaciones.items() if k in self.arbol_aristas},
                'peso_total': self.peso_total
            }
            with open(archivo, 'w', encoding='utf-8') as f:
                json.dump(datos, f, indent=4, ensure_ascii=False)

            DialogoClave(0, "Éxito", "mensaje", self.vista,
                         "Árbol guardado correctamente.").exec()

    def limpiar_resultado(self):
        """Limpia solo los resultados del algoritmo"""
        self.arbol_aristas = []
        self.peso_total = 0
        self.vista.visual_arbol.set_grafo(0, [], {}, {})
        self.vista.info_text.clear()
        self.vista.circuitos_text.clear()
        self.vista.circuitos_fund_text.clear()
        self.vista.conjuntos_text.clear()
        self.vista.matrices_text.clear()

    def limpiar_todo(self):
        """Limpia todo: grafo original y resultados"""
        self.limpiar_grafo()
        self.limpiar_resultado()
