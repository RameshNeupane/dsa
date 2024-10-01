from abc import ABC, abstractmethod
from typing import Any, Optional, Iterator


class TreeABC(ABC):
    """Abstract base class for tree data structure."""

    class _Position(ABC):
        """An abstraction representing the location of a single element within a tree."""

        @abstractmethod
        def element(self) -> Any:
            """Return the element at this Position."""
            raise NotImplementedError("Must be implemented by subclass.")

        @abstractmethod
        def __eq__(self, other: object) -> bool:
            "Return True if the other Postion represents the same location."
            raise NotImplementedError("Must be implemented by subclass.")

        def __ne__(self, other: object) -> bool:
            "Return True if the other Postion does not represent the same location."

            return not (self == other)

    ##############################################################
    # Abstract methods of the Tree class
    ##############################################################

    @abstractmethod
    def root(self) -> Optional["TreeABC._Position"]:
        """Return the root Position of the tree (or None if tree is empty)."""
        raise NotImplementedError("must be implemented by subclass")

    @abstractmethod
    def parent(self, p: "TreeABC._Position") -> Optional["TreeABC._Position"]:
        """Return the Position of p's parent (or None if p is the root)."""
        raise NotImplementedError("must be implemented by subclass")

    @abstractmethod
    def num_children(self, p: "TreeABC._Position") -> int:
        """Return the number of children that Position p has."""
        raise NotImplementedError("must be implemented by subclass")

    @abstractmethod
    def children(self, p: "TreeABC._Position") -> Iterator["TreeABC._Position"]:
        """Generate an iteration of Positions representing p's children."""
        raise NotImplementedError("must be implemented by subclass")

    @abstractmethod
    def __len__(self) -> int:
        """Return the total number of elements in the tree."""
        raise NotImplementedError("must be implemented by subclass")

    ##############################################################
    # Concrete methods
    ##############################################################

    def is_root(self, p: "TreeABC._Position") -> bool:
        """Return True if Position p represents the root of the tree."""
        return self.root() == p

    def is_leaf(self, p: "TreeABC._Position") -> bool:
        """Return True if Position p represents a leaf of the tree."""
        return self.num_children(p) == 0

    def is_empty(self) -> bool:
        """Return True if the tree is empty."""
        return len(self) == 0

    # -------------private method---------------------------
    def _height(self, p: _Position) -> int:
        """Return the height of the tree rooted at Position p."""
        if self.is_leaf(p):
            return 0
        else:
            return 1 + max(self.height(child) for child in self.children(p))

    def _depth(self, p: _Position) -> int:
        """Return the depth of Position p in the tree."""
        if self.is_root(p):
            return 0
        else:
            return 1 + self._depth(self.parent(p))
