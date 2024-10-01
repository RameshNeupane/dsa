from HashMapBase import HashMapBase
from UnsortedMap import UnsortedMap, K, V
from typing import Iterator


class ChainHashMap(HashMapBase):
    """Hash map implementation with separate chaining for collision resolution."""

    def __repr__(self) -> str:
        """Return a string representation of the hash map."""
        chain_str = "["
        for bucket in self._table:
            if bucket is not None:
                chain_str += "["
                for key in bucket:
                    chain_str += f"({key}, {bucket[key]}), "
                chain_str = chain_str[:-2] + "], "
            else:
                chain_str += " , "

        chain_str = chain_str[:-2] + "]"
        return f"\n{chain_str}\nLength: {len(self._table)}\n"

    def _bucket_getitem(self, hashed: int, key: K) -> V:
        """Return the value associated with key in the bucket for key.

        Args:
            hashed (int): The hashed key.
            key (K): The key to be searched for in the bucket.

        Returns:
            (V): The value associated with key in the bucket for key.

        Raises:
            KeyError: If key is not in the bucket for key.
        """
        bucket: UnsortedMap = self._table[hashed]
        if bucket is None:
            raise KeyError("Key Error: " + repr(key))
        return bucket[key]

    def _bucket_setitem(self, hashed: int, key: K, value: V) -> None:
        """Set the value for key in the bucket for key.

        Args:
            hashed (int): The hashed key.
            key (K): The key to be set in the bucket.
            value (V): The value to be set for key in the bucket.
        """

        if self._table[hashed] is None:
            self._table[hashed] = UnsortedMap()

        old_bucket_size = len(self._table[hashed])
        self._table[hashed][key] = value
        new_bucket_size = len(self._table[hashed])
        if new_bucket_size > old_bucket_size:
            self._n += 1

    def _bucket_delitem(self, hashed: int, key: K) -> None:
        """Remove the item with key from the bucket for key.

        Args:
            hashed (int): The hashed key.
            key (K): The key to be removed from the bucket.

        Raises:
            KeyError: If key is not in the bucket for key.
        """
        bucket = self._table[hashed]
        if bucket is None:
            raise KeyError("Key Error: " + repr(key))
        del bucket[key]
        if len(bucket) == 0:
            self._table[hashed] = None
        self._n -= 1

    def __iter__(self) -> Iterator[K]:
        for bucket in self._table:
            if bucket is not None:
                for key in bucket:
                    yield key


if __name__ == "__main__":
    chain = ChainHashMap()
    print(chain)
    chain[1] = "a"
    chain[2] = "b"
    chain[3] = "c"
    chain[4] = "d"
    chain[5] = "e"

    print(chain)

    print(f"key: 1, value: {chain[1]}")
    # print(chain[6]) # raises KeyError

    chain[5] = "z"
    print(chain)

    # delete key
    del chain[2]
    print(chain)

    # string key
    chain_str = ChainHashMap()
    chain_str["name"] = "ramesh"
    chain_str["age"] = 21
    print(chain_str)
