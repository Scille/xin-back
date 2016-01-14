class Tree:

    """
    Tree can be used to represent a tree of object ::

        >>> t = Tree({
        ...     'node_1': ('leaf_1_1', 'leaf_1_2'),
        ...     'node_2': ('leaf_2_1', {node_2_2': ('leaf_2_2_1', 'leaf_2_2_2')}),
        ... })
        ...
        >>> t.node_1.leaf_1_1
        'node_1.leaf_1_1'
        >>> t.node_1.node_2_2.leaf_2_2_1
        'node_1.node_2_2.leaf_2_2_1'

    Each node in the tree is a Tree object, each leaf is build
    using :method:`build_leaf`

    Tree can be used as an iterable to walk the leafs recursively

        >>> len(t)
        5
        >>> [x for x in t]
        ['node_1.leaf_1_1', 'node_1.leaf_1_2', 'node_2.leaf_2_1',
         'node_2.node_2_2.leaf_2_2_1', 'node_2.node_2_2.leaf_2_2_2']
    """

    def __init__(self, nodes, basename=''):
        self.nodes = []
        if basename:
            make = lambda *args: basename + '.' + '.'.join(args)
        else:
            make = lambda *args: '.'.join(args)
        if isinstance(nodes, dict):
            for key, value in nodes.items():
                self._set_leaf(key, self.__class__(value, make(key)))
        elif isinstance(nodes, (tuple, list, set)):
            for node in nodes:
                if isinstance(node, str):
                    self._set_leaf(node, self.build_leaf(make(node)))
                elif isinstance(node, dict):
                    for key, value in node.items():
                        self._set_leaf(key, self.__class__(value, make(key)))
                else:
                    raise ValueError('Bad node type' % node)
        elif isinstance(nodes, str):
            self._set_leaf(nodes, self.build_leaf(make(nodes)))
        else:
            raise ValueError('Bad node type' % nodes)

    def build_leaf(self, route):
        return route

    def _set_leaf(self, key, value):
        setattr(self, key, value)
        self.nodes.append(value)

    def __iter__(self):
        for node in self.nodes:
            if isinstance(node, Tree):
                for sub_node in node:
                    yield sub_node
            else:
                yield node

    def __len__(self):
        return len([e for e in self])

    def __getitem__(self, i):
        return [e for e in self][i]

    def __str__(self):
        return str([e for e in self])
