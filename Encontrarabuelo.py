class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def encontrar_abuelo(raiz, valor_nodo):
    if raiz is None:
        return None
    
    # Buscar el nodo con el valor dado
    nodo = buscar_nodo(raiz, valor_nodo)
    if nodo is None or nodo == raiz:
        return None
    
    # Encontrar el padre del nodo
    padre = encontrar_padre(raiz, nodo)
    if padre is None or padre == raiz:
        return None
    
    # Encontrar el abuelo del nodo (padre del padre)
    abuelo = encontrar_padre(raiz, padre)
    return abuelo

def buscar_nodo(raiz, valor):
    if raiz is None or raiz.valor == valor:
        return raiz
    izquierda = buscar_nodo(raiz.izquierda, valor)
    derecha = buscar_nodo(raiz.derecha, valor)
    return izquierda if izquierda else derecha

def encontrar_padre(raiz, nodo):
    if raiz is None or raiz == nodo:
        return None
    if raiz.izquierda == nodo or raiz.derecha == nodo:
        return raiz
    izquierda = encontrar_padre(raiz.izquierda, nodo)
    derecha = encontrar_padre(raiz.derecha, nodo)
    return izquierda if izquierda else derecha

# Ejemplo de uso:
# Creamos un árbol de ejemplo
raiz = Nodo(1)
raiz.izquierda = Nodo(2)
raiz.derecha = Nodo(3)
raiz.izquierda.izquierda = Nodo(4)
raiz.izquierda.derecha = Nodo(5)
raiz.derecha.izquierda = Nodo(6)
raiz.derecha.derecha = Nodo(7)

# Encontrar el abuelo del nodo con valor 5
abuelo = encontrar_abuelo(raiz, 5)
if abuelo:
    print("El abuelo del nodo con valor 5 es:", abuelo.valor)
else:
    print("El nodo con valor 5 no tiene abuelo o no existe en el árbol.")