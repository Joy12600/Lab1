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

    def altura(self, nodo):
        if not nodo:
            return 0
        return 1 + max(self.altura(nodo.izquierda), self.altura(nodo.derecha))

    def factor_balanceo(self, nodo):
        if not nodo:
            return 0
        return self.altura(nodo.izquierda) - self.altura(nodo.derecha)

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
        self._balancear(nodo)

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
        self._balancear(nodo)

        return nodo

    def _balancear(self, nodo):
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
                return self._rotar_izquierda(nodo)

        return nodo

    def imprimir_arbol(self, nodo=None, nivel=0):
        if not nodo:
            nodo = self.raiz
        if nodo:
            print(' ' * nivel + str(nodo.valor))
            if nodo.izquierda:
                self.imprimir_arbol(nodo.izquierda, nivel + 1)
            if nodo.derecha:
                self.imprimir_arbol(nodo.derecha, nivel + 1)

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