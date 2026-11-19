"""
Quick Sort Implementation

Quick sort is a divide and conquer algorithm. It picks an element as pivot
and partitions the given array around the picked pivot. There are many
different versions of quickSort that pick pivot in different ways:
    1. Always pick first element as pivot.
    2. Always pick last element as pivot (implemented below).
    3. Pick a random element as pivot.
    4. Pick median as pivot.

Time Complexity:
    Best Case:   O(n log n)
    Average:     O(n log n)
    Worst Case:  O(n^2)  (when array is already sorted and pivot is last/first)

Space Complexity: O(log n) auxiliary (recursion stack)
"""


def partition(arr, low, high):
    """
    Partition the array using the last element as pivot.
    Places the pivot element at its correct position in sorted array,
    and places all smaller elements to left of pivot and all greater
    elements to right of pivot.
    """
    pivot = arr[high]
    i = low - 1  # Index of smaller element
    for j in range(low, high):
        if arr[j] <= pivot:
            i = i + 1
            arr[i], arr[j] = arr[j], arr[i]
    arr[i + 1], arr[high] = arr[high], arr[i + 1]
    return i + 1


def quick_sort_helper(arr, low, high):
    if low < high:
        # pi is partitioning index
        pi = partition(arr, low, high)
        # Recursively sort elements before and after partition
        quick_sort_helper(arr, low, pi - 1)
        quick_sort_helper(arr, pi + 1, high)


def quick_sort(arr):
    """
    Sort a list in ascending order using quick sort.

    Args:
        arr (list): List of comparable items.

    Returns:
        list: The sorted list (same object as input).
    """
    quick_sort_helper(arr, 0, len(arr) - 1)
    return arr


if __name__ == "__main__":
    sample = [10, 7, 8, 9, 1, 5]
    print("Original array:", sample)
    quick_sort(sample)
    print("Sorted array:  ", sample)
