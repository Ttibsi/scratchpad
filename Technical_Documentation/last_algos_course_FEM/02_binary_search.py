# Binary Search
# Jumping halfway in a sorted array to check if the data has been jumped or not
# Running time: O(logn)
    # Because we're halving the space at each run
import math
def binary_search(haystack: list[int], needle: int) -> bool:
    low = 0;
    high = len(haystack)

    while(low < high):
        mid = math.floor(low + (high - low) / 2) # Divide by 2 so that you get the middle
        value = haystack[mid]

        if value == needle:
            return True
        elif value > needle: # Reduce the higher side to the pointer and exclude midpoint
            high = mid
        elif value < mid:
            # Value is less than where the pointer is - search the higher side
            # + 1 because we don't need to look at the old midpoint again
            low = mid + 1

    return False


