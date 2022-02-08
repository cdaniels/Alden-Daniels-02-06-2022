# example graph object

class Graph:
    def __init__(self):
        self.nodes = list([])
        self.edges = list([])

    def add_node(self, node_value):
        self.nodes.append(node_value)

    def add_nodes_from(self, node_list):
        for node_value in node_list:
            self.nodes.append(node_value)
