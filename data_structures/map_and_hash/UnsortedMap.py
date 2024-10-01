from typing import List, Iterator
from MapBase import MapBase, K, V


class UnsortedMap(MapBase):
    """Simple map class."""

    def __init__(self) -> None:
        self._table: List[MapBase._Item] = []

    def __len__(self) -> int:
        """Return total number of items in the map table.

        Returns:
            (int): total number of items in the map table.
        """
        return len(self._table)

    def __getitem__(self, key: K) -> V:
        """Return item's value associated with its key.

        Args:
            key (K): key of the item.

        Returns:
            (V): value of the item.

        Raises:
            KeyError: if key is not found.
        """
        for item in self._table:
            if item._key == key:
                return item._value
        raise KeyError("Key Error: " + repr(key))

    def __setitem__(self, key: K, value: V) -> None:
        """Set a new value to the item's key.

        Args:
            key (K): key of the item.
            value (V): new value to be set.
        """
        for item in self._table:
            if item._key == key:
                item._value = value
                return
        self._table.append(self._Item(key, value))

    def __delitem__(self, key: K) -> None:
        """Remove item associated with given key.

        Args:
            key (K): key of the item.

        Raises:
            KeyError: if key is not found.
        """
        for i in range(len(self._table)):
            if self._table[i]._key == key:
                self._table.pop(i)
                return
        raise KeyError("Key Error: " + repr(key))

    def __iter__(self) -> Iterator[K]:
        for item in self._table:
            yield item._key
