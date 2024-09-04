import os
import sys


# add 'tree' directory into PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from LinkedTree import LinkedTree


def parenthesize(t: LinkedTree, p: LinkedTree._Position) -> str:
    """Return a parenthesized string representation of the subtree rooted at p.
    
    It is customized version of preorder tree traversal.
    """
    node = t._validate(p)
    # print(node._element, end="")
    paren_str = f"{node._element}"
    if not t.is_leaf(p):
        first_time = True
        for child in t.children(p):
            paren_str += f"{' (' if first_time else ', '}"
            first_time = False
            paren_str += parenthesize(t, child)
        paren_str += ')'
    return paren_str


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
    print(f"Parenthesized version of tree is:\n{parenthesize(tree, a)}")
    
    ###########################################################################
    #---------------------OUTPUT----------------------------------------------
    
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

    # Parenthesized version of tree is:
    # a (b (e (k (q, r)), f (l (s, t)), g (m)), c (h (n (u))), d (i (o (v)), j (p (w (x, y (z))))))
    
    ###########################################################################
