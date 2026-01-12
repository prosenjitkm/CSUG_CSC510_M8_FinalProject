"""
Tree Data Structure Implementation
Binary Search Tree (BST) with visualization support
"""
from typing import Any, List, Dict, Optional
import time


class TreeNode:
    """Node for binary search tree"""

    def __init__(self, value: Any):
        self.value = value
        self.left: Optional[TreeNode] = None
        self.right: Optional[TreeNode] = None
        self.height = 1


class BinarySearchTree:
    """Binary Search Tree implementation with various traversals"""

    def __init__(self):
        self.root: Optional[TreeNode] = None
        self.operation_count = 0
        self.node_count = 0

    def insert(self, value: Any) -> Dict[str, Any]:
        """Insert value into BST"""
        start_time = time.time()
        self.root = self._insert_recursive(self.root, value)
        self.operation_count += 1
        end_time = time.time()

        return {
            'operation': 'insert',
            'value': value,
            'tree': self.to_dict(),
            'size': self.node_count,
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': True
        }

    def _insert_recursive(self, node: Optional[TreeNode], value: Any) -> TreeNode:
        """Helper method for recursive insertion"""
        if node is None:
            self.node_count += 1
            return TreeNode(value)

        if value < node.value:
            node.left = self._insert_recursive(node.left, value)
        elif value > node.value:
            node.right = self._insert_recursive(node.right, value)

        return node

    def search(self, value: Any) -> Dict[str, Any]:
        """Search for value in BST"""
        start_time = time.time()
        result = self._search_recursive(self.root, value)
        end_time = time.time()

        return {
            'operation': 'search',
            'value': value,
            'found': result,
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': True
        }

    def _search_recursive(self, node: Optional[TreeNode], value: Any) -> bool:
        """Helper method for recursive search"""
        if node is None:
            return False
        if node.value == value:
            return True
        if value < node.value:
            return self._search_recursive(node.left, value)
        return self._search_recursive(node.right, value)

    def delete(self, value: Any) -> Dict[str, Any]:
        """Delete value from BST"""
        start_time = time.time()
        found = self._search_recursive(self.root, value)
        if found:
            self.root = self._delete_recursive(self.root, value)
            self.node_count -= 1
        end_time = time.time()

        return {
            'operation': 'delete',
            'value': value,
            'found': found,
            'tree': self.to_dict(),
            'size': self.node_count,
            'execution_time': round((end_time - start_time) * 1000, 4),
            'success': found
        }

    def _delete_recursive(self, node: Optional[TreeNode], value: Any) -> Optional[TreeNode]:
        """Helper method for recursive deletion"""
        if node is None:
            return None

        if value < node.value:
            node.left = self._delete_recursive(node.left, value)
        elif value > node.value:
            node.right = self._delete_recursive(node.right, value)
        else:
            # Node found
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left

            # Node has two children
            min_node = self._find_min(node.right)
            node.value = min_node.value
            node.right = self._delete_recursive(node.right, min_node.value)

        return node

    def _find_min(self, node: TreeNode) -> TreeNode:
        """Find minimum value node in subtree"""
        while node.left:
            node = node.left
        return node

    def inorder_traversal(self) -> Dict[str, Any]:
        """Inorder traversal (Left, Root, Right)"""
        result = []
        self._inorder_recursive(self.root, result)
        return {
            'operation': 'inorder_traversal',
            'order': 'Left -> Root -> Right',
            'result': result,
            'description': 'Sorted order for BST'
        }

    def _inorder_recursive(self, node: Optional[TreeNode], result: List[Any]):
        """Helper for inorder traversal"""
        if node:
            self._inorder_recursive(node.left, result)
            result.append(node.value)
            self._inorder_recursive(node.right, result)

    def preorder_traversal(self) -> Dict[str, Any]:
        """Preorder traversal (Root, Left, Right)"""
        result = []
        self._preorder_recursive(self.root, result)
        return {
            'operation': 'preorder_traversal',
            'order': 'Root -> Left -> Right',
            'result': result,
            'description': 'Used for creating copy of tree'
        }

    def _preorder_recursive(self, node: Optional[TreeNode], result: List[Any]):
        """Helper for preorder traversal"""
        if node:
            result.append(node.value)
            self._preorder_recursive(node.left, result)
            self._preorder_recursive(node.right, result)

    def postorder_traversal(self) -> Dict[str, Any]:
        """Postorder traversal (Left, Right, Root)"""
        result = []
        self._postorder_recursive(self.root, result)
        return {
            'operation': 'postorder_traversal',
            'order': 'Left -> Right -> Root',
            'result': result,
            'description': 'Used for deleting tree'
        }

    def _postorder_recursive(self, node: Optional[TreeNode], result: List[Any]):
        """Helper for postorder traversal"""
        if node:
            self._postorder_recursive(node.left, result)
            self._postorder_recursive(node.right, result)
            result.append(node.value)

    def level_order_traversal(self) -> Dict[str, Any]:
        """Level-order traversal (breadth-first)"""
        if not self.root:
            return {
                'operation': 'level_order_traversal',
                'result': [],
                'levels': []
            }

        result = []
        levels = []
        queue = [(self.root, 0)]

        while queue:
            node, level = queue.pop(0)
            result.append(node.value)

            if level >= len(levels):
                levels.append([])
            levels[level].append(node.value)

            if node.left:
                queue.append((node.left, level + 1))
            if node.right:
                queue.append((node.right, level + 1))

        return {
            'operation': 'level_order_traversal',
            'order': 'Level by level',
            'result': result,
            'levels': levels,
            'description': 'Breadth-first traversal'
        }

    def get_height(self) -> int:
        """Get height of tree"""
        return self._get_height_recursive(self.root)

    def _get_height_recursive(self, node: Optional[TreeNode]) -> int:
        """Helper for calculating height"""
        if node is None:
            return 0
        return 1 + max(self._get_height_recursive(node.left),
                      self._get_height_recursive(node.right))

    def to_dict(self) -> Dict[str, Any]:
        """Convert tree to dictionary for visualization"""
        return {
            'root': self._node_to_dict(self.root),
            'size': self.node_count,
            'height': self.get_height(),
            'is_empty': self.root is None
        }

    def _node_to_dict(self, node: Optional[TreeNode]) -> Optional[Dict[str, Any]]:
        """Convert node to dictionary"""
        if node is None:
            return None

        return {
            'value': node.value,
            'left': self._node_to_dict(node.left),
            'right': self._node_to_dict(node.right)
        }

    def clear(self) -> Dict[str, Any]:
        """Clear entire tree"""
        self.root = None
        self.node_count = 0
        return {
            'operation': 'clear',
            'success': True,
            'size': 0
        }

