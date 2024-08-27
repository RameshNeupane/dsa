import os
import sys
from typing import TypeVar, Generic

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linked_list.LinkedList import LinkedList

T = TypeVar("T")


class LinkedQueue(Generic[T]):
    """Queue implementation using singly linked list.

    Queue follows the FIFO (First In First Out) principle.
    """

    def __init__(self, capacity=10) -> None:
        self.__queue: LinkedList[T] = LinkedList()
        self.__capacity: int = capacity
        self.__count: int = 0

    def __repr__(self) -> str:
        return self.__queue.__repr__() + f"Capacity: {self.__capacity}\n"

    def __len__(self) -> int:
        return self.__count

    def is_empty(self) -> bool:
        """Check if the queue is empty or not.

        Returns:
            (bool): True if the queue is empty, False otherwise.
        """
        return self.__count == 0

    def enqueue(self, item: T) -> None:
        """Add a item into the queue.

        Args:
            item (T): Item to be added
        """
        if self.__count == self.__capacity:
            print("Queue is full")
            return None

        self.__queue.append(item)
        self.__count += 1

    def dequeue(self) -> T:
        """Remove and return a item from the queue.

        Returns:
            (T): Value of the item which was removed from the queue
        """
        if self.__count == 0:
            print("Queue is empty")
            return None

        self.__count -= 1
        return self.__queue.remove_from_beginning()

    def first(self) -> T:
        """Return a item that is at the first in the queue.

        Returns:
            (T): Value of the item which is at the first in the queue
        """
        if self.__count == 0:
            print("Queue is empty")
            return None

        return self.__queue.head()


if __name__ == "__main__":
    lq: LinkedQueue[int] = LinkedQueue(capacity=5)

    print(lq)
    print(f"Length: {len(lq)}")
    print(f"Is empty? {lq.is_empty()}\n")

    lq.enqueue(11)
    print(lq)
    print(f"Length: {len(lq)}\n")

    print(f"Dequeue: {lq.dequeue()}")
    print(f"Dequeue: {lq.dequeue()}")
    print(lq)

    lq.enqueue(22)
    lq.enqueue(33)
    lq.enqueue(44)
    lq.enqueue(55)
    lq.enqueue(66)
    print(lq)

    lq.enqueue(77)
    print(f"First item: {lq.first()}")

    ###########################################################################

    # -------------------------------OUTPUT------------------------------------

    # None
    # Count: 0
    # Capacity: 5

    # Length: 0
    # Is empty? True

    # 11 -> None
    # Count: 1
    # Capacity: 5

    # Length: 1

    # Dequeue: 11
    # Queue is empty
    # Dequeue: None
    # None
    # Count: 0
    # Capacity: 5

    # 22 -> 33 -> 44 -> 55 -> 66 -> None
    # Count: 5
    # Capacity: 5

    # Queue is full
    # First item: 22

    ###########################################################################
