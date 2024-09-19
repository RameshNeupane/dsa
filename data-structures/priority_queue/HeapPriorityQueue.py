type index = int


class Empty(BaseException):
    pass


class HeapPriorityQueue:
    """Priority queue using binary heap data structure."""

    __slots__ = ("_data",)

    class _Item:
        """Lightweight, read-only wrapper for key-value pairs."""

        __slots__ = ("_key", "_value")

        def __init__(self, key: int, value: object) -> None:
            self._key = key
            self._value = value

        def __lt__(self, other: object) -> bool:
            return type(other) is type(self) and self._key < other._key

    def __init__(self) -> None:
        self._data: list[HeapPriorityQueue._Item] = []

    def __len__(self) -> int:
        """Return total number of items in the priority queue."""
        return len(self._data)

    def is_empty(self) -> bool:
        """Return true if priority queue is empty, false otherwise."""
        return len(self) == 0

    def __repr__(self) -> str:
        """String representation of heap priority queue."""
        repr = "[ "
        for item in self._data:
            repr += f"({item._key}, {item._value}), "
        repr = repr[:-2] if not self.is_empty() else repr
        repr += " ]"
        return f"\nHeap: {repr}\nsize: {len(self)}"

    def _parent(self, idx: index) -> index:
        """Return index of parent node of the child at index 'idx'."""
        return (idx - 1) // 2

    def _left(self, idx: index) -> index:
        """Return index of left child of parent at index 'idx'."""
        return 2 * idx + 1

    def _right(self, idx: index) -> index:
        """Return index of right child of parent at index 'idx'."""
        return 2 * idx + 2

    def _has_left(self, idx: index) -> bool:
        """Return true if the given index has a left child, false otherwise."""
        return self._left(idx) < len(self)

    def _has_right(self, idx: index) -> bool:
        """Return true if the given index has a right child, false otherwise."""
        return self._right(idx) < len(self)

    def _swap(self, idx_i: index, idx_j: index) -> None:
        """Swap the elements at indices idx_i and idx_j in the heap."""
        self._data[idx_i], self._data[idx_j] = self._data[idx_j], self._data[idx_i]

    def _upheap(self, idx: index) -> None:
        """Move the element at index 'idx' up the heap until it is in the correct position."""
        parent_idx = self._parent(idx)
        if idx > 0 and self._data[idx] < self._data[parent_idx]:
            self._swap(idx, parent_idx)
            self._upheap(parent_idx)

    def _downheap(self, idx: index) -> None:
        """Move the element at index 'idx' down the heap until it is in the correct position."""
        if self._has_left(idx):
            left_idx = self._left(idx)
            small_idx = left_idx
            if self._has_right(idx):
                right_idx = self._right(idx)
                if self._data[right_idx] < self._data[left_idx]:
                    small_idx = right_idx
            if self._data[small_idx] < self._data[idx]:
                self._swap(idx, small_idx)
                self._downheap(small_idx)

    def add(self, key: int, value: object) -> None:
        """Add a new key-value pair to the heap."""
        self._data.append(self._Item(key, value))
        self._upheap(len(self) - 1)  # len(self) - 1 gives last index of the list

    def remove(self) -> tuple[int, object]:
        """Remove and return the smallest element from the heap."""
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        self._swap(0, len(self) - 1)
        item = self._data.pop()
        self._downheap(0)
        return (item._key, item._value)

    def min(self) -> tuple[int, object]:
        if self.is_empty():
            raise Empty("Priority queue is empty.")
        item = self._data[0]
        return (item._key, item._value)


if __name__ == "__main__":
    heapqueue = HeapPriorityQueue()
    print(heapqueue)

    heapqueue.add(10, "ten")
    heapqueue.add(5, "five")
    print(heapqueue)

    heapqueue.add(1, "one")
    print(heapqueue)

    heapqueue.add(1, "one")
    heapqueue.add(50, "fifty")
    heapqueue.add(22, "twenty-two")
    print(heapqueue)

    print(f"\nmin: {heapqueue.min()}")
    print(f"\nRemoved: {heapqueue.remove()}")

    print(heapqueue)

    ###########################################################################

    # -------------------------OUTPUT----------------------------------------
    # Heap: []
    # size: 0

    # Heap: [(5, five), (10, ten)]
    # size: 2

    # Heap: [(1, one), (10, ten), (5, five)]
    # size: 3

    # Heap: [(1, one), (1, one), (5, five), (10, ten), (50, fifty), (22, twenty - two)]
    # size: 6

    # min: (1, "one")

    # Removed: (1, "one")

    # Heap: [(1, one), (10, ten), (5, five), (22, twenty - two), (50, fifty)]
    # size: 5

    ###########################################################################
