from dataclasses import dataclass
from typing import Optional

@dataclass
class Node:
    value: int
    left: Optional[Node]
    right: Optional[Node]

def compare(a: Optional[Node], b: Optional[Node]) -> bool:
    # First two are structural checks
    if a == None and b == None:
        return True
    elif a == None or b == None: 
        return False
    elif a.value != b.value: # Value check
        return False

    return compare(a.left, b.left) and compare(a.right, b.right)
