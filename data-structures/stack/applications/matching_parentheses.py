import os
import sys

# add parent dir to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Stack import Stack


def is_parentheses_matched(input_str: str) -> bool:
    """Check if the parentheses are matched or not.

    Args:
    input_str (str): Input string to check.

    Returns:
        (bool): True if the parentheses are matched, False otherwise.
    """
    lefty: str = "({["
    righty: str = ")}]"
    stack: Stack[str] = Stack(capacity=len(input_str))
    for char in input_str:
        if char in lefty:
            stack.push(char)
        elif char in righty:
            if stack.is_empty():
                return False
            if righty.index(char) != lefty.index(stack.pop()):
                return False

    return stack.is_empty()


if __name__ == "__main__":
    input_exp: str = "( )(( )){([( )])}"
    print(f"Input expression: {input_exp}")
    print(f"Is parentheses matched: {is_parentheses_matched(input_exp)}")

    input_exp: str = ")(( )){([( )])}"
    print(f"Input expression: {input_exp}")
    print(f"Is parentheses matched: {is_parentheses_matched(input_exp)}")

    input_exp: str = "({[ ])}"
    print(f"Input expression: {input_exp}")
    print(f"Is parentheses matched: {is_parentheses_matched(input_exp)}")

    input_exp: str = "("
    print(f"Input expression: {input_exp}")
    print(f"Is parentheses matched: {is_parentheses_matched(input_exp)}")

    input_exp: str = ""
    print(f"Input expression: {input_exp}")
    print(f"Is parentheses matched: {is_parentheses_matched(input_exp)}")
