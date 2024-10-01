import os
import sys

# add 'data-structures' into PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linked_list.PositionalList import PositionalList


class PriorityQueueBase:
    """Priority queue base class."""

    __slots__ = ("_data",)

    class _Item:
        """Lightweight, read-only wrapper for key-value pairs"""

        __slots__ = ("_key", "_value")

        def __init__(self, key: int, value: object) -> None:
            self._key = key
            self._value = value

        def __lt__(self, other: object) -> bool:
            return type(other) is type(self) and self._key < other._key

    def __init__(self) -> None:
        self._data = PositionalList[PriorityQueueBase._Item]()

    def is_empty(self) -> bool:
        """Return True if the priority queue is empty, False otherwise."""
        return len(self) == 0

    def __repr__(self) -> str:
        """Return a string representation of the priority queue."""
        repr = "\nheader -><- "
        for item in self._data:
            repr += f"({item._key}, {item._value}) -><- "
        repr += "trailer"
        return f"{repr}\nsize: {len(self)}"

    def __len__(self) -> int:
        """Return the number of elements in the priority queue."""
        return len(self._data)
