from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    value:Optional[int]
    prev: Optional["Node"]

class Stack():
    def __init__(self, head: Node):
        self.length:int = 0
        self.head:Optional[Node] = None


    def peek(self) -> Optional[int]:
        return self.head.value if self.head else None


    def push(self, item: int) -> None:
        n = Node(value=item)
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

