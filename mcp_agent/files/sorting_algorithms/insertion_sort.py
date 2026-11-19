"""
Insertion Sort Implementation

Insertion sort iterates, consuming one input element each repetition, and
growing a sorted output list. At each iteration, insertion sort removes one
element from the input data, finds the location it belongs within the sorted
list, and inserts it there. It repeats until no input elements remain.

Time Complexity:
    Best Case:   O(n)  (already sorted)
    Average:     O(n^2)
    Worst Case:  O(n^2)

Space Complexity: O(1) auxiliary (in-place sorting)
"""


def insertion_sort(arr):
    """
    Sort a list in ascending order using insertion sort.

    Args:
        arr (list): List of comparable items.

    Returns:
        list: The sorted list (same object as input).
    """
    # Traverse through 1 to len(arr)
    for i in range(1, len(arr)):
        key = arr[i]
        # Move elements of arr[0..i-1], that are greater than key,
        # to one position ahead of their current position
        j = i - 1
        while j >= 0 and key < arr[j]:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


if __name__ == "__main__":
    sample = [12, 11, 13, 5, 6]
    print("Original array:", sample)
    insertion_sort(sample)
    print("Sorted array:  ", sample)
