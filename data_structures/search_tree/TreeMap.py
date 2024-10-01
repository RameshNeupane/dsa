from tree.LinkedBinaryTree import LinkedBinaryTree
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
    

if __name__ == "__main__":
    m = TreeMap()
    print(m)
