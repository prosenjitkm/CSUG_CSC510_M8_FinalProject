"""
Queue Controller
REST API endpoints for queue operations
"""
import logging
from flask import Blueprint, request, jsonify
from models.queue import Queue

logger = logging.getLogger(__name__)
queue_bp = Blueprint('queue', __name__)

# Store queue instances per session
queues = {}


def get_queue(queue_id='default'):
    """Get or create queue instance"""
    if queue_id not in queues:
        queues[queue_id] = Queue()
    return queues[queue_id]


@queue_bp.route('/enqueue', methods=['POST'])
def enqueue():
    """
    Enqueue item
    Expected JSON: {"item": 5, "queue_id": "default"}
    """
    try:
        item = request.json.get('item')
        queue_id = request.json.get('queue_id', 'default')

        if item is None:
            return jsonify({'error': 'No item provided'}), 400

        queue = get_queue(queue_id)
        result = queue.enqueue(item)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queue_bp.route('/dequeue', methods=['POST'])
def dequeue():
    """
    Dequeue item
    Expected JSON: {"queue_id": "default"}
    """
    try:
        queue_id = request.json.get('queue_id', 'default')
        queue = get_queue(queue_id)
        result = queue.dequeue()

        if not result.get('success', True):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queue_bp.route('/peek', methods=['POST'])
def peek():
    """
    Peek at front item
    Expected JSON: {"queue_id": "default"}
    """
    try:
        queue_id = request.json.get('queue_id', 'default')
        queue = get_queue(queue_id)
        result = queue.peek()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queue_bp.route('/get', methods=['POST'])
def get_queue_data():
    """
    Get current queue state
    Expected JSON: {"queue_id": "default"}
    """
    try:
        queue_id = request.json.get('queue_id', 'default')
        queue = get_queue(queue_id)
        result = queue.to_dict()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@queue_bp.route('/clear', methods=['POST'])
def clear():
    """
    Clear queue
    Expected JSON: {"queue_id": "default"}
    """
    try:
        queue_id = request.json.get('queue_id', 'default')
        queue = get_queue(queue_id)
        result = queue.clear()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

