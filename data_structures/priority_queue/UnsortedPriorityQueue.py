import os
import sys

# add 'data-structures' into PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from priority_queue.PriorityQueueBase import PriorityQueueBase
from linked_list.PositionalList import PositionalList


class UnsortedPriorityQueue(PriorityQueueBase):
    """A min-oriented priority queue implemented with an unsorted list."""

    def enqueue(self, key: int, value: object) -> None:
        """Add a new key-value pair."""
        item = self._Item(key, value)
        self._data.add_last(item)

    def _find_min(self) -> PositionalList._Position[PriorityQueueBase._Item]:
        """Return Position of current min item (or None if empty)."""
        if self.is_empty():
            raise Exception("Queue is empty.")
        min = self._data.first()
        cursor = self._data.after(min)
        while cursor is not None:
            if cursor.item() < min.item():
                min = cursor
            cursor = self._data.after(cursor)
        return min

    def min(self) -> tuple[int, object]:
        """Return but do not remove (key, value) of current min item."""
        p = self._find_min()
        item = p.item()
        return (item._key, item._value)

    def deqeueue_min(self) -> tuple[int, object]:
        """Remove and return (key, value) of current min item."""
        p = self._find_min()
        item = self._data.delete(p)
        return (item._key, item._value)


if __name__ == "__main__":
    # Test the UnsortedPriorityQueue class
    pq = UnsortedPriorityQueue()
    pq.enqueue(3, "three")
    pq.enqueue(1, "one")
    pq.enqueue(1, "ONE")
    pq.enqueue(5, "five")

    print(pq)
    print(f"\nmin: {pq.min()}")
    print(f"Removed min: {pq.deqeueue_min()}")
    print(pq)

    ###########################################################################

    # ----------------------------OUTPUT---------------------------------------
    # header -><- (3, three) -><- (1, one) -><- (1, ONE) -><- (5, five) -><- trailer
    # size: 4

    # min: (1, 'one')
    # Removed min: (1, 'one')

    # header -><- (3, three) -><- (1, ONE) -><- (5, five) -><- trailer
    # size: 3

    ###########################################################################
