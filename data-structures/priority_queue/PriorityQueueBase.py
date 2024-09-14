class PriorityQueueBase:
    """Priority queue base class."""

    class _Item:
        """Lightweight, read-only wrapper for key-value pairs"""

        __slots__ = ("_key", "_value")

        def __init__(self, key: int, value: object) -> None:
            self._key = key
            self._value = value

        def __lt__(self, other: object) -> bool:
            return type(other) is type(self) and self._key < other._key

    def is_empty(self) -> bool:
        """Return True if the priority queue is empty, False otherwise."""
        return len(self) == 0
