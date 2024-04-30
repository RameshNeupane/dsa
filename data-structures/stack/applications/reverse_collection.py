import os
import sys
from typing import List, TypeVar

# add parent dir to the PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Stack import Stack

T = TypeVar("T")


def reverse_collection(input_collection: List[T] | str) -> List[T] | str:
    """Reverse the given input collection.

    Args:
        input_collection (List[T] | str): The input collection to be reversed.

    Returns:
        (List[T] | str): The reversed collection.
    """
    if len(input_collection) == 0:
        return input_collection

    stack = Stack[T](capacity=len(input_collection))
    for item in input_collection:
        stack.push(item)

    if isinstance(input_collection, str):
        reversed: str = ""
        while not stack.is_empty():
            reversed += stack.pop()
        return reversed

    else:
        reversed: List[T] = []
        while not stack.is_empty():
            reversed.append(stack.pop())
        return reversed


if __name__ == "__main__":
    input_collection: List[int] = [11, 22, 33, 44, 55]
    reversed_collection: List[int] = reverse_collection(input_collection)

    print(f"Input collection:\n {input_collection}")
    print(f"Reversed collection:\n {reversed_collection}")

    input_collection: List[str] = ["DSA", "Python", "AI", "ML", "DL"]
    reversed_collection: List[str] = reverse_collection(input_collection)

    print(f"Input collection:\n {input_collection}")
    print(f"Reversed collection:\n {reversed_collection}")

    input_str: str = "Ramesh Neupane"
    reversed_str: str = reverse_collection(input_str)

    print(f"Input string: {input_str}")
    print(f"Reversed string: {reversed_str}")

    input_str: str = ""
    reversed_str: str = reverse_collection(input_str)

    print(f"Input string: {input_str}")
    print(f"Reversed string: {reversed_str}")
