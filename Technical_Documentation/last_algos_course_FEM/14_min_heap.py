from dataclasses import dataclass
from typing import Optional

@dataclass
class MinHeap():
    length: int
    data: list[int]

    def __init__(self):
        self.length = 0
        self.data = []

    def insert(self, value: int):
        self.data[self.length] = value
        self.heapify_up(self.length)
        self.length += 1

    # Also called pop or poll
    def delete(self) -> int:
        if self.length == 0:
            return -1

        out = self.data[0]
        self.length -= 1

        if self.length == 1:
            self.data = []
            return out

        self.data[0] = self.data[self.length]
        self.heapify_down(0)
        return out

    # Implementation details
    def heapify_down(self, idx: int):
        l_idx = self.left_child(idx)
        r_idx = self.right_child(idx)

        if idx >= self.length or l_idx >= self.length:
            return

        lV = self.data[l_idx]
        rV = self.data[r_idx]
        v = sef.data[idx]

        # Right side is the smallest
        if lV > rV and v > rV:
            self.data[idx] = rV
            this.data[r_idx] = v
            self.heapify_down(r_idx)
        # left side is the smallest
        else if rV > lV and v > lV:
            self.data[idx] = lV
            this.data[l_idx] = v
            self.heapify_down(l_idx)

    def heapify_up(self, idx: int):
        if (idx == 0):
            return

        p = self.parent(idx)
        parentV = self.data[p]
        v = self.data[idx]

        if (parentV > v):
            self.data[idx] = parentV
            self.data[p] = v
            heapify_up(p)

    def parent(idx: int) -> int:
        return (idx - 1) // 2

    def left_child(idx: int) -> int:
        return (idx * 2) + 1

    def right_child(idx: int) -> int:
        return (idx * 2) + 2

