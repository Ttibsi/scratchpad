from dataclasses import dataclass
from typing import Optional


@dataclass
class Node:
    value:Optional[int]
    next: Optional["Node"]


class Queue:
    def __init__(self):
        self.length: int = 0 
        self.head: Optional[Node] = None 
        self.tail: Optional[Node] = None

    def peek(self) -> Optional[int]:
        return self.head.value if self.head else None

    def deque(self) -> Optional[int]:
        if not self.head:
          return None 

        self.length -= 1

        #save the head
        head = self.head
        #update the head
        self.head = self.head.next
        
        return head.value

    def enqueue(self, item:int) -> None:
        self.length += 1
        n = Node(item, None)

        if self.tail:
            self.tail.next = n
            self.tail = n
        else:
            self.tail = self.head = n

    def items(self) -> list[int]:
        ret = []

        ptr = self.head
        if ptr.value is None:
            return ret

        while True:
            ret.append(ptr.value)
            if ptr == self.tail:
                break

            ptr = ptr.next

        return ret


def main() -> None:
    q = Queue()

    for i in range(0, 5):
        q.enqueue(i)

    print(q.items())
    print(q.peek())

    q.deque()
    print(q.items())

if __name__ == "__main__":
    main()
