# Quick sort 
# Either O(n log n) or O(n^2) depending on the input data


# Perform the sort
def qs(arr: list[int], lo: int, hi: int) -> None:
    if lo >= hi:
        # Stopped needing to recurse here
        return

    pivotIdx = partition(arr, lo, hi)
    qs(arr, pivotIdx + 1, hi)

# Do all the swaps and move the partition point
def partition(arr: list[int], lo: int, hi: int) -> int:
    pivot = arr[hi]
    idx = lo - 1

    # Move every item in the list less than the pivot to being below it
    for i in range(hi):
        if arr[i] <= pivot:
            idx += 1
            tmp = arr[i]
            arr[i] = arr[idx]
            arr[idx] = tmp

    idx += 1
    arr[hi] = arr[idx]
    arr[idx] = pivot

    return idx

def solve(arr: list[int]) -> None:
    qs(arr, 0, len(arr) - 1)


