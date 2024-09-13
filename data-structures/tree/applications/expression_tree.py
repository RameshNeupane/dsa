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
    """Expression tree."""

    def __init__(
        self,
        token: str,
        left: "LinkedBinaryTree" = None,
        right: "LinkedBinaryTree" = None,
    ) -> None:
        super().__init__()
        if not isinstance(token, str):
            raise TypeError("Token must be a string")
        self._add_root(token)
        if left is not None and right is not None:
            if token not in "-+*/":
                raise ValueError("token must be a valid operator -+*/")
            self._attach(self.root(), left, right)

    def evaluate(self) -> float:
        """Evaluate the expression tree.

        Algorithm
            evaluate(p):
                if p is a leaf then
                    return the value stored at p
                else
                    let ◦ be the operator stored at p
                    x = evaluate recur(left(p))
                    y = evaluate recur(right(p))
                    return x ◦ y
        """

        def evaluate_recur(p: "LinkedBinaryTree._Position") -> float:
            if self.is_leaf(p):
                return float(p.element())
            else:
                operator = p.element()
                left = evaluate_recur(self.left(p))
                right = evaluate_recur(self.right(p))
                match operator:
                    case "+":
                        return left + right
                    case "-":
                        return left - right
                    case "*":
                        return left * right
                    case "/":
                        return left / right

        return evaluate_recur(self.root())


def build_expression_tree(expr: str) -> ExpressionTree:
    """Constructs an expression tree from a string of infix expression.

    Note: It supports multi-digit integer.
    """
    if not is_parentheses_matched(expr):
        raise ValueError("Invalid expression")
    stack = LinkedStack[Tuple["ExpressionTree", str]]()
    num = ""
    for token in expr:
        if token in "-+*/":
            if num:
                stack.push(ExpressionTree(num))
                num = ""
            stack.push(token)
        elif token in "1234567890":
            num += token
        elif token == ")":
            if num:
                stack.push(ExpressionTree(num))
                num = ""
            right: ExpressionTree = stack.pop()
            operator: str = stack.pop()
            left: ExpressionTree = stack.pop()
            stack.push(ExpressionTree(operator, left, right))

    return stack.pop()


if __name__ == "__main__":
    expr = "(((32+10)*41)/((99-35)+82))"
    print(f"Expression: {expr}\n")

    tree = build_expression_tree(expr)

    print(tree)
    print(f"total items: {len(tree)}")
    print(f"root: {tree.root().element()}")
    print(f"Expression evaluated: {tree.evaluate()}")

    ###########################################################################

    # --------------------OUTPUT-----------------------------------------

    # Expression: (((32+10)*41)/((99-35)+82))

    # Info: Root => Root node, L => Left child, R => Right child
    # Root(/)
    #     |___L(*)
    #         |___L(+)
    #             |___L(32)
    #             |___R(10)
    #         |___R(41)
    #     |___R(+)
    #         |___L(-)
    #             |___L(99)
    #             |___R(35)
    #         |___R(82)

    # total items: 11
    # root: /
    # Expression evaluated: 11.794520547945206

    ###########################################################################
