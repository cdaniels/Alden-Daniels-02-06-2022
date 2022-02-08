# example graph object

class Graph:
    def __init__(self):
        self.nodes = NodeView()
        self.edges_dict = {}

    def add_node(self, node_value):
        self.nodes[node_value] = {}

    def add_nodes_from(self, node_list):
        for node_value in node_list:
            if type(node_value) == tuple:
                self.nodes[node_value[0]] = node_value[1]
            elif type(node_value) == int:
                self.nodes[node_value] = {}

    def node_data(self, node_num):
        return self.nodes[node_num]

class NodeView(dict):
    def __init__(self):
        self._nodes = list([])

    def __call__(self):
        node_list = list(self.keys())
        return node_list

    def __delitem__(self, key):
        super().pop(key)
        self._nodes.remove(key)

    def __setitem__(self, key, value):
        self._nodes.append(key)
        super().__setitem__(key, value)

    def __iter__(self):
        return NodeViewIterator(self)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"

    def data(self):
        return self

class NodeViewIterator:
    def __init__(self, node_view):
        self._index = 0
        self._node_view = node_view

    def __next__(self):
        if(self._index < len(self._node_view._nodes)):
            item = self._node_view._nodes[self._index]
            self._index += 1
            return item
        raise StopIteration


# class NodeDataView:
#     def __init__(self):
