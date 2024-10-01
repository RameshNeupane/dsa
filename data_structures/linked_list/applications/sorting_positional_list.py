import os
import sys
import random
from typing import TypeVar

T = TypeVar("T")

# add parent dir into the PYTHONPATH
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)  # append linked_list dir
from PositionalList import PositionalList


# sort nodes in positional list using insertion sort in ascending order
def insertion_sort_pl(pl: PositionalList[T]) -> PositionalList[T]:
    """Sort Positional linked list using insertion sort in ascending order.

    Args:
        pl (PositionalList[T]): Positional linked list to be sorted.

    Returns:
        (PositionalList[T]): Sorted Positional linked list.
    """
    if len(pl) > 1:
        marker = pl.first()
        while marker != pl.last():
            pivot = pl.after(marker)
            value_at_pivot = pivot.item()
            if value_at_pivot > marker.item():
                marker = pivot
            else:
                walk = marker
                while walk != pl.first() and pl.before(walk).item() > value_at_pivot:
                    walk = pl.before(walk)
                pl.add_before(walk, value_at_pivot)
                pl.delete(pivot)

    return pl


if __name__ == "__main__":
    pl = PositionalList[int]()

    for i in range(10):
        random_num = random.randint(0, 100)
        if random_num % 2 == 0:
            pl.add_last(random_num)
        else:
            pl.add_first(random_num)
    print(f"Unsorted List: {pl}")

    sorted_pl = insertion_sort_pl(pl)
    print(f"Sorted List: {sorted_pl}")

    ################################################################################

    # ----------------------------------OUTPUT--------------------------------------

    # Unsorted List:
    # header -><- 57 -><- 55 -><- 70 -><- 48 -><- 52 -><- 28 -><- 18 -><- 60 -><- 44 -><- 8 -><- trailer
    # Size: 10

    # Sorted List:
    # header -><- 8 -><- 18 -><- 28 -><- 44 -><- 48 -><- 52 -><- 55 -><- 57 -><- 60 -><- 70 -><- trailer
    # Size: 10

    ################################################################################
