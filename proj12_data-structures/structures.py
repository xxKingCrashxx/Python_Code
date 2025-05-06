class BinaryTree:
    class Node:
        def __init__(self, item, left=None, right=None):
            self.item = item
            self.left = left
            self.right = right

    def __init__(self):
        self.root = None

    def insert(self, item):
        def __insert_recurse(root: BinaryTree.Node, item):
            if root is None:
                return BinaryTree.Node(item)
            
            if root.item > item:
                root.left = __insert_recurse(root.left, item)
            elif root.item < item:
                root.right = __insert_recurse(root.right, item)
            return root
        self.root = __insert_recurse(self.root, item)

    @staticmethod
    def __get_smallest_node(root: 'BinaryTree.Node'):
        cur = root
        while cur.left is not None:
            cur = cur.left
        return cur

    def remove(self, item):
        def __remove_recurse(root: BinaryTree.Node, item):
            if not root:
                return None, None
            
            if root.item > item:
                root.left, del_item = __remove_recurse(root.left, item)
            elif root.item < item:
                root.right, del_item = __remove_recurse(root.right, item)
            else:
                del_item = root.item

                if not root.right and not root.left:
                    return None, None
                elif not root.left:
                    return root.right, del_item
                elif not root.right:
                    return root.left, del_item
                
                min_node = BinaryTree.__get_smallest_node(root.right)
                root.item = min_node.item
                root.right, _ = __remove_recurse(root.right, min_node.item)

            return root, del_item
        self.root, del_item = __remove_recurse(self.root, item)
        return del_item
    
    def print_tree(self):
        def __print_tree_recurse(root: BinaryTree.Node, printStr: str):
            if root is None:
                return printStr
            
            printStr += f" {root.item}"

            if root.left is not None:
                printStr = __print_tree_recurse(root.left, printStr)
            
            if root.right is not None:
                printStr = __print_tree_recurse(root.right, printStr)
            
            return printStr
        
        return __print_tree_recurse(self.root, "")
          
class Queue:
    pass

class Stack:
    pass

class LinkedList:
    class Node:
        def __init__(self, item, next=None, prev=None):
            self.item = item
            self.next = next
            self.prev = prev

        def __str__(self):
            return f"[item: {self.item}]"

    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        str_repr = ""
        cur = self.head
        count = 0
        while cur:
            str_repr += f"[index: {count} node: {cur}] "
            cur = cur.next
            count += 1
        return str_repr

    def insert_at(self, insert_index, item):
        if insert_index < 0 or insert_index > self.size:
            raise Exception(f"Cannot insert at an index of {insert_index}")

        if item is None:
            raise Exception("Cannot insert None Items")

        # quick handling for head / tail nodes
        if insert_index == 0:
            self.append_to_front(item)
            return
        elif insert_index == self.size:
            self.append_to_back(item)
            return

        # determining the closest end to start from based on whether the insert_index > or < midpoint
        midpoint = self.size // 2

        curr_node = self.head if insert_index <= midpoint else self.tail
        count = 0 if curr_node == self.head else self.size - 1

        #case where the inserted index is closer to the tail
        if curr_node == self.tail:
            while curr_node is not None and count > insert_index:
                curr_node = curr_node.prev
                count -= 1
        #case where the inserted index is closer to the head
        else:
            while curr_node is not None and count < insert_index:
                curr_node = curr_node.next
                count += 1

        node_after = curr_node
        node_before = curr_node.prev
        new_node = self.Node(item, next=node_after, prev=node_before)

        if node_before is not None:
            node_before.next = new_node

        if node_after is not None:
            node_after.prev = new_node

        self.size += 1


    def append_to_front(self, item):
        if item is None:
            raise Exception("Cannot insert None Items")

        if self.head is None:
            self.head = self.Node(item)
            self.tail = self.head
        else:
            old_head = self.head
            new_head = self.Node(item, next=old_head)
            old_head.prev = new_head
            self.head = new_head
        self.size += 1


    def append_to_back(self, item):
        if item is None:
            raise Exception("Cannot insert None Items")

        if self.head is None:
            self.head = self.Node(item)
            self.tail = self.head
        else:
            old_tail = self.tail
            new_tail = self.Node(item, prev=old_tail)
            old_tail.next = new_tail
            self.tail = new_tail
        self.size += 1

    def pop(self):
        if not self.tail:
            raise Exception("Empty List")
        
        popped_node = self.tail
        if popped_node == self.head:
            self.head = None
            self.tail = None
        else:
            new_tail = popped_node.prev
            new_tail.next = None
            self.tail = new_tail
            popped_node.prev = None

        self.size -= 1
        return popped_node.item

    def dequeue(self):
        if not self.head:
            raise Exception("Empty List")
        
        del_node = self.head

        if del_node == self.tail:
            self.tail = None
            self.head = None
        else:
            new_head = del_node.next
            new_head.prev = None
            self.head = new_head
            del_node.next = None
        self.size -= 1
        return del_node.item
