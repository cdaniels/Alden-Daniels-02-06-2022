# example graph object

class Graph:
    def __init__(self):
        self.nodes = list([])
        self.edges = list([])

    def add_node(self, node_value):
        self.nodes.append(node_value)

