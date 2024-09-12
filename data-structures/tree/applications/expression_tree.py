import os
import sys
from typing import Tuple


# add 'data-structure' directory into PYTHONPATH
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)
from tree.LinkedBinaryTree import LinkedBinaryTree
from linked_list.LinkedStack import LinkedStack
from stack.applications.matching_parentheses import is_parentheses_matched


class ExpressionTree(LinkedBinaryTree):
    def __init__(
        self,
        token: str,
        left: "LinkedBinaryTree" = None,
        right: "LinkedBinaryTree" = None,
    ) -> None:
        super().__init__()
        if not isinstance(token, str):
            raise TypeError("Token must be a string")
        self.add_root(token)
        if left is not None and right is not None:
            if token not in "-+*/":
                raise ValueError("token must be a valid operator -+*/")
            self.attach(self.root(), left, right)


def build_expression_tree(expr: str) -> ExpressionTree:
    """Constructs an expression tree from a string of infix expression."""
    if not is_parentheses_matched(expr):
        raise ValueError("Invalid expression")
    stack = LinkedStack[Tuple["ExpressionTree", str]]()
    for token in expr:
        if token in "-+*/":
            stack.push(token)
        elif token not in "()":
            stack.push(ExpressionTree(token))
        elif token == ")":
            right: ExpressionTree = stack.pop()
            operator: str = stack.pop()
            left: ExpressionTree = stack.pop()
            stack.push(ExpressionTree(operator, left, right))

    return stack.pop()


if __name__ == "__main__":
    # create an expression tree
    expr = "(((3+1)*4)/((9-5)+2))"
    tree = build_expression_tree(expr)

    print(f"Expression: {expr}\n")
    print(tree)
    print(f"total items: {len(tree)}")
    print(f"root: {tree.root().element()}")

    ###########################################################################

    # --------------------OUTPUT-----------------------------------------

    # Expression: (((3+1)*4)/((9-5)+2))

    # Info: Root => Root node, L => Left child, R => Right child
    # Root(/)
    #     |___L(*)
    #         |___L(+)
    #             |___L(3)
    #             |___R(1)
    #         |___R(4)
    #     |___R(+)
    #         |___L(-)
    #             |___L(9)
    #             |___R(5)
    #         |___R(2)

    # total items: 11
    # root: /

    ###########################################################################
