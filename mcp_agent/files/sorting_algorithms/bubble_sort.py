"""
Bubble Sort Implementation

Bubble sort repeatedly steps through the list, compares adjacent elements,
and swaps them if they are in the wrong order. The pass through the list
is repeated until no swaps are needed, meaning the list is sorted.

Time Complexity:
    Best Case:   O(n)  (already sorted, with early exit optimization)
    Average:     O(n^2)
    Worst Case:  O(n^2)

Space Complexity: O(1) auxiliary (in-place sorting)
"""


def bubble_sort(arr):
    """
    Sort a list in ascending order using bubble sort.

    Args:
        arr (list): List of comparable items.

    Returns:
        list: The sorted list (same object as input).
    """
    n = len(arr)
    # Traverse through all array elements
    for i in range(n):
        # Track whether a swap happened; if none, the list is already sorted
        swapped = False
        # Last i elements are already in place
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swapped = True
        # If no two elements were swapped by inner loop, break
        if not swapped:
            break
    return arr


if __name__ == "__main__":
    sample = [64, 34, 25, 12, 22, 11, 90]
    print("Original array:", sample)
    bubble_sort(sample)
    print("Sorted array:  ", sample)
