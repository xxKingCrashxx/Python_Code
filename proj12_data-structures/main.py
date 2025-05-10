from structures import LinkedList, BinaryTree
from algorithm_problems import find_missing_repeating, get_maximum_profit

def main():
    my_linked_list = LinkedList()
    my_linked_list.append_to_back(1)
    my_linked_list.append_to_back(2)
    my_linked_list.append_to_back(3)
    my_linked_list.append_to_back(4)
    my_linked_list.append_to_back(5)
    my_linked_list.append_to_back(6)
    my_linked_list.insert_at(2, 69)
    item = my_linked_list.pop()

    print(f"my_linked_list size: {my_linked_list.size}")
    print(f"items in my_linked_list: {my_linked_list}")
    print(f"popped item: {item}")

    print("==============tree=========")
    tree = BinaryTree()
    tree.insert(2)
    tree.insert(1)
    tree.insert(4)
    tree.insert(3)
    tree.insert(5)

    results = find_missing_repeating([3, 1, 3])
    print(results)

    results = find_missing_repeating([4, 3, 6, 2, 1, 1])
    print(results)

    results = get_maximum_profit([7, 10, 1, 3, 6, 9, 2])
    print(results)

main()
