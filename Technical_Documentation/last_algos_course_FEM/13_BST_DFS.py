# Binary search tree Depth first search
from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    left: Optional[Node]
    right: Optional[Node]


def search(curr:Optional[Node], needle:int) -> bool:
    if not curr:
        return False

    if curr.value == needle:
        return True

    if curr.value < needle:
        return search(curr.right, needle)
    else: 
        return search(curr.left, needle)


def dfs(head: Node, needle: int) -> bool:
    return search(head, needle)
