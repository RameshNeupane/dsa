from typing import TypeVar, List, Generic, Iterator, Union
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from linked_list.LinkedQueue import LinkedQueue
from tree.TreeABC import TreeABC

T = TypeVar("T")


class LinkedTree(TreeABC, Generic[T]):
    """Tree data structure implementation using linked list."""

    __slots__ = "_root", "_size"

    class _Node(Generic[T]):
        """Node class for storing element in linked tree."""

        __slots__ = "_parent", "_element", "_children"

        def __init__(self, element: T, parent: Union["LinkedTree._Node", None]) -> None:
            self._element = element
            self._parent = parent
            self._children = LinkedQueue[LinkedTree._Position](capacity=99)

    class _Position(TreeABC._Position):
        """Locattion of the node in the tree."""

        __slots__ = "_container", "_node"

        def __init__(self, container: "LinkedTree", node: "LinkedTree._Node") -> None:
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

    # --------------tree constructor-------------------
    def __init__(self) -> None:
        """Initialize an empty tree."""
        self._root: LinkedTree._Node | None = None
        self._size = 0

    ###########################################################################
    #
    # ------------------private methods---------------------------------------
    #
    ###########################################################################

    def _validate(self, p: object) -> _Node:
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

    def _make_position(self, node: _Node) -> _Position | None:
        """Return Position instance for given node (or None if no position)."""
        return self._Position(self, node) if node is not None else None

    def _add_root(self, e: T) -> _Position:
        """Create a new root node and add it to the tree."""
        if self._root is not None:
            raise ValueError("Root already exists")
        self._size = 1
        self._root = self._Node(e, parent=None)
        return self._make_position(self._root)

    def _add_child(self, p: _Position, e: T) -> _Position:
        """Create a new child node with element e and add it to the tree as p's child node."""
        try:
            node = self._validate(p)
        except e:
            print(e)
            return None
        finally:
            self._size += 1
            child = self._Node(e, parent=node)
            p_child = self._make_position(child)
            node._children.enqueue(p_child)
            return p_child

    def _replace(self, p: _Position, e: T) -> T:
        """Replace the element at position p with e and return the old value."""
        node = self._validate(p)
        old = node._element
        node._element = e
        return old

    def _delete(self, p: _Position) -> T:
        """Delete the node at position p and return its element.
        It assigns the leftmost child as the parent to other children.
        """
        node = self._validate(p)

        if not node._children.is_empty():
            leftmost_child = node._children.dequeue()
            leftmost_child_node = self._validate(leftmost_child)
            leftmost_child_node._parent = node._parent
            node._parent._children.enqueue(leftmost_child)
            for child in node._children:
                child_node = self._validate(child)
                child_node._parent = leftmost_child_node
                leftmost_child_node._children.enqueue(child)

        for idx in range(len(node._parent._children)):
            if p == node._parent._children[idx]:
                node._parent._children.remove(idx)
                break
        node._parent = None
        node._children = None
        self._size -= 1
        return node._element

    def _attach(self, p: _Position, t: "LinkedTree") -> None:
        """Attach trees t1 and t2 to position p in this tree.

        - p is position in this tree where the root of t1 will be attached.
        - t1 is the tree to attach.
        """
        node = self._validate(p)
        if not self.is_leaf(p):
            raise ValueError("p must be a leaf node.")
        if not isinstance(t, self):
            raise TypeError("tree must be of same type.")
        if not t.is_empty():
            t._root._parent = node
            node._children.enqueue(t.root())
            self._size += t._size
            t._root = None
            t._size = 0

    ###########################################################################
    #
    # ------------------public methods---------------------------------------
    #
    ###########################################################################

    def __len__(self) -> int:
        """Return the number of elements in this tree."""
        return self._size

    def __repr__(self, level=0) -> str:
        """Return a string representation of this tree."""
        if self.is_empty():
            return ""

        def repr(p: LinkedTree._Position | None, level: int) -> str:
            node = self._validate(p)
            if node is None:
                return ""
            rep_str = f"{'    ' * level}{'|___' if node is not self._root else 'Root=>'}{node._element}\n"
            for child in node._children:
                rep_str += repr(child, level + 1)
            return rep_str

        return repr(self.root(), level)

    def root(self) -> _Position | None:
        """Return the root of this tree (or None if the tree is empty)"""
        return self._make_position(self._root)

    def parent(self, p: _Position) -> _Position | None:
        """Return the parent of position p (or None if p is the root)."""
        node = self._validate(p)
        return self._make_position(node._parent)

    def children(self, p: _Position) -> Iterator[_Position]:
        """Return an iterator over the children of position p."""
        node = self._validate(p)
        for child in node._children:
            yield child

    def num_children(self, p: _Position) -> int:
        """Return the number of children of position p."""
        node = self._validate(p)
        return len(node._children)

    def height(self, p: _Position) -> int:
        """Return the height of the subtree rooted at position p."""
        node = self._validate(p)
        if not node:
            return 0
        return self._height(p)

    def depth(self, p: _Position) -> int:
        """Return the depth of position p in the tree."""
        node = self._validate(p)
        if not node:
            return 0
        return self._depth(p)

    def add_root(self, e: T) -> _Position:
        "Create a new root node and add it to the tree."
        return self._add_root(e)

    def add_child(self, p: _Position, e: T) -> _Position:
        """Add a new child to position p and return it."""
        return self._add_child(p, e)

    def replace(self, p: _Position, e: T) -> T:
        """Replace the entry at position p with e and return the old entry."""
        return self._replace(p, e)

    def delete(self, p: _Position) -> T:
        """Remove the entry at position p and return the entry."""
        return self._delete(p)

    def attach(self, p: _Position, t: "LinkedTree") -> None:
        """Attach the tree t to the position p in this tree."""
        return self._attach(p, t)

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

    # 1. Preorder Traversal
    def preorder_traversal(self, root: _Position) -> list[T]:
        """Return a list of entries in preorder traversal order.

        Algorithm:
            Preorder(node):
                if node is not none:
                    visit(node)
                    for child in node.children:
                        Preorder(child)
        """
        result: list[T] = []
        node = self._validate(root)

        def preorder(node: LinkedTree._Node | None) -> None:
            if node is None:
                return
            result.append(node._element)
            for child in node._children:
                child = self._validate(child)
                preorder(child)

        preorder(node)
        return result

    # 2. Postorder Traversal
    def postorder_traversal(self, root: _Position) -> list[T]:
        """Return a list of entries in postorder traversal order.

        Algorithm:
            Postorder(node):
                if node is not none:
                    for child in node.children:
                        Postorder(child)
                    visit(node)
        """
        result: list[T] = []
        node = self._validate(root)

        def postorder(node: LinkedTree._Node | None) -> None:
            if node is None:
                return
            for child in node._children:
                child = self._validate(child)
                postorder(child)
            result.append(node._element)

        postorder(node)
        return result

    ###########################################################################
    #
    # -----------------------2. Breadth First Traversal Methods----------------
    #
    ###########################################################################

    # Level order traversal
    def levelorder_traversal(self, root: _Position) -> list[T]:
        """Return a list of entries in level order traversal order.

        Algorithm:
            LevelOrder(root):
                queue = Queue() # empty queue
                if root is not null:
                    queue.enqueue(root)
                while queue is not empty:
                    node = queue.dequeue()
                    visit(node)
                    for child in node.children:
                        if child is not null:
                            queue.enqueue(child)
        """
        result: list[T] = []
        node = self._validate(root)
        queue = LinkedQueue[LinkedTree._Node](capacity=self._size)
        if node is not None:
            queue.enqueue(node)
        while not queue.is_empty():
            node = queue.dequeue()
            result.append(node._element)
            for child in node._children:
                child = self._validate(child)
                if child is not None:
                    queue.enqueue(child)
        return result


if __name__ == "__main__":
    tree = LinkedTree[str]()

    print(f"Is tree empty: {tree.is_empty()}")
    print(f"Root:  {tree.root().element()if tree.root() else f"No root"}")
    print(tree)
    
    a = tree.add_root('a')
    print(tree)
    print(f"Is a node root?: {tree.is_root(a)}\n")
    
    b = tree.add_child(a, 'b')
    c = tree.add_child(a, 'c')
    d = tree.add_child(a, 'd')
    e = tree.add_child(b, 'e')
    f = tree.add_child(b, 'f')
    g = tree.add_child(b, 'g')
    h = tree.add_child(c, 'h')
    i = tree.add_child(d, 'i')
    j = tree.add_child(d, 'j')
    k = tree.add_child(e, 'k')
    l = tree.add_child(f, 'l')
    m = tree.add_child(g, 'm')
    n = tree.add_child(h, 'n')
    o = tree.add_child(i, 'o')
    p = tree.add_child(j, 'p')
    q = tree.add_child(k, 'q')
    r = tree.add_child(k, 'r')
    s = tree.add_child(l, 's')
    t = tree.add_child(l, 't')
    u = tree.add_child(n, 'u')
    v = tree.add_child(o, 'v')
    w = tree.add_child(p, 'w')
    x = tree.add_child(w, 'x')
    y = tree.add_child(w, 'y')
    z = tree.add_child(y, 'z')
    
    print(tree)
    
    print(f"Total number of nodes: {len(tree)}\n")

    print(f"Height of node a: {tree.height(a)}")
    print(f"Height of node m: {tree.height(m)}")
    print(f"Height of node w: {tree.height(w)}")
    print(f"Depth of node a: {tree.depth(a)}")
    print(f"Depth of node z: {tree.depth(z)}")
    print(f"Depth of node j: {tree.depth(j)}")
    
    print(f"\nIf x leaf node?: {tree.is_leaf(x)}")
    print(f"Is k leaf node?: {tree.is_leaf(k)}")
    print(f"Number of children of node b: {tree.num_children(b)}")
    print(f"Number of children of node v: {tree.num_children(v)}")
    print(f"Parent of node h: {tree.parent(h).element()}")
    print(f"Number of children of node b: {[child.element() for child in tree.children(b)]}")
    print(f"Number of children of node q: {[child.element() for child in tree.children(q)]}")
    
    print(f"\nPreorder traversal from node a: {tree.preorder_traversal(a)}")
    print(f"Preorder traversal from node d: {tree.preorder_traversal(d)}")
    print(f"Preorder traversal from node u: {tree.preorder_traversal(u)}")
    
    print(f"\nPostorder traversal from node a: {tree.postorder_traversal(a)}")
    print(f"Postorder traversal from node f: {tree.postorder_traversal(f)}")
    print(f"Postorder traversal from node s: {tree.postorder_traversal(s)}")
    
    print(f"\nLever order traversal of node a: {tree.levelorder_traversal(a)}")
    print(f"Lever order traversal of node j: {tree.levelorder_traversal(j)}")
    print(f"Lever order traversal of node t: {tree.levelorder_traversal(t)}")
    
    print(f"Delete node b: {tree.delete(b)}")
    print(tree)

    ####################################################################
    # ------------------------OUTPUT-------------------------------------
    #
    # Is tree empty: True
    # Root:  No root

    # Root=>a

    # Is a node root?: True

    # Root=>a
    #     |___b
    #         |___e
    #             |___k
    #                 |___q
    #                 |___r
    #         |___f
    #             |___l
    #                 |___s
    #                 |___t
    #         |___g
    #             |___m
    #     |___c
    #         |___h
    #             |___n
    #                 |___u
    #     |___d
    #         |___i
    #             |___o
    #                 |___v
    #         |___j
    #             |___p
    #                 |___w
    #                     |___x
    #                     |___y
    #                         |___z

    # Total number of nodes: 26

    # Height of node a: 6
    # Height of node m: 0
    # Height of node w: 2
    # Depth of node a: 0
    # Depth of node z: 6
    # Depth of node j: 2

    # If x leaf node?: True
    # Is k leaf node?: False
    # Number of children of node b: 3
    # Number of children of node v: 0
    # Parent of node h: c
    # Number of children of node b: ['e', 'f', 'g']
    # Number of children of node q: []

    # Preorder traversal from node a: ['a', 'b', 'e', 'k', 'q', 'r', 'f', 'l', 's', 't', 'g', 'm', 'c', 'h', 'n', 'u', 'd', 'i', 'o', 'v', 'j', 'p', 'w', 'x', 'y', 'z']
    # Preorder traversal from node d: ['d', 'i', 'o', 'v', 'j', 'p', 'w', 'x', 'y', 'z']
    # Preorder traversal from node u: ['u']

    # Postorder traversal from node a: ['q', 'r', 'k', 'e', 's', 't', 'l', 'f', 'm', 'g', 'b', 'u', 'n', 'h', 'c', 'v', 'o', 'i', 'x', 'z', 'y', 'w', 'p', 'j', 'd', 'a']
    # Postorder traversal from node f: ['s', 't', 'l', 'f']
    # Postorder traversal from node s: ['s']

    # Lever order traversal of node a: ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
    # Lever order traversal of node j: ['j', 'p', 'w', 'x', 'y', 'z']
    # Lever order traversal of node t: ['t']
    # Delete node b: b
    # Root=>a
    #     |___c
    #         |___h
    #             |___n
    #                 |___u
    #     |___d
    #         |___i
    #             |___o
    #                 |___v
    #         |___j
    #             |___p
    #                 |___w
    #                     |___x
    #                     |___y
    #                         |___z
    #     |___e
    #         |___k
    #             |___q
    #             |___r
    #         |___f
    #             |___l
    #                 |___s
    #                 |___t
    #         |___g
    #             |___m
    #
    ####################################################################
