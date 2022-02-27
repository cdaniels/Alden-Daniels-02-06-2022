# example graph object

import math, copy, time
from tkinter import *

def set_node_attributes(G, attributes):
    for node in attributes.keys():
        G.nodes[node] = attributes[node]

def set_edge_attributes(G, attributes):
    for edge in attributes.keys():
        G.edges[edge] = attributes[edge]

def draw(G):
    # init tk
    root = Tk()
    window = PlotWindow(root, 800, 600, G)
    window.animate()
    root.mainloop()

class PlotWindow:
    def __init__(self, master, width, height, G):
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


    def animate(self):
        G = self.graph
        start_time = time.time()
        while (time.time() - start_time < 2):
            self.increment_dynamics()
            time.sleep(self.refresh_rate)

    def increment_dynamics(self):
        G = self.graph
        for start_node in G.nodes:
            for end_node in G.nodes:
                if start_node != end_node:
                    move_vec = self.calculate_move_vec_between_nodes(start_node, end_node);
                    self.move_node_plot_by_vec(start_node, move_vec)

    def calculate_move_vec_between_nodes(self, start_node, end_node):
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
        G = self.graph
        circ = G.nodes[node_id]["_plot_circle_id"]
        label = G.nodes[node_id]["_plot_label_id"]
        self.canvas.move(circ, move_vec[0], move_vec[1])
        self.canvas.move(label, move_vec[0], move_vec[1])

        for edge in G.edges(node_id):
            self.update_edge_plot(edge[0], edge[1])

        self.root.update()

    def multiply_vec_by_scalar(self, vec, scalar):
        return tuple(list(map(lambda x: x * scalar, vec)))

    def add_vec_to_vec(self, vec1, vec2):
        sum_vec = [0, 0]
        sum_vec[0] = vec1[0] + vec2[0]
        sum_vec[1] = vec1[1] + vec2[1]
        return sum_vec

    def abs_len_of_vec(self, vec):
        tot = 0
        for elem in vec:
            tot = tot + elem**2
        return math.sqrt(tot)

    def update_edge_plot(self, start, end):
        G = self.graph
        start_circ = G.nodes[start]["_plot_circle_id"]
        start_coords = self.canvas.coords(start_circ)
        end_circ = G.nodes[end]["_plot_circle_id"]
        end_coords = self.canvas.coords(end_circ)
        r = self.node_radius
        x1 = start_coords[0] +r
        y1 = start_coords[1] +r
        x2 = end_coords[0] + r
        y2 = end_coords[1] + r

        line = G.edges[(start, end)]["_plot_line_id"]
        self.canvas.coords(line, x1, y1, x2, y2)
        self.root.update()

    def get_vec_between_points(self, start_point, end_point):
        x1 = start_point[0]
        y1 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]
        vec = (x2-x1, y2-y1)
        return vec
    
    def normalize_vec(self, vec):
        vec_mag = self.abs_len_of_vec(vec)
        norm_vec = self.multiply_vec_by_scalar(vec, 1/vec_mag)
        return norm_vec

    def plot_graph(self, G):

        # add plot positions for all the nodes in the graph
        self.add_plot_positions_to_graph(G)

        # get coordinates for each node and draw a circle at those coordinates
        for node_id in G.nodes:
            self.draw_node(node_id)
        # for each edge draw a line between its corresponding nodes
        for edge in G.edges:
            start_node = edge[0]
            end_node = edge[1]
            if "_plot_line_id" not in G.edges[start_node, end_node]:
                start_point = G.nodes[start_node]["_plot_position"]
                end_point = G.nodes[end_node]["_plot_position"]
                line = self.draw_line(start_point, end_point)
                G.edges[start_node, end_node]["_plot_line_id"] = line

    def add_plot_positions_to_graph(self, G):
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
        font = 'Helvetica ' + str(size) + ' bold'
        return self.canvas.create_text(x, y, text=text, fill="black", font=(font))

    def draw_circle(self, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        return self.canvas.create_oval(x0,y0,x1,y1)

    def draw_line(self, start_point, end_point):
        x1 = start_point[0]
        y1 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]
        return self.canvas.create_line(x1, y1, x2, y2)

    def get_regular_polygon_coords(self, center, radius, n):
        coord_list = []
        for i in range(n):
            x = math.floor(center[0] + radius * math.sin((2*math.pi/n) * i))
            y = math.floor(center[1] + radius * math.cos((2*math.pi/n) * i))
            coord = (x,y)
            coord_list.append(coord)
        return iter(coord_list)

class Graph:
    def __init__(self):
        self.nodes = NodeView()
        self.edges = EdgeView()

    def __getitem__(self, item):
        return self.edges(item)

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
            if e[0] == edge_tuple[0] and e[1] == edge_tuple[1]:
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

class DiGraph(Graph):
    def __init__(self):
        super().__init__()
        self.edges = OutEdgeView()

class OutEdgeView(EdgeView):
    def __call__(self, node=None):
        edge_list = list(self.keys())
        if node is not None:
            return list([e for e in edge_list if e[0] == node])
        else:
            return edge_list

class MultiGraph(Graph):
    def __init__(self):
        super().__init__()
        self.edges = MultiEdgeView()
        self.edge_indices = set()

    def __getitem__(self, item):
        return self.edges(item)

    def add_edge(self, start_node, end_node, **attributes):
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
        index = 0;
        while index in self.edge_indices:
            index = index + 1
        return index

    def get_edge_data(self, start_node, end_node, **attributes):
        for e in self.edges:
            if e[0] == start_node and e[1] == end_node and attributes['key'] == e[3]['key']:
                return self.edges[(e[0], e[1], e[2])]
        return None

class MultiEdgeView(EdgeView):
    def __call__(self, node=None):
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
        return MultiEdgeViewIterator(self)

class MultiEdgeViewIterator:
    def __init__(self, multiedge_view):
        self._index = 0
        self._multiedge_view = multiedge_view

    def __next__(self):
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


class MultiDiGraph(MultiGraph):
    def __init__(self):
        super().__init__()
        self.edges = MultiOutEdgeView()


class MultiOutEdgeView(EdgeView):
    def __call__(self, node=None):
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
        return MultiEdgeViewIterator(self)

