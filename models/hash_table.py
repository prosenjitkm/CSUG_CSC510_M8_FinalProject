"""
Hash Table Data Structure Implementation
Hash table with collision handling using chaining
"""
from typing import Any, List, Dict, Optional, Tuple
import time


class HashTable:
    """Hash Table implementation with chaining for collision resolution"""

    def __init__(self, size: int = 10):
        self.size = size
        self.table: List[List[Tuple[Any, Any]]] = [[] for _ in range(size)]
        self.item_count = 0
        self.collision_count = 0
        self.operation_count = 0

    def _hash(self, key: Any) -> int:
        """Hash function using Python's built-in hash"""
        return hash(key) % self.size

    def insert(self, key: Any, value: Any) -> Dict[str, Any]:
        """Insert key-value pair into hash table"""
        start_time = time.time()
        index = self._hash(key)
        bucket = self.table[index]

        # Check if key already exists
        for i, (k, v) in enumerate(bucket):
            if k == key:
                bucket[i] = (key, value)
                end_time = time.time()
                return {
                    'operation': 'insert',
                    'key': key,
                    'value': value,
                    'index': index,
                    'updated': True,
                    'execution_time': round((end_time - start_time) * 1000, 4),
                    'success': True
                }

        # Check for collision
        if len(bucket) > 0:
            self.collision_count += 1

        # Insert new key-value pair
        bucket.append((key, value))
        self.item_count += 1
        self.operation_count += 1
        end_time = time.time()

        return {
            'operation': 'insert',
            'key': key,
            'value': value,
            'index': index,
            'collision': len(bucket) > 1,
            'bucket_size': len(bucket),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': True
        }

    def get(self, key: Any) -> Dict[str, Any]:
        """Retrieve value by key"""
        start_time = time.time()
        index = self._hash(key)
        bucket = self.table[index]

        for k, v in bucket:
            if k == key:
                end_time = time.time()
                return {
                    'operation': 'get',
                    'key': key,
                    'value': v,
                    'index': index,
                    'found': True,
                    'execution_time': round((end_time - start_time) * 1000, 4),
                    'success': True
                }

        end_time = time.time()
        return {
            'operation': 'get',
            'key': key,
            'found': False,
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': False
        }

    def delete(self, key: Any) -> Dict[str, Any]:
        """Delete key-value pair"""
        start_time = time.time()
        index = self._hash(key)
        bucket = self.table[index]

        for i, (k, v) in enumerate(bucket):
            if k == key:
                deleted_value = v
                del bucket[i]
                self.item_count -= 1
                end_time = time.time()
                return {
                    'operation': 'delete',
                    'key': key,
                    'value': deleted_value,
                    'index': index,
                    'found': True,
                    'execution_time': round((end_time - start_time) * 1000, 4),
                    'success': True
                }

        end_time = time.time()
        return {
            'operation': 'delete',
            'key': key,
            'found': False,
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': False
        }

    def contains(self, key: Any) -> bool:
        """Check if key exists in hash table"""
        index = self._hash(key)
        bucket = self.table[index]
        return any(k == key for k, v in bucket)

    def get_all_keys(self) -> List[Any]:
        """Get all keys in hash table"""
        keys = []
        for bucket in self.table:
            for k, v in bucket:
                keys.append(k)
        return keys

    def get_all_items(self) -> List[Tuple[Any, Any]]:
        """Get all key-value pairs"""
        items = []
        for bucket in self.table:
            items.extend(bucket)
        return items

    def get_load_factor(self) -> float:
        """Calculate load factor (items / size)"""
        return self.item_count / self.size

    def get_statistics(self) -> Dict[str, Any]:
        """Get hash table statistics"""
        bucket_sizes = [len(bucket) for bucket in self.table]
        empty_buckets = sum(1 for size in bucket_sizes if size == 0)
        max_chain_length = max(bucket_sizes) if bucket_sizes else 0
        avg_chain_length = sum(bucket_sizes) / len(bucket_sizes) if bucket_sizes else 0

        return {
            'size': self.size,
            'item_count': self.item_count,
            'load_factor': round(self.get_load_factor(), 3),
            'collision_count': self.collision_count,
            'empty_buckets': empty_buckets,
            'max_chain_length': max_chain_length,
            'avg_chain_length': round(avg_chain_length, 2)
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert hash table to dictionary representation"""
        table_data = []
        for i, bucket in enumerate(self.table):
            if bucket:
                table_data.append({
                    'index': i,
                    'bucket': [{'key': k, 'value': v} for k, v in bucket]
                })

        return {
            'table': table_data,
            'statistics': self.get_statistics(),
            'all_items': [{'key': k, 'value': v} for k, v in self.get_all_items()]
        }

    def clear(self) -> Dict[str, Any]:
        """Clear entire hash table"""
        self.table = [[] for _ in range(self.size)]
        self.item_count = 0
        self.collision_count = 0
        return {
            'operation': 'clear',
            'success': True
        }

    def resize(self, new_size: int) -> Dict[str, Any]:
        """Resize hash table and rehash all items"""
        start_time = time.time()
        old_items = self.get_all_items()
        old_size = self.size

        self.size = new_size
        self.table = [[] for _ in range(new_size)]
        self.item_count = 0
        self.collision_count = 0

        for key, value in old_items:
            self.insert(key, value)

        end_time = time.time()

        return {
            'operation': 'resize',
            'old_size': old_size,
            'new_size': new_size,
            'items_rehashed': len(old_items),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': True
        }

