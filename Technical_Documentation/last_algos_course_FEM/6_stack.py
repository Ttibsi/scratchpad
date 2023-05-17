from dataclasses import dataclass

@dataclass
class Node:
    value:int
    prev:Node | None


class Stack():
    def __init__(self, head: Node):
        self.length = 0
        self.head = head


    def push(self, item: int) -> None:
        n = Node(item)
        self.length += 1

        if not self.head:
            self.head = n
            return

        n.prev = self.head
        self.head = n


    def pop(self) -> int | None:
        self.length = max(0, self.length - 1)
        if self.length == 0:
            head = self.head
            self.head = None
            return head.value

        self.head = self.head.prev
        return self.head.value


    def peek(self) -> int | None:
        if self.head:
            return self.head.value
        else:
            return None


