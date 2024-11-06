import pytest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from project.tree import CartesianTree


@pytest.fixture
def tree():
    return CartesianTree()


def test_insert_and_getitem(tree):
    tree[1] = "a"
    tree[2] = "b"
    tree[3] = "c"

    assert tree[1] == "a"
    assert tree[2] == "b"
    assert tree[3] == "c"


def test_update_value(tree):
    tree[1] = "a"
    tree[1] = "updated"

    assert tree[1] == "updated"


def test_delete_item(tree):
    tree[1] = "a"
    tree[2] = "b"

    del tree[1]

    assert 1 not in tree
    assert 2 in tree


def test_len(tree):
    assert len(tree) == 0
    tree[1] = "a"
    tree[2] = "b"
    assert len(tree) == 2
    del tree[1]
    assert len(tree) == 1


def test_contains(tree):
    tree[1] = "a"

    assert 1 in tree
    assert 2 not in tree


def test_key_error_on_missing_key(tree):
    with pytest.raises(KeyError):
        _ = tree[99]


def test_iter(tree):
    tree[3] = "c"
    tree[1] = "a"
    tree[2] = "b"

    keys = list(tree)
    assert keys == [1, 2, 3]


def test_reversed(tree):
    tree[3] = "c"
    tree[1] = "a"
    tree[2] = "b"

    keys = list(reversed(tree))
    assert keys == [3, 2, 1]


def test_subtree_structure(tree):
    tree[10] = "root"
    tree[5] = "left child"
    tree[15] = "right child"
    tree[3] = "left grandchild"
    tree[7] = "right grandchild"

    def check_subtree(node):
        if node is None:
            return True
        if node.left:
            assert node.left.key < node.key
            assert node.left.priority <= node.priority
            check_subtree(node.left)
        if node.right:
            assert node.right.key > node.key
            assert node.right.priority <= node.priority
            check_subtree(node.right)
        return True

    assert check_subtree(tree.root)
