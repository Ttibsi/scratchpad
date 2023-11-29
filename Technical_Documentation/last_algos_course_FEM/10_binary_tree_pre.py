from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    left: Optional[Node]
    right: Optional[Node]


def walk(curr: Optional[Node], path: list[int]) -> list[int]:
    if not curr:
        return path

    path.append(curr.value) # pre-order
    walk(curr.left, path)
    #path.append(curr.value) # in-order
    walk(curr.right, path)
    #path.append(curr.value) # post-order

    return path

def pre_order(head: Node) -> list[int]:
    return walk(head, [])
