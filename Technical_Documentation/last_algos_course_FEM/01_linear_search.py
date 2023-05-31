# Find the needle number in the haystack array
# This implements linear search, the most basic algorithm
# This is the same as the kind of function that an array `getIndex()` method would implement 
# Running time: O(n)
def linear_search(haystack: list[int], needle: int) -> bool:
    for elem in haystack:
        if elem == needle:
            return True

    return False

