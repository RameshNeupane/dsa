from LinkedList import LinkedList
from typing import TypeVar, Generic

T = TypeVar("T")


class LinkedStack(Generic[T]):
    """Stack implementation using singly linked list."""

    def __init__(self) -> None:
        self.stack: LinkedList[T] = LinkedList()

    def __repr__(self) -> str:
        return self.stack.__repr__()

    def is_empty(self) -> bool:
        """Check if the stack is empty or not.

        Returns:
            (bool): Retuns True if the stack is empty, False otherwise.
        """
        return self.stack.is_empty()

    def size(self) -> int:
        """Return total elements count in the stack.

        Returns:
            (int): Total elements count
        """
        return self.stack.count()

    def push(self, item: T) -> None:
        """Insert item at the top of the stack.

        Args:
            item (T): Item to be inserted at the top of the stack.
        """
        self.stack.prepend(item)

    def pop(self) -> T:
        """Remove item from the top of stack.

        Returns:
            (T): Item removed from the top of the stack.
        """
        return self.stack.remove_from_beginning()

    def peek(self) -> T:
        """Return the item at the top of stack without removing it.

        Returns:
            (T): Item from the top of the stack.
        """
        return self.stack.head()


if __name__ == "__main__":
    ls: LinkedStack[int] = LinkedStack()
    print(f"Is empty?: {ls.is_empty()}")

    ls.push(25)
    ls.push(50)
    print(ls)

    print(f"Pop: {ls.pop()}")
    print(f"Peek: {ls.peek()}")

    print(f"Size: {ls.size()}")
    print(f"Is empty?: {ls.is_empty()}")

    ls.push(100)
    ls.push(200)
    print(ls)
