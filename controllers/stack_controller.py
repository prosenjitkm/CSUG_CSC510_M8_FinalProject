"""
Stack Controller
REST API endpoints for stack operations
"""
import logging
from flask import Blueprint, request, jsonify
from models.stack import Stack

logger = logging.getLogger(__name__)
stack_bp = Blueprint('stack', __name__)

# Store stack instances per session (in production, use proper session management)
stacks = {}


def get_stack(stack_id='default'):
    """Get or create stack instance"""
    if stack_id not in stacks:
        stacks[stack_id] = Stack()
    return stacks[stack_id]


@stack_bp.route('/push', methods=['POST'])
def push():
    """
    Push item onto stack
    Expected JSON: {"item": 5, "stack_id": "default"}
    """
    try:
        item = request.json.get('item')
        stack_id = request.json.get('stack_id', 'default')

        if item is None:
            logger.warning(f"Stack push called without item: stack_id={stack_id}")
            return jsonify({'error': 'No item provided'}), 400

        stack = get_stack(stack_id)
        result = stack.push(item)
        logger.info(f"Stack push: item={item}, stack_id={stack_id}, new_size={result['size']}")

        return jsonify(result), 200

    except Exception as e:
        logger.error(f"Stack push error: {str(e)}", exc_info=True)
        return jsonify({'error': str(e)}), 500


@stack_bp.route('/pop', methods=['POST'])
def pop():
    """
    Pop item from stack
    Expected JSON: {"stack_id": "default"}
    """
    try:
        stack_id = request.json.get('stack_id', 'default')
        stack = get_stack(stack_id)
        result = stack.pop()

        if not result.get('success', True):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stack_bp.route('/peek', methods=['POST'])
def peek():
    """
    Peek at top item without removing
    Expected JSON: {"stack_id": "default"}
    """
    try:
        stack_id = request.json.get('stack_id', 'default')
        stack = get_stack(stack_id)
        result = stack.peek()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stack_bp.route('/get', methods=['POST'])
def get_stack_data():
    """
    Get current stack state
    Expected JSON: {"stack_id": "default"}
    """
    try:
        stack_id = request.json.get('stack_id', 'default')
        stack = get_stack(stack_id)
        result = stack.to_dict()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@stack_bp.route('/clear', methods=['POST'])
def clear():
    """
    Clear stack
    Expected JSON: {"stack_id": "default"}
    """
    try:
        stack_id = request.json.get('stack_id', 'default')
        stack = get_stack(stack_id)
        result = stack.clear()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

