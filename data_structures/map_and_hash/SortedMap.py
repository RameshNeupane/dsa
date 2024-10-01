from MapBase import MapBase, K, V
from typing import Iterator

type index = int


class SortedMap(MapBase):
    """A map that uses a sorted list of keys."""

    __slots__ = ("_table",)

    def __init__(self) -> None:
        self._table: list[MapBase._Item] = []

    def __len__(self) -> int:
        """Return the number of key-value pairs in the map."""

        return len(self._table)

    def __repr__(self) -> str:
        """Return a string representation of the map."""
        repr = "["
        for item in self._table:
            repr += f"({item._key}, {item._value}), "
        repr = repr[:-2] if not self.is_empty() else repr
        repr += " ]"
        return f"\nMap: {repr}\nsize: {len(self)}"

    def is_empty(self) -> bool:
        """Return True if the map is empty."""
        return len(self) == 0

    def _find_index(self, key: K, low: int, high: int) -> index:
        """Return the index for the key associated with item else -1 if key is not found.

        Note: It uses binary search algorithm.
        """
        if high < low:
            return high + 1
        mid = (low + high) // 2
        if key == self._table[mid]._key:
            return mid
        elif key < self._table[mid]._key:
            return self._find_index(key, low, mid - 1)
        else:
            return self._find_index(key, mid + 1, high)

    def __getitem__(self, key: K) -> V:
        """Return the value associated with the given key."""
        idx = self._find_index(key, 0, len(self) - 1)
        if idx >= len(self) and self._table[idx]._key != key:
            raise ValueError(f"Invalid key. {repr(key)}")
        return self._table[idx]._value

    def __setitem__(self, key: K, value: V) -> None:
        """Insert or update the key-value pair in the map."""
        idx = self._find_index(key, 0, len(self) - 1)
        if idx < len(self) and self._table[idx]._key == key:
            self._table[idx]._value = value
        else:
            self._table.insert(idx, MapBase._Item(key, value))

    def __delitem__(self, key: K) -> tuple[K, V]:
        """Remove the key-value pair with the given key from the map."""
        idx = self._find_index(key, 0, len(self) - 1)
        if idx == len(self) and self._table[idx]._key != key:
            raise ValueError(f"Invalid key: {repr(key)}")
        item = self._table.pop(idx)
        return (item._key, item._value)

    def __iter__(self) -> Iterator[K]:
        """Return an iterator over the keys in the map."""
        for item in self._table:
            yield item._key

    def __reversed__(self) -> Iterator[K]:
        """Return an iterator over the keys in the map in reverse order."""
        for item in reversed(self._table):
            yield item._key

    def find_min(self) -> tuple[K, V] | None:
        """Return the key-value pair with the minimum key in the map."""
        if self.is_empty():
            return None
        item = self._table[0]
        return (item._key, item._value)

    def find_max(self) -> tuple[K, V] | None:
        """Return the key-value pair with the maximum key in the map."""
        if self.is_empty():
            return None
        item = self._table[-1]
        return (item._key, item._value)

    def find_ge(self, key: K) -> tuple[K, V] | None:
        """Return the key-value pair with the minimum key greater than or equal to the given key."""
        idx = self._find_index(key, 0, len(self) - 1)
        if idx < len(self) and self._table[idx]._key == key:
            item = self._table[idx]
            return (item._key, item._value)
        return None

    def find_lt(self, key: K) -> tuple[K, V] | None:
        """Return the key-value pair with the maximum key strictly less than the given key."""
        idx = self._find_index(key, 0, len(self) - 1)
        if idx > 0:
            item = self._table[idx - 1]
            return (item._key, item._value)
        return None

    def find_gt(self, key: K) -> tuple[K, V] | None:
        """Return the key-value pair with the minimum key strictly greater than the given key."""
        idx = self._find_index(key, 0, len(self) - 1)
        if idx < len(self) and self._table[idx]._key == key:
            idx += 1
        if idx < len(self):
            item = self._table[idx]
            return (item._key, item._value)
        return None

    def find_range(self, start: K = None, stop: K = None) -> Iterator[tuple[K, V]]:
        """Return an iterator over the key-value pairs with keys in the range [start, stop).
        The end point is exclusive; keys equal to stop are not included in the iteration.
        """
        if start is None:
            idx = 0
        else:
            idx = self._find_index(start, 0, len(self) - 1)
        while idx < len(self) and (stop is None or self._table[idx]._key < stop):
            item = self._table[idx]
            yield (item._key, item._value)
            idx += 1


if __name__ == "__main__":
    sm = SortedMap()
    print(sm)

    sm[2] = "two"
    sm[10] = "ten"
    sm[7] = "seven"
    print(sm)

    sm[34] = "thirty-four"
    sm[23] = "twenty-three"
    sm[99] = "ninety-nine"
    print(sm)

    sm[7] = "SEVEN"  # update value
    print(f"\nUpdated value at key 7: {sm[7]}")

    del sm[99]  # delete item with key 99
    print(sm)

    # iterate over key
    print("\nIterate over keys:")
    for key in sm:
        print(f"({key}, {sm[key]})")

    # reverse the map
    print("\nReverse the map:")
    for key in reversed(sm):
        print(f"({key}, {sm[key]})")

    print(f"\nitem with min key: {sm.find_min()}")
    print(f"\nitem with max key: {sm.find_max()}")

    print(f"\nitem with key 12: {sm.find_ge(12)}")
    print(f"\nitem with key 10: {sm.find_ge(10)}")

    print(f"\nitem with immediate less key than 2: {sm.find_lt(2)}")
    print(f"\nitem with immediate less key than 23: {sm.find_lt(23)}")

    print(f"\nitem with immediate greater key than 2: {sm.find_gt(2)}")
    print(f"\nitem with immediate greater key than 34: {sm.find_gt(34)}")

    # range with no specified start and end
    print("\nRange with no specified start and end:")
    for key, value in sm.find_range():
        print(f"({key}, {value})")

    # range with specified start and end
    print("\nRange with specified start=5 and end=20:")
    for key, value in sm.find_range(5, 20):
        print(f"({key}, {value})")

    ###########################################################################

    # --------------------------------OUTPUT-----------------------------------
    # Map: [ ]
    # size: 0

    # Map: [(2, two), (7, seven), (10, ten) ]
    # size: 3

    # Map: [(2, two), (7, seven), (10, ten), (23, twenty-three), (34, thirty-four), (99, ninety-nine) ]
    # size: 6

    # Updated value at key 7: SEVEN

    # Map: [(2, two), (7, SEVEN), (10, ten), (23, twenty-three), (34, thirty-four) ]
    # size: 5

    # Iterate over keys:
    # (2, two)
    # (7, SEVEN)
    # (10, ten)
    # (23, twenty-three)
    # (34, thirty-four)

    # Reverse the map:
    # (34, thirty-four)
    # (23, twenty-three)
    # (10, ten)
    # (7, SEVEN)
    # (2, two)

    # item with min key: (2, 'two')

    # item with max key: (34, 'thirty-four')

    # item with key 12: None

    # item with key 10: (10, 'ten')

    # item with immediate less key than 2: None

    # item with immediate less key than 23: (10, 'ten')

    # item with immediate greater key than 2: (7, 'SEVEN')

    # item with immediate greater key than 34: None

    # Range with no specified start and end:
    # (2, two)
    # (7, SEVEN)
    # (10, ten)
    # (23, twenty-three)
    # (34, thirty-four)

    # Range with specified start=5 and end=20:
    # (7, SEVEN)
    # (10, ten)

    ###########################################################################
