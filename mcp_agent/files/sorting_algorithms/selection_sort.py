"""
Selection Sort Implementation

Selection sort divides the input list into two parts: a sorted sublist of
items which is built up from left to right at the front (left) of the list,
and a sublist of the remaining unsorted items. The algorithm proceeds by
finding the smallest (or largest, depending on ordering) element in the
unsorted sublist, swapping it with the leftmost unsorted element, and
moving the sublist boundaries one element to the right.

Time Complexity:
    Best Case:   O(n^2)
    Average:     O(n^2)
    Worst Case:  O(n^2)

Space Complexity: O(1) auxiliary (in-place sorting)
"""


def selection_sort(arr):
    """
    Sort a list in ascending order using selection sort.

    Args:
        arr (list): List of comparable items.

    Returns:
        list: The sorted list (same object as input).
    """
    n = len(arr)
    # One by one move boundary of unsorted subarray
    for i in range(n - 1):
        # Find the minimum element in remaining unsorted array
        min_idx = i
        for j in range(i + 1, n):
            if arr[j] < arr[min_idx]:
                min_idx = j
        # Swap the found minimum element with the first element
        arr[i], arr[min_idx] = arr[min_idx], arr[i]
    return arr


if __name__ == "__main__":
    sample = [64, 25, 12, 22, 11]
    print("Original array:", sample)
    selection_sort(sample)
    print("Sorted array:  ", sample)
