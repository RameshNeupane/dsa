from typing import TypeVar, List

T = TypeVar("T")


def binary_search(array: List[T], key: T, low: int, high: int) -> int:
    """Binary searching.

    Calculates middle index of list and compare key against value at middle index of array.
    If key is found at middle index, then returns middle index.
    If key is smaller than the value at middle index, searches key against array left to middle index.
    If key is greater than the value at middle index, searches key against array right to middle index.
    If key is not found, then returns -1.

    Note: Array need to be sorted.

    Time complexity: O(log(n))

    Args:
        array (List[T]): The sorted list to be searched.
        key (T): Element to be search for in the list.
        low (int): Lower (start) index of the list.
        high (int): Higher (end) index of the list.

    Returns:
        (int): Index of the key element if present in the list, otherwise -1.
    """
    if low > high:
        return -1
    mid: int = (high + low + 1) // 2
    print(f"mid: {mid}")
    if key == array[mid]:
        return mid
    elif key < array[mid]:
        return binary_search(array, key, low, mid - 1)
    else:
        return binary_search(array, key, mid + 1, high)


if __name__ == "__main__":
    arr: List[int] = [1, 3, 5, 7, 9, 11, 13, 15]
    print(binary_search(arr, 9, 0, len(arr) - 1))
    print(binary_search(arr, 1, 0, len(arr) - 1))
    print(binary_search(arr, 15, 0, len(arr) - 1))
    print(binary_search(arr, 19, 0, len(arr) - 1))
