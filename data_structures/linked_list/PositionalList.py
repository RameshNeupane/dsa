from typing import TypeVar, Generic

T = TypeVar("T")


class PositionalList(Generic[T]):
    """Positional linked list based upon doubly linked list.

    Data (node) manipulation can be done with position access.

    Attributes:
        __header (_Node): dummy header node
        __trailer (_Node): dummy trailer node
        __size (int): number of nodes in the list
    """

    class _Node(Generic[T]):
        """Doubly linked node.

        Attributes:
            _item (T): data stored in the node
            _prev (_Node | None): previous node
            _next (_Node | None): next node
        """

        __slots__ = "_item", "_prev", "_next"

        def __init__(self, item: T) -> None:
            self._item: T = item
            self._prev: PositionalList[T]._Node | None = None
            self._next: PositionalList[T]._Node | None = None

    class _Position(Generic[T]):
        """An abstraction representing location of node in the list.

        Attributes:
            _container (PositionalList[T]): Reference to the container
            _node (PositionalList[T]._Node): Reference to the node
        """

        __slots__ = "_container", "_node"

        def __init__(
            self, container: "PositionalList[T]", node: "PositionalList[T]._Node"
        ) -> None:
            self._container: PositionalList[T] = container
            self._node: PositionalList[T]._Node = node

        def __eq__(self, other: "PositionalList[T]._Position") -> bool:
            """Check if both position represent same location or not.

            Returns:
                bool: True if both position represent same location, False otherwise.
            """
            return type(other) is type(self) and other._node is self._node

        def __ne__(self, other: "PositionalList[T]._Position") -> bool:
            """Check for different location representation."""
            return not (self == other)

        def item(self) -> T:
            """Return the item stored at this position."""
            return self._node._item

    def __init__(self) -> None:
        self.__header: PositionalList[T]._Node = self._Node(None)
        self.__trailer: PositionalList[T]._Node = self._Node(None)
        self.__header._next = self.__trailer
        self.__trailer._prev = self.__header
        self.__size: int = 0

    def __iter__(self):
        cursor = self.first()
        while cursor is not None:
            yield cursor.item()
            cursor = self.after(cursor)

    def __repr__(self) -> str:
        PositionalListStr: str = "\nheader -><- "
        for item in self:
            PositionalListStr += f"{item} -><- "

        PositionalListStr += "trailer"
        return f"{PositionalListStr}\nSize: {len(self)}\n"

    def __len__(self) -> int:
        """Return the number of nodes in the list."""
        return self.__size

    def is_empty(self) -> bool:
        """Check if the list is empty or not.

        Returns:
            (bool): True if the list is empty, False otherwise
        """
        return len(self) == 0

    def _validate(self, position: "_Position") -> "_Node":
        """Validate position and return node at this position.

        Args:
            position (_Position): Position of the node

        Returns:
            (_Node): Node at the given position

        Raises:
            TypeError: If the position is not of proper type
            ValueError: If the position does not belong to this container and
                        If the position is no longer valid
        """
        if not isinstance(position, self._Position):
            raise TypeError("position must be proper Position type")

        if position._container is not self:
            raise ValueError("position does not belong to this container")

        if position._node._next is None:
            raise ValueError("position is no longer valid")

        return position._node

    def _make_position(self, node: "_Node") -> "_Position":
        """Return position instance for the given node.

        Args:
        node (_Node): Node to which to provide position reference

        Returns:
            (_Position): Position instance for the given node
            None: If the node is None
        """
        if node is self.__header or node is self.__trailer:
            return None

        return self._Position(self, node)

    def first(self) -> "_Position":
        """Return the position of the first node of the list.

        Returns:
            (_Position): Position reference of the first node
        """
        return self._make_position(self.__header._next)

    def last(self) -> "_Position":
        """Return the position of the last node of the list.

        Returns:
            (_Position): Position reference of the last node
        """
        return self._make_position(self.__trailer._prev)

    def before(self, position: "_Position") -> "_Position":
        """Return the position of the node just before of the given position.

        Args:
            position (_Position): Position reference

        Returns:
            (_Position): Position reference of the node just before of the given position
        """
        node: PositionalList[T]._Node = self._validate(position)
        return self._make_position(node._prev)

    def after(self, position: "_Position") -> "_Position":
        """Return the position of the node just after the given position.

        Args:
            position (_Position): Position reference

        Returns:
            (_Position): Position reference of the node just after the given position
        """
        node: PositionalList[T]._Node = self._validate(position)
        return self._make_position(node._next)

    def _insert_between(
        self, item: T, predecessor: "_Node", successor: "_Node"
    ) -> "_Position":
        """Insert the node between predecessor and successor node and return position reference of that node.

        Args:
            item (T): Value to be stored in the node
            predecessor (_Node): Node reference of the node just before the new node
            successor (_Node): Node reference of the node just after the new node

        Returns:
            (_Position): Position reference of the new node
        """
        new_node: PositionalList[T]._Node = self._Node(item)
        new_node._next = successor
        new_node._prev = predecessor

        predecessor._next = new_node
        successor._prev = new_node
        self.__size += 1

        return self._make_position(new_node)

    def add_first(self, item: T) -> "_Position":
        """Add a node at the front of the list.

        Args:
            item (T): Value to be stored

        Returns:
            (_Position): Position reference of first node
        """
        return self._insert_between(item, self.__header, self.__header._next)

    def add_last(self, item: T) -> "_Position":
        """Add a node at the back of the list.

        Args:
            item (T): Value to be stored

        Returns:
            (_Position): Position reference of last node
        """
        return self._insert_between(item, self.__trailer._prev, self.__trailer)

    def add_before(self, position: "_Position", item: T) -> "_Position":
        """Add a node just before the given position.

        Args:
            position (_Position): Position reference of node
            item (T): Value to be stored

        Returns:
            (_Position): Position reference of new node
        """
        node = self._validate(position)
        return self._insert_between(item, node._prev, node)

    def add_after(self, position: "_Position", item: T) -> "_Position":
        """Add a node just after the given position.

        Args:
            position (_Position): Position reference of node
            item (T): Value to be stored

        Returns:
            (_Position): Position reference of new node
        """
        node = self._validate(position)
        return self._insert_between(item, node, node._next)

    def delete(self, position: "_Position") -> T:
        """Remove the node at the given position.

        Args:
            position (_Position): Position reference of node

        Returns:
            (T): Value stored in the node
        """
        node: PositionalList[T]._Node = self._validate(position)

        node._prev._next = node._next
        node._next._prev = node._prev

        self.__size -= 1
        item = node._item
        node._next = node._prev = node._item = None
        del node

        return item

    def replace(self, position: "_Position", new_item: T) -> T:
        """Repalce the item stored in node at the given position with the new_item.

        Args:
            position (_Position): Position reference of node
            new_item (T): New item to replace old item in the node

        Returns:
            (T): Old item stored in the node
        """
        node: PositionalList[T]._Node = self._validate(position)
        old_item = node._item
        node._item = new_item
        return old_item


if __name__ == "__main__":
    pl = PositionalList[str]()
    print(pl)
    print(f"\nIs empty?: {pl.is_empty()}")

    position_dsa = pl.add_first("DSA")
    print(position_dsa, type(position_dsa))
    pl.add_first("Python")
    print(pl)

    pl.add_last("Computer Science")
    print(pl)

    pl.add_after(position_dsa, "Computation")
    pl.add_before(position_dsa, "C")
    print(pl)

    position_first = pl.first()
    print(f"\nFirst item: {position_first.item()}")
    print(f"Second item: {pl.after(position_first).item()}")

    position_last = pl.last()
    print(f"\nLast item: {position_last.item()}")

    position_second_last = pl.before(position_last)
    new_item = "C++"
    replaced = pl.replace(position_second_last, new_item)
    print(f"\n{replaced} replaced by: {new_item}")

    print(pl)

    deleted = pl.delete(position_last)
    print(f"\nDeleted item: {deleted}")
    print(pl)

    print(f"\nItems in the list are:")

    # usage of __iter__() method
    for item in pl:
        print(item)

    print(pl)

    ################################################################################

    # ---------------------------------OUTPUT---------------------------------------

    # header -><- trailer
    # Size: 0

    # Is empty?: True
    # <__main__.PositionalList._Position object at 0x0000026D8044FD70> <class '__main__.PositionalList._Position'>

    # header -><- Python -><- DSA -><- trailer
    # Size: 2

    # header -><- Python -><- DSA -><- Computer Science -><- trailer
    # Size: 3

    # header -><- Python -><- C -><- DSA -><- Computation -><- Computer Science -><- trailer
    # Size: 5

    # First item: Python
    # Second item: C

    # Last item: Computer Science

    # Computation replaced by: C++

    # header -><- Python -><- C -><- DSA -><- C++ -><- Computer Science -><- trailer
    # Size: 5

    # Deleted item: Computer Science

    # header -><- Python -><- C -><- DSA -><- C++ -><- trailer
    # Size: 4

    # None

    # Items in the list are:
    # Python
    # C
    # DSA
    # C++

    # header -><- Python -><- C -><- DSA -><- C++ -><- trailer
    # Size: 4

    ################################################################################
