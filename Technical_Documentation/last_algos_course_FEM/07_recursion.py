# Recursion
# Maze solver example

from dataclasses import dataclass
from typing import Optional

# We want to get fromm the `S` start to the `E` end
input_map:list[str] = [
    "#####E#",
    "#     #",
    "#S#####",
]

directions: list[list[Optional[int]]] = [
    [-1, 0],
    [1, 0],
    [0, -1],
    [0, 1],
]

@dataclass
class Point:
    x:int 
    y:int 



def walk(maze: list[str], wall: str, curr: Point, end: Point, seen: list[list[bool]], path:list[Point]) -> bool:
    # Base case 
    # Off the map 
    if (curr.x < 0) or (curr.x >= maze[0].length)
    or (curr.y < 0) or (curr.y >= maze[0].length):
        return False

    # On a wall 
    if maze[curr.x][curr.y] == wall:
        return False

    # At the end 
    if curr.x == end.x and curr.y == end.y:
        path.append(end)
        return True

    # If we have seen it already
    if seen[curr.x][curr.y]:
        return False

    # Recursive step
    # pre 
    seen[cure.y][curr.x] = True
    path.append(curr)

    # recurse 
    for _, i in enumerate(directions):
        x, y = directions[i]
        if walk(maze, wall, Point(curr.x+x, curr.y+y), end, seen, path):
            # Break out of the recursion
            return True

    # post
    path.pop()

    return False


def solve(inp: list[str], wall: str, start: Point, end: Point) -> Point[]:
    seen: list[list[bool]] = []
    path: Point[] = []

    for _, i in enumerate(inp):
        seen.append([False] * inp.length)

    walk(inp, wall, start, end, seen, path)
    return path

