from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value:Optional[int]
    prev: Optional["Node"]


class Stack():
    def __init__(self):
        self.length:int = 0
        self.head:Optional[Node] = None

    def peek(self) -> Optional[int]:
        return self.head.value if self.head else None

    def push(self, item: int) -> None:
        n = Node(item, None)
        self.length += 1

        if self.head:
            n.prev = self.head

        self.head = n

    def pop(self) -> Optional[int]:
        # Can't have negative length
        self.length = max(0, self.length - 1)

        if self.length == 0:
            head = self.head
            self.head = None
            return head.value

        self.head = self.head.prev
        return self.head.value

    def items(self) -> list[int]:
        ret = []
        ptr = self.head
        if ptr.value is None:
            return ret

        while True:
            ret.append(ptr.value)
            if not ptr.prev: 
                break

            ptr = ptr.prev

        return ret


def main() -> None:
    s = Stack()

    for i in range(0, 5):
        s.push(i)

    print(s.items())
    print(s.peek())

    s.pop()
    print(s.items())


if __name__ == "__main__":
    main()
