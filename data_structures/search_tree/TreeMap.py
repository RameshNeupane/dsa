from data_structures.tree.LinkedBinaryTree import LinkedBinaryTree
from map_and_hash.MapBase import MapBase, K, V

type key = K
type value = V


class TreeMap(LinkedBinaryTree, MapBase):
    """Sorted map implementation using binary search tree."""

    # _Position class overridden
    class _Position(LinkedBinaryTree._Position):
        def key(self) -> key:
            return self.element()._key

        def value(self) -> value:
            return self.element()._value

    def _subtree_search(self, p: _Position, k: key) -> _Position:
        """Return Position of k in subtree rooted at p.

        It uses binary search algorithm.
        """
        if k == p.key():
            return p
        elif k < p.key() and self.left(p) is not None:
            return self._subtree_search(self.left(p), k)
        else:
            if self.right(p) is not None:
                return self._subtree_search(self.right(p), k)
        return p  # on unsuccessful search, p is position of last visited/search node

    def _subtree_first_position(self, p: _Position) -> _Position:
        """Return the first position in subtree rooted at p."""
        cursor = p
        while self.left(cursor) is not None:
            cursor = self.left(cursor)
        return cursor

    def _subtree_last_position(self, p: _Position) -> _Position:
        """Return the last position in subtree rooted at p."""
        cursor = p
        while self.right(cursor) is not None:
            cursor = self.right(cursor)
        return cursor

    def first(self) -> _Position | None:
        """Return the first position in the tree (or None if empty)."""
        return self._subtree_first_position(self.root()) if len(self) > 0 else None

    def last(self) -> _Position | None:
        """Return the last position in the tree (or None if empty)."""
        return self._subtree_last_position(self.root()) if len(self) > 0 else None

    def before(self, p: _Position) -> _Position | None:
        """Return the position just before p in the natural order.
        Return None if p is the first position.
        """
        self._validate(p)
        if self.left(p) is not None:
            # last position in the left subtree of p
            return self._subtree_last_position(self.left(p))
        else:
            cursor = p
            parent = self.parent(cursor)
            while parent is not None and cursor == self.left(parent):
                cursor = parent
                parent = self.parent(cursor)
            return parent

    def after(self, p: _Position) -> _Position | None:
        """Return the position just after p in the natural order.
        Return None if p is the last position."""
        self._validate(p)
        if self.right(p) is not None:
            # first position in the right subtree of p
            return self._subtree_first_position(self.right(p))
        else:
            cursor = p
            parent = self.parent(cursor)
            while parent is not None and cursor == self.right(parent):
                cursor = parent
                parent = self.parent(cursor)
            return parent


# if __name__ == "__main__":
# m = TreeMap()
# print(m)
