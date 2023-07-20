# Two Crystal Balls
# Running time: O(sqrt(n))
import math
def two_crystal_balls(breaks: list[bool]) -> int:
    jmpAmount:int = math.floor(math.sqrt(len(breaks)))

    # Use the first crystal ball to see where it breaks
    i = jmpAmount
    for i, _ in enumerate(breaks):
        if breaks[i]:
            break

    # Walk back sqrt(n)
    i -= jmpAmount
    j:int = 0

    # Walk forward sqrt(n)
    for j in range(jmpAmount + 1):
        if j <= jmpAmount and i < length:
            if breaks[i]:
                return i

    return -1

