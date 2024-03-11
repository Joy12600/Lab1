class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def imprimir_arbol(self):
        self._imprimir_arbol(self.raiz)

    def _imprimir_arbol(self, nodo):
        if nodo:
            self._imprimir_arbol(nodo.izquierda)
            print(nodo.valor, end=' ')
            self._imprimir_arbol(nodo.derecha)

    def mostrar_nivel_nodo(self, nodo):
        return self._mostrar_nivel_nodo(self.raiz, nodo, 1)

    def _mostrar_nivel_nodo(self, nodo_actual, nodo_buscado, nivel):
        if nodo_actual is None:
            return None
        if nodo_actual == nodo_buscado:
            return nivel
        if nodo_buscado.valor < nodo_actual.valor:
            return self._mostrar_nivel_nodo(nodo_actual.izquierda, nodo_buscado, nivel + 1)
        else:
            return self._mostrar_nivel_nodo(nodo_actual.derecha, nodo_buscado, nivel + 1)

    def encontrar_padre(self, nodo_buscado):
        parent_dict = {}
        return self._encontrar_padre(self.raiz, None, nodo_buscado, parent_dict)

    def _encontrar_padre(self, nodo_actual, padre_actual, nodo_buscado, parent_dict):
        if nodo_actual is None:
            return None

        parent_dict[nodo_actual] = padre_actual

        if nodo_actual == nodo_buscado:
            return padre_actual

        izquierda = self._encontrar_padre(nodo_actual.izquierda, nodo_actual, nodo_buscado, parent_dict)
        derecha = self._encontrar_padre(nodo_actual.derecha, nodo_actual, nodo_buscado, parent_dict)

        return izquierda if izquierda is not None else derecha