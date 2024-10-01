from typing import TypeVar, Generic
from DoublyLinkedList import DoublyLinkedList

T = TypeVar("T")


class DoublyLinkeDequeUnderflowException(BaseException):
    pass


class DoublyLinkeDequeOverflowException(BaseException):
    pass


class DoublyLinkedDeque(Generic[T]):
    """Deque (Double ended queue) implementation based upon doubly linked list.

    Attributes:
        __queue: list of items, default is empty list
        __capacity: maximum number of items that can be stored, default is 10
    """

    def __init__(self, capacity=10) -> None:
        self.__queue = DoublyLinkedList[T]()
        self.__capacity = capacity

    def __repr__(self) -> str:
        """Return string representation of the queue."""
        return self.__queue.__repr__() + f"Capacity: {self.__capacity}\n"

    def __len__(self) -> int:
        """Return total number of items in the queue.

        Returns:
            (int): Total number of items in the queue
        """
        return self.__queue.__len__()

    def is_empty(self) -> bool:
        """Check if the queue is empty or not.

        Returns:
            (bool): True if the queue is empty, False otherwise
        """
        return self.__queue.is_empty()

    def is_full(self) -> bool:
        """Check if the queue is full or not.

        Returns:
            (bool): True if the queue is full, False otherwise"""
        return len(self) == self.__capacity

    def enqueue_first(self, item: T) -> None:
        """Add an item at the front of the queue.

        Args:
            item (T): The item to add to the queue

        Raises:
            DoublyLinkeDequeOverflowException: If the queue is full
        """
        if self.is_full():
            raise DoublyLinkeDequeOverflowException("Queue is full.")

        self.__queue.prepend(item)

    def enqueue_last(self, item: T) -> None:
        """Add an item at the back of the queue.

        Args:
            item (T): The item to add to the queue

        Raises:
            DoublyLinkeDequeOverflowException: If the queue is full
        """
        if self.is_full():
            raise DoublyLinkeDequeOverflowException("Queue is full.")

        self.__queue.append(item)

    def dequeue_first(self) -> T:
        """Remove and return the item from the front of the queue.

        Returns:
            (T): The item removed from the queue

        Raises:
            DoublyLinkeDequeUnderflowException: If the queue is empty
        """
        if self.is_empty():
            raise DoublyLinkeDequeUnderflowException("Queue is empty.")

        return self.__queue.remove_from_first()

    def dequeue_last(self) -> T:
        """Remove and return the item from the back of the queue.

        Returns:
            (T): The item removed from the queue

        Raises:
            DoublyLinkeDequeUnderflowException: If the queue is empty
        """
        if self.is_empty():
            raise DoublyLinkeDequeUnderflowException("Queue is empty.")

        return self.__queue.remove_from_last()

    def first(self) -> T:
        """Return the first item from the queue without removing it.

        Returns:
            (T): The item at the front of the queue

        Raises:
            DoublyLinkeDequeUnderflowException: If the queue is empty
        """
        if self.is_empty():
            raise DoublyLinkeDequeUnderflowException("Queue is empty.")

        return self.__queue.first()

    def last(self) -> T:
        """Return the last item from the queue without removing it.

        Returns:
            (T): The item at back of the queue

        Raises:
            DoublyLinkeDequeUnderflowException: If the queue is empty
        """
        if self.is_empty():
            raise DoublyLinkeDequeUnderflowException("Queue is empty.")

        return self.__queue.last()


if __name__ == "__main__":
    queue = DoublyLinkedDeque[int]()

    print(queue)
    print(f"Length: {len(queue)}")
    print(f"Is empty?: {queue.is_empty()}\n")

    # raises DoublyLinkeDequeUnderflowException: Queue is empty
    # print(f"First: {queue.first()}")

    for num in range(10):
        if num % 2 == 0:
            queue.enqueue_first(num)
        else:
            queue.enqueue_last(num)

    print(queue)

    print(f"Is full?: {queue.is_full()}\n")

    # raises DoublyLinkeDequeOverflowException: Queue is full.
    # queue.enqueue_first(10)

    print(f"First: {queue.first()}\n")
    print(f"Last: {queue.last()}\n")

    print(f"Dequeue first: {queue.dequeue_first()}\n")
    print(f"Dequeue last: {queue.dequeue_last()}\n")

    print(queue)

    ###########################################################################################

    # --------------------------------------OUTPUT---------------------------------------------

    # header -><- trailer
    # Size: 0
    # Capacity: 10

    # Length: 0
    # Is empty?: True

    # header -><- 8 -><- 6 -><- 4 -><- 2 -><- 0 -><- 1 -><- 3 -><- 5 -><- 7 -><- 9 -><- trailer
    # Size: 10
    # Capacity: 10

    # Is full?: True

    # First: 8

    # Last: 9

    # Dequeue first: 8

    # Dequeue last: 9

    # header -><- 6 -><- 4 -><- 2 -><- 0 -><- 1 -><- 3 -><- 5 -><- 7 -><- trailer
    # Size: 8
    # Capacity: 10

    ###########################################################################################
