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
         not self.head:
          return None 

        self.length -= 1

        #save the head
        head = self.head
        #update the head
        self.head = self.head.next
        
        return head.value

    def enqueue(self, item:int) -> None:
        self.length += 1
        n = Node(value=item)

        if self.tail:
            self.tail.next = n
            self.tail = n
        else:
            self.tail = self.head = n

