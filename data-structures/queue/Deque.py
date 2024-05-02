from typing import List, TypeVar, Generic, Iterator

T = TypeVar("T")


class DequeUnderflowException(BaseException):
    pass


class DequeOverflowException(BaseException):
    pass


class Deque(Generic[T]):
    """Deque: double ended queue.

    Data manipulation can be done from both ends.

    Attributes:
        __deque (List[T]): list of items, default is empty list
        __capacity (int): maximum number of items that can be stored, default is 10

    Methods:
        is_empty() -> bool: returns True if the deque is empty
        is_full() -> bool: returns True if the deque is full
        add_first(item: T): adds an item to the front of the deque, raises DequeOverflowException if the deque is full
        add_last(item: T): adds an item to the back of the deque, raises DequeOverflowException if the deque is full
        remove_first() -> T: removes and returns the item at the front of the deque, raises DequeUnderflowException if the deque is empty
        remove_last() -> T: removes and returns the item at the back of the deque, raises DequeUnderflowException if the deque is empty
        first() -> T: returns the item at the front of the deque, raises DequeUnderflowException if the deque is empty
        last() -> T: returns the item at the back of the deque, raises DequeUnderflowException if the deque is empty
        clear() -> None: removes all items from the deque
    """

    def __init__(self, capacity=10):
        self.__queue: List[T] = []
        self.__capacity: int = capacity

    def __len__(self) -> int:
        return len(self.__queue)

    def __repr__(self) -> str:
        return (
            f"\nQueue: {self.__queue}\nCapacity:{self.__capacity}\nLength: {len(self)}"
        )

    def __iter__(self) -> Iterator:
        return iter(self.__queue)

    def is_empty(self) -> bool:
        """Check if the deque is empty or not.

        Returns:
            (bool): True if the deque is empty, False otherwise
        """
        return len(self) == 0

    def is_full(self) -> bool:
        """Check if the deque is full or not.

        Returns:
            (bool): True if the deque is full, False otherwise
        """
        return len(self) == self.__capacity

    def add_first(self, item: T) -> None:
        """Add an item to the front of the deque.

        Args:
            item (T): The item to add to the deque

        Raises:
            DequeOverflowException: If the deque is full
        """
        if self.is_full():
            raise DequeOverflowException("Queue is full.")
        self.__queue.insert(0, item)

    def add_last(self, item: T) -> None:
        """Add an item to the back of the deque.

        Args:
            item (T): The item to add to the deque

        Raises:
            DequeOverflowException: If the deque is full
        """
        if self.is_full():
            raise DequeOverflowException("Queue is full.")
        self.__queue.append(item)

    def remove_first(self) -> T:
        """Remove and return an item at the front of the deque.

        Returns:
            (T): The item at the front of the deque

        Raises:
            DequeUnderflowException: If the deque is empty
        """
        if self.is_empty():
            raise DequeUnderflowException("Queue is empty.")
        return self.__queue.pop(0)

    def remove_last(self) -> T:
        """Remove and return an item at the back of the deque.

        Returns:
            (T): The item at the back of the deque

        Raises:
            DequeUnderflowException: If the deque is empty
        """
        if self.is_empty():
            raise DequeUnderflowException("Queue is empty.")
        return self.__queue.pop()

    def first(self) -> T:
        """Return an item at the front of the deque without removing it.

        Returns:
            (T): The item at the front of the deque

        Raises:
            DequeUnderflowException: If the deque is empty
        """
        if self.is_empty():
            raise DequeUnderflowException("Queue is empty.")
        return self.__queue[0]

    def last(self) -> T:
        """Return an item at the back of the deque without removing it.

        Returns:
            (T): The item at the back of the deque

        Raises:
            DequeUnderflowException: If the deque is empty
        """
        if self.is_empty():
            raise DequeUnderflowException("Queue is empty.")
        return self.__queue[-1]

    def clear(self) -> None:
        """Remove all items from the deque."""
        self.__queue = []


if __name__ == "__main__":
    dq: Deque[int] = Deque(capacity=5)
    print(dq)
    print(f"\nIs empty?: {dq.is_empty()}")

    dq.add_first(1)
    dq.add_last(2)
    dq.add_last(3)
    dq.add_first(4)
    dq.add_first(5)
    print(dq)
    print(f"\nIs empty?: {dq.is_empty()}")

    # dq.add_last(6)  # Raises DequeOverflowException

    print(f"\nRemove from first: {dq.remove_first()}")
    print(f"\nRemove from last: {dq.remove_last()}")

    print(dq)
    print(f"\nfirst: {dq.first()}")
    print(f"\nLast: {dq.last()}")

    dq.clear()
    print("\nQueue cleared.")
    print(dq)
    print(f"\nIs empty?: {dq.is_empty()}")

    # print(f"\nRemove from first: {dq.remove_first()}")  # Raises DequeUnderflowException
