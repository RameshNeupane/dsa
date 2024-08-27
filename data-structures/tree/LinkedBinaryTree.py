from typing import TypeVar, Optional, Union, List, Generic
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linked_list.LinkedQueue import LinkedQueue
from tree.BinaryTreeABC import BinaryTreeABC

T = TypeVar("T")


class LinkedBinaryTree(BinaryTreeABC, Generic[T]):
    """Linked binary tree implementation."""

    class _Node(Generic[T]):
        """Node class for storing storing element."""

        __slots__ = "_parent", "_element", "_left", "_right"

        def __init__(
            self,
            element: T,
            parent: Optional["LinkedBinaryTree._Node"] = None,
            left: Optional["LinkedBinaryTree._Node"] = None,
            right: Optional["LinkedBinaryTree._Node"] = None,
        ) -> None:
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class _Position(BinaryTreeABC._Position):
        """Locattion of the node in the tree."""

        __slots__ = "_container", "_node"

        def __init__(
            self, container: "LinkedBinaryTree", node: "LinkedBinaryTree._Node"
        ) -> None:
            self._container = container
            self._node = node

        def element(self) -> T:
            """Return element at the position."""
            return self._node._element

        def __eq__(self, other: object) -> bool:
            """Return true if other postion represents same location."""
            return (
                isinstance(other, type(self))
                and other._node is self._node
                and other._container is self._container
            )

    # ---------binary tree constructor-----------
    def __init__(self) -> None:
        self._root: Optional[LinkedBinaryTree._Node] = None
        self._size: int = 0

    # ---------private methods--------------------
    def _validate(self, p: object) -> Optional["_Node"]:
        """Return appropriate node if the position is valid."""
        if not isinstance(p, self._Position):
            raise TypeError("p must be a Position")
        if p._container is not self:
            raise ValueError("p does not belong to this container")
        if p._node is None:
            raise ValueError("p is no longer valid")
        if p._node._parent is p._node:
            raise ValueError("p is no longer valid")
        return p._node

    def _make_position(self, node: _Node) -> Union["_Position", None]:
        """Return Position instance for given node (or None if no position)."""
        return self._Position(self, node) if node is not None else None

    def _add_root(self, e: T) -> _Position:
        """Place element e at root of the tree."""
        if self._root is not None:
            raise ValueError("Root already exists.")
        self._size = 1
        self._root = self._Node(e)
        return self._make_position(self._root)

    def _add_left(self, p: _Position, e: T) -> _Position:
        """Create a new node with element e and add it to the left of p."""
        node = self._validate(p)
        if node._left is not None:
            raise ValueError("Left child already exists.")
        self._size += 1
        node._left = self._Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p: _Position, e: T) -> _Position:
        """Create a new node with element e and add it to the right of p."""
        node = self._validate(p)
        if node._right is not None:
            raise ValueError("Right child already exists.")
        self._size += 1
        node._right = self._Node(e, node)
        return self._make_position(node._right)

    def _replace(self, p: _Position, e: T) -> T:
        """Replace the element at position p with e and return the old value."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p: _Position) -> T:
        """Delete the node at position p, returning its element."""
        node = self._validate(p)

        # if the tree consists of only a root node
        if self._size == 1:
            self._root = None
            return node._element

        if self.num_children(p) == 2:
            raise ValueError("node has two children.")

        # if the node is root node
        if node is self._root:
            self._size -= 1
            self._root = node._left if node._left else node._right
            self._root._parent = node._parent
            return node._element

        # if the node is leaf node
        if self.is_leaf(p):
            self._size -= 1
            parent = node._parent
            if node is parent._left:
                parent._left = None
            else:
                parent._right = None
            return node._element
        else:
            # if the node is internal node
            parent = node._parent
            child = node._left if node._left else node._right
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
            child._parent = node._parent
            node._parent = None
            node._left = None
            node._right = None
            self._size -= 1
            return node._element

    def _attach(
        self, p: _Position, t1: "LinkedBinaryTree", t2: "LinkedBinaryTree"
    ) -> None:
        """Attach trees t1 and t2 to position p in this tree.

        - p is position in this tree where the heads of t1 and t2 will be attached.
        - t1 and t2 are the trees to attach.
        """
        node = self._validate(p)  # assert p is valid node in this tree
        if not self.is_leaf(p):
            raise ValueError("p must be position of a leaf node in this tree.")
        if not type(self) is type(t1) is type(t2):
            raise TypeError("Trees must be of same type.")
        self._size += t1._size + t1._size
        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0
        if not t2.is_empty():
            t2._root._parent = node
            node._right = t2._root
            t2._root = None
            t2._size = 0

    # -----------public methos-----------------------

    def __repr__(self, level=0) -> str:
        """Return a string representation of the tree."""
        if not self._root:
            return ""

        def _repr(node: LinkedBinaryTree._Node, level: int, tag: str) -> str:
            if node is None:
                return ""
            rep = f"{'    ' * level}{'|___' if node is not self._root else ''}{tag}({node._element})\n"
            rep += _repr(node._left, level + 1, "L")
            rep += _repr(node._right, level + 1, "R")
            return rep

        info_str = f"Info: Root => Root node, L => Left child, R => Right child\n"
        rep = _repr(self._root, level, "Root")
        return info_str + rep

    def __len__(self) -> int:
        """Return the number of elements in the tree."""
        return self._size

    def root(self) -> Union[_Position, None]:
        """Return the root position of the tree (or None if the tree is empty)."""
        return self._make_position(self._root)

    def parent(self, p: _Position) -> Union[_Position, None]:
        """Return position of p's parent (or None if the p is root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def left(self, p: _Position) -> Union[_Position, None]:
        """Return position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p: _Position) -> Union[_Position, None]:
        """Return position of p's right child (or None if no right child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def num_children(self, p: _Position) -> int:
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def height(self, p: _Position) -> Union[int, None]:
        """Return the height of the tree rooted at p."""
        node = self._validate(p)
        if not node:
            return 0
        return self._height(p)

    def depth(self, p: _Position) -> int:
        """Return the depth of the tree rooted at p."""
        node = self._validate(p)
        if not node:
            return 0
        return self._depth(p)

    def add_root(self, e: T) -> _Position:
        """Create a new root node and add it to the tree."""
        return self._add_root(e)

    def add_left(self, p: _Position, e: T) -> _Position:
        """Create a new left child for node p, storing value e."""
        return self._add_left(p, e)

    def add_right(self, p: _Position, e: T) -> _Position:
        """Create a new right child for node p, storing value e."""
        return self._add_right(p, e)

    def replace(self, p: _Position, e: T) -> T:
        """Replace the entry at position p with e and return the old entry."""
        return self._replace(p, e)

    def delete(self, p: _Position) -> T:
        """Remove the entry at position p and return the entry."""
        return self._delete(p)

    def attach(
        self,
        p: _Position,
        t1: "LinkedBinaryTree._Position",
        t2: "LinkedBinaryTree._Position",
    ) -> None:
        """Attach t1 and t2 to p, respectively, replacing the node at position p and
        its children. t1 and t2 are trees respectively.
        """
        return self._attach(p, t1, t2)

    ###########################################################################
    #
    # -----------------------Binary Tree Traversal Methods---------------------
    #
    ###########################################################################

    ###########################################################################
    #
    # -----------------------1. Depth First Traversal Methods-----------------
    #
    ###########################################################################

    # 1. Inorder Traversal
    def inorder_traversal(self, root: _Position) -> Union[list[T], None]:
        """Return a list of values of the nodes in the tree in inorder traversal order.

        In an Inorder Traversal, the nodes are visited in the following order:
            1. Left subtree (L)
            2. Root node (N)
            3. Right subtree (R)
            i.e. Order => L -> N -> R

        Recursive approach:
            Inorder(root):
                if root is not null:
                    Inorder(root.left)      # Traverse the left subtree
                    Visit(root)             # Visit the root node
                    Inorder(root.right)     # Traverse the right subtree
        """
        result: list[T] = []
        root_node = self._validate(root)
        if root_node is None:
            return None

        # inorder traverse recursive approach
        def traverse(node: Union[LinkedBinaryTree._Node, None]) -> Union[list[T], None]:
            if node is None:
                return
            traverse(node._left)
            result.append(node._element)
            traverse(node._right)

        traverse(root._node)
        return result

    # 2. Preorder Traversal
    def preorder_traversal(self, root: _Position) -> Union[list[T], None]:
        """Return a list of values of the nodes in the tree in preorder traversal order.

        In a preorder traversal, the nodes are visited in the following order:
            1. Root node (N)
            2. Left subtree (L)
            3. Right subtree (R)
            i.e. Order => N -> L -> R

        Recursive approach:
            Preorder(root):
                if root is not null:
                    Visit(root)           # visit root node
                    Preorder(root.left)   # traverse left subtree
                    Preorder(root.right)  # traverse right subtree
        """
        result: List[T] = []
        root_node = self._validate(root)
        if root_node is None:
            return None

        # preorder traverse recursive approach
        def traverse(node: Union[LinkedBinaryTree._Node, None]) -> Union[list[T], None]:
            if node is None:
                return
            result.append(node._element)  # visit root node
            traverse(node._left)  # traverse left subtree
            traverse(node._right)  # traverse right subtree

        traverse(root._node)
        return result

    # 3. Postorder Traversal
    def postorder_traversal(self, root: _Position) -> Union[list[T], None]:
        """Return a list of values of the nodes in the tree in postorder traversal order.

        In a postorder traversal, the nodes are visited in the following order:
            1. Left subtree (L)
            2. Right subtree (R)
            3. Root node (N)
            i.e. Order => L -> R -> N

        Recursive approach:
            Postorder(root):
                if root is not null:
                    Postorder(root.left)    # traverse left subtree
                    Postorder(root.right)   # traverse right subtree
                    Visit(root)             # visit root node
        """
        result: list[T] = []
        root_node = self._validate(root)
        if root_node is None:
            return None

        # postorder traverse recursive approach
        def traverse(node: Union[LinkedBinaryTree._Node, None]) -> Union[list[T], None]:
            if node is None:
                return
            traverse(node._left)  # traverse left subtree
            traverse(node._right)  # traverse right subtree
            result.append(node._element)  # visit root node

        traverse(root._node)
        return result

    ###########################################################################
    #
    # -----------------------2. Breadth First Traversal Methods-----------------
    #
    ###########################################################################

    # Lever Order Traversal
    def levelorder_traversal(
        self, root: _Position, tree_size: int
    ) -> Union[list[T], None]:
        """Return a list of values of the nodes in the tree in level order traversal order.

        Level Order Traversal is the most common form of Breadth-First Traversal applied
        to trees. In Level Order Traversal, the nodes of the tree are visited level by
        level, starting from the root and moving downwards, visiting all nodes at each level
        from left to right.

        Algorithm:
            LevelOrder(root):
                if root is null:
                    return

                queue = empty queue
                queue.enqueue(root)

                while queue is not empty:
                    node = queue.dequeue()  # Dequeue the front node
                    Visit(node)             # Visit the node

                    if node.left is not null:
                        queue.enqueue(node.left)   # Enqueue left child
                    if node.right is not null:
                        queue.enqueue(node.right)  # Enqueue right child
        """
        result: list[T] = []
        root_node = self._validate(root)
        if root_node is None:
            return None

        queue = LinkedQueue[LinkedBinaryTree._Node](capacity=tree_size)
        queue.enqueue(root_node)
        while not queue.is_empty():
            node = queue.dequeue()
            result.append(node._element)

            if node._left is not None:
                queue.enqueue(node._left)
            if node._right is not None:
                queue.enqueue(node._right)
        return result


if __name__ == "__main__":
    # Test the LinkedBinaryTree class
    tree = LinkedBinaryTree[str]()
    print(f"Is tree empty?: {tree.is_empty()}\n")

    a = tree.add_root("a")
    print(f"Root: {tree.root().element()}\n")
    print(tree)

    b = tree.add_left(a, "b")
    c = tree.add_right(a, "c")
    d = tree.add_left(b, "d")
    e = tree.add_right(b, "e")
    f = tree.add_left(c, "f")
    g = tree.add_right(c, "g")
    h = tree.add_left(e, "h")
    i = tree.add_right(g, "i")

    print(tree)

    print(f"Parent of node c is: {tree.parent(c).element()}\n")
    print(
        f"Left and right children of node b is: {tree.left(b).element()}, {tree.right(b).element()}\n"
    )

    print(f"Is g leaf node?: {tree.is_leaf(g)}")
    print(f"Is d leaf node?: {tree.is_leaf(d)}")
    print(f"Is c root node?: {tree.is_root(c)}")
    print(f"Is tree empty?: {tree.is_empty()}")
    print(f"Total nodes in the tree: {len(tree)}")
    print(f"Number of children of node c: {tree.num_children(c)}")
    print(f"Number of children of node f: {tree.num_children(f)}")

    print(f"Replace c with k: {tree.replace(c, 'k')}\n")

    print(tree)
    tree.replace(c, "c")

    print(f"Height of node a: {tree.height(a)}")
    print(f"Height of node d: {tree.height(d)}")
    print(f"Height of node g: {tree.height(g)}\n")

    print(f"Depth of node a: {tree.depth(a)}")
    print(f"Depth of node d: {tree.depth(d)}")
    print(f"Depth of node h: {tree.depth(h)}\n")

    print(tree)

    print(f"Inorder traversal: {tree.inorder_traversal(tree.root())}")
    print(f"Preorder traversal: {tree.preorder_traversal(tree.root())}")
    print(f"Postorder traversal: {tree.postorder_traversal(tree.root())}")
    print(f"Lever Order traversal: {tree.levelorder_traversal(tree.root(), len(tree))}")

    ####################################################################
    # ------------------------OUTPUT-------------------------------------
    # Is tree empty?: True

    # Root: a

    # Info: Root => Root node, L => Left child, R => Right child
    # Root(a)

    # Info: Root => Root node, L => Left child, R => Right child
    # Root(a)
    #     |___L(b)
    #         |___L(d)
    #         |___R(e)
    #             |___L(h)
    #     |___R(c)
    #         |___L(f)
    #         |___R(g)
    #             |___R(i)

    # Parent of node c is: a

    # Left and right children of node b is: d, e

    # Is g leaf node?: False
    # Is d leaf node?: True
    # Is c root node?: False
    # Is tree empty?: False
    # Total nodes in the tree: 9
    # Number of children of node c: 2
    # Number of children of node f: 0
    # Replace c with k: c

    # Info: Root => Root node, L => Left child, R => Right child
    # Root(a)
    #     |___L(b)
    #         |___L(d)
    #         |___R(e)
    #             |___L(h)
    #     |___R(k)
    #         |___L(f)
    #         |___R(g)
    #             |___R(i)

    # Height of node a: 3
    # Height of node d: 0
    # Height of node g: 1

    # Depth of node a: 0
    # Depth of node d: 2
    # Depth of node h: 3

    # Info: Root => Root node, L => Left child, R => Right child
    # Root(a)
    #     |___L(b)
    #         |___L(d)
    #         |___R(e)
    #             |___L(h)
    #     |___R(c)
    #         |___L(f)
    #         |___R(g)
    #             |___R(i)

    # Inorder traversal: ['d', 'b', 'h', 'e', 'a', 'f', 'c', 'g', 'i']
    # Preorder traversal: ['a', 'b', 'd', 'e', 'h', 'c', 'f', 'g', 'i']
    # Postorder traversal: ['d', 'h', 'e', 'b', 'f', 'i', 'g', 'c', 'a']
    # Lever Order traversal: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i']

    ####################################################################
