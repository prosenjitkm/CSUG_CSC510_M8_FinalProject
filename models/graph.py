"""
Graph Data Structure Implementation
Supporting both adjacency list and adjacency matrix representations
"""
from typing import Dict, List, Any, Set, Optional
from collections import deque
import time


class Graph:
    """Graph implementation with DFS, BFS, and pathfinding algorithms"""

    def __init__(self, directed: bool = False):
        self.directed = directed
        self.adjacency_list: Dict[Any, List[Any]] = {}
        self.operation_count = 0

    def add_vertex(self, vertex: Any) -> Dict[str, Any]:
        """Add vertex to graph"""
        start_time = time.time()
        if vertex not in self.adjacency_list:
            self.adjacency_list[vertex] = []
            self.operation_count += 1
            success = True
        else:
            success = False
        end_time = time.time()

        return {
            'operation': 'add_vertex',
            'vertex': vertex,
            'success': success,
            'graph': self.to_dict(),
            'execution_time': round((end_time - start_time) * 1000, 4)
        }

    def add_edge(self, from_vertex: Any, to_vertex: Any, weight: float = 1.0) -> Dict[str, Any]:
        """Add edge between vertices"""
        start_time = time.time()

        # Ensure vertices exist
        if from_vertex not in self.adjacency_list:
            self.adjacency_list[from_vertex] = []
        if to_vertex not in self.adjacency_list:
            self.adjacency_list[to_vertex] = []

        # Add edge
        edge_info = {'to': to_vertex, 'weight': weight}
        if edge_info not in self.adjacency_list[from_vertex]:
            self.adjacency_list[from_vertex].append(edge_info)

            # For undirected graph, add reverse edge
            if not self.directed:
                reverse_edge = {'to': from_vertex, 'weight': weight}
                if reverse_edge not in self.adjacency_list[to_vertex]:
                    self.adjacency_list[to_vertex].append(reverse_edge)

            self.operation_count += 1
            success = True
        else:
            success = False

        end_time = time.time()

        return {
            'operation': 'add_edge',
            'from': from_vertex,
            'to': to_vertex,
            'weight': weight,
            'success': success,
            'graph': self.to_dict(),
            'execution_time': round((end_time - start_time) * 1000, 4)
        }

    def remove_vertex(self, vertex: Any) -> Dict[str, Any]:
        """Remove vertex and all connected edges"""
        start_time = time.time()

        if vertex not in self.adjacency_list:
            return {
                'operation': 'remove_vertex',
                'vertex': vertex,
                'success': False,
                'error': 'Vertex not found'
            }

        # Remove vertex
        del self.adjacency_list[vertex]

        # Remove edges to this vertex
        for v in self.adjacency_list:
            self.adjacency_list[v] = [
                edge for edge in self.adjacency_list[v]
                if edge['to'] != vertex
            ]

        end_time = time.time()

        return {
            'operation': 'remove_vertex',
            'vertex': vertex,
            'success': True,
            'graph': self.to_dict(),
            'execution_time': round((end_time - start_time) * 1000, 4)
        }

    def dfs(self, start_vertex: Any) -> Dict[str, Any]:
        """Depth-First Search traversal"""
        if start_vertex not in self.adjacency_list:
            return {
                'operation': 'dfs',
                'error': 'Start vertex not found',
                'success': False
            }

        start_time = time.time()
        visited = set()
        result = []
        steps = []

        def dfs_recursive(vertex: Any):
            visited.add(vertex)
            result.append(vertex)
            steps.append({
                'visiting': vertex,
                'visited': list(visited),
                'stack': result.copy()
            })

            for edge in self.adjacency_list[vertex]:
                neighbor = edge['to']
                if neighbor not in visited:
                    dfs_recursive(neighbor)

        dfs_recursive(start_vertex)
        end_time = time.time()

        return {
            'operation': 'dfs',
            'start': start_vertex,
            'order': result,
            'steps': steps,
            'visited_count': len(visited),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'description': 'Depth-First Search traversal'
        }

    def bfs(self, start_vertex: Any) -> Dict[str, Any]:
        """Breadth-First Search traversal"""
        if start_vertex not in self.adjacency_list:
            return {
                'operation': 'bfs',
                'error': 'Start vertex not found',
                'success': False
            }

        start_time = time.time()
        visited = set([start_vertex])
        queue = deque([start_vertex])
        result = []
        steps = []

        while queue:
            vertex = queue.popleft()
            result.append(vertex)
            steps.append({
                'visiting': vertex,
                'visited': list(visited),
                'queue': list(queue)
            })

            for edge in self.adjacency_list[vertex]:
                neighbor = edge['to']
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(neighbor)

        end_time = time.time()

        return {
            'operation': 'bfs',
            'start': start_vertex,
            'order': result,
            'steps': steps,
            'visited_count': len(visited),
            'execution_time': round((end_time - start_time) * 1000, 4),
            'description': 'Breadth-First Search traversal'
        }

    def find_shortest_path(self, start: Any, end: Any) -> Dict[str, Any]:
        """Find shortest path using BFS (unweighted)"""
        if start not in self.adjacency_list or end not in self.adjacency_list:
            return {
                'operation': 'shortest_path',
                'error': 'Start or end vertex not found',
                'success': False
            }

        start_time = time.time()
        visited = {start}
        queue = deque([(start, [start])])

        while queue:
            vertex, path = queue.popleft()

            if vertex == end:
                end_time = time.time()
                return {
                    'operation': 'shortest_path',
                    'start': start,
                    'end': end,
                    'path': path,
                    'length': len(path) - 1,
                    'execution_time': round((end_time - start_time) * 1000, 4),
                    'success': True
                }

            for edge in self.adjacency_list[vertex]:
                neighbor = edge['to']
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        end_time = time.time()
        return {
            'operation': 'shortest_path',
            'start': start,
            'end': end,
            'path': None,
            'message': 'No path found',
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': False
        }

    def has_cycle(self) -> Dict[str, Any]:
        """Detect if graph has a cycle"""
        visited = set()
        rec_stack = set()

        def has_cycle_util(vertex: Any, parent: Optional[Any] = None) -> bool:
            visited.add(vertex)
            rec_stack.add(vertex)

            for edge in self.adjacency_list[vertex]:
                neighbor = edge['to']
                if neighbor not in visited:
                    if has_cycle_util(neighbor, vertex):
                        return True
                elif neighbor in rec_stack and (self.directed or neighbor != parent):
                    return True

            rec_stack.remove(vertex)
            return False

        for vertex in self.adjacency_list:
            if vertex not in visited:
                if has_cycle_util(vertex):
                    return {
                        'operation': 'has_cycle',
                        'result': True,
                        'description': 'Graph contains at least one cycle'
                    }

        return {
            'operation': 'has_cycle',
            'result': False,
            'description': 'Graph is acyclic'
        }

    def get_vertex_count(self) -> int:
        """Get number of vertices"""
        return len(self.adjacency_list)

    def get_edge_count(self) -> int:
        """Get number of edges"""
        count = sum(len(edges) for edges in self.adjacency_list.values())
        return count if self.directed else count // 2

    def to_dict(self) -> Dict[str, Any]:
        """Convert graph to dictionary representation"""
        edges = []
        for vertex, neighbors in self.adjacency_list.items():
            for edge in neighbors:
                edges.append({
                    'from': vertex,
                    'to': edge['to'],
                    'weight': edge['weight']
                })

        return {
            'vertices': list(self.adjacency_list.keys()),
            'edges': edges,
            'vertex_count': self.get_vertex_count(),
            'edge_count': self.get_edge_count(),
            'directed': self.directed,
            'adjacency_list': {
                k: [e['to'] for e in v]
                for k, v in self.adjacency_list.items()
            }
        }

    def clear(self) -> Dict[str, Any]:
        """Clear entire graph"""
        self.adjacency_list.clear()
        return {
            'operation': 'clear',
            'success': True
        }

