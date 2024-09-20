import os
import sys

# add priority_queue into PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from HeapPriorityQueue import HeapPriorityQueue


def sort_using_heapq(l: list[tuple[int, object]]) -> list[tuple[int, object]]:
    """Sorts a list of tuples using the heap priority queue."""
    sorted: list[tuple[int, object]] = []
    heapq = HeapPriorityQueue(contents=l)
    print(heapq)
    for _ in range(len(heapq)):
        item = heapq.remove()
        # yield item
        sorted.append(item)
    return sorted


if __name__ == "__main__":
    # unsorted list
    unsorted_list = [
        (5, "apple"),
        (2, "banana"),
        (8, "mango"),
        (12, "orange"),
        (1, "avocado"),
        (100, "cherry"),
        (25, "papaya"),
    ]
    print(f"\nUnsored list: {unsorted_list}")

    sorted_list = sort_using_heapq(unsorted_list)
    print(f"\nSorted list: {sorted_list}")
    # for item in sort_using_heapq(unsorted_list):
    #     print(item)

    ###########################################################################

    # -------------------------------OUTPUT------------------------------------
    # Unsored list: [(5, 'apple'), (2, 'banana'), (8, 'mango'), (12, 'orange'), (1, 'avocado'), (100, 'cherry'), (25, 'papaya')]

    # Heap: [ (1, avocado), (2, banana), (8, mango), (12, orange), (5, apple), (100, cherry), (25, papaya) ]
    # size: 7

    # Sorted list: [(1, 'avocado'), (2, 'banana'), (5, 'apple'), (8, 'mango'), (12, 'orange'), (25, 'papaya'), (100, 'cherry')]

    ###########################################################################
