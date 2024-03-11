import os

class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def imprimir_arbol(self, nodo=None, nivel=0):
        if not nodo:
            nodo = self.raiz
        print(' ' * nivel + str(nodo.valor))
        if nodo.izquierda:
            self.imprimir_arbol(nodo.izquierda, nivel + 1)
        if nodo.derecha:
            self.imprimir_arbol(nodo.derecha, nivel + 1)

    def insertar(self, valor):
        if not self.raiz:
            self.raiz = Nodo(valor)
        else:
            self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        if not nodo:
            return Nodo(valor)
        elif valor < nodo.valor:
            nodo.izquierda = self._insertar(nodo.izquierda, valor)
        else:
            nodo.derecha = self._insertar(nodo.derecha, valor)

        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))
        balance = self._obtener_balance(nodo)

        if balance > 1:
            if valor < nodo.izquierda.valor:
                return self._rotar_derecha(nodo)
            else:
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
                return self._rotar_derecha(nodo)
        elif balance < -1:
            if valor > nodo.derecha.valor:
                return self._rotar_izquierda(nodo)
            else:
                nodo.derecha = self._rotar_derecha(nodo.derecha)
                return self._rotar_izquierda(nodo)

        return nodo

    def eliminar(self, valor):
        if not self.raiz:
            return
        else:
            self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        if not nodo:
            return nodo
        elif valor < nodo.valor:
            nodo.izquierda = self._eliminar(nodo.izquierda, valor)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar(nodo.derecha, valor)
        else:
            if not nodo.izquierda:
                return nodo.derecha
            elif not nodo.derecha:
                return nodo.izquierda
            else:
                nodo_min = self._obtener_nodo_minimo(nodo.derecha)
                nodo.valor = nodo_min.valor
                nodo.derecha = self._eliminar(nodo.derecha, nodo_min.valor)

        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))
        balance = self._obtener_balance(nodo)

        if balance > 1:
            if self._obtener_balance(nodo.izquierda) >= 0:
                return self._rotar_derecha(nodo)
            else:
                nodo.izquierda = self._rotar_izquierda(nodo.izquierda)
                return self._rotar_derecha(nodo)
        elif balance < -1:
            if self._obtener_balance(nodo.derecha) <= 0:
                return self._rotar_izquierda(nodo)
            else:
                nodo.derecha = self._rotar_derecha(nodo.derecha)

        return nodo

    def buscar(self, valor):
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        if not nodo or nodo.valor == valor:
            return nodo
        elif valor < nodo.valor:
            return self._buscar(nodo.izquierda, valor)
        else:
            return self._buscar(nodo.derecha, valor)

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

    def altura(self, nodo):
        if not nodo:
            return 0
        return 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

    def balanceado(self, nodo):
        if not nodo:
            return True
        altura_izq = self.altura(nodo.izquierda)
        altura_der = self.altura(nodo.derecha)
        return abs(altura_izq - altura_der) <= 1 and self.balanceado(nodo.izquierda) and self.balanceado(nodo.derecha)

    def imprimir_nivel(self, raiz):
        h = self.altura(raiz)
        for i in range(1, h + 1):
            self.imprimir_nivel_dado(raiz, i)

    def imprimir_nivel_dado(self, raiz, nivel):
        if not raiz:
            return
        if nivel == 1:
            print(raiz.valor, end=" ")
        elif nivel > 1:
            self.imprimir_nivel_dado(raiz.izquierda, nivel - 1)
            self.imprimir_nivel_dado(raiz.derecha, nivel - 1)

    def encontrar_nodo(self, raiz, metrica):
        if not raiz:
            return []

        nodos = []
        if metrica(raiz):
            nodos.append(raiz.valor)

        nodos += self.encontrar_nodo(raiz.izquierda, metrica)
        nodos += self.encontrar_nodo(raiz.derecha, metrica)

        return nodos

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

    def buscar_por_categoria_y_tamano(self, categoria, tamano_min, tamano_max):
        resultado = []
        self._buscar_por_categoria_y_tamano(self.raiz, categoria, tamano_min, tamano_max, resultado)
        return resultado

    def _buscar_por_categoria_y_tamano(self, nodo, categoria, tamano_min, tamano_max, resultado):
        if nodo:
            if categoria <= nodo.valor.categoria <= categoria and tamano_min <= nodo.valor.tamano <= tamano_max:
                resultado.append(nodo)

            if nodo.valor.categoria >= categoria:
                self._buscar_por_categoria_y_tamano(nodo.izquierda, categoria, tamano_min, tamano_max, resultado)

            if nodo.valor.categoria <= categoria:
                self._buscar_por_categoria_y_tamano(nodo.derecha, categoria, tamano_min, tamano_max, resultado)

    def _obtener_altura(self, nodo):
        if not nodo:
            return 0
        return nodo.altura

    def _obtener_balance(self, nodo):
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)

    def _rotar_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))

        return y

    def _rotar_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))

        return y

    def _obtener_nodo_minimo(self, nodo):
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual

# Ruta de la carpeta de datos
carpeta_datos = 'data'

# Crear un árbol AVL
arbol = ArbolAVL()

# Leer y agregar valores de archivos a la estructura del árbol AVL
for nombre_archivo in os.listdir(carpeta_datos):
    ruta_archivo = os.path.join(carpeta_datos, nombre_archivo)
    if os.path.isfile(ruta_archivo):
        with open(ruta_archivo, 'r') as archivo:
            # Leer el contenido del archivo e insertar el valor en el árbol AVL
            valor = archivo.read()
            arbol.insertar(valor)

# Imprimir el árbol AVL
arbol.imprimir_arbol()
