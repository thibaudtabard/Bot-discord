
class CommandNode:
    """Représente un nœud dans la liste chaînée d'historique."""
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    """Implémentation manuelle d'une liste chaînée simple."""
    def __init__(self):
        self.head = None
        self.tail = None
        self._size = 0

    def append(self, data):
        """Ajoute un élément à la fin (agit comme 'push' pour l'historique)."""
        new_node = CommandNode(data)
        if not self.head:
            self.head = new_node
            self.tail = new_node
        else:
            self.tail.next = new_node
            self.tail = new_node
        self._size += 1

    def get_last(self):
        """Retourne le dernier élément ajouté (le tail)."""
        return self.tail.data if self.tail else None

    def get_all(self):
        """Retourne tous les éléments sous forme de liste Python pour l'affichage/sauvegarde."""
        elements = []
        current = self.head
        while current:
            elements.append(current.data)
            current = current.next
        return elements

    def clear(self):
        """Vide la liste."""
        self.head = None
        self.tail = None
        self._size = 0

    def size(self):
        """Retourne le nombre d'éléments dans la liste."""
        return self._size

class TreeNode:
    """Représente un nœud dans l'arbre de discussion."""
    def __init__(self, content, is_result=False):
        self.content = content
        self.is_result = is_result
        self.children = {}

    def add_child(self, key, node):
        """Ajoute un enfant au nœud."""
        self.children[key.lower()] = node

    def get_child(self, key):
        """Retourne l'enfant correspondant à la clé."""
        return self.children.get(key.lower())

    def get_available_keys(self):
        """Retourne les clés de réponse disponibles (pour les boutons)."""
        return list(self.children.keys())