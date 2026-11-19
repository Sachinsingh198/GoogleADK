"""
Sorting Algorithms Demo

Run this file to see all sorting algorithms in action and compare their outputs.
"""

import random
from bubble_sort import bubble_sort
from selection_sort import selection_sort
from insertion_sort import insertion_sort
from merge_sort import merge_sort
from quick_sort import quick_sort
from heap_sort import heap_sort


def test_sort(sort_func, arr, name):
    """Test a sorting function and print results."""
    test_arr = arr.copy()
    sort_func(test_arr)
    print(f"{name:15} -> {test_arr}")
    return test_arr


def main():
    # Test arrays
    test_cases = [
        [64, 34, 25, 12, 22, 11, 90],
        [5, 1, 4, 2, 8],
        [1],
        [],
        [3, 3, 3, 3],
        [9, 8, 7, 6, 5, 4, 3, 2, 1],
        [1, 2, 3, 4, 5, 6, 7, 8, 9],
    ]

    algorithms = [
        (bubble_sort, "Bubble Sort"),
        (selection_sort, "Selection Sort"),
        (insertion_sort, "Insertion Sort"),
        (merge_sort, "Merge Sort"),
        (quick_sort, "Quick Sort"),
        (heap_sort, "Heap Sort"),
    ]

    for i, arr in enumerate(test_cases):
        print(f"\n=== Test Case {i + 1}: {arr} ===")
        for func, name in algorithms:
            test_sort(func, arr, name)


if __name__ == "__main__":
    main()