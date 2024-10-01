import os
import sys
from typing import TypeVar, Generic, Generator

T = TypeVar("T")

# add parent dir into the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PositionalList import PositionalList


class FavoritesList(Generic[T]):
    """List of items ordered from most frequently accessed to least.

    Attributes:
        _data (PositionalList[_Item]): List of items ordered from most frequently accessed to least.
    """

    class _Item:
        """Item class.

        Attributes:
            _value (T): Value of the item.
            _count (int): Number of times the item has been accessed.
        """

        __slots__ = "_value", "_count"

        def __init__(self, value: T) -> None:
            self._value = value
            self._count: int = 0

    def __init__(self) -> None:
        self._data: PositionalList[FavoritesList[T]._Item] = PositionalList()

    def __repr__(self) -> str:
        favoritesListStr = f"\n{self.__class__.__name__} (\nheader -><- "
        walk = self._data.first()
        for item in self._data:
            favoritesListStr += f"{item._value}({item._count}) -><- "

        favoritesListStr += f"trailer\nSize: {len(self)}\n)\n"
        return favoritesListStr

    def __len__(self) -> int:
        """Return total number of Items in the list.

        Returns:
            (int): Total number of items
        """
        return len(self._data)

    def is_empty(self) -> bool:
        """Check if the list is empty or not.

        Returns:
            (bool): True if the list is empty, False otherwise.
        """
        return len(self._data) == 0

    def _find_position(self, value: T) -> "PositionalList._Position":
        """Return the position instance for the value passed into it.

        Args:
            value (T): Value to search for in the list.

        Returns:
            (PositionalList._Position): Position instance for the value passed into it, None if value does not exist.
        """
        walk = self._data.first()
        while walk is not None and walk.item()._value != value:
            walk = self._data.after(walk)
        return walk

    def _move_up(self, position: PositionalList._Position) -> None:
        """Move upward the item accessed at given position and sort item based upon access count.

        Args:
            position (PositionalList._Position): Position instance for the value passed into it.
        """
        if len(self) == 1:
            return

        access_count: int = position.item()._count
        walk = self._data.before(position)
        if access_count > walk.item()._count:
            while (
                walk != self._data.first()
                and access_count > self._data.before(walk).item()._count
            ):
                walk = self._data.before(walk)
            delete_item = self._data.delete(position)
            self._data.add_before(walk, delete_item)

    def access(self, value: T) -> None:
        """Access the passed value from the list. If value does not exist then add it into the back of the list.

        Args:
            value (T): Value to be accessed.
        """
        position = self._find_position(value)

        if position is None:
            item = self._Item(value)
            position = self._data.add_last(item)
        position.item()._count += 1
        self._move_up(position)

    def remove(self, value: T) -> "_Item":
        """Remove the value from the list if exists.

        Args:
            value (T): Value to be removed.

        Returns:
            _Item: The removed item if value exists.
        """
        position = self._find_position(value)
        if position is not None:
            return self._data.delete(position)

    def top(self, k: int) -> Generator[T, None, None]:
        """Return top k items from the list.

        Args:
            k (int): Number of items to be returned.

        Returns:
            Generator[T]: Generator of top k items.

        Raiese:
            ValueError: If k is not in range [1, len(self)].
        """
        if not 1 <= k <= len(self):
            raise ValueError("Invalid value of k.")
        walk = self._data.first()
        for j in range(k):
            item = walk.item()
            yield item._value
            walk = self._data.after(walk)


if __name__ == "__main__":
    fl: FavoritesList[str] = FavoritesList()
    print(fl)

    fl.access("a")
    fl.access("b")
    fl.access("c")
    print(fl)

    fl.access("b")
    fl.access("d")
    fl.access("a")
    fl.access("a")
    print(fl)

    print(f"Top 3:")
    for item in fl.top(3):
        print(item)

    removed = fl.remove("c")
    print(f"\nRemoved: {removed._value}")
    print(fl)

    fl.remove("e")

    ################################################################################

    # --------------------------------OUTPUT----------------------------------------

    # FavoritesList (
    # header -><- trailer
    # Size: 0
    # )

    # FavoritesList (
    # header -><- a(1) -><- b(1) -><- c(1) -><- trailer
    # Size: 3
    # )

    # FavoritesList (
    # header -><- a(3) -><- b(2) -><- c(1) -><- d(1) -><- trailer
    # Size: 4
    # )

    # Top 3:
    # a
    # b
    # c

    # Removed: c

    # FavoritesList (
    # header -><- a(3) -><- b(2) -><- d(1) -><- trailer
    # Size: 3
    # )

    ################################################################################
