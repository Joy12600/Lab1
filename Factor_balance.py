class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None

def altura(nodo):
    if nodo is None:
        return 0
    return max(altura(nodo.izquierda), altura(nodo.derecha)) + 1

def factor_balanceo(nodo):
    if nodo is None:
        return 0
    return altura(nodo.izquierda) - altura(nodo.derecha)

def imprimir_arbol(nodo, nivel=0):
    if nodo is not None:
        imprimir_arbol(nodo.derecha, nivel + 1)
        print("  " * nivel + str(nodo.valor))
        imprimir_arbol(nodo.izquierda, nivel + 1)

def obtener_nodo_por_valor(nodo, valor):
    if nodo is None:
        return None
    if nodo.valor == valor:
        return nodo
    elif nodo.valor < valor:
        return obtener_nodo_por_valor(nodo.derecha, valor)
    else:
        return obtener_nodo_por_valor(nodo.izquierda, valor)

# Ejemplo de uso
nodo = Nodo(10)
nodo.izquierda = Nodo(5)
nodo.derecha = Nodo(15)
nodo.derecha.derecha = Nodo(20)

print("Árbol:")
imprimir_arbol(nodo)

valor_nodo = int(input("Ingresa el valor del nodo para ver su factor de balanceo: "))
nodo_seleccionado = obtener_nodo_por_valor(nodo, valor_nodo)
if nodo_seleccionado:
    print("Factor de balanceo del nodo:", factor_balanceo(nodo_seleccionado))
else:
    print("Nodo no encontrado en el árbol.")