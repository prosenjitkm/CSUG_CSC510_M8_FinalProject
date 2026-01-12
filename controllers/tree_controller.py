"""
Tree Controller
REST API endpoints for binary search tree operations
"""
import logging
from flask import Blueprint, request, jsonify
from models.tree import BinarySearchTree

logger = logging.getLogger(__name__)
tree_bp = Blueprint('tree', __name__)

# Store tree instances per session
trees = {}


def get_tree(tree_id='default'):
    """Get or create tree instance"""
    if tree_id not in trees:
        trees[tree_id] = BinarySearchTree()
    return trees[tree_id]


@tree_bp.route('/insert', methods=['POST'])
def insert():
    """
    Insert value into tree
    Expected JSON: {"value": 5, "tree_id": "default"}
    """
    try:
        value = request.json.get('value')
        tree_id = request.json.get('tree_id', 'default')

        if value is None:
            return jsonify({'error': 'No value provided'}), 400

        tree = get_tree(tree_id)
        result = tree.insert(value)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/search', methods=['POST'])
def search():
    """
    Search for value in tree
    Expected JSON: {"value": 5, "tree_id": "default"}
    """
    try:
        value = request.json.get('value')
        tree_id = request.json.get('tree_id', 'default')

        if value is None:
            return jsonify({'error': 'No value provided'}), 400

        tree = get_tree(tree_id)
        result = tree.search(value)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/delete', methods=['POST'])
def delete():
    """
    Delete value from tree
    Expected JSON: {"value": 5, "tree_id": "default"}
    """
    try:
        value = request.json.get('value')
        tree_id = request.json.get('tree_id', 'default')

        if value is None:
            return jsonify({'error': 'No value provided'}), 400

        tree = get_tree(tree_id)
        result = tree.delete(value)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/traverse/inorder', methods=['POST'])
def inorder():
    """Get inorder traversal"""
    try:
        tree_id = request.json.get('tree_id', 'default')
        tree = get_tree(tree_id)
        result = tree.inorder_traversal()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/traverse/preorder', methods=['POST'])
def preorder():
    """Get preorder traversal"""
    try:
        tree_id = request.json.get('tree_id', 'default')
        tree = get_tree(tree_id)
        result = tree.preorder_traversal()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/traverse/postorder', methods=['POST'])
def postorder():
    """Get postorder traversal"""
    try:
        tree_id = request.json.get('tree_id', 'default')
        tree = get_tree(tree_id)
        result = tree.postorder_traversal()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/traverse/levelorder', methods=['POST'])
def levelorder():
    """Get level-order traversal"""
    try:
        tree_id = request.json.get('tree_id', 'default')
        tree = get_tree(tree_id)
        result = tree.level_order_traversal()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/get', methods=['POST'])
def get_tree_data():
    """Get current tree state"""
    try:
        tree_id = request.json.get('tree_id', 'default')
        tree = get_tree(tree_id)
        result = tree.to_dict()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tree_bp.route('/clear', methods=['POST'])
def clear():
    """Clear tree"""
    try:
        tree_id = request.json.get('tree_id', 'default')
        tree = get_tree(tree_id)
        result = tree.clear()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

