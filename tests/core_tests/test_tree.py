from xin_back.tree import Tree
from collections import OrderedDict
import pytest


def test_empty_tree():
    tree = Tree({})
    assert 0 == len(tree)


def test_one_node_tree():
    tree = Tree({'Root'})
    assert 1 == len(tree)
    assert 'Root' == tree.Root


def test_complete_Tree():
    tree = Tree({'node_1': ('leaf_1_1', 'leaf_1_2'), 'node_2': (
        'leaf_2_1', {'node_2_2': ('leaf_2_2_1', 'leaf_2_2_2')})
    })
    assert 5 == len(tree)
    assert 'node_1.leaf_1_1' == tree.node_1.leaf_1_1
    assert 'node_2.node_2_2.leaf_2_2_1' == tree.node_2.node_2_2.leaf_2_2_1


def test_one_node_tree_basenamed():
    tree = Tree({'Root'}, 'test')
    assert 1 == len(tree)
    assert 'test.Root' == tree.Root
    assert 'test.Root' == tree[0]


def test_complete_Tree_basenamed():
    tree = Tree(OrderedDict({'node_1': ('leaf_1_1', 'leaf_1_2'),
                             'node_2': ('leaf_2_1', {'node_2_2': ('leaf_2_2_1', 'leaf_2_2_2')}),
                             }), 'test')
    assert 5 == len(tree)
    assert 'test.node_1.leaf_1_1' == tree.node_1.leaf_1_1


def test_nodes_type_str():
    tree = Tree("node1.leaf_1.leaf_1_1")
    assert 1 == len(tree)
    assert "['node1.leaf_1.leaf_1_1']" == str(tree)


def test_bad_node_type():
    class Test:

        def __init__(self):
            self.node = "leaf"

    with pytest.raises(ValueError):
        tree = Tree(OrderedDict({'node_1': ('leaf_1_1', 'leaf_1_2'),
                                 'node_2': ('leaf_2_1', {'node_2_2': ('leaf_2_2_1', Test())}),
                                 }), 'test')


def test_bad_nodes_type():
    tree = Tree(OrderedDict({'node_1': ('leaf_1_1', 'leaf_1_2'),
                             'node_2': ('leaf_2_1', {'node_2_2': ('leaf_2_2_1')}),
                             }), 'test')
    with pytest.raises(ValueError):
        copy_tree = Tree(tree)
