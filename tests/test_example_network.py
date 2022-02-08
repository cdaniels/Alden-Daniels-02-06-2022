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
        self.assertEqual(graph.nodes(), [])
        self.assertEqual(graph.edges(), [])


    def test_node_creation(self):
        # given the node creation funtion is called with a certain number
        num = random.randint(1,100)
        G = example_network.Graph()

        G.add_node(num)
        # when the nodes are checked
        nodes = G.nodes()
        # then there should be a node with the corresponding number
        self.assertEqual(nodes, [num])


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
        nodes = G.nodes()
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
        node_data = G.node_data(test_num)
        self.assertEqual(node_data[test_attr_name], test_attr_val)
        self.assertEqual(G.nodes_data()[test_num][test_attr_name], test_attr_val)

if __name__ == '__main__':
    unittest.main()

