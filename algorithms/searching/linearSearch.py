from typing import TypeVar, List

T = TypeVar("T")


def linear_search(array: List[T], key: T) -> int:
    """Search sequentially whole array against key.
    Returns index of array if key is found in the array else returns -1.

    Note: List need not to be sorted.

    Time complexity: O(n)

    Args:
        array (List[T]): The list to be searched.
        key (T): Element to search for in the list.

    Returns:
        int: Index of element if it's present in the list, otherwise -1.
    """
    index = -1
    for i in range(len(array)):
        if key == array[i]:
            index = i
            break
    return index


if __name__ == "__main__":
    arr: List[int] = [23, 45, 67, 89, 101, 123]
    print(linear_search(arr, 123))  # Output: 5
    print(linear_search(arr, 99))  # Output: -1
