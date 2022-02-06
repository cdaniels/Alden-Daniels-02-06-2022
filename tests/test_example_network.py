# test_example_network.py

import unittest
from src.example_network_package import example_network

class TestExampleNetwork(unittest.TestCase):
    def test_graph_instantiation(self):
        # given the graph class, when it is instantiated
        graph = example_network.Graph()
        # it should have an empty array of nodes and edges
        self.assertEqual(graph.nodes, [])
        self.assertEqual(graph.edges, [])

if __name__ == '__main__':
    unittest.main()

