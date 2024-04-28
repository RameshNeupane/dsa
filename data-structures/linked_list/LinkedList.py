from typing import TypeVar, Generic

T = TypeVar("T")


class Node(Generic[T]):
    """Node class.

    Fields:
        data (T): data of the current node
        next (Node): next node in the linked list, initially None.
    """

    def __init__(self, data: T):
        self.data: T = data
        self.next: Node[T] | None = None


class LinkedList(Generic[T]):
    """Singly linked list."""

    def __init__(self):
        self.__head: Node[T] | None = None
        self.__count: int = 0

    def __repr__(self) -> str:
        list_str: str = ""
        current_node: Node[T] = self.__head

        while current_node:
            list_str += f"{current_node.data} -> "
            current_node = current_node.next
        list_str += "None"
        list_str += f"\nCount: {self.count()}\n"
        return list_str

    # return value at the head
    def head(self) -> T:
        """Return the value that is at the head of the list.

        Returns:
            (T): Value at the head
        """
        return self.__head.data if self.__head else None

    # count total items in the linked list
    def count(self) -> int:
        """Count total elements in the list.

        Returns:
            (int): total counts
        """
        return self.__count

    # check if the list is empty or not
    def is_empty(self) -> bool:
        """Check if the list is empty or not.

        Returns:
            (bool): True if list is empty, else False.
        """
        return self.__count == 0

    # add node at the beginning of the list
    def prepend(self, data: T) -> None:
        """Add a Node at the beginning of the list.

        Args:
            data (T): Data to be added to the list.
        """
        new_node: Node[T] = Node(data)
        new_node.next = self.__head
        self.__head = new_node
        self.__count += 1

    # add node at the end of the list
    def append(self, data: T) -> None:
        """Add a Node at the end of the list.

        Args:
            data (T): Data to be added to the list.
        """
        new_node: Node[T] = Node(data)

        # if linked list is empty
        if not self.__head and self.__count == 0:
            self.__head = new_node
            self.__count += 1
            return None

        list_index: int = 0
        current_node: Node[T] = self.__head
        while list_index < self.__count - 1:
            current_node = current_node.next
            list_index += 1

        if list_index == self.__count - 1:
            current_node.next = new_node
            self.__count += 1

    # insert node at the specified index
    def insert(self, index: int, data: T) -> None:
        """Add a Node at the given index position in the list.

        Args:
            index (int): Index position to add the node.
            data (T): Data to be added to the list.
        """
        new_node: Node[T] = Node(data)
        current_node: Node[T] = self.__head

        if index > self.__count or index < 0:
            print(f"Index: {index} is out of range.\n")
            return None

        if index == 0:
            self.prepend(data)
            return None

        if index == self.__count - 1:
            self.append(data)
            return None

        list_index: int = 0
        while list_index < index - 1:
            current_node = current_node.next
            list_index += 1

        if list_index == index - 1:
            new_node.next = current_node.next
            current_node.next = new_node
            self.__count += 1

    # remove node from the beginning of the list
    def remove_from_beginning(self) -> T:
        """Remove a node from the beginning of the list.

        Returns:
            (T): The value of the node that was removed.
        """
        if not self.__head and self.__count == 0:
            return None

        head_node: Node[T] = self.__head
        head_node_value: T = head_node.data
        del head_node
        self.__head = self.__head.next
        self.__count -= 1
        return head_node_value

    # remove node from the end of the list
    def remove_from_end(self) -> T:
        """Remove a node from the end of the list.

        Returns:
            (T): The value of the node that was removed.
        """
        if not self.__head and self.__count == 0:
            return None

        if self.__count == 1:
            return self.remove_from_beginning()

        list_index: int = 0
        current_node: Node[T] = self.__head
        while list_index < self.__count - 2:
            current_node = current_node.next
            list_index += 1

        if list_index == self.__count - 2:
            remove_node = current_node.next
            current_node.next = None
            remove_node_value = remove_node.data
            del remove_node
            self.__count -= 1
            return remove_node_value

    # remove a node from the given index
    def remove_from(self, index: int) -> T:
        """Remove a node from the specified index in the list.

        Args:
            index (int): Index position to remove the node.

        Returns:
            (T): The value of the node that was removed.
        """
        if index < 0 or index >= self.__count:
            print(f"Index: {index} is out of range.")
            return None

        if index == 0:
            return self.remove_from_beginning()

        if index == self.__count - 1:
            return self.remove_from_end()

        list_index: int = 0
        current_node: Node[T] = self.__head
        while list_index < index - 1:
            current_node = current_node.next
            list_index += 1

        if list_index == index - 1:
            remove_node: Node[T] = current_node.next
            current_node.next = remove_node.next
            remove_node_value: T = remove_node.data
            del remove_node
            self.__count -= 1
            return remove_node_value


if __name__ == "__main__":
    l: LinkedList[T] = LinkedList()
    print(l)
    print(f"Is empty?: {l.is_empty()}")
    print(f"Head: {l.head()}")
    print(f"Remove from beginning: {l.remove_from_beginning()}")
    print(f"Remove from end: {l.remove_from_end()}")

    l.append(3)
    l.prepend(1)
    l.prepend(2)
    l.prepend(4)
    l.append(5)
    l.append(6)
    print(l)

    print(f"Remove from beginning: {l.remove_from_beginning()}")
    print(l)

    l.insert(23, 44)
    l.insert(6, 7)
    l.insert(2, 8)
    print(l)

    print(f"Remove from end: {l.remove_from_end()}")
    print(l)

    print(f"Remove from index 2: {l.remove_from(2)}")
    print(l)

    print(f"Remove from index 0: {l.remove_from(0)}")
    print(l)

    print(f"Remove from index 4: {l.remove_from(4)}")
    print(l)

    print(f"Is empty?: {l.is_empty()}")
    print(f"Head: {l.head()}")
