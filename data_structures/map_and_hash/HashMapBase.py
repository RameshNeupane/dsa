from typing import List
from MapBase import MapBase, K, V
import random
from UnsortedMap import UnsortedMap


class HashMapBase(MapBase):
    """Map base class using a hash table."""

    def __init__(self, cap=7, prime=1_999_999_777):
        """Create an empty hash table map."""
        self._table: List[None] | List[UnsortedMap] = cap * [None]
        self._n = 0
        self._prime = prime
        self._scale = 1 + random.randrange(prime - 1)
        self._shift = random.randrange(prime)

    def __len__(self) -> int:
        return self._n

    def _hash(self, key: K) -> int:
        """Hash key using MAD (multiply-add-divide) method.

        Args:
            key (K): key to hash

        Returns:
            (int): hashed key
        """
        return ((hash(key) * self._scale + self._shift) % self._prime) % len(
            self._table
        )

    def __getitem__(self, key: K) -> V:
        """Return value associated with key (raise KeyError if not found).

        Args:
        key (K): key to search for

        Returns:
            V: value associated with key
        """
        hashed = self._hash(key)
        return self._bucket_getitem(hashed, key)

    def __setitem__(self, key: K, value: V) -> None:
        """Assign value to key (raise KeyError if key is already in map).

        Args:
            key (K): key to assign value to
            value (V): value to assign to key
        """
        hashed = self._hash(key)
        self._bucket_setitem(hashed, key, value)
        if self._n > (len(self._table) // 2):
            self._resize()

    def __delitem__(self, key: K) -> None:
        """Remove item associated with key (raise KeyError if not found).

        Args:
            key (K): key to delete value of
        """
        hashed = self._hash(key)
        self._bucket_delitem(hashed, key)

    def _resize(self):
        """Resize bucket array to a new capacity."""
        old = list(self.items())
        new_cap = 2 * len(self._table) - 1
        self._table = [None] * new_cap
        self._n = 0
        for k, v in old:
            self[k] = v
