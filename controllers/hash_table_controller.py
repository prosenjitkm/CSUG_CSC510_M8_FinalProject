"""
Hash Table Controller
REST API endpoints for hash table operations
"""
import logging
from flask import Blueprint, request, jsonify
from models.hash_table import HashTable

logger = logging.getLogger(__name__)
hash_table_bp = Blueprint('hashtable', __name__)

# Store hash table instances per session
hash_tables = {}


def get_hash_table(table_id='default', size=10):
    """Get or create hash table instance"""
    if table_id not in hash_tables:
        hash_tables[table_id] = HashTable(size=size)
    return hash_tables[table_id]


@hash_table_bp.route('/create', methods=['POST'])
def create():
    """
    Create new hash table
    Expected JSON: {"table_id": "default", "size": 10}
    """
    try:
        table_id = request.json.get('table_id', 'default')
        size = request.json.get('size', 10)

        hash_tables[table_id] = HashTable(size=size)

        return jsonify({
            'operation': 'create',
            'table_id': table_id,
            'size': size,
            'success': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/insert', methods=['POST'])
def insert():
    """
    Insert key-value pair
    Expected JSON: {"key": "name", "value": "John", "table_id": "default"}
    """
    try:
        key = request.json.get('key')
        value = request.json.get('value')
        table_id = request.json.get('table_id', 'default')

        if key is None:
            return jsonify({'error': 'No key provided'}), 400

        table = get_hash_table(table_id)
        result = table.insert(key, value)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/get', methods=['POST'])
def get_value():
    """
    Get value by key
    Expected JSON: {"key": "name", "table_id": "default"}
    """
    try:
        key = request.json.get('key')
        table_id = request.json.get('table_id', 'default')

        if key is None:
            return jsonify({'error': 'No key provided'}), 400

        table = get_hash_table(table_id)
        result = table.get(key)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/delete', methods=['POST'])
def delete():
    """
    Delete key-value pair
    Expected JSON: {"key": "name", "table_id": "default"}
    """
    try:
        key = request.json.get('key')
        table_id = request.json.get('table_id', 'default')

        if key is None:
            return jsonify({'error': 'No key provided'}), 400

        table = get_hash_table(table_id)
        result = table.delete(key)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/get-all', methods=['POST'])
def get_all():
    """Get entire hash table state"""
    try:
        table_id = request.json.get('table_id', 'default')
        table = get_hash_table(table_id)
        result = table.to_dict()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/statistics', methods=['POST'])
def statistics():
    """Get hash table statistics"""
    try:
        table_id = request.json.get('table_id', 'default')
        table = get_hash_table(table_id)
        result = table.get_statistics()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/resize', methods=['POST'])
def resize():
    """
    Resize hash table
    Expected JSON: {"new_size": 20, "table_id": "default"}
    """
    try:
        new_size = request.json.get('new_size')
        table_id = request.json.get('table_id', 'default')

        if new_size is None:
            return jsonify({'error': 'No new size provided'}), 400

        table = get_hash_table(table_id)
        result = table.resize(new_size)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@hash_table_bp.route('/clear', methods=['POST'])
def clear():
    """Clear hash table"""
    try:
        table_id = request.json.get('table_id', 'default')
        table = get_hash_table(table_id)
        result = table.clear()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

