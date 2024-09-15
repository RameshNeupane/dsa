import os
import sys

# add 'data-structures' into PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from priority_queue.PriorityQueueBase import PriorityQueueBase


class SortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented using sorted list."""

    def enqueue(self, key: int, value: object) -> None:
        """add new item into the queue and get sorted."""
        new = self._Item(key, value)
        cursor = self._data.last()
        while cursor is not None and new < cursor.item():
            cursor = self._data.before(cursor)
        if cursor is None:
            self._data.add_first(new)
        else:
            self._data.add_after(cursor, new)

    def min(self) -> tuple[int, object]:
        """return the item with the minimum key"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        item = self._data.first().item()
        return (item._key, item._value)

    def dequeue_min(self) -> tuple[int, object]:
        """remove the item with the minimum key and return it"""
        if self.is_empty():
            raise IndexError("Priority queue is empty")
        p = self._data.first()
        item = self._data.delete(p)
        return (item._key, item._value)


if __name__ == "__main__":
    # test the SortedPriorityQueue class
    sq = SortedPriorityQueue()
    print(sq)

    sq.enqueue(3, "three")
    sq.enqueue(2, "two")
    sq.enqueue(5, "five")
    print(sq)

    sq.enqueue(1, "one")
    sq.enqueue(4, "four")
    print(sq)

    print(f"\nmin: {sq.min()}")
    print(f"Removed item: {sq.dequeue_min()}")

    print(sq)

    ###########################################################################

    # --------------------------OUTPUT-----------------------------------------
    # header -><- trailer
    # size: 0

    # header -><- (2, two) -><- (3, three) -><- (5, five) -><- trailer
    # size: 3

    # header -><- (1, one) -><- (2, two) -><- (3, three) -><- (4, four) -><- (5, five) -><- trailer
    # size: 5

    # min: (1, 'one')
    # Removed item: (1, 'one')

    # header -><- (2, two) -><- (3, three) -><- (4, four) -><- (5, five) -><- trailer
    # size: 4

    ###########################################################################
