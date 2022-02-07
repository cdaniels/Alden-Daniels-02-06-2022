# test_example_network.py

import unittest
import random

from src.example_network_package import example_network

class TestExampleNetwork(unittest.TestCase):
    def test_graph_instantiation(self):
        # given the graph class, when it is instantiated
        graph = example_network.Graph()
        # it should have an empty array of nodes and edges
        self.assertEqual(graph.nodes, [])
        self.assertEqual(graph.edges, [])


    def test_node_creation(self):
        # given the node creation funtion is called with a certain number
        num = random.randint(1,100)
        G = example_network.Graph()

        G.add_node(num)
        # when the nodes are checked
        nodes = G.nodes
        # then there should be a node with the corresponding number
        self.assertEqual(nodes, [num])

if __name__ == '__main__':
    unittest.main()

