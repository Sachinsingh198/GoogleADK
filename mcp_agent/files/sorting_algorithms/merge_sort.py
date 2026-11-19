"""
Merge Sort Implementation

Merge sort is a divide and conquer algorithm. It divides the input array
into two halves, calls itself for the two halves, and then merges the two
sorted halves. The merge() function is used for merging two halves.

Time Complexity:
    Best Case:   O(n log n)
    Average:     O(n log n)
    Worst Case:  O(n log n)

Space Complexity: O(n) auxiliary
"""


def merge_sort(arr):
    """
    Sort a list in ascending order using merge sort.

    Args:
        arr (list): List of comparable items.

    Returns:
        list: A new sorted list.
    """
    if len(arr) > 1:
        mid = len(arr) // 2  # Finding the mid of the array
        left_half = arr[:mid]  # Dividing the array elements
        right_half = arr[mid:]

        # Recursively sort both halves
        merge_sort(left_half)
        merge_sort(right_half)

        i = j = k = 0

        # Copy data to temp arrays left_half[] and right_half[]
        while i < len(left_half) and j < len(right_half):
            if left_half[i] < right_half[j]:
                arr[k] = left_half[i]
                i += 1
            else:
                arr[k] = right_half[j]
                j += 1
            k += 1

        # Checking if any element was left
        while i < len(left_half):
            arr[k] = left_half[i]
            i += 1
            k += 1

        while j < len(right_half):
            arr[k] = right_half[j]
            j += 1
            k += 1

    return arr


if __name__ == "__main__":
    sample = [38, 27, 43, 3, 9, 82, 10]
    print("Original array:", sample)
    merge_sort(sample)
    print("Sorted array:  ", sample)
