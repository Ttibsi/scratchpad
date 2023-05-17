from dataclasses import dataclass

@dataclass
class Node:
    value:int
    next:Node


class Queue:
    def __init__(self, length, head, tail):
        self.length = 0 
        self.head = head
        self.tail = tail

    def peek(self) -> int:
        return self.head.value

    def deque(self) -> int | None:
        if not self.head:
            return None 

        self.length -= 1

        #save the head
        head = self.head
        #update the head
        self.head = self.head.next
        
        return head.value

    # I don't think this is exactly right
    def enqueue(self, item:int) -> None:
        self.length  += 1
        n = Node(value=item)

        if not self.tail:
            self.tail = self.head = n

        self.tail.next = n
        self.tail = n


