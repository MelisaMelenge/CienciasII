# Controlador.arboles.DistanciaController

from collections import deque


class DistanciaController:
    """Controlador para calcular distancia entre dos árboles"""

    def __init__(self):
        self.arbol1 = {'vertices': 0, 'aristas': [], 'etiquetas': {}, 'ponderaciones': {}}
        self.arbol2 = {'vertices': 0, 'aristas': [], 'etiquetas': {}, 'ponderaciones': {}}

    def set_arbol1(self, num_vertices, aristas, etiquetas, ponderaciones=None):
        """Configura el árbol 1"""
        self.arbol1 = {
            'vertices': num_vertices,
            'aristas': aristas.copy(),
            'etiquetas': etiquetas.copy() if etiquetas else {},
            'ponderaciones': ponderaciones.copy() if ponderaciones else {}
        }

    def set_arbol2(self, num_vertices, aristas, etiquetas, ponderaciones=None):
        """Configura el árbol 2"""
        self.arbol2 = {
            'vertices': num_vertices,
            'aristas': aristas.copy(),
            'etiquetas': etiquetas.copy() if etiquetas else {},
            'ponderaciones': ponderaciones.copy() if ponderaciones else {}
        }

    def es_arbol(self, arbol):
        """Verifica si el grafo es un árbol"""
        vertices = arbol['vertices']
        aristas = arbol['aristas']

        if not aristas:
            return vertices == 1

        if len(aristas) != vertices - 1:
            return False

        return self.es_conexo(arbol)

    def es_conexo(self, arbol):
        """Verifica si el grafo es conexo usando BFS"""
        vertices = arbol['vertices']
        aristas = arbol['aristas']

        if vertices == 0:
            return True

        adyacencia = [[] for _ in range(vertices)]
        for origen, destino in aristas:
            adyacencia[origen].append(destino)
            adyacencia[destino].append(origen)

        visitados = [False] * vertices
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

        return count == vertices

    def obtener_conjuntos_vertices_aristas(self, arbol):
        """Obtiene los conjuntos SV y SA de un árbol con ponderaciones"""
        etiquetas = arbol['etiquetas']
        aristas = arbol['aristas']
        ponderaciones = arbol.get('ponderaciones', {})

        # SV: conjunto de etiquetas de vértices
        sv = set(etiquetas.values())

        # SA: conjunto de aristas con etiquetas y ponderaciones
        sa = {}
        for origen, destino in aristas:
            etiq_o = etiquetas.get(origen, str(origen))
            etiq_d = etiquetas.get(destino, str(destino))
            # Normalizar orden (menor primero)
            arista = tuple(sorted([etiq_o, etiq_d]))
            # Obtener ponderación (default 1)
            arista_key = tuple(sorted([origen, destino]))
            ponderacion = ponderaciones.get(arista_key, 1)
            sa[arista] = ponderacion

        return sv, sa

    def calcular_distancia_arboles(self):
        """
        Calcula la distancia entre dos árboles usando la fórmula con ponderaciones:
        D(T1,T2) = (Σ|w1(e) - w2(e)|) / 2

        Donde w1(e) es la ponderación de la arista e en T1 y w2(e) en T2.
        Si la arista no existe en un árbol, su ponderación es 0.
        """
        # Validar que ambos sean árboles
        if not self.es_arbol(self.arbol1):
            return None, "El grafo 1 no es un árbol válido"

        if not self.es_arbol(self.arbol2):
            return None, "El grafo 2 no es un árbol válido"

        # Obtener conjuntos
        sv1, sa1 = self.obtener_conjuntos_vertices_aristas(self.arbol1)
        sv2, sa2 = self.obtener_conjuntos_vertices_aristas(self.arbol2)

        # Convertir a conjuntos de aristas
        aristas1 = set(sa1.keys())
        aristas2 = set(sa2.keys())

        # Operaciones de conjuntos
        vertices_union = sv1.union(sv2)
        vertices_interseccion = sv1.intersection(sv2)

        aristas_union = aristas1.union(aristas2)
        aristas_interseccion = aristas1.intersection(aristas2)

        # Clasificar aristas para el reporte
        solo_en_t1 = aristas1 - aristas2
        solo_en_t2 = aristas2 - aristas1
        en_ambos = aristas_interseccion

        # CALCULAR DISTANCIA CON PONDERACIONES
        suma_diferencias = 0
        detalles_aristas = []

        # Procesar todas las aristas en la unión
        for arista in sorted(aristas_union):
            w1 = sa1.get(arista, 0)  # Ponderación en T1, 0 si no existe
            w2 = sa2.get(arista, 0)  # Ponderación en T2, 0 si no existe

            diferencia_abs = abs(w1 - w2)
            suma_diferencias += diferencia_abs

            # Determinar ubicación
            if arista in solo_en_t1:
                ubicacion = 'Solo en T1'
            elif arista in solo_en_t2:
                ubicacion = 'Solo en T2'
            else:
                ubicacion = 'En ambos'

            detalles_aristas.append({
                'arista': arista,
                'en_t1': arista in aristas1,
                'en_t2': arista in aristas2,
                'w1': w1,
                'w2': w2,
                'diferencia': diferencia_abs,
                'ubicacion': ubicacion
            })

        # Distancia final: suma de diferencias absolutas dividida entre 2
        distancia = suma_diferencias / 2

        # Calcular sumas de ponderaciones para el reporte
        suma_union = sum(max(sa1.get(a, 0), sa2.get(a, 0)) for a in aristas_union)
        suma_interseccion = sum(min(sa1.get(a, 0), sa2.get(a, 0)) for a in aristas_interseccion)

        # Preparar detalles
        detalles = {
            'arbol1': {
                'sv': sv1,
                'sa': sa1,
                'cardinalidad_sv': len(sv1),
                'cardinalidad_sa': len(sa1),
                'suma_ponderaciones': sum(sa1.values())
            },
            'arbol2': {
                'sv': sv2,
                'sa': sa2,
                'cardinalidad_sv': len(sv2),
                'cardinalidad_sa': len(sa2),
                'suma_ponderaciones': sum(sa2.values())
            },
            'operaciones': {
                'vertices_union': vertices_union,
                'vertices_interseccion': vertices_interseccion,
                'aristas_union': aristas_union,
                'aristas_interseccion': aristas_interseccion,
                'aristas_solo_t1': solo_en_t1,
                'aristas_solo_t2': solo_en_t2,
                'card_vertices_union': len(vertices_union),
                'card_vertices_interseccion': len(vertices_interseccion),
                'card_aristas_union': len(aristas_union),
                'card_aristas_interseccion': len(aristas_interseccion),
                'suma_union': suma_union,
                'suma_interseccion': suma_interseccion,
                'suma_diferencias': suma_diferencias,
                'detalles_aristas': detalles_aristas
            },
            'distancia': distancia
        }

        return distancia, detalles

    def generar_reporte_html(self, detalles):
        """Genera un reporte HTML detallado de la distancia con ponderaciones"""
        if not detalles:
            return "<p>No hay datos disponibles</p>"

        a1 = detalles['arbol1']
        a2 = detalles['arbol2']
        ops = detalles['operaciones']
        dist = detalles['distancia']

        html = "<div style='font-family: Arial; color: #2d1f15;'>"

        # Título
        html += "<h3 style='color: #6C4E31; border-bottom: 2px solid #bf8f62; padding-bottom: 5px;'>Cálculo de Distancia entre Árboles</h3>"

        # Árbol 1
        html += "<h4 style='color: #8B6342; margin-top: 20px;'>Árbol T1</h4>"
        html += f"<p><b>ST1 =</b> {{{', '.join(sorted(a1['sv']))}}}</p>"
        html += "<p><b>AT1 =</b> {{"
        aristas_t1 = [f"({a[0]},{a[1]}):w={w}" for a, w in sorted(a1['sa'].items())]
        html += ', '.join(aristas_t1)
        html += "}</p>"
        html += f"<p style='margin-left: 20px;'>|ST1| = {a1['cardinalidad_sv']}, |AT1| = {a1['cardinalidad_sa']}, suma= {a1['suma_ponderaciones']}</p>"

        # Árbol 2
        html += "<h4 style='color: #8B6342; margin-top: 20px;'>Árbol T2</h4>"
        html += f"<p><b>ST2 =</b> {{{', '.join(sorted(a2['sv']))}}}</p>"
        html += "<p><b>AT2 =</b> {{"
        aristas_t2 = [f"({a[0]},{a[1]}):w={w}" for a, w in sorted(a2['sa'].items())]
        html += ', '.join(aristas_t2)
        html += "}</p>"
        html += f"<p style='margin-left: 20px;'>|ST2| = {a2['cardinalidad_sv']}, |AT2| = {a2['cardinalidad_sa']}, suma = {a2['suma_ponderaciones']}</p>"

        # Tabla de aristas con ponderaciones
        html += "<h4 style='color: #7a5a3e; margin-top: 20px;'>Análisis de Aristas y Ponderaciones</h4>"
        html += "<table style='border-collapse: collapse; margin: 10px 0; width: 100%;'>"
        html += "<tr style='background-color: #E8D4B8; font-weight: bold;'>"
        html += "<th style='border: 1px solid #8B6342; padding: 8px;'>Arista</th>"
        html += "<th style='border: 1px solid #8B6342; padding: 8px;'>w1(e)</th>"
        html += "<th style='border: 1px solid #8B6342; padding: 8px;'>w2(e)</th>"
        html += "<th style='border: 1px solid #8B6342; padding: 8px;'>|w1(e) - w2(e)|</th>"
        html += "<th style='border: 1px solid #8B6342; padding: 8px;'>Ubicación</th>"
        html += "</tr>"

        for detalle in ops['detalles_aristas']:
            arista = detalle['arista']
            w1 = detalle['w1']
            w2 = detalle['w2']
            diferencia = detalle['diferencia']
            ubicacion = detalle['ubicacion']

            # Color según ubicación
            if ubicacion == 'En ambos':
                if diferencia == 0:
                    color_fondo = '#E8F5E9'  # Verde claro (iguales)
                else:
                    color_fondo = '#FFF9C4'  # Amarillo claro (diferentes ponderaciones)
            else:
                color_fondo = '#d7ab8d'  # Rojo claro (solo en uno)

            html += f"<tr style='background-color: {color_fondo};'>"
            html += f"<td style='border: 1px solid #8B6342; padding: 8px; text-align: center;'>({arista[0]},{arista[1]})</td>"
            html += f"<td style='border: 1px solid #8B6342; padding: 8px; text-align: center;'>{w1}</td>"
            html += f"<td style='border: 1px solid #8B6342; padding: 8px; text-align: center;'>{w2}</td>"
            html += f"<td style='border: 1px solid #8B6342; padding: 8px; text-align: center; font-weight: bold;'>{diferencia}</td>"
            html += f"<td style='border: 1px solid #8B6342; padding: 8px; text-align: center;'>{ubicacion}</td>"
            html += "</tr>"

        html += "</table>"

        # Cálculo de la distancia
        html += "<h4 style='color: #8B6342; margin-top: 20px;'>Cálculo de la Distancia</h4>"
        html += "<div style='background-color: #FFFEF7; border: 2px solid #bf8f62; border-radius: 8px; padding: 15px; margin: 10px 0;'>"
        html += "<p style='margin: 5px 0;'><b>Paso 1:</b> Calcular  (AT1 ∪ AT2) - (AT1 ∩ AT2) </p>"
        html += f"<p style='margin: 5px 0; margin-left: 20px;'>(AT1 ∪ AT2) - (AT1 ∩ AT2) = {ops['suma_diferencias']}</p>"
        html += "<hr style='border: 1px solid #bf8f62; margin: 10px 0;'>"
        html += "<p style='margin: 5px 0;'><b>Paso 2:</b> Dividir entre 2</p>"
        html += f"<p style='margin: 5px 0; margin-left: 20px;'>D(T1,T2) = {ops['suma_diferencias']} / 2</p>"
        html += f"<p style='margin: 5px 0; font-size: 18px; margin-left: 20px;'><b>D(T1,T2) = {dist}</b></p>"
        html += "</div>"

        # Resultado final destacado
        html += "<div style='background-color: #FFFEF7; border: 3px solid #6C4E31; border-radius: 8px; padding: 15px; margin-top: 20px;'>"
        html += f"<h3 style='color: #6C4E31; text-align: center; margin: 0;'>DISTANCIA = {dist}</h3>"
        html += "</div>"

        # Interpretación
        html += "<h4 style='color: #8B6342; margin-top: 20px;'>Interpretación</h4>"
        html += f"<p>La distancia entre los árboles T1 y T2 es <b>{dist}</b>.</p>"

        if dist == 0:
            html += "<p style='color: #2E7D32;'><b>Los árboles son idénticos</b> - tienen exactamente las mismas aristas con las mismas ponderaciones.</p>"
        else:
            html += f"<p style='color: #F57C00;'>La suma total de diferencias absolutas de ponderaciones es <b>{ops['suma_diferencias']}</b>, "
            html += f"lo que resulta en una distancia de <b>{dist}</b>.</p>"

            # Desglose de diferencias
            aristas_diferentes = sum(1 for d in ops['detalles_aristas'] if d['diferencia'] > 0)
            html += f"<p>Hay <b>{aristas_diferentes}</b> arista(s) con diferencias en ponderación.</p>"

        html += "</div>"

        return html