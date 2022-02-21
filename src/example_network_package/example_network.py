# example graph object

def set_node_attributes(G, attributes):
    for node in attributes.keys():
        G.nodes[node] = attributes[node]

class Graph:
    def __init__(self):
        self.nodes = NodeView()
        self.edges = EdgeView()

    def add_node(self, node_value, **attributes):
        self.nodes[node_value] = attributes

    def add_edge(self, start_node, end_node, **attributes):
        if not self.has_node(start_node):
            self.add_node(start_node)
        if not self.has_node(end_node):
            self.add_node(end_node)
        edge_tuple = (start_node, end_node)
        self.edges[edge_tuple] = attributes

    def add_nodes_from(self, node_list):
        for node_value in node_list:
            if type(node_value) == tuple:
                self.nodes[node_value[0]] = node_value[1]
            elif type(node_value) == int:
                self.nodes[node_value] = {}

    def add_edges_from(self, edge_list):
        for edge_tuple in edge_list:
            if type(edge_tuple) == tuple:
                start_node = edge_tuple[0]
                end_node = edge_tuple[1]
                node_tuple = (start_node, end_node)
                attribute_dict = {}
                if(len(edge_tuple) > 2):
                    attribute_dict = edge_tuple[2]
                self.add_edge(start_node, end_node, **attribute_dict)

    def has_node(self, node_value):
        graph_has_node = False
        for n in self.nodes:
            if n == node_value:
                graph_has_node = True
        return graph_has_node

    def has_edge(self, edge_tuple):
        graph_has_edge = False
        for e in self.edges:
            if e == edge_tuple:
                graph_has_edge = True
        return graph_has_edge

    def remove_node(self, node_value):
        # if a corresponding node is found remove that node
        if self.has_node(node_value):
            del self.nodes[node_value]
            # remove dependent edges
            for edge in self.edges(node_value):
                del self.edges[edge]
        else:
            # raise an error if no node is found
            raise ValueError

    def remove_nodes_from(self, node_list):
        for node in node_list:
            self.remove_node(node)


    def remove_edge(self, start_node, end_node):
        if self.has_node(start_node) and self.has_node(end_node):
            edge_tuple = (start_node, end_node)
            if self.has_edge(edge_tuple):
                del self.edges[edge_tuple]
            else:
                raise ValueError
        else:
            raise ValueError

    def remove_edges_from(self, edge_list):
        for edge in edge_list:
            if type(edge) == tuple:
                start_node = edge[0]
                end_node = edge[1]
                self.remove_edge(start_node, end_node)

    def node_data(self, node_num):
        return self.nodes[node_num]

    def get_edge_data(self, start_node, end_node):
        edge_tuple = (start_node, end_node)
        return self.edges[edge_tuple]

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


class EdgeView(dict):
    def __init__(self):
        self._edges = list([])

    def __call__(self, node=None):
        edge_list = list(self.keys())
        if node is not None:
            return list([e for e in edge_list if node in e])
        else:
            return edge_list

    def __delitem__(self, key):
        super().pop(key)
        self._edges.remove(key)

    def __setitem__(self, key, value):
        self._edges.append(key)
        super().__setitem__(key, value)

    def __iter__(self):
        return EdgeViewIterator(self)

    def __repr__(self):
        return f"{type(self).__name__}({super().__repr__()})"

    def data(self):
        return self

class EdgeViewIterator:
    def __init__(self, edge_view):
        self._index = 0
        self._edge_view = edge_view

    def __next__(self):
        if(self._index < len(self._edge_view._edges)):
            item = self._edge_view._edges[self._index]
            self._index += 1
            attributes_dict = self._edge_view[item]
            edge_tuple = ()
            if(len(attributes_dict.keys()) > 0) :
                edge_tuple = (item[0], item[1], attributes_dict)
            else:
                edge_tuple = (item[0], item[1])
            return edge_tuple
        raise StopIteration


# class NodeDataView:
#     def __init__(self):
