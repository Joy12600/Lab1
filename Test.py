import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTreeWidget, QTreeWidgetItem
from PyQt5.uic import loadUi
import os
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.height = 1
        self.factor_balanceo = 0

class AVLTree:
    def __init__(self):
        self.root = None
    def insert(self, root, key):
        if not root:
            return TreeNode(key)
        
        if key < root.key:
            root.left = self.insert(root.left, key)
        else:
            root.right = self.insert(root.right, key)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        left_height = self.get_height(root.left)
        right_height = self.get_height(root.right)
        root.balanceo = left_height - right_height
        balance = root.balanceo
        root.factor_balanceo = right_height - left_height

        if balance > 1 and key < root.left.key:
            return self.right_rotate(root)

        if balance < -1 and key > root.right.key:
            return self.left_rotate(root)

        if balance > 1 and key > root.left.key:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and key < root.right.key:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        return root
    def get_height(self, root):
        if not root:
            return 0
        return root.height
    
    def get_balance(self, root):
        if not root:
            return 0
        return self.get_height(root.left) - self.get_height(root.right)

    def left_rotate(self, z):
        y = z.right
        T2 = y.left

        y.left = z
        z.right = T2

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))

        return y

    def plot_tree(self):
        fig, ax = plt.subplots()
        self._plot_tree_recursive(ax, self.root, 0, 0, 1000)
        ax.set_aspect('equal')
        ax.axis('off')
        plt.show()

    def _plot_tree_recursive(self, ax, node, x, y, dx):
        if node is None:
            return

        ax.plot(x, y, 'ko', markersize=10, alpha=0.3)  # Ajuste de la transparencia
        ax.text(x, y, f'{node.key}\n{node.factor_balanceo}', fontsize=12, ha='center', va='center')

        if node.left:
            ax.plot([x, x - dx], [y, y - 50], 'k-', alpha=0.3)  # Ajuste de la transparencia
            self._plot_tree_recursive(ax, node.left, x - dx, y - 50, dx / 2)

        if node.right:
            ax.plot([x, x + dx], [y, y - 50], 'k-', alpha=0.3)  # Ajuste de la transparencia
            self._plot_tree_recursive(ax, node.right, x + dx, y - 50, dx / 2)
class ventana_agregar(QMainWindow):
    def __init__(self, avl_tree, Principal):
        super().__init__()
        loadUi("AgregarArbol.ui", self)
        self.cargar_categoria('data')
        self.comboBox.currentIndexChanged.connect(self.cargar_segundo_comboBox)
        self.ventana_principal=Principal
        self.pushButton_2.clicked.connect(self.agregar_nodo)
        self.avl_tree = avl_tree
        self.pushButton_3.clicked.connect(self.regresar_principal)
        self.valores_agregados = set()
    def cargar_categoria(self, directory):
        try:
            archivo = os.listdir(directory)
            categoria = [file for file in archivo if os.path.isdir(os.path.join(directory, file))]
            self.comboBox.addItems(categoria)
        except FileNotFoundError:
            print(f"El directorio '{directory}' no se encontró.")
    def cargar_segundo_comboBox(self):
        categoria_seleccionada = self.comboBox.currentText()
        self.comboBox_2.clear()
        try:
            files = os.listdir(os.path.join('data', categoria_seleccionada))
            self.comboBox_2.addItems(files)
        except FileNotFoundError:
            print(f"No se encontraron archivos para la categoría '{categoria_seleccionada}'.")
    def buscar_valor(self, node, valor):
        if node is None:
           return False
        try:
            valor_entero = int(valor)
        except ValueError:
            # Si no podemos convertir a entero, intentamos extraer los números de la cadena
            numeros = [int(s) for s in valor.split() if s.isdigit()]
            if numeros:
                valor_entero = numeros[0]  # Tomamos el primer número encontrado
            else:
                return False  # Si no hay números en la cadena, no se puede convertir a entero y no está en el árbol
    
        if node.key == valor_entero:
            return True
        elif node.key < valor_entero:
            return self.buscar_valor(node.right, valor)
        else:
            return self.buscar_valor(node.left, valor)
                
    def extraer_numero(self, s):
        # Extraer solo los dígitos numéricos de la cadena
        digits = ''.join(filter(str.isdigit, s))
        return int(digits)
    def agregar_nodo(self):
        valor_seleccionado = str(self.comboBox_2.currentText())
        if valor_seleccionado in self.valores_agregados:
            QMessageBox.warning(self, "Error", f"El valor '{valor_seleccionado}' ya ha sido agregado al árbol.")
            return
        try:
            numero = self.extraer_numero(valor_seleccionado)
            self.avl_tree.root = self.avl_tree.insert(self.avl_tree.root, numero)
            self.valores_agregados.add(valor_seleccionado) 
            self.avl_tree.plot_tree()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    def regresar_principal(self):  # Función para regresar a la ventana principal
        self.close()  # Cerrar la ventana de agregar
        self.ventana_principal.show()  # Mostrar la ventana principal
class ventana_eliminar():
    pass
class ventana_buscar():
    pass
class tam_peso():
    pass
class recorrido_niveles():
    pass
class Principal(QMainWindow):
    def __init__(self):
        super(Principal, self).__init__()
        loadUi("ArbolAVL.ui", self)
        self.avl_tree = AVLTree()
        self.pushButton.clicked.connect(self.abrir_agregar)
    def abrir_agregar(self):
        self.ventana_agregar = ventana_agregar(self.avl_tree, self)  # Crear una instancia de ventana_agregar
        self.hide()
        self.ventana_agregar.show() 
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    my_app = Principal()
    my_app.show()
    sys.exit(app.exec_())