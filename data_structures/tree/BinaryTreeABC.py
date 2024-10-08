from abc import ABC, abstractmethod
from typing import Iterator, Optional
import os
import sys

sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from tree.TreeABC import TreeABC


class BinaryTreeABC(TreeABC, ABC):
    """Abstract base class for binary tree data structure."""

    ##########################################
    # Abstract methods to be implemented by subclasses
    ##########################################

    @abstractmethod
    def left(self, p: TreeABC._Position) -> Optional["TreeABC._Position"]:
        """Return the position of the left child of p, or None if p has no left child"""
        raise NotImplementedError("Must be implemented by subclass")

    @abstractmethod
    def right(self, p: TreeABC._Position) -> Optional["TreeABC._Position"]:
        """Return the position of the right child of p, or None if p has no right child"""
        raise NotImplementedError("Must be implemented by subclass")

    ##########################################
    # Concrete methods of Binary Tree
    ##########################################

    def sibling(self, p: TreeABC._Position) -> Optional["TreeABC._Position"]:
        """Return the position of the sibling of p, or None if no sibling."""
        parent = self.parent(p)
        if parent is None:
            return None
        else:
            if p == self.left(parent):
                return self.right(parent)
            else:
                return self.left(parent)

    def children(self, p: TreeABC._Position) -> Iterator["TreeABC._Position"]:
        """Generate iteration of Positions of p's children."""
        if self.left(p) is not None:
            yield self.left(p)
        if self.right(p) is not None:
            yield self.right(p)
