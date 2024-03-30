from typing import Generic, TypeVar, List

T = TypeVar("T")


class StackUnderflowException(BaseException):
    pass


class StackOverflowException(BaseException):
    pass


class Stack(Generic[T]):
    """Stack data structure.

    Fields:
        stack: Store of the elements of the stack in a list. Default is an empty list.

    Methods:
        push(item): Add an item to the top of the stack.
        pop(): Remove and return the item at the top of the stack. Raises IndexError if the stack is empty.
        peek(): Return the item at the top of the stack without removing it. Returns None if the stack is empty.
    """

    def __init__(self, capacity=10):
        self.stack: List[T] = []
        self.__capacity = capacity
        self.__size = 0

    # get stack capacity
    @property
    def capacity(self) -> int:
        """Returns the capacity of the stack. Default is 10."""
        return self.__capacity

    # set new stack capacity
    @capacity.setter
    def capacity(self, value: int):
        """Sets the new capacity as passed in the 'value'.

        Args:
            value (int): The number that will be used as the new capacity. Must be greater than zero.

        Raises ValueError if the 'value' is not positive.
        """
        if isinstance(value, int) and value > 0:
            self.__capacity = value
        else:
            raise ValueError("Capacity must be a positive integer")

    # get stack size
    @property
    def size(self) -> int:
        """Retuns total items count in the stack."""
        return self.__size

    # check if the stack is full or not
    def is_full(self) -> bool:
        """Returns true if stack is reached to its capacity else false."""
        return self.__size == self.__capacity

    # Check if the stack is empty
    def is_empty(self) -> bool:
        """Returns true if the stack is empty else false."""
        return self.__size == 0

    # Add an element to the top of the stack
    def push(self, item: T) -> None:
        """Add item into the stack.
        Args:
            item (T): element to be added

        Raises OverflowError if there is no space left in the stack.
        """
        if self.is_full():
            raise StackOverflowException("Stack is Full!")
        else:
            self.stack.append(item)
            self.__size += 1

    # Remove an element from the top of the stack
    def pop(self) -> T:
        """Remove item from the top of stack.

        Returns:
            Item of type T.

        Raises IndexError if the stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowException("Stack is Empty!")
        else:
            removed_element = self.stack.pop()
            self.__size -= 1
            return removed_element

    # Return the top element without removing it
    def peek(self) -> T:
        """Return the element at the top of stack without removing it.
        Returns:
            Item of type T

        Raises IndexError if the stack is empty.
        """
        if self.is_empty():
            raise StackUnderflowException("Stack is empty")
        else:
            return self.stack[-1]

    # reset stack
    def clear(self):
        """Reset stack into initial state."""
        self.stack = []
        self.__size = 0


if __name__ == "__main__":
    s = Stack[str]()

    print("IsEmpty : ", s.is_empty())  # True
    print("Size    : ", s.size)  # 0
    try:
        s.push(5)  # Push operation
        s.push(7)
        print("Peek    : ", s.peek())  # Error, stack is empty
    except Exception as e:
        print(e)
    print("IsEmpty : ", s.is_empty())  # False
    print(f"Stack: {s.stack}, Type: {type(s.stack)}, type peek: {type(s.peek())}")
