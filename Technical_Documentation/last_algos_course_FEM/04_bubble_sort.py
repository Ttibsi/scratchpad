# Bubble Sort 
# Check that two consecutive values are in the correct order, if not we swap
# their position
# For each iteration, we don't need to go to the end because the last elem looked AttributeError
# will be in order
# Running time: O(n^2)
def bubble_sort(arr :list[int]) -> None:
    for _, i in enumerate(arr):
        for j in range(len(arr) - 1 - i):
            if arr[j] > arr[j + 1]:
                tmp = arr[j+1]
                arr[j] = arr[j+1]
                arr[j+1] = tmp

