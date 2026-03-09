"""
Sorting/Selection module used by Astrology AI.
Currently includes QuickSelect for top-k style ranking support.
"""

from __future__ import annotations

import logging
import time
from typing import Any, Dict, List

logger = logging.getLogger(__name__)


class QuickSelect:
    """QuickSelect algorithm for finding kth smallest element."""

    def __init__(self, data: List[int]):
        self.data = data.copy()
        self.comparisons = 0
        self.partitions = 0
        self.steps: List[Dict[str, Any]] = []

    def partition(self, arr: List[int], low: int, high: int) -> int:
        pivot = arr[high]
        i = low - 1

        self.steps.append(
            {
                "array": arr.copy(),
                "low": low,
                "high": high,
                "pivot": pivot,
                "message": f"Partitioning around pivot {pivot}",
            }
        )

        for j in range(low, high):
            self.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]

        arr[i + 1], arr[high] = arr[high], arr[i + 1]
        self.partitions += 1
        return i + 1

    def quick_select(self, arr: List[int], low: int, high: int, k: int) -> int:
        if low == high:
            return arr[low]

        pivot_index = self.partition(arr, low, high)

        if k == pivot_index:
            return arr[k]
        if k < pivot_index:
            return self.quick_select(arr, low, pivot_index - 1, k)
        return self.quick_select(arr, pivot_index + 1, high, k)

    def find_kth_smallest(self, k: int) -> Dict[str, Any]:
        """
        Find kth smallest element (1-indexed).
        Returns result + execution stats.
        """
        if k < 1 or k > len(self.data):
            return {"error": f"k must be between 1 and {len(self.data)}", "success": False}

        start_time = time.time()
        arr = self.data.copy()
        result = self.quick_select(arr, 0, len(arr) - 1, k - 1)
        execution_time = (time.time() - start_time) * 1000

        logger.info(
            "QuickSelect completed: k=%s, result=%s, %s comparisons, %s partitions, %.4fms",
            k,
            result,
            self.comparisons,
            self.partitions,
            execution_time,
        )

        return {
            "success": True,
            "kth_smallest": result,
            "k": k,
            "original_array": self.data,
            "steps": self.steps,
            "comparisons": self.comparisons,
            "partitions": self.partitions,
            "execution_time": round(execution_time, 4),
            "time_complexity": "O(n) average, O(n^2) worst",
            "space_complexity": "O(log n)",
        }
