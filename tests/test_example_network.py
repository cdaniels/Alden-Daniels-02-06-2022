# test_example_network.py

import unittest, random, string

from src.example_network_package import example_network

def random_word(length):
   letters = string.ascii_lowercase
   rand_word = ''.join(random.choice(letters) for i in range(length))
   return rand_word

class TestExampleNetwork(unittest.TestCase):
    def test_graph_instantiation(self):
        # given the graph class, when it is instantiated
        graph = example_network.Graph()
        # it should have an empty array of nodes and edges
        self.assertEqual(list(graph.nodes), [])
        # self.assertEqual(graph.edges, [])


    def test_node_creation(self):
        # given the node creation funtion is called with a certain number
        num = random.randint(1,100)
        G = example_network.Graph()

        G.add_node(num)
        # when the nodes are checked
        nodes = G.nodes()
        # then there should be a node with the corresponding number
        self.assertEqual(nodes, [num])
        self.assertEqual(list(G.nodes), [num])


    def test_batch_node_creation(self):
        # given an array of numbers of a certain length
        rand_length = random.randint(1,100)
        node_list = []
        for i in range(rand_length):
            node_list.append(i)

        # when the batch node creation function is called with this array
        G = example_network.Graph()
        G.add_nodes_from(node_list)

        # then the graph should contain nodes with the corresponding numbers
        nodes = G.nodes
        self.assertCountEqual(nodes, node_list)


    def test_batch_node_creation_with_attributes(self):
        # given an array of number-attribute tuples of a certain length
        rand_length = random.randint(1,100)
        node_list = []
        test_num = random.randint(1,100)
        test_attr_name = random_word(5)
        test_attr_val = random_word(5)

        for i in range(rand_length):
            rand_attr_name = random_word(5)
            rand_attr_val = random_word(5)
            node_attr_tuple = (i, {rand_attr_name: rand_attr_val})
            node_list.append(node_attr_tuple)
        node_attr_tuple = (test_num, {test_attr_name: test_attr_val})
        node_list.append(node_attr_tuple)

        # when the batch node creation function is called with this array
        G = example_network.Graph()
        G.add_nodes_from(node_list)

        # then the graph should contain nodes with data corresponding to what was passed
        node_data = G.nodes.data()
        self.assertEqual(node_data[test_num][test_attr_name], test_attr_val)
        self.assertEqual(G.nodes[test_num][test_attr_name], test_attr_val)


    def test_node_checking_fails_for_non_existent_node(self):
        # given an empty graph and any number representing a node id
        G = example_network.Graph()
        num = random.randint(1,100)

        # when the graph is checked for a node with the corresponding id
        graph_has_node = G.has_node(num)
        # then the check should come back negative
        self.assertEqual(graph_has_node, False)


    def test_node_checking_passes_for_present_node(self):
        # given a graph containing a node with a certain id
        num = random.randint(1,100)
        G = example_network.Graph()
        G.add_node(num)

        # when the graph is checked for a node with the corresponding id
        graph_has_node = G.has_node(num)
        # then the check should come back positive
        self.assertEqual(graph_has_node, True)


    def test_edge_creation(self):
        # given a graph with two nodes and a tuple containing the ids of the nodes 
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G = example_network.Graph()
        G.add_nodes_from([start_node, end_node])
        edge = (start_node, end_node)

        # when the edge creation function is called with this
        G.add_edge(edge)
        # then the graph should now contain a corresponding edge
        edge_list = [e for e in G.edges]
        self.assertEqual(edge_list, [edge])


    def test_batch_edge_creation(self):
        # given an array of tuples representing edges for a graph
        rand_length = random.randint(1,100)
        edge_list = []
        for i in range(rand_length):
            start_node = i
            end_node = random.randint(1,100)
            edge_tuple = (start_node, end_node)
            edge_list.append(edge_tuple)

        # when the batch edge creation function is called with this array
        G = example_network.Graph()
        G.add_edges_from(edge_list)

        # then the graph should contain edges with the corresponding tuples
        edges = G.edges
        self.assertCountEqual(edges, edge_list)


    def test_batch_edge_creation_with_attributes(self):
        # given an array of start_node-end_node-attribute tuples
        rand_length = random.randint(1,100)
        edge_list = []

        test_attr_name = random_word(5)
        test_attr_val = random_word(5)
        test_start_node = random.randint(1,100)
        test_end_node = random.randint(1,100)
        test_attr_tuple = (test_start_node, test_end_node, {test_attr_name: test_attr_val})

        for i in range(rand_length):
            start_node = i
            end_node = random.randint(1,100)
            rand_attr_name = random_word(5)
            rand_attr_val = random_word(5)
            edge_attr_tuple = (start_node, end_node, {rand_attr_name: rand_attr_val})
            edge_list.append(edge_attr_tuple)
        edge_list.append(test_attr_tuple)

        # when the batch edge creation function is called with this array
        G = example_network.Graph()
        G.add_edges_from(edge_list)

        # then the graph should contain edges with data corresponding to what was passed
        self.assertIn(test_attr_tuple, [e for e in G.edges])

    def test_edge_creation_creates_dependent_nodes(self):
        # given an empty graph and a tuple containing the ids of two nodes 
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        edge = (start_node, end_node)

        # when the edge creation function is called with this
        G.add_edge(edge)
        # then the graph should now contain both nodes
        nodes_in_graph = G.nodes()
        given_nodes = [start_node, end_node]
        self.assertEqual(nodes_in_graph, given_nodes)

    # def test_node_removal(self):
    #     return self.fail("test not yet implemented")

    # def test_non_existent_node_removal_raises_error(self):
    #     return self.fail("test not yet implemented")

    # def test_batch_node_removal(self):
    #     return self.fail("test not yet implemented")

    # def test_edge_removal(self):
    #     return self.fail("test not yet implemented")

    # def test_non_existent_edge_removal_raises_error(self):
    #     return self.fail("test not yet implemented")

    # def test_batch_edge_removal(self):
    #     return self.fail("test not yet implemented")

    # def test_node_removal_removes_dependent_edges(self):
    #     return self.fail("test not yet implemented")

    # def test_set_node_attribute(self):
    #     return self.fail("test not yet implemented")

    # def test_set_node_attributes(self):
    #     return self.fail("test not yet implemented")

    # def test_set_edge_attribute(self):
    #     return self.fail("test not yet implemented")

    # def test_set_edge_ettributes(self):
    #     return self.fail("test not yet implemented")

    # def test_plot_opens_window(self):
    #     return self.fail("test not yet implemented")


if __name__ == '__main__':
    unittest.main()

