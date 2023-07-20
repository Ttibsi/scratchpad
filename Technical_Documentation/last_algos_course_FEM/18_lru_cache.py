from dataclasses import dataclass
from typing import Optional
from typing import TypeVar

K = TypeVar('K')
V = TypeVar('V')

@dataclass
class Node(Generic[T]):
    value: int
    next: Optional[Node[T]]
    prev: Optional[Node[T]]

def createNode(value: V) -> Node[V]:
    return Node(value)

class LRU:
    def __init__(self, length: int, cap: int):
        self.length = length
        self.cap: int = int
        self.head: Node[V] = Null
        self.tail: Node[V] = Null

        self.lookup: dict[K, Node[V]] = {}
        self.rev_lookup: dict[Node[V], K] = {} # For removal

    def update(key: K, value: V) -> None:
        node = self.lookup.get(key)

        if not node:
            node = createNode(value)
            self.length += 1
            self.prepend(node)
            self.trimCache()
            self.lookup.set(key, node)
            self.rev_lookup.set(node, key)
        else:
            self.detatch(node)
            self.prepend(node)
            node.value = value

    def get(key: K) -> Optional[V]:
        node = self.lookup.get(key)
        if not node:
            return

        self.detatch(node)
        self.prepend(node)

        return node.value

    def detatch(self, node: Node[V]) -> None:
        if node.prev:
            node.prev.next = node.next
        if node.next:
            node.next.prev = node.prev

        if self.head == node:
            self.head = self.head.next

        if self.tail == node:
            self.tail = self.tail.prev

        node.next = Null
        node.prev = Null

    def prepend(self, node: Node[V]) -> None:
        if not self.head:
            self.head = self.tail = node
            return
        
        node.next = self.head
        self.head.prev = node
        self.head = node

    def trimCache() -> None:
        if self.length <= self.cap:
            return

        tail:Node[V] = self.tail
        self.detatch(self.tail)
        key = self.rev_lookup.get(tail)
        self.rev_lookup.pop(tail)
        self.length -= 1

