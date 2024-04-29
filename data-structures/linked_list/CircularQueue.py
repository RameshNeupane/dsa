from typing import TypeVar, Generic, Optional

T = TypeVar("T")


class Node(Generic[T]):
    """Node class.

    Fields:
        data (T): data of the current node
        _next (Node): next node in the linked list, initially None.
    """

    __slots__ = "_data", "_next"

    def __init__(self, data: T):
        self._data: T = data
        self._next: Node[T] | None = None


class CircularQueue(Generic[T]):
    """Queue implementation using circularly linked list."""

    def __init__(self) -> None:
        self.__tail: Node[T] | None = None
        self.__count: int = 0

    def __len__(self) -> int:
        """Return the number of items in the queue.

        Returns:
            (int): number of items in the queue
        """
        return self.__count

    def is_empty(self) -> bool:
        """Check if the queue is empty or not.

        Returns:
            (bool): True if the queue is empty, False otherwise
        """
        return len(self) == 0

    def first(self) -> T:
        """Return the item at the front of the queue.

        Returns:
            (T): item at the front of the queue
        """
        if self.is_empty():
            print("Queue is empty.")
            return None

        head: Node[T] = self.__tail._next
        return head._data

    def enqueue(self, item: T) -> None:
        """Add an item to the back of the queue.

        Args:
            item (T): item to be added to the back of the queue
        """
        new_node: Node[T] = Node(item)
        if self.is_empty():
            new_node._next = new_node
        else:
            new_node._next = self.__tail._next  # new node points to head
            self.__tail._next = new_node  # tail points to new node

        self.__tail = new_node  # tail is new node
        self.__count += 1

    def dequeue(self) -> T:
        """Remove and return the first item of the queue.

        Returns:
            (T): the first item of the queue, returns None if queue is empty
        """
        if self.is_empty():
            print("Queue is empty.")
            return None
        head: Node[T] = self.__tail._next
        self.__count -= 1
        if self.is_empty():
            self.__tail = None
        else:
            self.__tail._next = head._next
        return head._data

    def rotate(self) -> None:
        """Rotate front item to the back of the queue."""
        if not self.is_empty():
            self.__tail = self.__tail._next


if __name__ == "__main__":
    cq: CircularQueue[str] = CircularQueue()
    print(f"Is empty?: {cq.is_empty()}\n")
    print(f"Length: {len(cq)}\n")
    print(f"First: {cq.first()}\n")

    cq.enqueue("dsa")
    print(f"Is empty?: {cq.is_empty()}")
    print(f"Length: {len(cq)}\n")
    print(f"First: {cq.first()}\n")

    print(f"Dequeue: {cq.dequeue()}\n")
    print(f"Dequeue: {cq.dequeue()}\n")

    cq.enqueue("python")
    cq.enqueue("AI")
    cq.enqueue("ML")
    cq.enqueue("DL")
    print(f"Length: {len(cq)}\n")
    print(f"First: {cq.first()}\n")

    cq.rotate()
    print(f"First: {cq.first()}\n")

    cq.rotate()
    print(f"First: {cq.first()}\n")
