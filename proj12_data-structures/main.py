from structures import LinkedList

def main():
    my_linked_list = LinkedList()
    my_linked_list.append_to_back(1)
    my_linked_list.append_to_back(2)
    my_linked_list.append_to_back(3)
    my_linked_list.append_to_back(4)
    my_linked_list.append_to_back(5)
    my_linked_list.append_to_back(6)
    my_linked_list.insert_at(2, 69)

    print(f"my_linked_list size: {my_linked_list.size}")
    print(f"items in my_linked_list: {my_linked_list}")
main()
