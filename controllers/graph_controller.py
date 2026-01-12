"""
Graph Controller
REST API endpoints for graph operations
"""
import logging
from flask import Blueprint, request, jsonify
from models.graph import Graph

logger = logging.getLogger(__name__)
graph_bp = Blueprint('graph', __name__)

# Store graph instances per session
graphs = {}


def get_graph(graph_id='default', directed=False):
    """Get or create graph instance"""
    if graph_id not in graphs:
        graphs[graph_id] = Graph(directed=directed)
    return graphs[graph_id]


@graph_bp.route('/create', methods=['POST'])
def create():
    """
    Create new graph
    Expected JSON: {"graph_id": "default", "directed": false}
    """
    try:
        graph_id = request.json.get('graph_id', 'default')
        directed = request.json.get('directed', False)

        graphs[graph_id] = Graph(directed=directed)

        return jsonify({
            'operation': 'create',
            'graph_id': graph_id,
            'directed': directed,
            'success': True
        }), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/add-vertex', methods=['POST'])
def add_vertex():
    """
    Add vertex to graph
    Expected JSON: {"vertex": "A", "graph_id": "default"}
    """
    try:
        vertex = request.json.get('vertex')
        graph_id = request.json.get('graph_id', 'default')

        if vertex is None:
            return jsonify({'error': 'No vertex provided'}), 400

        graph = get_graph(graph_id)
        result = graph.add_vertex(vertex)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/add-edge', methods=['POST'])
def add_edge():
    """
    Add edge to graph
    Expected JSON: {"from": "A", "to": "B", "weight": 1, "graph_id": "default"}
    """
    try:
        from_vertex = request.json.get('from')
        to_vertex = request.json.get('to')
        weight = request.json.get('weight', 1.0)
        graph_id = request.json.get('graph_id', 'default')

        if from_vertex is None or to_vertex is None:
            return jsonify({'error': 'From and to vertices required'}), 400

        graph = get_graph(graph_id)
        result = graph.add_edge(from_vertex, to_vertex, weight)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/remove-vertex', methods=['POST'])
def remove_vertex():
    """Remove vertex from graph"""
    try:
        vertex = request.json.get('vertex')
        graph_id = request.json.get('graph_id', 'default')

        if vertex is None:
            return jsonify({'error': 'No vertex provided'}), 400

        graph = get_graph(graph_id)
        result = graph.remove_vertex(vertex)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/dfs', methods=['POST'])
def dfs():
    """
    Depth-first search
    Expected JSON: {"start": "A", "graph_id": "default"}
    """
    try:
        start = request.json.get('start')
        graph_id = request.json.get('graph_id', 'default')

        if start is None:
            return jsonify({'error': 'No start vertex provided'}), 400

        graph = get_graph(graph_id)
        result = graph.dfs(start)

        if not result.get('success', True):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/bfs', methods=['POST'])
def bfs():
    """
    Breadth-first search
    Expected JSON: {"start": "A", "graph_id": "default"}
    """
    try:
        start = request.json.get('start')
        graph_id = request.json.get('graph_id', 'default')

        if start is None:
            return jsonify({'error': 'No start vertex provided'}), 400

        graph = get_graph(graph_id)
        result = graph.bfs(start)

        if not result.get('success', True):
            return jsonify(result), 400

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/shortest-path', methods=['POST'])
def shortest_path():
    """
    Find shortest path
    Expected JSON: {"start": "A", "end": "B", "graph_id": "default"}
    """
    try:
        start = request.json.get('start')
        end = request.json.get('end')
        graph_id = request.json.get('graph_id', 'default')

        if start is None or end is None:
            return jsonify({'error': 'Start and end vertices required'}), 400

        graph = get_graph(graph_id)
        result = graph.find_shortest_path(start, end)

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/has-cycle', methods=['POST'])
def has_cycle():
    """Check if graph has cycle"""
    try:
        graph_id = request.json.get('graph_id', 'default')
        graph = get_graph(graph_id)
        result = graph.has_cycle()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/get', methods=['POST'])
def get_graph_data():
    """Get current graph state"""
    try:
        graph_id = request.json.get('graph_id', 'default')
        graph = get_graph(graph_id)
        result = graph.to_dict()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@graph_bp.route('/clear', methods=['POST'])
def clear():
    """Clear graph"""
    try:
        graph_id = request.json.get('graph_id', 'default')
        graph = get_graph(graph_id)
        result = graph.clear()

        return jsonify(result), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

