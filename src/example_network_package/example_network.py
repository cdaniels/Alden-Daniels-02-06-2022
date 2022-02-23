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
    window = PlotWindow(root, G)
    window.animate()
    root.mainloop()

class PlotWindow:
    def __init__(self, master, G):
        self.root = master
        self.canvas = Canvas(self.root, bg="white", height=300, width=300)
        self.graph = copy.copy(G)

        self.node_radius = 15

        self.refresh_rate = 0.1 # in seconds
        self.move_inc = 2
        self.global_repulsie_f = 0.1 # force to repel all nodes to each other
        self.edge_attractive_f = 0.2 # force to attract adjacent nodes
    
        self.plot_graph(self.graph)
        self.canvas.pack()


    def animate(self):
        G = self.graph
        while True:
            for node_id in G.nodes:
                circ = G.nodes[node_id]["_plot_circle_id"]
                label = G.nodes[node_id]["_plot_label_id"]
                self.canvas.move(circ, self.move_inc, self.move_inc)
                self.canvas.move(label, self.move_inc, self.move_inc)
                self.root.update()
                # move adjacent edges as well
            for start, end, attr in G.edges:
                start_circ = G.nodes[start]["_plot_circle_id"]
                start_coords = self.canvas.coords(start_circ)
                end_circ = G.nodes[end]["_plot_circle_id"]
                end_coords = self.canvas.coords(end_circ)
                r = self.node_radius
                x1 = start_coords[0] +r
                y1 = start_coords[1] +r
                x2 = end_coords[0] + r
                y2 = end_coords[1] + r

                line = G.edges[start, end]["_plot_line_id"]
                self.canvas.coords(line, x1, y1, x2, y2)
                self.root.update()

            time.sleep(self.refresh_rate)

    def plot_graph(self, G):

        # add plot positions for all the nodes in the graph
        self.add_plot_positions_to_graph(G)

        # get coordinates for each node and draw a circle at those coordinates
        for node_id in G.nodes:
            self.draw_node(node_id)
        # for each edge draw a line between its corresponding nodes
        for start_node, end_node in G.edges:
            start_point = G.nodes[start_node]["_plot_position"]
            end_point = G.nodes[end_node]["_plot_position"]
            line = self.draw_line(start_point, end_point)
            G.edges[start_node, end_node]["_plot_line_id"] = line

    def add_plot_positions_to_graph(self, G):
        # get number of nodes in graph
        node_num = len(G.nodes)

        # get the coordinates for vertices of a regular n-gon of this size around the center of the canvas
        # center = (math.floor(self.canvas.winfo_width()/2), math.floor(self.canvas.winfo_width()/2)
        center = (150, 150)
        radius = 120
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
            if e == edge_tuple:
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


# class NodeDataView:
#     def __init__(self):
