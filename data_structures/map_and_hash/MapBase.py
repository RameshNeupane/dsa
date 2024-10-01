from collections.abc import MutableMapping
from typing import TypeVar, Generic

K = TypeVar("K")
V = TypeVar("V")


class MapBase(MutableMapping, Generic[K, V]):
    """Abstract Map base class with nested _Item class."""

    class _Item:
        """Non public _Item class.

        Attributes:
            _key: Key of the item.
            _value: Value of the item.
        """

        __slots__ = "_key", "_value"

        def __init__(self, k: K, v: V):
            self._key: K = k
            self._value: V = v

        def __eq__(self, other: "MapBase._Item") -> bool:
            """Compare items based on their key.

            Returns:
                (bool): True if both item contains same key, False otherwise
            """
            return self._key == other._key

        # opposite of __eq__
        def __ne__(self, other: "MapBase._Item") -> bool:

            return not (self == other)

        # comapre item based on their key
        def __lt__(self, other: "MapBase._Item") -> bool:
            return self._key < other._key
