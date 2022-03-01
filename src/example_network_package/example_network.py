# example graph object

import math, copy, time, random
from tkinter import *

def set_node_attributes(G, attributes):
    """Set multiple node attributes at the same time

    Args:
        G (Graph): a Graph object containing nodes and edges
        attributes (dict): dictionary with key-value pairs for attribute assignment
    """
    for node in attributes.keys():
        G.nodes[node] = attributes[node]

def set_edge_attributes(G, attributes):
    """Set multiple edge attributes at the same time

    Args:
        G (Graph): a Graph object containing nodes and edges
        attributes (dict): dictionary with key-value pairs for attribute assignment
    """
    for edge in attributes.keys():
        G.edges[edge] = attributes[edge]

def draw(G):
    """Create a Tkinter window with a plot displaying 
    nodes as circles and edges as connecting line segments for the given Graph, or Graph subclass
    DiGraphs will be displayed with arrows instead of line segments
    MultiGraphs will be displayed with multiple offset line segments for the multiples edges
    and MultiDiGraphs will be displayed with multiple offset arrows


    Args:
        G (Graph): a Graph object containing nodes and edges
    """
    # init tk
    root = Tk()
    window = PlotWindow(root, 800, 600, G)
    window.animate()
    root.mainloop()

class PlotWindow:
    """ Window for displaying a visual representation of a Graph object
    """
    def __init__(self, master, width, height, G):
        """initialize the plot window

        Args:
            master (tkinter): the tkinter window which acts as the root for this window
            width (int): the width of the window
            height (int): the height of the window
            G (Graph): a Graph object containing nodes and edges
        """
        self.root = master
        self.w, self.h = width, height
        self.canvas = Canvas(self.root, bg="white", height=self.h, width=self.w)
        self.graph = copy.copy(G)

        self.node_radius = 15

        self.refresh_rate = 0.01 # in seconds
        self.global_repulsie_f = -1.0 # force to repel all nodes to each other
        self.edge_attractive_f = 2.0 # force to attract adjacent nodes

        self.node_dist_max_threshold = self.h * 0.4 # maximum distance for nodes to seperate
        self.node_dist_min_threshold = self.node_radius * 4 # maximum distance for nodes to seperate
        self.center_dist_max_threshold = self.h * 0.4 # maximum distance for nodes to seperate
    
        self.plot_graph(self.graph)
        self.canvas.pack()


    def animate(self, seconds):
        """Run an animation loop for the specified number of seconds
        Durring the loop node dynamics will be calculated and the node positions will
        be modified
        
        Args:
            seconds (int): the number of seconds to run the animation for
        """
        G = self.graph
        start_time = time.time()
        while (time.time() - start_time < seconds):
            self.increment_dynamics()
            time.sleep(self.refresh_rate)

    def increment_dynamics(self):
        """ increment the graph dinamics forword by one timestep
        this calculates the amount that each node should be moved by and
        sends calls to move them accordingly
        """
        G = self.graph
        for start_node in G.nodes:
            for end_node in G.nodes:
                if start_node != end_node:
                    move_vec = self.calculate_move_vec_between_nodes(start_node, end_node);
                    self.move_node_plot_by_vec(start_node, move_vec)

    def calculate_move_vec_between_nodes(self, start_node, end_node):
        """Calculate the vector which indicates the amount which one node should 
        be moved by relative to another node

        Args:
            start_node (int): the id of the node to be moved
            end_node (int): the id of the node the movement is calculated relative to

        Returns:
            tuple: a tuple representing the movement vector
        """
        G = self.graph
        start_point = G.nodes[start_node]["_plot_position"]
        end_point = G.nodes[end_node]["_plot_position"]

        center_point = (self.w/2, self.h/2)
        center_vec = self.get_vec_between_points(start_point, center_point)
        center_dist = self.abs_len_of_vec(center_vec)

        sep_vec = self.get_vec_between_points(start_point, end_point)
        sep_dist = self.abs_len_of_vec(sep_vec)
        norm_sep_vec = self.normalize_vec(sep_vec)
        repulse = self.multiply_vec_by_scalar(norm_sep_vec, self.global_repulsie_f)
        attract = self.multiply_vec_by_scalar(norm_sep_vec, self.edge_attractive_f)

        # apply general forces if seperation vector is below max threshold and above min threshold
        move_vec = [0,0]
        if sep_dist < self.node_dist_max_threshold and center_dist < self.center_dist_max_threshold:
            move_vec = self.add_vec_to_vec(move_vec, repulse)
        if sep_dist > self.node_dist_min_threshold and (G.has_edge((start_node, end_node)) or G.has_edge((end_node, start_node))):
            move_vec = self.add_vec_to_vec(move_vec, attract)
        return tuple(move_vec)

    def move_node_plot_by_vec(self, node_id, move_vec):
        """Move a certain nodes plotted circle by the given move vector

        Args:
            node_id (int): the id of the node to be moved
            move_vec (tuple): a tuple representing the node movement
        """
        G = self.graph
        circ = G.nodes[node_id]["_plot_circle_id"]
        label = G.nodes[node_id]["_plot_label_id"]
        self.canvas.move(circ, move_vec[0], move_vec[1])
        self.canvas.move(label, move_vec[0], move_vec[1])

        for edge in G.edges(node_id):
            if(issubclass(type(G), MultiGraph)):
                edge_data = G[node_id][edge]
                for data in edge_data:
                    self.update_edge_plot(node_id, edge, data)
            else:
                self.update_edge_plot(edge[0], edge[1])

        self.root.update()

    def multiply_vec_by_scalar(self, vec, scalar):
        """Multiply the given vector by a scalar value

        Args:
            vec (tuple): a tuple representing a vector
            scalar (float): a scalar value to multiply the vector by

        Returns:
            tuple: the tuple representing the resultant vector after scalar multiplication
        """
        return tuple(list(map(lambda x: x * scalar, vec)))

    def add_vec_to_vec(self, vec1, vec2):
        """Add one vector to another vector

        Args:
            vec1 (tuple): a tuple representing one vector
            vec2 (tuple): a tuple representing another vector

        Returns:
            tuple: the tuple representing the vector sum
        """
        sum_vec = (0, 0)
        sum_vec[0] = vec1[0] + vec2[0]
        sum_vec[1] = vec1[1] + vec2[1]
        return sum_vec

    def abs_len_of_vec(self, vec):
        """Calculate the absolute length of the given vector (its magnitude)

        Args:
            vec (tulpe): a tuple representing a vector

        Returns:
            float: a number representing the magnitude of the given vector
        """
        tot = 0
        for elem in vec:
            tot = tot + elem**2
        return math.sqrt(tot)

    def update_edge_plot(self, start, end, edge_index=None):
        """Update the line segment plot for the edge corresponding with the given node ids

        Args:
            start (int): the id of the starting node
            end (int): the id of the ending node
            edge_index (int, optional): the id of the edge (for the case of MultiGraphs). Defaults to None.
        """
        G = self.graph
        start_circ = G.nodes[start]["_plot_circle_id"]
        start_coords = self.canvas.coords(start_circ)
        end_circ = G.nodes[end]["_plot_circle_id"]
        end_coords = self.canvas.coords(end_circ)
        r = self.node_radius

        if issubclass(type(self.graph), MultiGraph) and edge_index != None:
            r = r + random.randint(-4,4)
            x1 = start_coords[0] + r
            y1 = start_coords[1] + r
            x2 = end_coords[0] + r
            y2 = end_coords[1] + r
            in_edge_tuple = (start, end, edge_index)
            out_edge_tuple = (end, start, edge_index)
            if in_edge_tuple in G.edges:
                line = G.edges[in_edge_tuple]["_plot_line_id"]
                self.canvas.coords(line, x1, y1, x2, y2)
            elif out_edge_tuple in G.edges:
                line = G.edges[out_edge_tuple]["_plot_line_id"]
                self.canvas.coords(line, x1, y1, x2, y2)
        else:
            x1 = start_coords[0] + r
            y1 = start_coords[1] + r
            x2 = end_coords[0] + r
            y2 = end_coords[1] + r
            line = G.edges[(start, end)]["_plot_line_id"]
            self.canvas.coords(line, x1, y1, x2, y2)
        self.root.update()

    def get_vec_between_points(self, start_point, end_point):
        """Get a vector between two points

        Args:
            start_point (tuple): a tuple representing one points x,y position
            end_point (tuple): a tuple representing another points x,y position

        Returns:
            tuple: a tuple representing the difference vector between thes two points
        """
        x1 = start_point[0]
        y1 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]
        vec = (x2-x1, y2-y1)
        return vec
    
    def normalize_vec(self, vec):
        """Normalize the given vector 
        scaling it so its elements sum to one

        Args:
            vec (tuple): a tuple representing a vector

        Returns:
            tuple: a tuple representing the normalized vector
        """
        vec_mag = self.abs_len_of_vec(vec)
        norm_vec = self.multiply_vec_by_scalar(vec, 1/vec_mag)
        return norm_vec

    def plot_graph(self, G):
        """PLot the given graph
        creating visual displays for its nodes and edges

        Args:
            G (Graph): the graph to be displayed
        """

        # add plot positions for all the nodes in the graph
        self.add_plot_positions_to_graph(G)

        # get coordinates for each node and draw a circle at those coordinates
        for node_id in G.nodes:
            self.draw_node(node_id)
        # for each edge draw a line between its corresponding nodes
        if  issubclass(type(self.graph), MultiGraph):
            for edge in G.edges:
                start_node = edge[0]
                end_node = edge[1]
                edge_index = edge[2]
                if "_plot_line_id" not in G.edges[start_node, end_node, edge_index]:
                    start_point = G.nodes[start_node]["_plot_position"]
                    end_point = G.nodes[end_node]["_plot_position"]
                    line = self.draw_line(start_point, end_point)
                    G.edges[start_node, end_node, edge_index]["_plot_line_id"] = line

        else:
            for edge in G.edges:
                start_node = edge[0]
                end_node = edge[1]
                if "_plot_line_id" not in G.edges[start_node, end_node]:
                    start_point = G.nodes[start_node]["_plot_position"]
                    end_point = G.nodes[end_node]["_plot_position"]
                    line = self.draw_line(start_point, end_point)
                    G.edges[start_node, end_node]["_plot_line_id"] = line

    def add_plot_positions_to_graph(self, G):
        """Add metadata to the given Graph to keep track of the plotted positions
        of nodes

        Args:
            G (Graph): the Graph to be modified
        """
        # get number of nodes in graph
        node_num = len(G.nodes)

        # get the coordinates for vertices of a regular n-gon of this size around the center of the canvas
        # center = (math.floor(self.canvas.winfo_width()/2), math.floor(self.canvas.winfo_width()/2)
        center = (self.w/2, self.h/2)
        radius = self.h * 0.4
        coords = self.get_regular_polygon_coords(center, radius, node_num)
        # for each node in the graph give it the coordinates of one of the n-gon vertices
        for node_id in G.nodes:
            x, y = next(coords)
            G.nodes[node_id]["_plot_position"] = (x,y)

    def draw_node(self, node_id):
        """Draw a visual representation for the given node
        a circle is drawn on the window at the nodes location
        and a label is drawn on the circle corresponding with the nodes id

        Args:
            node_id (int): the id of the node to be displayed
        """
        # expand the coordinates
        x, y = self.graph.nodes[node_id]["_plot_position"]
        r = self.node_radius
        # draw a circle at the desired location
        circ = self.draw_circle(x, y, r)
        # then create text for the node id at the same location 
        label = self.draw_text(x, y, math.floor(r*0.7), node_id)
        self.graph.nodes[node_id]["_plot_circle_id"] = circ
        self.graph.nodes[node_id]["_plot_label_id"] = label

    def draw_text(self, x, y, size, text):
        """Draw the given text on the canvas at the given position

        Args:
            x (float): the horizontal position on the canvas to draw the text
            y (float): the vertical position on the canvas to draw the text
            size (float): the point size to use when displaying the text
            text (string): the text to draw

        Returns:
            int: the tkinter object id of the drawn text
        """
        font = 'Helvetica ' + str(size) + ' bold'
        return self.canvas.create_text(x, y, text=text, fill="black", font=(font))

    def draw_circle(self, x, y, r):
        """Draw a circle on the canvas at the given position

        Args:
            x (float): the horizontal position on the canvas to draw the text
            y (float): the vertical position on the canvas to draw the text
            r (float): the radius of the circle to draw

        Returns:
            int: the tkinter object id of the drawn circle
        """
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0,y0,x1,y1)

    def draw_line(self, start_point, end_point):
        """Draw a line on the canvas between the given points

        Args:
            start_point (tuple): a tuple representing one point
            end_point (tuple): a tuple representing another point

        Returns:
            int: the tkinter object id of the drawn line
        """
        x1 = start_point[0] 
        y1 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]
        if(issubclass(type(self.graph), DiGraph)):
            return self.canvas.create_line(x1, y1, x2, y2, arrow=LAST)
        else:
            return self.canvas.create_line(x1, y1, x2, y2)

    def get_regular_polygon_coords(self, center, radius, n):
        """Get the coordinates corresponding with vertices of a regular n-gon

        Args:
            center (tuple): a tuple representing the center of the n-gon
            radius (float): a number representing the radius of the n-gon
            n (int): the number of sides the n-gon should have (its what puts the n in)

        Returns:
            array[tuple]: an array containg tuples which represent the vertices
        """
        coord_list = []
        for i in range(n):
            x = math.floor(center[0] + radius * math.sin((2*math.pi/n) * i))
            y = math.floor(center[1] + radius * math.cos((2*math.pi/n) * i))
            coord = (x,y)
            coord_list.append(coord)
        return iter(coord_list)

class Graph:
    """_A graph containg nodes and edges with metadata
    """
    def __init__(self):
        """initialize the graph
        create a NodeView and EdgeView to represent its nodes and edges
        """
        self.nodes = NodeView()
        self.edges = EdgeView()

    def __getitem__(self, item):
        """Controls the subscript behavior of the object 
        what happens when it is passed an integer such as G[1]

        Args:
            item (int): the subscript representing a node id

        Returns:
            list: a list of edges adjacent to the node with the given id
        """
        return self.edges(item)

    def add_node(self, node_value, **attributes):
        """Add a node to the graph

        Args:
            node_value (int): the id of the node to be created
        """
        self.nodes[node_value] = attributes

    def add_edge(self, start_node, end_node, **attributes):
        """Add an edge to the graph

        Args:
            start_node (int): the id of the node at one end of the edge
            end_node (int): the id of the node at the other end of the edge

        """
        if not self.has_node(start_node):
            self.add_node(start_node)
        if not self.has_node(end_node):
            self.add_node(end_node)
        edge_tuple = (start_node, end_node)
        self.edges[edge_tuple] = attributes

    def add_nodes_from(self, node_list):
        """Add nodes in a batch

        Args:
            node_list (array[int]): an array containg the ids of multipl nodes to be created
        """
        for node_value in node_list:
            if type(node_value) == tuple:
                self.nodes[node_value[0]] = node_value[1]
            elif type(node_value) == int:
                self.nodes[node_value] = {}

    def add_edges_from(self, edge_list):
        """Add edges in a batch

        Args:
            edge_list (array[tuple]): an array containing tuples which represent edges to be created
        """
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
        """Check if the given node is already present in the graph

        Args:
            node_value (int): the id of the node to check

        Returns:
            bool: a boolean value indicating whether the node is present
        """
        graph_has_node = False
        for n in self.nodes:
            if n == node_value:
                graph_has_node = True
        return graph_has_node

    def has_edge(self, edge_tuple):
        """Check if the given edge is already present in the graph

        Args:
            edge_tuple (tuple): a tuple representing the edge to check

        Returns:
            bool: a boolean value indicating whether the edge is present
        """
        graph_has_edge = False
        for e in self.edges:
            if e[0] == edge_tuple[0] and e[1] == edge_tuple[1]:
                graph_has_edge = True
        return graph_has_edge

    def remove_node(self, node_value):
        """Remove the given node from the graph

        Args:
            node_value (int): the id of the node to remove

        Raises:
            ValueError: an error indicating the node is not present 
        """
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
        """Remove multiple nodes from the graph in a batch

        Args:
            node_list (list): a list representing the nodes to remove
        """
        for node in node_list:
            self.remove_node(node)


    def remove_edge(self, start_node, end_node):
        """Remove the given edge from the graph

        Args:
            start_node (int): the id of the node at one end of the edge
            end_node (int): the id of the node at the other end of the edge

        Raises:
            ValueError: an error indicating the edge is not present
            ValueError: an error indicating one of the nodes is not present
        """
        if self.has_node(start_node) and self.has_node(end_node):
            edge_tuple = (start_node, end_node)
            if self.has_edge(edge_tuple):
                del self.edges[edge_tuple]
            else:
                raise ValueError
        else:
            raise ValueError

    def remove_edges_from(self, edge_list):
        """Remove multiple edges from the graph in a batch

        Args:
            edge_list (list[tuple]): an list of tuples representing edges to be removed from the graph
        """
        for edge in edge_list:
            if type(edge) == tuple:
                start_node = edge[0]
                end_node = edge[1]
                self.remove_edge(start_node, end_node)

    def node_data(self, node_num):
        """Display the attribute data corresponding with the given node

        Args:
            node_num (int): the id of a node in the graph

        Returns:
            dict: dictionary with key-value pairs representing attribute values
        """
        return self.nodes[node_num]

    def get_edge_data(self, start_node, end_node):
        """Display the attribuet data corresponding with the given edge

        Args:
            start_node (int): the id of the node at one end of the edge
            end_node (int): the id of the node at the other end of the edge

        Returns:
            dict: dictionary with key-value pairs representing attribute values
        """
        edge_tuple = (start_node, end_node)
        return self.edges[edge_tuple]

class NodeView(dict):
    """A class controlling the disaplay of nodes for a graph

    Args:
        dict (type): indicates the NodeView acts like a dictionary by inheriting its methods
    """
    def __init__(self):
        """initialzi the class
        creats a list of nodes
        """
        self._nodes = list([])

    def __call__(self):
        """Handles the calling of the nodes ie: "G.nodes()"

        Returns:
            list: a list representing the present nodes
        """
        node_list = list(self.keys())
        return node_list

    def __delitem__(self, key):
        """Delete an item from the node dictionary corresponding with the given key

        Args:
            key (int): a number which acts as an identifying key for a node
        """
        super().pop(key)
        self._nodes.remove(key)

    def __setitem__(self, key, value):
        """Set an item in the node dictionary corresponding with the given key to the given value

        Args:
            key (int): the id of a node to set
            value (dict): the attribute assignemnet for this node
        """
        self._nodes.append(key)
        super().__setitem__(key, value)

    def __iter__(self):
        """Handles how the nodes will be iterated ie "for n in G.nodes"

        Returns:
            NodeViewIterator: an iterator object for listing the nodes
        """
        return NodeViewIterator(self)

    def data(self):
        """Returns the node view
        a simpel overloading of the NodeView display to mimic the networkx behavior

        Returns:
            NodeView: this very same NodeView object 
        """
        return self

class NodeViewIterator:
    """An object which handles the iterating of nodes for a graph
    """
    def __init__(self, node_view):
        """initialize the iterator

        Args:
            node_view (NodeView): the node view object to be iterated
        """
        self._index = 0
        self._node_view = node_view

    def __next__(self):
        """Handles the next item passed durring iteration

        Raises:
            StopIteration: an error indicating the iterator was attempting to access beyond its bounds

        Returns:
            int: the id of the next node to iterate
        """
        if(self._index < len(self._node_view._nodes)):
            item = self._node_view._nodes[self._index]
            self._index += 1
            return item
        raise StopIteration


class EdgeView(dict):
    """A class controlling the disaplay of edges for a graph

    Args:
        dict (type): indicates the EdgeView acts like a dictionary by inheriting its methods
    """
    def __init__(self):
        """initialzi the class
        creates a list of edges
        """
        self._edges = list([])

    def __call__(self, node=None):
        """Handles the calling of the nodes ie: "G.edges()"

        Returns:
            list: a list representing the present edges
        """
        edge_list = list(self.keys())
        if node is not None:
            return list([e for e in edge_list if node in e])
        else:
            return edge_list

    def __delitem__(self, key):
        """Delete an item from the edge dictionary corresponding with the given key

        Args:
            key (tuple): a tuple which acts as an identifying key for an edge
        """
        super().pop(key)
        self._edges.remove(key)

    def __setitem__(self, key, value):
        """Set an item in the edge dictionary corresponding with the given key to the given value

        Args:
            key (tuple): the tuple of an edge to set
            value (dict): the attribute assignemnet for this edge
        """
        self._edges.append(key)
        super().__setitem__(key, value)

    def __iter__(self):
        """Handles how the edges will be iterated ie "for n in G.edges"

        Returns:
            EdgeViewIterator: an iterator object for listing the edges
        """
        return EdgeViewIterator(self)

    def data(self):
        """Returns the edge view
        a simpel overloading of the EdgeView display to mimic the networkx behavior

        Returns:
            EdgeView: this very same EdgeView object 
        """
        return self


class EdgeViewIterator:
    """An object which handles the iterating of edges for a graph
    """
    def __init__(self, edge_view):
        """initialize the iterator

        Args:
            edge_view (EdgeView): the edge view object to be iterated
        """
        self._index = 0
        self._edge_view = edge_view

    def __next__(self):
        """Handles the next item passed durring iteration

        Raises:
            StopIteration: an error indicating the iterator was attempting to access beyond its bounds

        Returns:
            tuple: the tuple of the next edge to iterate
        """
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

class DiGraph(Graph):
    """A class representing a directed graph

    Args:
        Graph (type): indicates that the DiGraph acst as a subclass of Graph and inherits its methods
    """
    def __init__(self):
        """initialzi the class
        creates a list of edges as an OutEdgeVew
        """
        super().__init__()
        self.edges = OutEdgeView()

class OutEdgeView(EdgeView):
    """A class controlling the display of outgoing edges for a graph

    Args:
        EdgeView (type): indicates that the OutEdgeView acst as a subclass of EdgeView and inherits its methods
    """
    def __call__(self, node=None):
        """Handles the calling of the edges ie: "G.edges()"
        crucially differs from the EdgeView implementation in that only
        outgoing edges are returned

        Returns:
            list: a list representing the present edges
        """
        edge_list = list(self.keys())
        if node is not None:
            return list([e for e in edge_list if e[0] == node])
        else:
            return edge_list

class MultiGraph(Graph):
    """A class representing a multigraph

    Args:
        Graph (type): indicates that the DiGraph acst as a subclass of Graph and inherits its methods
    """
    def __init__(self):
        """initialzi the class
        creates a list of edges as an MultiEdgeView
        and a set to represent the edge indices
        """
        super().__init__()
        self.edges = MultiEdgeView()
        self.edge_indices = set()

    def add_edge(self, start_node, end_node, **attributes):
        """Add an edge to the graph
        allows for the updating of a specific edges attributes by checking the 'key' attribute

        Args:
            start_node (int): the id of the node at one end of the edge
            end_node (int): the id of the node at the other end of the edge
            attributes (dict): dictionary with key-value pairs for attribute assignment
        """
        if not self.has_node(start_node):
            self.add_node(start_node)
        if not self.has_node(end_node):
            self.add_node(end_node)

        # if an edge exists with the same key then update that one
        if 'key' in attributes:
            for e in self.edges:
                if e[0] == start_node and e[1] == end_node and attributes['key'] == e[3]['key']:
                    edge_index = e[2]
                    self.edges[(start_node, end_node, edge_index)] = attributes
                    return
        # otherwise create a new edge
        edge_index = self.get_next_edge_index()
        self.edges[(start_node, end_node, edge_index)] = attributes
        self.edge_indices.add(edge_index)
        
    def remove_edge(self, start_node, end_node):
        """Remove one edge corresponding with the given node pair from the graph

        Args:
            start_node (int): the id of the node at one end of the edge
            end_node (int): the id of the node at the other end of the edge

        Raises:
            ValueError: an error indicating an edge is not present
            ValueError: an error indicating one of the nodes is not present
        """
        if self.has_node(start_node) and self.has_node(end_node):
            edge_tuple = (start_node, end_node)
            if self.has_edge(edge_tuple):
                for e in self.edges:
                    if e[0] == start_node and e[1] == end_node:
                        del self.edges[e]
                        break
            else:
                raise ValueError
        else:
            raise ValueError

    def get_next_edge_index(self):
        """Get the next unused integer to reresent an edge index

        Returns:
            int: a number to represent a new edge in the graph
        """
        index = 0;
        while index in self.edge_indices:
            index = index + 1
        return index

    def get_edge_data(self, start_node, end_node, **attributes):
        """Display the attribute data corresponding with the edge which has the 'key' attribue set 
        to a given vale

        Args:
            start_node (int): the id of the node at one end of the edge
            end_node (int): the id of the node at the other end of the edge
            attributes (dict): dictionary with key-value pairs for checking attribute values

        Returns:
            dict: dictionary with key-value pairs representing attribute values
        """

        for e in self.edges:
            if e[0] == start_node and e[1] == end_node and attributes['key'] == e[3]['key']:
                return self.edges[(e[0], e[1], e[2])]
        return None

class MultiEdgeView(EdgeView):
    """A class controlling the display of multiple edges for a graph

    Args:
        EdgeView (type): indicates that the OutEdgeView acst as a subclass of EdgeView and inherits its methods
    """
    def __call__(self, node=None):
        """Handles the calling of the edges ie: "G.edges()"
        crucially differs from the EdgeView implementation in that 
        a nested dictionary is returned instead of a normal list
        the first layer of the dictionary has other node ids as keys while the second layer
        has edge indices as keys and the attribute dictionaries as values 

        Returns:
            dict or list: a dictionary containg the edges indexed by node and edge index,
            defaults to a list representing the present edges
        """
        edge_list = list(self.keys())
        if node is not None:
            adjacency_dict = {}
            for e in edge_list:
                start_node = e[0]
                end_node = e[1]
                edge_index = e[2]
                if start_node == node:
                    if end_node not in adjacency_dict: adjacency_dict[end_node] = {}
                    attr = self[e]
                    adjacency_dict[end_node].update({edge_index: attr})
                if end_node == node:
                    if start_node not in adjacency_dict: adjacency_dict[start_node] = {}
                    attr = self[e]
                    adjacency_dict[start_node].update({edge_index: attr})
            return adjacency_dict
        else:
            return edge_list

    def __iter__(self):
        """Handles how the edges will be iterated ie "for n in G.edges"

        Returns:
            MultiEdgeViewIterator: an iterator object for listing the edges
        """
        return MultiEdgeViewIterator(self)

class MultiEdgeViewIterator:
    """An object which handles the iterating of multiedges for a graph
    """
    def __init__(self, multiedge_view):
        """initialize the iterator

        Args:
            multiedge_view (MultiEdgeView): the multiedge view object to be iterated
        """
        self._index = 0
        self._multiedge_view = multiedge_view

    def __next__(self):
        """Handles the next item passed durring iteration

        Raises:
            StopIteration: an error indicating the iterator was attempting to access beyond its bounds

        Returns:
            tuple: the tuple of the next edge to iterate
            this tuple containg three values for the two node ids and the edge index
        """
        if(self._index < len(self._multiedge_view._edges)):
            item = self._multiedge_view._edges[self._index]
            self._index += 1
            attributes_dict = self._multiedge_view[item]
            edge_tuple = ()
            if(len(attributes_dict.keys()) > 0) :
                edge_tuple = (item[0], item[1], item[2], attributes_dict)
            else:
                edge_tuple = (item[0], item[1], item[2])
            return edge_tuple
        raise StopIteration


class MultiDiGraph(MultiGraph, DiGraph):
    """A class representing a multidigraph

    Args:
        MultiGraph (type): indicates that the MutiDiGraph acst as a subclass of MultiGraph and inherits its methods
        DiGraph (type): indicates that the MutiDiGraph acst as a subclass of MultiGraph and inherits its methods
    """
    def __init__(self):
        """initialzi the class
        creates a list of edges as an MultiOutEdgeView
        """
        super().__init__()
        self.edges = MultiOutEdgeView()


class MultiOutEdgeView(EdgeView):
    """A class controlling the display of multiple outgoing edges for a graph

    Args:
        EdgeView (type): indicates that the MultiOutEdgeView acst as a subclass of EdgeView and inherits its methods
    """
    def __call__(self, node=None):
        """Handles the calling of the edges ie: "G.edges()"
        crucially differs from the EdgeView implementation in that 
        a nested dictionary is returned instead of a normal list
        the first layer of the dictionary has other node ids as keys while the second layer
        has edge indices as keys and the attribute dictionaries as values 
        also diffes from the normal EdgeView in that only outgoing edges are returned

        Returns:
            dict or list: a dictionary containg the outgoing edges indexed by node and edge index,
            defaults to a list representing the present edges
        """
        edge_list = list(self.keys())
        if node is not None:
            adjacency_dict = {}
            for e in edge_list:
                start_node = e[0]
                end_node = e[1]
                edge_index = e[2]
                if start_node == node:
                    if end_node not in adjacency_dict: adjacency_dict[end_node] = {}
                    attr = self[e]
                    adjacency_dict[end_node].update({edge_index: attr})
            return adjacency_dict
        else:
            return edge_list

    def __iter__(self):
        """Handles how the edges will be iterated ie "for n in G.edges"

        Returns:
            MultiEdgeViewIterator: an iterator object for listing the edges
        """
        return MultiEdgeViewIterator(self)

