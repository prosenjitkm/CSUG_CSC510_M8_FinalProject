"""
Set Operations Controller
REST API endpoints for set operations
"""
import logging
from flask import Blueprint, request, jsonify
from models.set_operations import Set

logger = logging.getLogger(__name__)
set_bp = Blueprint('set', __name__)


@set_bp.route('/union', methods=['POST'])
def union():
    """
    Perform union operation on two sets
    Expected JSON: {"set_a": [1, 2, 3], "set_b": [3, 4, 5]}
    """
    try:
        set_a_data = request.json.get('set_a', [])
        set_b_data = request.json.get('set_b', [])
        logger.info(f"Set union requested: Set A size={len(set_a_data)}, Set B size={len(set_b_data)}")

        set_a = Set(set_a_data)
        set_b = Set(set_b_data)

        result = set_a.union(set_b)
        logger.info(f"Set union completed: result size={result['size']}, time={result['execution_time']}ms")
        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Set union error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@set_bp.route('/intersection', methods=['POST'])
def intersection():
    """
    Perform intersection operation on two sets
    Expected JSON: {"set_a": [1, 2, 3], "set_b": [3, 4, 5]}
    """
    try:
        set_a_data = request.json.get('set_a', [])
        set_b_data = request.json.get('set_b', [])

        set_a = Set(set_a_data)
        set_b = Set(set_b_data)

        result = set_a.intersection(set_b)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@set_bp.route('/difference', methods=['POST'])
def difference():
    """
    Perform difference operation on two sets
    Expected JSON: {"set_a": [1, 2, 3], "set_b": [3, 4, 5]}
    """
    try:
        set_a_data = request.json.get('set_a', [])
        set_b_data = request.json.get('set_b', [])

        set_a = Set(set_a_data)
        set_b = Set(set_b_data)

        result = set_a.difference(set_b)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@set_bp.route('/symmetric-difference', methods=['POST'])
def symmetric_difference():
    """
    Perform symmetric difference operation on two sets
    Expected JSON: {"set_a": [1, 2, 3], "set_b": [3, 4, 5]}
    """
    try:
        set_a_data = request.json.get('set_a', [])
        set_b_data = request.json.get('set_b', [])

        set_a = Set(set_a_data)
        set_b = Set(set_b_data)

        result = set_a.symmetric_difference(set_b)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@set_bp.route('/is-subset', methods=['POST'])
def is_subset():
    """
    Check if set A is subset of set B
    Expected JSON: {"set_a": [1, 2], "set_b": [1, 2, 3, 4]}
    """
    try:
        set_a_data = request.json.get('set_a', [])
        set_b_data = request.json.get('set_b', [])

        set_a = Set(set_a_data)
        set_b = Set(set_b_data)

        result = set_a.is_subset(set_b)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@set_bp.route('/is-superset', methods=['POST'])
def is_superset():
    """
    Check if set A is superset of set B
    Expected JSON: {"set_a": [1, 2, 3, 4], "set_b": [1, 2]}
    """
    try:
        set_a_data = request.json.get('set_a', [])
        set_b_data = request.json.get('set_b', [])

        set_a = Set(set_a_data)
        set_b = Set(set_b_data)

        result = set_a.is_superset(set_b)
        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

