# Breadth first search
# Depth first search is on 10_binary_Tree
# This is usually O(n)

from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    left: Optional[Node]
    right: Optional[Node]

def bfs(head: Node, needle: int) -> bool:
    q = [head]

    while len(q):
        curr = q.pop(0)

        if curr.value == needle:
            return True

        if curr.left:
            q.push(curr.left)

        if curr.right:
            q.push(curr.right)

    return False
