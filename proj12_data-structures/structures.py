class BinaryTree:
    class Node:
        def __init__(self, item, left=None, right=None):
            self.item = item
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None

    def insert(self, item):
        #TODO
        pass

    def remove(self, item):
        #TODO
        pass

class LinkedList:
    class Node:
        def __init__(self, item, next=None, prev=None):
            self.item = item
            self.next = None
            self.prev = None

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def insert_at(self, insert_index, item):
        #TODO
        pass


    def append_to_front(self, item):
        #TODO
        pass

    def append_to_back(self, item):
        #TODO
        pass

    def pop(self):
        #TODO
        pass

    def dequeue(self):
        #todo
        pass
