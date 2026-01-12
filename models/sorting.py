"""
Sorting Algorithms Module
Contains Bubble Sort with visualization and QuickSelect implementation
"""
import time
import logging
from typing import List, Dict, Any

logger = logging.getLogger(__name__)


class BubbleSort:
    """Bubble Sort implementation with step-by-step visualization tracking"""

    def __init__(self, data: List[int]):
        self.data = data.copy()
        self.steps = []
        self.comparisons = 0
        self.swaps = 0

    def sort(self) -> Dict[str, Any]:
        """
        Sort the data using bubble sort algorithm and track all steps
        Returns: Dictionary with sorted array, steps, and statistics
        """
        arr = self.data.copy()
        n = len(arr)
        start_time = time.time()

        # Initial state
        self.steps.append({
            'step': 0,
            'array': arr.copy(),
            'comparing': [],
            'swapped': False,
            'message': 'Initial array'
        })

        step_count = 1
        for i in range(n):
            swapped = False
            for j in range(0, n - i - 1):
                self.comparisons += 1

                # Record comparison
                self.steps.append({
                    'step': step_count,
                    'array': arr.copy(),
                    'comparing': [j, j + 1],
                    'swapped': False,
                    'message': f'Comparing {arr[j]} and {arr[j + 1]}'
                })
                step_count += 1

                if arr[j] > arr[j + 1]:
                    # Swap elements
                    arr[j], arr[j + 1] = arr[j + 1], arr[j]
                    self.swaps += 1
                    swapped = True

                    # Record swap
                    self.steps.append({
                        'step': step_count,
                        'array': arr.copy(),
                        'comparing': [j, j + 1],
                        'swapped': True,
                        'message': f'Swapped {arr[j + 1]} and {arr[j]}'
                    })
                    step_count += 1

            # If no swaps occurred, array is sorted
            if not swapped:
                self.steps.append({
                    'step': step_count,
                    'array': arr.copy(),
                    'comparing': [],
                    'swapped': False,
                    'message': 'Array is sorted!'
                })
                break

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000  # Convert to milliseconds

        return {
            'sorted_array': arr,
            'steps': self.steps,
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'execution_time': round(execution_time, 4),
            'time_complexity': 'O(n²)',
            'space_complexity': 'O(1)'
        }


class QuickSelect:
    """QuickSelect algorithm for finding kth smallest element"""

    def __init__(self, data: List[int]):
        self.data = data.copy()
        self.comparisons = 0
        self.partitions = 0
        self.steps = []

    def partition(self, arr: List[int], low: int, high: int) -> int:
        """Partition the array around pivot"""
        pivot = arr[high]
        i = low - 1

        self.steps.append({
            'array': arr.copy(),
            'low': low,
            'high': high,
            'pivot': pivot,
            'message': f'Partitioning around pivot {pivot}'
        })

        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.partitions += 1

        return i + 1

    def quick_select(self, arr: List[int], low: int, high: int, k: int) -> int:
        """
        Find kth smallest element using quickselect
        k is 0-indexed (k=0 means smallest element)
        """
        if low == high:
            return arr[low]

        pivot_index = self.partition(arr, low, high)

        if k == pivot_index:
            return arr[k]
        elif k < pivot_index:
            return self.quick_select(arr, low, pivot_index - 1, k)
        else:
            return self.quick_select(arr, pivot_index + 1, high, k)

    def find_kth_smallest(self, k: int) -> Dict[str, Any]:
        """
        Find kth smallest element (1-indexed)
        Returns: Dictionary with result and statistics
        """
        if k < 1 or k > len(self.data):
            return {
                'error': f'k must be between 1 and {len(self.data)}',
                'success': False
            }

        start_time = time.time()
        arr = self.data.copy()

        # Convert to 0-indexed
        result = self.quick_select(arr, 0, len(arr) - 1, k - 1)

        end_time = time.time()
        execution_time = (end_time - start_time) * 1000

        logger.info(f"QuickSelect completed: k={k}, result={result}, {self.comparisons} comparisons, {self.partitions} partitions, {round(execution_time, 4)}ms")

        return {
            'success': True,
            'kth_smallest': result,
            'k': k,
            'original_array': self.data,
            'steps': self.steps,
            'comparisons': self.comparisons,
            'partitions': self.partitions,
            'execution_time': round(execution_time, 4),
            'time_complexity': 'O(n) average, O(n²) worst',
            'space_complexity': 'O(log n)'
        }

