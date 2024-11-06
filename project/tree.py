from collections.abc import MutableMapping
import random
from typing import List, Optional, Tuple, Iterator, Any


class CartesianTree(MutableMapping):
    class Node:
        """A node in the Cartesian Tree containing key, priority, value, and links to left and right subtrees."""

        def __init__(self, key: Any, priority: float, value: Any):
            self.key: Any = key
            self.priority: float = priority
            self.value: Any = value
            self.left: Optional["CartesianTree.Node"] = None
            self.right: Optional["CartesianTree.Node"] = None

    def __init__(self):
        """Initializes an empty Cartesian Tree."""
        self.root: Optional["CartesianTree.Node"] = None
        self.size: int = 0

    def _split(
        self, node: Optional["CartesianTree.Node"], key: Any
    ) -> Tuple[Optional["CartesianTree.Node"], Optional["CartesianTree.Node"]]:
        """
        Splits the tree into two subtrees based on the given key.
        Left subtree contains nodes with keys less than the specified key,
        and right subtree contains nodes with keys greater or equal to the key.
        """
        if node is None:
            return None, None
        elif key > node.key:
            left, right = self._split(node.right, key)
            node.right = left
            return node, right
        else:
            left, right = self._split(node.left, key)
            node.left = right
            return left, node

    def _merge(
        self,
        left: Optional["CartesianTree.Node"],
        right: Optional["CartesianTree.Node"],
    ) -> Optional["CartesianTree.Node"]:
        """
        Merges two subtrees while preserving the Cartesian Tree properties,
        using node priorities to control the structure.
        """
        if left is None:
            return right
        if right is None:
            return left
        if left.priority > right.priority:
            left.right = self._merge(left.right, right)
            return left
        else:
            right.left = self._merge(left, right.left)
            return right

    def __setitem__(self, key: Any, value: Any) -> None:
        """
        Inserts a key-value pair into the tree. If the key exists, updates its value.
        """

        def find_and_update(
            node: Optional["CartesianTree.Node"], key: Any, value: Any
        ) -> bool:
            if node is None:
                return False
            if key < node.key:
                return find_and_update(node.left, key, value)
            elif key > node.key:
                return find_and_update(node.right, key, value)
            else:
                node.value = value
                return True

        if find_and_update(self.root, key, value):
            return

        new_node = self.Node(key, random.random(), value)
        if self.root is None:
            self.root = new_node
        else:
            left, right = self._split(self.root, key)
            left = self._merge(left, new_node)
            self.root = self._merge(left, right)
        self.size += 1

    def __getitem__(self, key: Any) -> Any:
        """
        Retrieves the value associated with a given key.
        Raises KeyError if the key is not found.
        """
        node = self.root
        while node:
            if key < node.key:
                node = node.left
            elif key > node.key:
                node = node.right
            else:
                return node.value
        raise KeyError(f"Key {key} not found in CartesianTree")

    def __delitem__(self, key: Any) -> None:
        """
        Deletes a node by its key. Raises KeyError if the key is not found.
        """

        def delete(
            node: Optional["CartesianTree.Node"], key: Any
        ) -> Optional["CartesianTree.Node"]:
            if node is None:
                raise KeyError(f"Key {key} not found in CartesianTree")
            if key < node.key:
                node.left = delete(node.left, key)
            elif key > node.key:
                node.right = delete(node.right, key)
            else:
                return self._merge(node.left, node.right)
            return node

        self.root = delete(self.root, key)
        self.size -= 1

    def __iter__(self) -> Iterator[Any]:
        """
        Implements in-order traversal (ascending order) of the tree's keys.
        """
        stack: List[CartesianTree.Node] = []
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.left
            node = stack.pop()
            yield node.key
            node = node.right

    def __reversed__(self) -> Iterator[Any]:
        """
        Implements reverse in-order traversal (descending order) of the tree's keys.
        """
        stack: List[CartesianTree.Node] = []  # Annotated as a List of Node
        node = self.root
        while stack or node:
            while node:
                stack.append(node)
                node = node.right
            node = stack.pop()
            yield node.key
            node = node.left

    def __contains__(self, key: Any) -> bool:
        """
        Checks if a key exists in the tree.
        """
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __len__(self) -> int:
        """
        Returns the number of nodes in the tree.
        """
        return self.size
