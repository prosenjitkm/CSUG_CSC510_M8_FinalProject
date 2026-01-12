"""
Queue Data Structure Implementation
FIFO (First In First Out)
"""
from typing import Any, List, Dict
from collections import deque
import time


class Queue:
    """Queue implementation using Python deque for O(1) operations"""

    def __init__(self):
        self._items = deque()
        self.operation_count = 0

    def enqueue(self, item: Any) -> Dict[str, Any]:
        """Add item to rear of queue"""
        start_time = time.time()
        self._items.append(item)
        self.operation_count += 1
        end_time = time.time()

        return {
            'operation': 'enqueue',
            'item': item,
            'queue': list(self._items),
            'size': len(self._items),
            'execution_time': round((end_time - start_time) * 1000, 4)
        }

    def dequeue(self) -> Dict[str, Any]:
        """Remove and return item from front of queue"""
        start_time = time.time()
        if self.is_empty():
            return {
                'operation': 'dequeue',
                'error': 'Queue is empty',
                'success': False
            }

        item = self._items.popleft()
        self.operation_count += 1
        end_time = time.time()

        return {
            'operation': 'dequeue',
            'item': item,
            'queue': list(self._items),
            'size': len(self._items),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': True
        }

    def peek(self) -> Dict[str, Any]:
        """View front item without removing it"""
        if self.is_empty():
            return {
                'operation': 'peek',
                'error': 'Queue is empty',
                'success': False
            }

        return {
            'operation': 'peek',
            'item': self._items[0],
            'queue': list(self._items),
            'size': len(self._items),
            'success': True
        }

    def is_empty(self) -> bool:
        """Check if queue is empty"""
        return len(self._items) == 0

    def size(self) -> int:
        """Return size of queue"""
        return len(self._items)

    def clear(self) -> Dict[str, Any]:
        """Clear all items from queue"""
        self._items.clear()
        return {
            'operation': 'clear',
            'queue': [],
            'size': 0,
            'success': True
        }

    def get_all(self) -> List[Any]:
        """Get all items in queue"""
        return list(self._items)

    def to_dict(self) -> Dict[str, Any]:
        """Convert queue to dictionary representation"""
        return {
            'items': list(self._items),
            'size': len(self._items),
            'is_empty': self.is_empty(),
            'front': self._items[0] if not self.is_empty() else None,
            'rear': self._items[-1] if not self.is_empty() else None
        }

