import os

class Nodo:
    def __init__(self, valor):
        """
        Crea un nuevo nodo con el valor dado.

        Args:
            valor: El valor del nodo.
        """
        self.valor = valor
        self.izquierda = None
        self.derecha = None
        self.altura = 1

class ArbolAVL:
    def __init__(self):
        """
        Crea un nuevo árbol AVL vacío.
        """
        self.raiz = None

    def imprimir_arbol(self):
        """
        Imprime todo el árbol AVL en orden ascendente.
        """
        self._imprimir_arbol(self.raiz)

    def _imprimir_arbol(self, nodo):
        """
        Imprime todo el árbol AVL en orden ascendente de forma recursiva.

        Args:
            nodo: El nodo actual en el que se está imprimiendo.
        """
        if nodo:
            self._imprimir_arbol(nodo.izquierda)
            print(nodo.valor)
            self._imprimir_arbol(nodo.derecha)
        
    def insertar(self, valor):
        """
        Inserta un nuevo valor en el árbol AVL.

        Args:
            valor: El valor a insertar.
        """
        if not self.raiz:
            self.raiz = Nodo(valor)
        else:
            self.raiz = self._insertar(self.raiz, valor)

    def _insertar(self, nodo, valor):
        """
        Inserta un nuevo valor en el árbol AVL de forma recursiva.

        Args:
            nodo: El nodo actual en el que se está insertando.
            valor: El valor a insertar.

        Returns:
            El nodo actualizado después de la inserción.
        """
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
        """
        Elimina un valor del árbol AVL.

        Args:
            valor: El valor a eliminar.
        """
        if not self.raiz:
            return
        else:
            self.raiz = self._eliminar(self.raiz, valor)

    def _eliminar(self, nodo, valor):
        """
        Elimina un valor del árbol AVL de forma recursiva.

        Args:
            nodo: El nodo actual en el que se está eliminando.
            valor: El valor a eliminar.

        Returns:
            El nodo actualizado después de la eliminación.
        """
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
        """
        Busca un valor en el árbol AVL.

        Args:
            valor: El valor a buscar.

        Returns:
            El nodo que contiene el valor buscado, o None si no se encuentra.
        """
        return self._buscar(self.raiz, valor)

    def _buscar(self, nodo, valor):
        """
        Busca un valor en el árbol AVL de forma recursiva.

        Args:
            nodo: El nodo actual en el que se está buscando.
            valor: El valor a buscar.

        Returns:
            El nodo que contiene el valor buscado, o None si no se encuentra.
        """
        if not nodo or nodo.valor == valor:
            return nodo
        elif valor < nodo.valor:
            return self._buscar(nodo.izquierda, valor)
        else:
            return self._buscar(nodo.derecha, valor)
        
    def mostrar_nivel_nodo(nodo, raiz, nivel = 0):
        """
        Se verifica primero que el nodo sea igual a la raiz, si es asi retornara el nivel inicial.
        Si no, la funcion se llamara a si misma recursivamente aumentando el nivel en 1 cada vez 
        que se verifique que el nodo no sea el nodo raiz.
        """
        if nodo == raiz:
            return nivel
        else:
            return nivel(raiz, raiz, nivel + 1)
        
    def encontrar_padre(node, current_node, parent_dict):
        """
        Esta funcion tiene como parametros el nodo, el nodo actual y padres
        que sirve como una lista que mapea cada nodo.
        Entrando a una condicion que verifica si el nodo esta vacio o si el mismo es igual al nodo actual,
        sino este entrara a un ciclo para en el que verificara si el hijo esta en el nodo, luego si el hijo
        es parte de la lista padres.
        Verificara que la variable padre no este vacia y retornara 
        """
        if node is None or node == current_node:
            return None
        else:
            for child in node:
                if child in parent_dict:
                    parent = parent_dict[child]
                    if parent is not None:
                        return parent(parent, current_node, parent_dict)
                else:
                    return parent(node[child], current_node, parent_dict)

    def buscar_por_categoria_y_tamano(self, categoria, tamano_min, tamano_max):
        """
        Busca nodos en el árbol AVL que cumplan con una categoría y un rango de tamaño.

        Args:
            categoria: La categoría a buscar.
            tamano_min: El tamaño mínimo permitido.
            tamano_max: El tamaño máximo permitido.

        Returns:
            Una lista de nodos que cumplen con los criterios de búsqueda.
        """
        resultado = []
        self._buscar_por_categoria_y_tamano(self.raiz, categoria, tamano_min, tamano_max, resultado)
        return resultado

    def _buscar_por_categoria_y_tamano(self, nodo, categoria, tamano_min, tamano_max, resultado):
        """
        Busca nodos en el árbol AVL que cumplan con una categoría y un rango de tamaño de forma recursiva.

        Args:
            nodo: El nodo actual en el que se está buscando.
            categoria: La categoría a buscar.
            tamano_min: El tamaño mínimo permitido.
            tamano_max: El tamaño máximo permitido.
            resultado: La lista en la que se almacenarán los nodos encontrados.
        """
        if nodo:
            if nodo.valor.categoria == categoria and tamano_min <= nodo.valor.tamano <= tamano_max:
                resultado.append(nodo)
                
            if nodo.valor.categoria >= categoria:
                self._buscar_por_categoria_y_tamano(nodo.izquierda, categoria, tamano_min, tamano_max, resultado)
                
            if nodo.valor.categoria <= categoria:
                self._buscar_por_categoria_y_tamano(nodo.derecha, categoria, tamano_min, tamano_max, resultado)

    def _obtener_altura(self, nodo):
        """
        Obtiene la altura de un nodo.

        Args:
            nodo: El nodo del que se desea obtener la altura.

        Returns:
            La altura del nodo.
        """
        if not nodo:
            return 0
        return nodo.altura

    def _obtener_balance(self, nodo):
        """
        Obtiene el factor de balance de un nodo.

        Args:
            nodo: El nodo del que se desea obtener el factor de balance.

        Returns:
            El factor de balance del nodo.
        """
        if not nodo:
            return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)

    def _rotar_izquierda(self, z):
        """
        Realiza una rotación a la izquierda en el árbol AVL.

        Args:
            z: El nodo en el que se realizará la rotación.

        Returns:
            El nodo resultante después de la rotación.
        """
        y = z.derecha
        T2 = y.izquierda

        y.izquierda = z
        z.derecha = T2

        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))

        return y

    def _rotar_derecha(self, z):
        """
        Realiza una rotación a la derecha en el árbol AVL.

        Args:
            z: El nodo en el que se realizará la rotación.

        Returns:
            El nodo resultante después de la rotación.
        """
        y = z.izquierda
        T3 = y.derecha

        y.derecha = z
        z.izquierda = T3

        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))

        return y

    def _obtener_nodo_minimo(self, nodo):
        """
        Obtiene el nodo con el valor mínimo en un subárbol.

        Args:
            nodo: El nodo raíz del subárbol.

        Returns:
            El nodo con el valor mínimo.
        """
        actual = nodo
        while actual.izquierda:
            actual = actual.izquierda
        return actual

    def imprimir_arbol(self, nodo=None, nivel=0):
        """
        Imprime el árbol AVL.

        Args:
            nodo: El nodo desde el cual comenzar a imprimir. Si es None, comenzará desde la raíz.
            nivel: El nivel actual del árbol. Se utiliza para la indentación.
        """
        if not nodo:
            nodo = self.raiz
        print(' ' * nivel + str(nodo.valor))
        if nodo.izquierda:
            self.imprimir_arbol(nodo.izquierda, nivel + 1)
        if nodo.derecha:
            self.imprimir_arbol(nodo.derecha, nivel + 1)
