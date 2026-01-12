"""
Sorting Controller
REST API endpoints for sorting algorithms
"""
import logging
from flask import Blueprint, request, jsonify
from models.sorting import BubbleSort, QuickSelect

logger = logging.getLogger(__name__)
sorting_bp = Blueprint('sorting', __name__)


@sorting_bp.route('/bubble-sort', methods=['POST'])
def bubble_sort():
    """
    Perform bubble sort on array
    Expected JSON: {"data": [3, 1, 4, 1, 5, 9, 2, 6]}
    """
    try:
        data = request.json.get('data', [])

        if not data:
            return jsonify({'error': 'No data provided'}), 400

        if not isinstance(data, list):
            return jsonify({'error': 'Data must be a list'}), 400

        if not all(isinstance(x, (int, float)) for x in data):
            return jsonify({'error': 'All elements must be numbers'}), 400

        sorter = BubbleSort(data)
        result = sorter.sort()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@sorting_bp.route('/quickselect', methods=['POST'])
def quickselect():
    """
    Find kth smallest element using quickselect
    Expected JSON: {"data": [3, 1, 4, 1, 5, 9, 2, 6], "k": 3}
    """
    try:
        data = request.json.get('data', [])
        k = request.json.get('k')
        logger.info(f"QuickSelect requested: k={k}, array size={len(data)}")

        if not data:
            logger.warning("QuickSelect called with no data")
            return jsonify({'error': 'No data provided'}), 400

        if k is None:
            logger.warning("QuickSelect called without k value")
            return jsonify({'error': 'k value not provided'}), 400

        if not isinstance(data, list):
            logger.warning(f"QuickSelect called with invalid data type: {type(data)}")
            return jsonify({'error': 'Data must be a list'}), 400

        if not all(isinstance(x, (int, float)) for x in data):
            logger.warning("QuickSelect called with non-numeric elements")
            return jsonify({'error': 'All elements must be numbers'}), 400

        selector = QuickSelect(data)
        result = selector.find_kth_smallest(k)

        if not result.get('success', False):
            logger.warning(f"QuickSelect failed: {result.get('error')}")
            return jsonify(result), 400

        logger.info(f"QuickSelect completed: found {result['kth_smallest']} as {k}th smallest in {result['execution_time']}ms")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"QuickSelect error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500

