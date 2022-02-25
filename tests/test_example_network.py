# test_example_network.py

import unittest, random, string, math, sys

sys.path.append('.')
sys.path.append('./src')

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
        self.assertEqual(list(graph.edges), [])


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

    def test_node_creation_with_attributes(self):
        # given an empty graph, a random number, and a collection of keyword values pairs
        G = example_network.Graph()
        test_num = random.randint(1,100)
        attr1_val = random_word(5)
        attr2_val = random_word(5)

        # when a node is added with this number as an id and these keywords assigned to the values
        G.add_node(test_num, attr1_key=attr1_val, attr2_key=attr2_val)

        # then the graph should contain a node with data corresponding to what was passed
        node_data = G.nodes.data()
        self.assertEqual(node_data[test_num]["attr1_key"], attr1_val)
        self.assertEqual(G.nodes[test_num]["attr1_key"], attr1_val)
        self.assertEqual(node_data[test_num]["attr2_key"], attr2_val)
        self.assertEqual(G.nodes[test_num]["attr2_key"], attr2_val)


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
        G.add_edge(start_node, end_node)
        # then the graph should now contain a corresponding edge
        edge_list = [e for e in G.edges]
        self.assertEqual(edge_list, [edge])


    def test_edge_creation_with_attributes(self):
        # given a graph with two nodes and a tuple containing the ids of the nodes along with a collection of key value pairs
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G = example_network.Graph()
        G.add_nodes_from([start_node, end_node])
        attr1_val = random_word(5)
        attr2_val = random_word(5)

        # when the edge creation function is called with this
        G.add_edge(start_node, end_node, attr1_key=attr1_val, attr2_key=attr2_val)

        # then the graph should contain edges with data corresponding to what was passed
        edge_data = G.get_edge_data(start_node, end_node)
        self.assertEqual(edge_data["attr1_key"], attr1_val)
        self.assertEqual(edge_data["attr2_key"], attr2_val)


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


    def test_edge_checking_fails_for_non_existent_node(self):
        # given a graph containing two nodes without any edge between them
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G.add_node(start_node)
        G.add_node(end_node)

        # when the graph is checked for a edge with the corresponding node ids
        edge_tuple = (start_node, end_node)
        graph_has_edge = G.has_edge(edge_tuple)
        # then the check should come back negative
        self.assertEqual(graph_has_edge, False)


    def test_edge_checking_passes_for_present_edge(self):
        # given a graph containing an edge between two nodes
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G.add_edge(start_node, end_node)

        # when the graph is checked for an edge with the corresponding node ids
        edge_tuple = (start_node, end_node)
        graph_has_edge = G.has_edge(edge_tuple)
        # then the check should come back positive
        self.assertEqual(graph_has_edge, True)


    def test_edge_checking_passes_for_present_edge_with_attributes(self):
        # given a graph containing an edge between two nodes
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        attr_val = random_word(5)
        G.add_edge(start_node, end_node, attr=attr_val)

        # when the graph is checked for an edge with the corresponding node ids
        edge_tuple = (start_node, end_node)
        graph_has_edge = G.has_edge(edge_tuple)
        # then the check should come back positive
        self.assertEqual(graph_has_edge, True)

    def test_edge_creation_creates_dependent_nodes(self):
        # given an empty graph and a tuple containing the ids of two nodes 
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)

        # when the edge creation function is called with this
        G.add_edge(start_node, end_node)
        # then the graph should now contain both nodes
        nodes_in_graph = G.nodes()
        given_nodes = [start_node, end_node]
        self.assertEqual(nodes_in_graph, given_nodes)

    def test_node_removal(self):
        # given a graph containing a node with a certain id
        num = random.randint(1,100)
        G = example_network.Graph()
        G.add_node(num)

        # when the node removal function is called with this id
        G.remove_node(num)
        # then the graph should now be empty
        nodes = G.nodes()
        self.assertCountEqual(nodes, [])

    def test_non_existent_node_removal_raises_error(self):
        # given a graph containing no nodes and a number representing a node id
        num = random.randint(1,100)
        G = example_network.Graph()

        # when the node removal function is called with this id
        # then an error should be thrown
        self.assertRaises(ValueError, G.remove_node, num)

    def test_batch_node_removal(self):
        # given a graph with nodes and an array containing a subset of these node's ids
        rand_length = random.randint(4,100)
        node_list = []
        for i in range(rand_length):
            node_list.append(i)
        G = example_network.Graph()
        G.add_nodes_from(node_list)
        sub_list_end = math.floor(rand_length/2)
        nodes_to_remove = node_list[0:sub_list_end]

        # when the batch node removal function is called with this array
        G.remove_nodes_from(nodes_to_remove)

        # then the graph should not contain nodes with the corresponding numbers
        nodes = G.nodes()
        for node_to_remove in nodes_to_remove:
            self.assertNotIn(node_to_remove, nodes)

    def test_edge_removal(self):
        # given a graph containing an edge between two with certain ids 
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G.add_edge(start_node, end_node)

        # when the edge removal function is called with this pair of ids
        G.remove_edge(start_node, end_node)
        # then the graph should now be empty
        edges = G.edges()
        self.assertCountEqual(edges, [])

    def test_non_existent_edge_removal_raises_error(self):
        # given a graph containing nodes with no edges
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G.add_node(start_node)
        G.add_node(end_node)

        # when the edge removal function is called with this id
        # then an error should be thrown
        self.assertRaises(ValueError, G.remove_edge, start_node, end_node)

    def test_batch_edge_removal(self):
        # given a graph with edges and an array containing a subset of these edge tuples
        rand_length = random.randint(1,100)
        edge_list = []
        for i in range(rand_length):
            start_node = i
            end_node = random.randint(1,100)
            edge_tuple = (start_node, end_node)
            edge_list.append(edge_tuple)
        G = example_network.Graph()
        G.add_edges_from(edge_list)

        sub_list_end = math.floor(rand_length/2)
        edges_to_remove = edge_list[0:sub_list_end]

        # when the batch edge removal function is called with this array
        G.remove_edges_from(edges_to_remove)

        # then the graph should not contain edges for the corresponding tuples
        edges = G.edges()
        for edge_to_remove in edges_to_remove:
            self.assertNotIn(edge_to_remove, edges)

    def test_node_removal_removes_dependent_edges(self):
        # given a graph with an edge between nodes with certain starting and ending node ids
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G.add_edge(start_node, end_node)

        # when the node removal function is called with one of the node ids
        G.remove_node(start_node)

        # then any edges which were adjacent to that node should no longer be there
        adjacent_edges = G.edges(start_node)
        edge_tuple = (start_node, end_node)
        self.assertNotIn(edge_tuple, adjacent_edges)

    def test_adjacent_edges_returned_for_node(self):
        # given a graph with an edge between nodes with certain starting and ending node ids
        G = example_network.Graph()
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G.add_edge(start_node, end_node)

        # when the edges are accesed with a certain node id passed in
        adjacent_edges = G.edges(start_node)

        # then the corresponding edge should be returned
        edge_tuple = (start_node, end_node)
        self.assertIn(edge_tuple, adjacent_edges)


    def test_set_node_attribute(self):
        # given a graph containing a node with a certain attribute value
        G = example_network.Graph()
        node_id = random.randint(1,100)
        old_attr_val = random_word(5)
        G.add_node(node_id, attr=old_attr_val)

        # when a new attribute value is assigned to the node
        new_attr_val = random_word(5)
        G.nodes[node_id]["attr"] = new_attr_val

        # then this value should show up on future node queries
        self.assertEqual(G.nodes[node_id]["attr"], new_attr_val)

    def test_set_node_attributes(self):
        # given an array of number-attribute tuples of a certain length
        rand_length = random.randint(1,100)
        node_list = []
        node1_id = random.randint(1,rand_length-1)
        node2_id = random.randint(node1_id,rand_length)
        test_attr_name = random_word(5)
        old_attr_val = random_word(5)

        for i in range(rand_length):
            rand_attr_name = random_word(5)
            rand_attr_val = random_word(5)
            node_attr_tuple = (i, {rand_attr_name: rand_attr_val})
            node_list.append(node_attr_tuple)
        node1_attr_tuple = (node1_id, {test_attr_name: old_attr_val})
        node2_attr_tuple = (node2_id, {test_attr_name: old_attr_val})
        node_list.append(node1_attr_tuple)
        node_list.append(node2_attr_tuple)

        G = example_network.Graph()
        G.add_nodes_from(node_list)

        # when the set node attributes function is called
        new_attr_val = random_word(5)
        attrs = {node1_id: {test_attr_name: new_attr_val}, node2_id: {test_attr_name: new_attr_val}}
        example_network.set_node_attributes(G, attrs)

        # then the graph should contain nodes with data corresponding to what was passed
        node_data = G.nodes.data()
        self.assertEqual(G.nodes[node1_id][test_attr_name], new_attr_val)
        self.assertEqual(G.nodes[node2_id][test_attr_name], new_attr_val)

    def test_set_edge_attribute(self):
        # given a graph with an edge that has an attribute with a certain value
        start_node = random.randint(1,100)
        end_node = random.randint(1,100)
        G = example_network.Graph()
        G.add_nodes_from([start_node, end_node])
        old_attr_val = random_word(5)
        G.add_edge(start_node, end_node, attr=old_attr_val)

        # when a new value is assigned to this edge
        new_attr_val = random_word(5)
        G.edges[start_node, end_node]["attr"] = new_attr_val

        # then this value should show up on future edge queries
        self.assertEqual(G.edges[start_node, end_node]["attr"], new_attr_val)

    def test_set_edge_attributes(self):
        # given an array of start_node-end_node-attribute tuples
        rand_length = random.randint(1,100)
        edge_list = []

        test_attr_name = random_word(5)
        old_attr_val = random_word(5)
        start_node1 = random.randint(1,100)
        start_node2 = random.randint(1,100)
        end_node1 = random.randint(1,100)
        end_node2 = random.randint(1,100)
        edge_tuple_1 = (start_node1, end_node1, {test_attr_name: old_attr_val})
        edge_tuple_2 = (start_node2, end_node2, {test_attr_name: old_attr_val})

        for i in range(rand_length):
            start_node = i
            end_node = random.randint(1,100)
            rand_attr_name = random_word(5)
            rand_attr_val = random_word(5)
            edge_attr_tuple = (start_node, end_node, {rand_attr_name: rand_attr_val})
            edge_list.append(edge_attr_tuple)
        edge_list.append(edge_tuple_1)
        edge_list.append(edge_tuple_2)

        G = example_network.Graph()
        G.add_edges_from(edge_list)

        # when the set node attributes function is called
        new_attr_val = random_word(5)
        attrs = {(start_node1, end_node1): {test_attr_name: new_attr_val}, (start_node2, end_node2): {test_attr_name: new_attr_val}}
        example_network.set_edge_attributes(G, attrs)

        # then the graph should contain edges with data corresponding to what was passed
        self.assertEqual(G.edges[start_node1, end_node1][test_attr_name], new_attr_val)
        self.assertEqual(G.edges[start_node2, end_node2][test_attr_name], new_attr_val)

    # def test_plot_window_calculates_distance_between_nodes(self):


    # def test_plot_opens_window(self):
    #     # given an array of tuples representing edges for a graph
    #     rand_length = random.randint(1,12)
    #     edge_list = []
    #     for i in range(rand_length):
    #         start_node = i
    #         end_node = random.randint(1,100)
    #         edge_tuple = (start_node, end_node)
    #         edge_list.append(edge_tuple)

    #     # when the batch edge creation function is called with this array
    #     G = example_network.Graph()
    #     G.add_edges_from(edge_list)
        
    #     example_network.draw(G)
        
    #     # return self.fail("test not yet implemented")


if __name__ == '__main__':
    unittest.main()

