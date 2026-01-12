"""
Stack Data Structure Implementation
LIFO (Last In First Out)
"""
from typing import Any, List, Dict
import time


class Stack:
    """Stack implementation using Python list"""

    def __init__(self):
        self._items = []
        self.operation_count = 0

    def push(self, item: Any) -> Dict[str, Any]:
        """Push item onto stack"""
        start_time = time.time()
        self._items.append(item)
        self.operation_count += 1
        end_time = time.time()

        return {
            'operation': 'push',
            'item': item,
            'stack': self._items.copy(),
            'size': len(self._items),
            'execution_time': round((end_time - start_time) * 1000, 4)
        }

    def pop(self) -> Dict[str, Any]:
        """Pop item from stack"""
        start_time = time.time()
        if self.is_empty():
            return {
                'operation': 'pop',
                'error': 'Stack is empty',
                'success': False
            }

        item = self._items.pop()
        self.operation_count += 1
        end_time = time.time()

        return {
            'operation': 'pop',
            'item': item,
            'stack': self._items.copy(),
            'size': len(self._items),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': True
        }

    def peek(self) -> Dict[str, Any]:
        """View top item without removing it"""
        if self.is_empty():
            return {
                'operation': 'peek',
                'error': 'Stack is empty',
                'success': False
            }

        return {
            'operation': 'peek',
            'item': self._items[-1],
            'stack': self._items.copy(),
            'size': len(self._items),
            'success': True
        }

    def is_empty(self) -> bool:
        """Check if stack is empty"""
        return len(self._items) == 0

    def size(self) -> int:
        """Return size of stack"""
        return len(self._items)

    def clear(self) -> Dict[str, Any]:
        """Clear all items from stack"""
        self._items.clear()
        return {
            'operation': 'clear',
            'stack': [],
            'size': 0,
            'success': True
        }

    def get_all(self) -> List[Any]:
        """Get all items in stack"""
        return self._items.copy()

    def to_dict(self) -> Dict[str, Any]:
        """Convert stack to dictionary representation"""
        return {
            'items': self._items.copy(),
            'size': len(self._items),
            'is_empty': self.is_empty(),
            'top': self._items[-1] if not self.is_empty() else None
        }

