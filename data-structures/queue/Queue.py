from typing import Generic, TypeVar, List

T = TypeVar("T")


class QueueUnderflowException(BaseException):
    pass


class QueueOverflowException(BaseException):
    pass


class Queue(Generic[T]):
    """Queue data structure.
    It follows FIFO (First-In-First-Out) behaviour.
    """

    def __init__(self, capacity=10) -> None:
        self.__capacity = capacity
        self.queue: List[T] = [None] * capacity
        self.__count = 0

    def __repr__(self) -> str:
        return (
            f"Queue: {self.queue}\nCapacity: {self.__capacity}\nCount: {self.__count}\n"
        )

    @property
    def capacity(self) -> int:
        """Returns capacity of the queue."""
        return self.__capacity

    @capacity.setter
    def capacity(self, value: int) -> None:
        if isinstance(value, int) and value > 0:
            if value < self.__capacity:
                self.queue = self.queue[0:value]
            else:
                self.queue.extend([None] * (value - self.__capacity))
            self.__capacity = value
        else:
            raise ValueError("Value passed in argument must be a positive integer.")

    @property
    def count(self):
        """Counts the items present in queue."""
        return self.__count

    def enqueue(self, item: T) -> None:
        """Add an element to the rear of the queue."""
        if self.__count == self.__capacity:
            raise QueueOverflowException("Queue overflow.")
        self.queue[self.__count] = item
        self.__count += 1

    def dequeue(self) -> T:
        """Remove an element from the front of the queue."""
        if self.__count == 0:
            raise QueueUnderflowException("Queue underflow.")
        elif self.__count == 1:
            item = self.queue[0]
        else:
            item = self.queue[0]
            for i in range(1, self.__count):
                self.queue[i - 1] = self.queue[i]
        self.__count -= 1
        self.queue[self.__count] = None
        return item

    def peek(self) -> T:
        """Return the item from the front of queue.

        Raises Uderflow error if the queue is empty.
        """
        if self.__count == 0:
            raise QueueUnderflowException("Queue underflow.")
        return self.queue[0]

    def clear(self) -> None:
        """Reset all the items to None."""
        self.queue = [None] * self.__capacity
        self.__count = 0


if __name__ == "__main__":
    q = Queue[int]()
    print(q)

    # change capacity to 5
    q.capacity = 5
    print(f"After changing capacity:\n{q}")

    # add elements
    q.enqueue(3)
    q.enqueue(6)
    q.enqueue(8)
    print(f"After adding three elements:\n{q}")

    # remove and display elements
    print(f"\nRemoved element: {q.dequeue()}")
    print(f"After removing one element:\n{q}")

    # remove and display elements
    print(f"\nRemoved element: {q.dequeue()}")
    print(f"After removing one element:\n{q}")

    q.clear()
    print(f"\nAfter clearing the queue, it should be empty now:\n{q}\n")

    try:
        print("\nTrying to dequeue from an empty queue...")
        _ = q.dequeue()
    except Exception as e:
        print(e)
