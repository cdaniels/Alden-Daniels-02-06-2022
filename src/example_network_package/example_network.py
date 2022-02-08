# example graph object

class Graph:
    def __init__(self):
        self.nodes_dict = {}
        self.edges_dict = {}

    def add_node(self, node_value):
        self.nodes_dict[node_value] = {}

    def add_nodes_from(self, node_list):
        for node_value in node_list:
            if type(node_value) == tuple:
                self.nodes_dict[node_value[0]] = node_value[1]
            elif type(node_value) == int:
                self.nodes_dict[node_value] = {}

    def nodes(self):
        node_list = list(self.nodes_dict.keys())
        return node_list


    def edges(self):
        node_list = list(self.edges_dict.keys())
        return node_list

    def node_data(self, node_num):
        return self.nodes_dict[node_num]


