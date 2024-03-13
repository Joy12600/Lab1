#Clase Nodo
class Nodo_arbol:
    def __init__(self, valor):
        self.valor = valor
        self.izq = None
        self.der = None

#Funciones
def agregar_nodo(raiz, valor):
    if not raiz:
        return Nodo_arbol(valor)
    if valor < raiz.valor:
        raiz.izq = agregar_nodo(raiz.izq, valor)
    elif valor > raiz.valor:
        raiz.der = agregar_nodo(raiz.der, valor)
    return raiz

def altura(nodo):
    if not nodo:
        return 0
    return 1 + max(altura(nodo.izq), altura(nodo.der))

def balanceado(nodo):
    if not nodo:
        return True
    altura_izq = altura(nodo.izq)
    altura_der = altura(nodo.der)
    return abs(altura_izq - altura_der) <= 1 and balanceado(nodo.izq) and balanceado(nodo.der)

def imprimir_nivel(raiz):
    h = altura(raiz)
    for i in range(1, h + 1):
        imprimir_niveldado(raiz, i)

def imprimir_niveldado(raiz, nivel):
    if not raiz:
        return
    if nivel == 1:
        print(raiz.valor, end=" ")
    elif nivel > 1:
        imprimir_niveldado(raiz.izq, nivel - 1)
        imprimir_niveldado(raiz.der, nivel - 1)

# Función principal para encontrar nodos con la métrica dada
def encontrar_nodo(raiz, metrica):
    if not raiz:
        return []

    nodos = []
    if metrica(raiz):
        nodos.append(raiz.valor)

    nodos += encontrar_nodo(raiz.izq, metrica)
    nodos += encontrar_nodo(raiz.der, metrica)

    return nodos

# Ejemplo de uso
if __name__ == "__main__":
    # Construcción del árbol
    raiz= None
    valores = [10, 5, 15, 3, 7, 12, 18]
    for valor in valores:
        raiz = agregar_nodo(raiz, valor)

    # Mostrar recorrido por niveles
    print("Recorrido por niveles:")
    imprimir_nivel(raiz)
    print("\n")

    # Función métrica para buscar nodos equilibrados
    def balanceo(nodo):
        return balanceado(nodo)

    # Buscar nodos que cumplan con la métrica de ser equilibrados
    nodos_balanceados = encontrar_nodo(raiz, balanceo)
    if nodos_balanceados:
        print("Nodos equilibrados encontrados:", nodos_balanceados)
    else:
        print("No se encontraron nodos equilibrados.")