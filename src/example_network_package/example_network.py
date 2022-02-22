# example graph object

import math
from tkinter import *

def set_node_attributes(G, attributes):
    for node in attributes.keys():
        G.nodes[node] = attributes[node]

def set_edge_attributes(G, attributes):
    for edge in attributes.keys():
        G.edges[edge] = attributes[edge]

def draw(G):
    root = Tk()
    window = PlotWindow(root)
    window.plot_graph(G)
    root.mainloop()

class PlotWindow:
    def __init__(self, master):
        # init tk
        self.root = master
        # create canvas
        self.canvas = Canvas(self.root, bg="white", height=300, width=300)
        # add to window and show
        self.canvas.pack()

    def plot_graph(self, G):
        # get number of nodes in grah
        node_num = len(list(G.nodes))
        # get the coordinates for vertices of a regular n-gon of this size around the center of the canvas
        # center = (math.floor(self.canvas.winfo_width()/2), math.floor(self.canvas.winfo_width()/2))
        center = (150, 150)
        radius = 120
        coords = self.get_regular_polygon_coords(center, radius, node_num)
        # get coordinates for each node and draw a circle at those coordinates
        node_coords = list(zip(coords, list(G.nodes)))
        for tup in node_coords:
            coords = tup[0]
            node_val = tup[1]
            self.draw_node(coords, node_val)
        # for each edge draw a line between its corresponding nodes
        for edge in list(G.edges):
            start_point = self.get_coords_for_node(node_coords, edge[0])
            end_point = self.get_coords_for_node(node_coords, edge[1])
            self.draw_line(start_point, end_point)
            

    def get_coords_for_node(self, node_coords, node_val):
        for tup in node_coords:
            coords = tup[0]
            val = tup[1]
            if val is node_val:
                return coords
        return ()


    def draw_node(self, coords, val):
        # expand the coordinates
        x = coords[0]
        y = coords[1]
        r = 15
        # draw a circle at the desired location
        self.draw_circle(x, y, r)
        # then create text for the node id at the same location 
        self.draw_text(x, y, math.floor(r*0.7), val)

    def draw_text(self, x, y, size, text):
        font = 'Helvetica ' + str(size) + ' bold'
        self.canvas.create_text(x, y, text=text, fill="black", font=(font))

    def draw_circle(self, x, y, r):
        x0 = x - r
        y0 = y - r
        x1 = x + r
        y1 = y + r
        self.canvas.create_oval(x0,y0,x1,y1)

    def draw_line(self, start_point, end_point):
        x1 = start_point[0]
        y1 = start_point[1]
        x2 = end_point[0]
        y2 = end_point[1]
        self.canvas.create_line(x1, y1, x2, y2)

    def get_regular_polygon_coords(self, center, radius, n):
        coord_list = []
        for i in range(n):
            x = math.floor(center[0] + radius * math.sin((2*math.pi/n) * i))
            y = math.floor(center[1] + radius * math.cos((2*math.pi/n) * i))
            coord = (x,y)
            coord_list.append(coord)
        return coord_list


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
