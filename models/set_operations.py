"""
Set Operations Module
Comprehensive Set class with all set operations
"""
import logging
from typing import Set as PythonSet, List, Dict, Any
import time

logger = logging.getLogger(__name__)


class Set:
    """
    Custom Set implementation supporting:
    - Union
    - Intersection
    - Difference
    - Symmetric Difference
    - Add/Remove operations
    """

    def __init__(self, elements: List[Any] = None):
        """Initialize set with optional list of elements"""
        self._elements = set()
        if elements:
            for element in elements:
                self._elements.add(element)
        self.operation_count = 0
        logger.debug(f"Set initialized with {len(self._elements)} unique elements")

    def add(self, element: Any) -> bool:
        """Add element to set"""
        self.operation_count += 1
        if element not in self._elements:
            self._elements.add(element)
            return True
        return False

    def remove(self, element: Any) -> bool:
        """Remove element from set"""
        self.operation_count += 1
        if element in self._elements:
            self._elements.discard(element)
            return True
        return False

    def contains(self, element: Any) -> bool:
        """Check if element exists in set"""
        self.operation_count += 1
        return element in self._elements

    def size(self) -> int:
        """Return size of set"""
        return len(self._elements)

    def to_list(self) -> List[Any]:
        """Convert set to sorted list"""
        try:
            return sorted(list(self._elements))
        except TypeError:
            return list(self._elements)

    def union(self, other: 'Set') -> Dict[str, Any]:
        """
        Return union of this set and another set
        A ∪ B = {x | x ∈ A or x ∈ B}
        """
        start_time = time.time()
        result = Set()
        result._elements = self._elements.union(other._elements)
        end_time = time.time()

        logger.info(f"Set union: |A|={len(self._elements)}, |B|={len(other._elements)}, |result|={result.size()}, time={round((end_time - start_time) * 1000, 4)}ms")

        return {
            'operation': 'union',
            'result': result.to_list(),
            'set_a': self.to_list(),
            'set_b': other.to_list(),
            'size': result.size(),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'description': 'Elements in A or B or both'
        }

    def intersection(self, other: 'Set') -> Dict[str, Any]:
        """
        Return intersection of this set and another set
        A ∩ B = {x | x ∈ A and x ∈ B}
        """
        start_time = time.time()
        result = Set()
        result._elements = self._elements.intersection(other._elements)
        end_time = time.time()

        return {
            'operation': 'intersection',
            'result': result.to_list(),
            'set_a': self.to_list(),
            'set_b': other.to_list(),
            'size': result.size(),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'description': 'Elements in both A and B'
        }

    def difference(self, other: 'Set') -> Dict[str, Any]:
        """
        Return difference of this set and another set
        A - B = {x | x ∈ A and x ∉ B}
        """
        start_time = time.time()
        result = Set()
        result._elements = self._elements.difference(other._elements)
        end_time = time.time()

        return {
            'operation': 'difference',
            'result': result.to_list(),
            'set_a': self.to_list(),
            'set_b': other.to_list(),
            'size': result.size(),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'description': 'Elements in A but not in B'
        }

    def symmetric_difference(self, other: 'Set') -> Dict[str, Any]:
        """
        Return symmetric difference of this set and another set
        A △ B = (A - B) ∪ (B - A) = {x | x ∈ A ⊕ x ∈ B}
        """
        start_time = time.time()
        result = Set()
        result._elements = self._elements.symmetric_difference(other._elements)
        end_time = time.time()

        return {
            'operation': 'symmetric_difference',
            'result': result.to_list(),
            'set_a': self.to_list(),
            'set_b': other.to_list(),
            'size': result.size(),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'description': 'Elements in A or B but not in both'
        }

    def is_subset(self, other: 'Set') -> Dict[str, Any]:
        """Check if this set is a subset of another"""
        result = self._elements.issubset(other._elements)
        return {
            'operation': 'is_subset',
            'result': result,
            'set_a': self.to_list(),
            'set_b': other.to_list(),
            'description': 'Is A a subset of B?'
        }

    def is_superset(self, other: 'Set') -> Dict[str, Any]:
        """Check if this set is a superset of another"""
        result = self._elements.issuperset(other._elements)
        return {
            'operation': 'is_superset',
            'result': result,
            'set_a': self.to_list(),
            'set_b': other.to_list(),
            'description': 'Is A a superset of B?'
        }

    def __repr__(self) -> str:
        return f"Set({self.to_list()})"

