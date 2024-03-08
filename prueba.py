
class Node:
    def __init__(self, value):
        """
        Inicializa un nuevo nodo con el valor dado.

        Args:
            value: El valor del nodo.
        """
        self.value = value
        self.left = None
        self.right = None

class AvlTree:
    def __init__(self):
        """
        Inicializa un nuevo árbol AVL vacío.
        """
        self.root = None

    def insert(self, value):
        """
        Inserta un nuevo valor en el árbol AVL.

        Args:
            value: El valor a insertar.
        """
        self.root = self._insert(self.root, value)

    def _insert(self, node, value):
        """
        Inserta un nuevo valor en el subárbol con raíz en el nodo dado.

        Args:
            node: El nodo raíz del subárbol.
            value: El valor a insertar.

        Returns:
            El nodo raíz del subárbol después de la inserción.
        """
        if node is None:
            return Node(value)
        elif value < node.value:
            node.left = self._insert(node.left, value)
        else:
            node.right = self._insert(node.right, value)

        node = self._balance(node)
        return node

    def delete(self, value):
        self.root = self._delete(self.root, value)

    def _delete(self, node, value):
        if node is None:
            return node
        elif value < node.value:
            node.left = self._delete(node.left, value)
        elif value > node.value:
            node.right = self._delete(node.right, value)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            else:
                successor = self._findMin(node.right)
                node.value = successor.value
                node.right = self._delete(node.right, successor.value)

        node = self._balance(node)
        return node

    def search(self, value):
        return self._search(self.root, value)

    def _search(self, node, value):
        if node is None or node.value == value:
            return node
        elif value < node.value:
            return self._search(node.left, value)
        else:
            return self._search(node.right, value)

    def searchByCategory(self, category):
        result = []
        self._searchByCategory(self.root, category, result)
        return result

    def _searchByCategory(self, node, category, result):
        if node is None:
            return
        if node.value.category == category:
            result.append(node.value)
        self._searchByCategory(node.left, category, result)
        self._searchByCategory(node.right, category, result)

    def searchBySizeRange(self, minSize, maxSize):
        result = []
        self._searchBySizeRange(self.root, minSize, maxSize, result)
        return result

    def _searchBySizeRange(self, node, minSize, maxSize, result):
        if node is None:
            return
        if minSize <= node.value.size <= maxSize:
            result.append(node.value)
        if node.value.size > minSize:
            self._searchBySizeRange(node.left, minSize, maxSize, result)
        if node.value.size < maxSize:
            self._searchBySizeRange(node.right, minSize, maxSize, result)

    def _balance(self, node):
        if node is None:
            return node

        balanceFactor = self._getBalanceFactor(node)

        if balanceFactor > 1:
            if self._getBalanceFactor(node.left) < 0:
                node.left = self._rotateLeft(node.left)
            node = self._rotateRight(node)
        elif balanceFactor < -1:
            if self._getBalanceFactor(node.right) > 0:
                node.right = self._rotateRight(node.right)
            node = self._rotateLeft(node)

        return node

    def _rotateRight(self, node):
        newRoot = node.left
        node.left = newRoot.right
        newRoot.right = node
        return newRoot

    def _rotateLeft(self, node):
        newRoot = node.right
        node.right = newRoot.left
        newRoot.left = node
        return newRoot

    def _getBalanceFactor(self, node):
        leftHeight = self._getHeight(node.left)
        rightHeight = self._getHeight(node.right)
        return leftHeight - rightHeight

    def _getHeight(self, node):
        if node is None:
            return 0
        return max(self._getHeight(node.left), self._getHeight(node.right)) + 1

    def _findMin(self, node):
        current = node
        while current.left is not None:
            current = current.left
        return current

    def test_findMin():
        # Test case 1: Tree with only one node
        tree = Node(5)
        instance = AvlTree()  # Replace ClassName with the name of your class
        assert instance._findMin(tree) == tree

        # Test case 2: Tree with multiple nodes
        tree = Node(10)
        tree.left = Node(5)
        tree.right = Node(15)
        tree.left.left = Node(3)
        tree.left.right = Node(7)
        tree.right.left = Node(12)
        tree.right.right = Node(20)
        assert instance._findMin(tree) == tree.left.left

        # Test case 3: Tree with negative values
        tree = Node(-10)
        tree.left = Node(-5)
        tree.right = Node(-15)
        tree.left.left = Node(-3)
        tree.left.right = Node(-7)
        tree.right.left = Node(-12)
        tree.right.right = Node(-20)
        assert instance._findMin(tree) == tree.right.right

        # Test case 4: Tree with duplicate values
        tree = Node(10)
        tree.left = Node(10)
        tree.right = Node(10)
        tree.left.left = Node(10)
        tree.left.right = Node(10)
        tree.right.left = Node(10)
        tree.right.right = Node(10)
        assert instance._findMin(tree) == tree.left.left

    print("All test cases pass")
a=AvlTree()