from typing import TypeVar, Generic

T = TypeVar("T")


class _Node(Generic[T]):
    """Doubly linked node.

    Attributes:
        _item: data stored in the node
        _prev: reference to the previous node
        _next: reference to the next node
    """

    __slots__ = "_item", "_prev", "_next"

    def __init__(self, item: T | None = None) -> None:
        self._item: T | None = item
        self._prev: _Node[T] | None = None
        self._next: _Node[T] | None = None


class DoublyLinkedList(Generic[T]):
    """Doubly linked list with two sentinels (or dummy nodes) viz. header and trailer.

    Each node has a reference to the previous node and the next node.

    Attributes:
        __header: dummy header node
        __trailer: dummy trailer node
        __size: number of nodes in the list

    Methods:
        __len__(self) -> int:
            Return the number of nodes in the list.

        __repr__(self) -> str:
            Return a string representation of the list.

        is_empty(self) -> bool:
            Return True if the list is empty.

        first(self) -> T:
            Return the first item in the list.

        last(self) -> T:
            Return the last item in the list.

        prepend(self, item: T) -> None:
            Add a new node with the item at the beginning of the list.

        append(self, item: T) -> None:
            Add a new node with the item at the end of the list.

        insert_at(self, index: int, item: T) -> None:
            Insert a new node with the item at the given index.

        remove_from_first(self) -> T:
            Remove and return the first item in the list.

        remove_from_last(self) -> T:
            Remove and return the last item in the list.

        remove_from(self, index:int) -> T:
            Remove and return the item at the given index.

    Example:
    >>> lst = DoublyLinkedList[int]()
    >>> lst.is_empty()
    True
    """

    def __init__(self) -> None:
        self.__header: _Node[T] = _Node()  # dummy header node
        self.__trailer: _Node[T] = _Node()  # dummy trailer node
        self.__header._next = self.__trailer
        self.__trailer._prev = self.__header
        self.__size = 0

    def __len__(self) -> int:
        """Return the total number of non-sentinel nodes.

        Returns:
            (int): The total number of non-sentinel nodes
        """
        return self.__size

    def __repr__(self) -> str:
        """Return a string representation of the doubly linked list.

        Returns:
            (str): A string representation of the doubly linked list.
        """
        doublyListStr: str = "\nheader -><- "

        current_node = self.__header._next
        while current_node != self.__trailer:
            doublyListStr += f"{current_node._item} -><- "
            current_node = current_node._next
        doublyListStr += "trailer"

        return f"{doublyListStr}\nSize: {len(self)}\n"

    def is_empty(self) -> bool:
        """Check if the list is empty or not.

        Returns:
            (bool): True if the list is empty, False otherwise.
        """
        return len(self) == 0

    def first(self) -> T:
        """Return the item stored in the first node of the list.

        Returns:
            (T): The item stored in the first node of the list.

        Raises:
            Exception: If the list is empty.
        """
        if self.is_empty():
            raise Exception("List is empty.")
        return self.__header._next._item

    def last(self) -> T:
        """Return the item stored in the last node of the list.

        Returns:
            (T): The item stored in the last node of the list.

        Raises:
            Exception: If the list is empty.
        """
        if self.is_empty():
            raise Exception("List is empty.")

        return self.__trailer._prev._item

    def prepend(self, item: T) -> None:
        """Add a new node with the item stored within at the front of the list.

        Args:
            item (T): The item to store within the new node.
        """
        new_node: _Node[T] = _Node(item)

        if self.is_empty():
            self.__header._next = new_node
            new_node._prev = self.__header
            new_node._next = self.__trailer
            self.__trailer._prev = new_node
        else:
            first_node: _Node[T] = self.__header._next
            self.__header._next = new_node
            new_node._prev = self.__header
            new_node._next = first_node
            first_node._prev = new_node
        self.__size += 1

    def append(self, item: T) -> None:
        """Add a new node with the item stored within at the back of the list.

        Args:
            item (T): The item to store within the new node.
        """
        if self.is_empty():
            self.prepend(item)
        else:
            new_node: _Node[T] = _Node(item)
            current_node = self.__header._next
            while current_node._next != self.__trailer:
                current_node = current_node._next

            current_node._next = new_node
            new_node._prev = current_node
            new_node._next = self.__trailer
            self.__trailer._prev = new_node
            self.__size += 1

    def insert_at(self, index: int, item: T) -> None:
        """Insert a new node with the item stored within at the given index into the list.

        Args:
            index (int): The index to insert the new node at.
            item (T): The item to store into the new node.

        Raises:
            IndexError: If the index is out of range.
        """
        if index > self.__size or index < 0:
            raise IndexError(f"Index: {index} is out of range.")

        if index == 0:
            self.prepend(item)
            return None

        if index == self.__size:
            self.append(item)
            return None

        list_index: int = 0
        current_node = self.__header._next
        while list_index < index - 1:
            current_node = current_node._next
            list_index += 1

        new_node: _Node[T] = _Node(item)
        new_node._next = current_node
        new_node._prev = current_node._prev

    def remove_from_first(self) -> T:
        """Remove the node from the front of the list and return the item stored into removed node.

        Returns:
            (T): The item stored into the removed node.

        Raises:
            Exception: If the list is empty.
        """
        if self.is_empty():
            raise Exception("List is empty.")

        removed_node = self.__header._next
        self.__size -= 1

        if self.is_empty():
            self.__header._next = self.__trailer
            self.__trailer._prev = self.__header
        else:
            self.__header._next = removed_node._next
            removed_node._next._prev = self.__header

        return removed_node._item

    def remove_from_last(self) -> T:
        """Remove the node from the back of the list and return the item stored into removed node.

        Returns:
            (T): The item stored into the removed node.

        Raises:
            Exception: If the list is empty.
        """
        if self.is_empty():
            raise Exception("List is empty.")

        if len(self) == 1:
            return self.remove_from_first()

        removed_node = self.__trailer._prev
        self.__trailer._prev = removed_node._prev
        removed_node._prev._next = self.__trailer
        self.__size -= 1

        return removed_node._item

    def remove_from(self, index: int) -> T:
        """Remove a node from the list at the given index and return the item stored into it.

        Args:
            index (int): The index of the node to be removed.

        Returns:
            (T): The item stored into the removed node.

        Raises:
            IndexError: If the index is out of range.
            Exception: If the list is empty.
        """
        if index < 0 or index >= len(self):
            raise IndexError(f"Index: {index} is out of range.")

        if self.is_empty():
            raise Exception("List is empty.")

        if index == 0:
            return self.remove_from_first()

        if index == len(self) - 1:
            return self.remove_from_last()

        current_node = self.__header._next
        list_index = 0
        while list_index < index - 1:
            current_node = current_node._next
            list_index += 1

        removed_node = current_node._next
        current_node._next = removed_node._next
        removed_node._next._prev = current_node
        self.__size -= 1
        return removed_node._item


if __name__ == "__main__":
    dl = DoublyLinkedList[int]()

    # dl.remove_from_first() # raises Exception: List is empty

    dl.append(5)
    dl.prepend(1)
    dl.prepend(2)
    dl.prepend(3)
    print(dl)
    print(f"First: {dl.first()}")
    print(f"Last: {dl.last()}")

    dl.append(4)
    print(dl)
    print(f"Last: {dl.last()}\n")

    print(f"Removed from first: {dl.remove_from_first()}")
    print(dl)

    print(f"Remove from Last: {dl.remove_from_last()}\n")
    print(dl)

    print(f"Remove from index 2: {dl.remove_from(2)}")
    print(dl)

    print(f"Remove from index 0: {dl.remove_from(0)}")
    print(dl)

    # print(f"Remove from index 1: {dl.remove_from(1)}") # raises IndexError: index out of  range

    odd_even = DoublyLinkedList[int]()
    for num in range(10):
        if num % 2 == 0:
            odd_even.append(num)
        else:
            odd_even.prepend(num)

    print(odd_even)

    ################################################################################

    # -----------------------------OUTPUT-------------------------------------------

    # header -><- 3 -><- 2 -><- 1 -><- 5 -><- trailer
    # Size: 4

    # First: 3
    # Last: 5

    # header -><- 3 -><- 2 -><- 1 -><- 5 -><- 4 -><- trailer
    # Size: 5

    # Last: 4

    # Removed from first: 3

    # header -><- 2 -><- 1 -><- 5 -><- 4 -><- trailer
    # Size: 4

    # Remove from Last: 4

    # header -><- 2 -><- 1 -><- 5 -><- trailer
    # Size: 3

    # Remove from index 2: 5

    # header -><- 2 -><- 1 -><- trailer
    # Size: 2

    # Remove from index 0: 2

    # header -><- 1 -><- trailer
    # Size: 1

    # header -><- 9 -><- 7 -><- 5 -><- 3 -><- 1 -><- 0 -><- 2 -><- 4 -><- 6 -><- 8 -><- trailer
    # Size: 10

    ################################################################################
