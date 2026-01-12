"""
Performance Analysis Controller
REST API endpoints for performance comparison and analysis
"""
import logging
from flask import Blueprint, request, jsonify
from models.sorting import BubbleSort, QuickSelect
import time
import random

logger = logging.getLogger(__name__)
performance_bp = Blueprint('performance', __name__)


@performance_bp.route('/compare-sorts', methods=['POST'])
def compare_sorts():
    """
    Compare different sorting algorithms
    Expected JSON: {"sizes": [10, 50, 100, 500]}
    """
    try:
        sizes = request.json.get('sizes', [10, 50, 100, 500])
        logger.info(f"Sort comparison requested for sizes: {sizes}")

        results = []

        for size in sizes:
            # Generate random data
            data = [random.randint(1, 1000) for _ in range(size)]

            # Test Bubble Sort
            bubble_sorter = BubbleSort(data)
            bubble_result = bubble_sorter.sort()

            results.append({
                'size': size,
                'bubble_sort': {
                    'time': bubble_result['execution_time'],
                    'comparisons': bubble_result['comparisons'],
                    'swaps': bubble_result['swaps']
                },
                'python_sorted': {
                    'time': measure_python_sort(data)
                }
            })
            logger.info(f"Completed comparison for size {size}: Bubble={bubble_result['execution_time']}ms")

        logger.info(f"Sort comparison completed for {len(sizes)} different sizes")
        return jsonify({
            'results': results,
            'analysis': 'Bubble sort has O(n²) complexity while Python\'s Timsort is O(n log n)'
        }), 200

    except Exception as e:
        logger.error(f"Sort comparison error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


def measure_python_sort(data):
    """Measure Python's built-in sort performance"""
    arr = data.copy()
    start = time.time()
    sorted(arr)
    end = time.time()
    return round((end - start) * 1000, 4)


@performance_bp.route('/analyze-quickselect', methods=['POST'])
def analyze_quickselect():
    """
    Analyze QuickSelect performance
    Expected JSON: {"sizes": [100, 500, 1000], "k_positions": ["first", "middle", "last"]}
    """
    try:
        sizes = request.json.get('sizes', [100, 500, 1000])

        results = []

        for size in sizes:
            data = [random.randint(1, 10000) for _ in range(size)]

            size_results = {
                'size': size,
                'k_positions': []
            }

            # Test different k positions
            for k in [1, size // 2, size]:
                selector = QuickSelect(data)
                result = selector.find_kth_smallest(k)

                size_results['k_positions'].append({
                    'k': k,
                    'position': 'first' if k == 1 else ('middle' if k == size // 2 else 'last'),
                    'time': result['execution_time'],
                    'comparisons': result['comparisons'],
                    'partitions': result['partitions']
                })

            results.append(size_results)

        return jsonify({
            'results': results,
            'analysis': 'QuickSelect has average O(n) time complexity, much better than sorting O(n log n)'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@performance_bp.route('/memory-analysis', methods=['POST'])
def memory_analysis():
    """
    Analyze memory usage of data structures
    """
    try:
        import sys

        # Analyze different data structures
        results = []

        # Stack/Queue
        from models.stack import Stack
        from models.queue import Queue

        stack = Stack()
        queue = Queue()

        for i in range(100):
            stack.push(i)
            queue.enqueue(i)

        results.append({
            'structure': 'Stack (100 items)',
            'approximate_bytes': sys.getsizeof(stack._items)
        })

        results.append({
            'structure': 'Queue (100 items)',
            'approximate_bytes': sys.getsizeof(queue._items)
        })

        # Hash Table
        from models.hash_table import HashTable

        ht = HashTable(size=10)
        for i in range(50):
            ht.insert(f'key{i}', f'value{i}')

        results.append({
            'structure': 'Hash Table (50 items, size 10)',
            'approximate_bytes': sys.getsizeof(ht.table),
            'statistics': ht.get_statistics()
        })

        return jsonify({
            'results': results,
            'note': 'Memory sizes are approximate and platform-dependent'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@performance_bp.route('/set-operations-performance', methods=['POST'])
def set_operations_performance():
    """
    Analyze performance of set operations
    Expected JSON: {"sizes": [100, 500, 1000]}
    """
    try:
        from models.set_operations import Set

        sizes = request.json.get('sizes', [100, 500, 1000])
        results = []

        for size in sizes:
            # Create two sets with some overlap
            set_a_data = list(range(size))
            set_b_data = list(range(size // 2, size + size // 2))

            set_a = Set(set_a_data)
            set_b = Set(set_b_data)

            # Test operations
            union_result = set_a.union(set_b)
            intersection_result = set_a.intersection(set_b)
            difference_result = set_a.difference(set_b)
            sym_diff_result = set_a.symmetric_difference(set_b)

            results.append({
                'set_size': size,
                'operations': {
                    'union': {
                        'time': union_result['execution_time'],
                        'result_size': union_result['size']
                    },
                    'intersection': {
                        'time': intersection_result['execution_time'],
                        'result_size': intersection_result['size']
                    },
                    'difference': {
                        'time': difference_result['execution_time'],
                        'result_size': difference_result['size']
                    },
                    'symmetric_difference': {
                        'time': sym_diff_result['execution_time'],
                        'result_size': sym_diff_result['size']
                    }
                }
            })

        return jsonify({
            'results': results,
            'analysis': 'Set operations are O(n) on average for hash-based sets'
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

