"""
Heap Sort Implementation

Heap sort is a comparison-based sorting technique based on Binary Heap data
structure. It is similar to selection sort where we first find the maximum
element and place the maximum element at the end. We repeat the same process
for the remaining elements.

Time Complexity:
    Best Case:   O(n log n)
    Average:     O(n log n)
    Worst Case:  O(n log n)

Space Complexity: O(1) auxiliary (in-place sorting)
"""


def heapify(arr, n, i):
    """
    To heapify a subtree rooted with node i which is an index in arr[].
    n is size of heap.
    """
    largest = i  # Initialize largest as root
    left = 2 * i + 1     # left = 2*i + 1
    right = 2 * i + 2    # right = 2*i + 2

    # See if left child of root exists and is greater than root
    if left < n and arr[left] > arr[largest]:
        largest = left

    # See if right child of root exists and is greater than root
    if right < n and arr[right] > arr[largest]:
        largest = right

    # Change root, if needed
    if largest != i:
        arr[i], arr[largest] = arr[largest], arr[i]  # swap
        # Heapify the root.
        heapify(arr, n, largest)


def heap_sort(arr):
    """
    Sort a list in ascending order using heap sort.

    Args:
        arr (list): List of comparable items.

    Returns:
        list: The sorted list (same object as input).
    """
    n = len(arr)

    # Build a maxheap.
    # Since last parent will be at ((n // 2) - 1), we can start at that location.
    for i in range(n // 2 - 1, -1, -1):
        heapify(arr, n, i)

    # One by one extract elements
    for i in range(n - 1, 0, -1):
        arr[i], arr[0] = arr[0], arr[i]  # swap
        heapify(arr, i, 0)

    return arr


if __name__ == "__main__":
    sample = [12, 11, 13, 5, 6, 7]
    print("Original array:", sample)
    heap_sort(sample)
    print("Sorted array:  ", sample)
