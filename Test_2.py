import sys
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QPushButton, QMessageBox, QTreeWidget, QTreeWidgetItem
from PyQt5.uic import loadUi
import os
import matplotlib.pyplot as plt

class TreeNode:
    def __init__(self, key, full_name):
        self.key = key
        self.full_name = full_name
        self.left = None
        self.right = None
        self.height = 1
        self.balanceo= 0
        self.factor_balanceo=0
        self.bytes_size = sys.getsizeof(key) + sys.getsizeof(full_name)
class AVLTree:
    def __init__(self):
        self.root = None
    def insert(self, root, key, full_name):
        if not root:
            return TreeNode(key, full_name)
        
        if key < root.key:
            root.left = self.insert(root.left, key, full_name)
        else:
            root.right = self.insert(root.right, key, full_name)

        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))
        left_height = self.get_height(root.left)
        right_height = self.get_height(root.right)
        root.balanceo = left_height - right_height
        root.factor_balanceo=right_height - left_height
        balance = root.balanceo

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
    
    def delete(self, root, key):
        if not root:
            return root

        # Si el nodo a eliminar es menor que la raíz, buscar en el subárbol izquierdo
        if key < root.key:
            root.left = self.delete(root.left, key)

        # Si el nodo a eliminar es mayor que la raíz, buscar en el subárbol derecho
        elif key > root.key:
            root.right = self.delete(root.right, key)

        # Si el nodo a eliminar es igual a la raíz, proceder con la eliminación
        else:
            # Caso 1: nodo a eliminar es una hoja o tiene un solo hijo
            if root.left is None:
                temp = root.right
                root = None
                return temp
            elif root.right is None:
                temp = root.left
                root = None
                return temp

            # Caso 2: nodo a eliminar tiene dos hijos
            # Encontrar el sucesor inmediato (el nodo más pequeño en el subárbol derecho)
            temp = self.get_min_value_node(root.right)

            # Copiar los datos del sucesor inmediato al nodo actual
            root.key = temp.key
            root.full_name = temp.full_name

            # Eliminar el sucesor inmediato
            root.right = self.delete(root.right, temp.key)

        # Actualizar la altura del nodo actual
        if root is None:
            return root
        root.height = 1 + max(self.get_height(root.left), self.get_height(root.right))

        # Calcular el factor de equilibrio del nodo actual
        balance = self.get_balance(root)

        # Realizar rotaciones si es necesario para balancear el árbol
        if balance > 1 and self.get_balance(root.left) >= 0:
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) <= 0:
            return self.left_rotate(root)

        if balance > 1 and self.get_balance(root.left) < 0:
            root.left = self.left_rotate(root.left)
            return self.right_rotate(root)

        if balance < -1 and self.get_balance(root.right) > 0:
            root.right = self.right_rotate(root.right)
            return self.left_rotate(root)

        # Actualizar el factor de equilibrio del nodo actual
        root.balanceo = self.get_height(root.right) - self.get_height(root.left)
        root.factor_balanceo = self.get_height(root.right) - self.get_height(root.left)

        return root
    def get_min_value_node(self, root):
        current = root
        while current.left is not None:
            current = current.left
        return current
    def buscar_nodo(self, root, key):
        if root is None or root.key == key:
            return root
        if root.key < key:
            return self.buscar_nodo(root.right, key)
        return self.buscar_nodo(root.left, key)

    def buscar_nodo_padre(self, root, key):
        if root is None or root.key == key:
            return None
        if (root.left and root.left.key == key) or (root.right and root.right.key == key):
            return root
        if root.key < key:
            return self.buscar_nodo_padre(root.right, key)
        return self.buscar_nodo_padre(root.left, key)
    def buscar_abuelo(self, root, key):
        padre = self.buscar_nodo_padre(root, key)
        if padre:
            abuelo = self.buscar_nodo_padre(root, padre.key)
            return abuelo
        return None

    def buscar_tio(self, root, key):
        padre = self.buscar_nodo_padre(root, key)
        if padre is None:
            return None

        izquierdo_hijo = padre.left
        derecho_hijo = padre.right

        if padre.right and padre.right.key == key:
            if derecho_hijo is not None and derecho_hijo.left is not None:
                tio = self.buscar_nodo_padre(root, derecho_hijo.left.key)
                return tio

            if derecho_hijo is not None and derecho_hijo.right is not None:
                tio = self.buscar_nodo_padre(root, derecho_hijo.right.key)
                return tio

        if padre.left and padre.left.key == key:
            if izquierdo_hijo is not None and izquierdo_hijo.right is not None:
                tio = self.buscar_nodo_padre(root, izquierdo_hijo.right.key)
                return tio

            if izquierdo_hijo is not None and izquierdo_hijo.left is not None:
                tio = self.buscar_nodo_padre(root, izquierdo_hijo.left.key)
                return tio

        return None
    def recorrido_nivel(self):
        resultado = []
        if self.root is None:
            return resultado
        self._recorrido_nivel_recursive([self.root], resultado)
        return resultado
    def _recorrido_nivel_recursive(self, nodes, resultado):
        if not nodes:
            return
        nivel_actual = []
        siguiente_nivel = []
        for node in nodes:
            nivel_actual.append((node.key, node.full_name))
            if node.left:
                siguiente_nivel.append(node.left)
            if node.right:
                siguiente_nivel.append(node.right)

        resultado.append(nivel_actual)
        self._recorrido_nivel_recursive(siguiente_nivel, resultado)
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
        z.factor_balanceo = self.get_height(z.left) - self.get_height(z.right)
        y.factor_balanceo = self.get_height(y.left) - self.get_height(y.right)

        return y

    def right_rotate(self, z):
        y = z.left
        T3 = y.right

        y.right = z
        z.left = T3

        z.height = 1 + max(self.get_height(z.left), self.get_height(z.right))
        y.height = 1 + max(self.get_height(y.left), self.get_height(y.right))
        z.factor_balanceo = self.get_height(z.left) - self.get_height(z.right)
        y.factor_balanceo = self.get_height(y.left) - self.get_height(y.right)

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
        ax.text(x, y, f'{node.key}\n{node.full_name}\n{node.factor_balanceo}', fontsize=12, ha='center', va='center')

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
        nombre_completo = valor_seleccionado
        if valor_seleccionado in self.valores_agregados:
            QMessageBox.warning(self, "Error", f"El valor '{valor_seleccionado}' ya ha sido agregado al árbol.")
            return
        try:
            numero = self.extraer_numero(valor_seleccionado)
            self.avl_tree.root = self.avl_tree.insert(self.avl_tree.root, numero,  nombre_completo)
            self.valores_agregados.add(valor_seleccionado) 
            self.avl_tree.plot_tree()
        except Exception as e:
            QMessageBox.warning(self, "Error", str(e))
    def regresar_principal(self):  # Función para regresar a la ventana principal
        self.close()  # Cerrar la ventana de agregar
        self.ventana_principal.show()  # Mostrar la ventana principal
class ventana_eliminar(QMainWindow):
     def __init__(self, avl_tree, Principal):
        super().__init__()
        loadUi("EliminarArbol.ui", self)
        self.avl_tree = avl_tree
        self.ventana_principal=Principal
        self.actualizar_combobox()
        self.pushButton.clicked.connect(self.eliminar_nodo)
        self.pushButton_2.clicked.connect(self.regresar_principal)
     def actualizar_combobox(self):
        if self.avl_tree.root:
            self.comboBox.clear()
            self.actualizar_combobox_recursivo(self.avl_tree.root)
     def actualizar_combobox_recursivo(self, node):
        if node is None:
            return
        self.actualizar_combobox_recursivo(node.left)
        self.comboBox.addItem(node.full_name, node.key)
        self.actualizar_combobox_recursivo(node.right)
     def eliminar_nodo(self):
        valor_seleccionado = self.comboBox.currentData()  # Obtener el valor (número) del nodo seleccionado
        if valor_seleccionado:
            nodo_a_eliminar = int(valor_seleccionado)
            nodo = self.avl_tree.buscar_nodo(self.avl_tree.root, nodo_a_eliminar)
            if nodo:
                nombre_nodo = nodo.full_name
                self.avl_tree.root = self.avl_tree.delete(self.avl_tree.root, nodo_a_eliminar)
                self.valores_agregados.discard(nombre_nodo)  # Eliminar el nombre del nodo de la lista de valores agregados
                self.avl_tree.plot_tree()
            else:
                QMessageBox.warning(self, "Error", "El nodo seleccionado no se encontró en el árbol.")
     def regresar_principal(self):  # Función para regresar a la ventana principal
        self.close()  # Cerrar la ventana de agregar
        self.ventana_principal.show()  # Mostrar la ventana principal
class ventana_buscar(QMainWindow):
    def __init__(self, avl_tree, Principal):
        super().__init__()
        loadUi("BuscarNodo.ui", self)
        self.avl_tree = avl_tree
        self.ventana_principal=Principal
        self.llenar_combobox()
        self.pushButton_2.clicked.connect(self.buscar_nodo_mostrar_info)
        self.pushButton_3.clicked.connect(self.regresar_principal)
    def llenar_combobox(self):
        nodos = self.avl_tree.recorrido_nivel()
        for nivel in nodos:
            for nodo in nivel:
                self.comboBox.addItem(nodo[1], nodo[0])
    def buscar_nodo_mostrar_info(self):
        nodo_seleccionado = self.comboBox.currentData()
        if nodo_seleccionado:
            nodo = self.avl_tree.buscar_nodo(self.avl_tree.root, nodo_seleccionado)
            if nodo:
                mensaje = f"Nombre del Nodo: {nodo.full_name}\n"
                padre = self.avl_tree.buscar_nodo_padre(self.avl_tree.root, nodo.key)
                if padre:
                    mensaje += f"Nombre del Padre: {padre.full_name}\n"
                else:
                    mensaje += "No tiene padre.\n"
                abuelo = self.avl_tree.buscar_abuelo(self.avl_tree.root, nodo.key)
                if abuelo:
                    mensaje += f"Nombre del Abuelo: {abuelo.full_name}\n"
                else:
                    mensaje += "No tiene abuelo.\n" 
                tio = self.avl_tree.buscar_tio(self.avl_tree.root, nodo.key)
                if tio:
                    mensaje += f"Nombre del Tío: {tio.full_name}\n"
                else:
                    mensaje += "No tiene tío.\n"
                QMessageBox.information(self, "Información del Nodo", mensaje)
            else:
                QMessageBox.warning(self, "Error", "El nodo seleccionado no se encontró en el árbol.")
        else:
            QMessageBox.warning(self, "Error", "Por favor seleccione un nodo del árbol.")
    def regresar_principal(self):  # Función para regresar a la ventana principal
        self.close()  # Cerrar la ventana de agregar
        self.ventana_principal.show()  # Mostrar la ventana principal
class tam_peso(QMainWindow):
    def __init__(self, avl_tree, Principal):
        super().__init__()
        loadUi("Byte_Tam.ui", self)
        self.avl_tree = avl_tree
        self.ventana_principal=Principal
        self.pushButton_3.clicked.connect(self.regresar_principal)
        self.pushButton_2.clicked.connect(self.buscar_nodos)
    def buscar_nodos(self):
        categoria_seleccionada = self.comboBox.currentText()
        try:
            peso_min = float(self.lineEdit.text())
            peso_max = float(self.lineEdit_2.text())
            nodos_encontrados = []
            self._buscar_nodos_recursive(self.avl_tree.root, categoria_seleccionada, peso_min, peso_max, nodos_encontrados)
            mensaje = "Nodos encontrados:\n\n"
            for nodo in nodos_encontrados:
                mensaje += f"Nombre: {nodo.full_name}, Peso: {nodo.key}\n"
            if not nodos_encontrados:
                mensaje = "No se encontraron nodos que cumplan con los criterios de búsqueda."
            QMessageBox.information(self, "Resultados de Búsqueda", mensaje)
        except ValueError:
            QMessageBox.warning(self, "Error", "Por favor ingrese valores numéricos válidos para el rango de peso.")

    def _buscar_nodos_recursive(self, node, categoria, peso_min, peso_max, nodos_encontrados):
        if node is None:
            return

        # Inicializar la categoría del nodo como None
        categoria_nodo = None

        # Extraer la categoría del nombre del nodo
        nombre = node.full_name.lower()
        if nombre.startswith("b"):
            categoria_nodo = "bike"
        elif nombre.startswith("car"):
            categoria_nodo = "car"
        elif nombre.startswith("cat"):
            categoria_nodo = "cat"
        elif nombre.startswith("dog"):
            categoria_nodo = "dog"
        elif nombre.startswith("00"):
            categoria_nodo = "flowers"
        elif nombre.startswith("h"):
            categoria_nodo = "horse"
        elif nombre.startswith("r"):
            categoria_nodo = "human"

        # Guardar la categoría en el nodo
        node.category = categoria_nodo

        # Calcular el peso del nodo en kilobytes
        peso_nodo_kb = (node.bytes_size) / 1024  # Convertir bytes a kilobytes

        # Verificar si el nodo está en la categoría seleccionada y en el rango de peso
        if categoria_nodo == categoria and peso_min <= peso_nodo_kb <= peso_max:
            nodos_encontrados.append(TreeNode(node.key, node.full_name))  # Crear una copia del nodo y agregarlo a la lista

        # Llamar recursivamente a la función para los hijos del nodo
        self._buscar_nodos_recursive(node.left, categoria, peso_min, peso_max, nodos_encontrados)
        self._buscar_nodos_recursive(node.right, categoria, peso_min, peso_max, nodos_encontrados)
    def regresar_principal(self):  # Función para regresar a la ventana principal
        self.close()  # Cerrar la ventana de agregar
        self.ventana_principal.show()  # Mostrar la ventana principal
class Principal(QMainWindow):
    def __init__(self):
        super(Principal, self).__init__()
        loadUi("ArbolAVL.ui", self)
        self.avl_tree = AVLTree()
        self.pushButton.clicked.connect(self.abrir_agregar)
        self.pushButton_2.clicked.connect(self.abrir_eliminar)
        self.pushButton_3.clicked.connect(self.mostrar_recorrido_niveles)
        self.pushButton_4.clicked.connect(self.abrir_buscar)
        self.pushButton_5.clicked.connect(self.abrir_Byte_tam)
    def abrir_agregar(self):
        self.ventana_agregar = ventana_agregar(self.avl_tree, self)  # Crear una instancia de ventana_agregar
        self.hide()
        self.ventana_agregar.show() 
    def abrir_eliminar(self):
        self.ventana_eliminar=ventana_eliminar(self.avl_tree,self)
        self.hide()
        self.ventana_eliminar.show()
    def abrir_buscar(self):
        self.ventana_buscar=ventana_buscar(self.avl_tree,self)
        self.hide()
        self.ventana_buscar.show()
    def abrir_buscar(self):
        self.ventana_buscar=ventana_buscar(self.avl_tree,self)
        self.hide()
        self.ventana_buscar.show()
    def abrir_Byte_tam(self):
        self.tam_peso=tam_peso(self.avl_tree,self)
        self.hide()
        self.tam_peso.show()
    def mostrar_recorrido_niveles(self):
        nivel_recorrido = self.avl_tree.recorrido_nivel()
        mensaje = "Recorrido por Niveles:\n\n"
        for i, nivel in enumerate(nivel_recorrido):
            mensaje += f"Nivel {i}: "  # Cambio aquí: comenzar desde 0
            for nodo in nivel:
                mensaje += f"{nodo[1]} - "  # Agregar el nombre del nodo al mensaje
            mensaje += "\n"
        QMessageBox.information(self, "Recorrido por Niveles", mensaje)
if __name__ == "__main__": 
    app = QApplication(sys.argv)
    my_app = Principal()
    my_app.show()
    sys.exit(app.exec_())