# Example Network Package

This is a simple network plotting package serving as sample code for the Agnostiq code challenge

# This package was build to comply with the following specifications:
Using nothing but core python libraries, develop a package that mimics the core features of networkx http://networkx.org. This would include (but is not limited to):
- Creating a custom “mynetwork” graph object
- Adding/connecting nodes, edges
- Adding meta-data/weights to nodes/edges
- Plotting the given graph

Bonus: Enhance the above module to include multi directed graph structure with the same functionality.

# Intention and Development 
A custom "exapmle_network" package was written to mimic the "networkx" package as closely as possible
The main exception to this was the plotting feature which was implemented with Tkinter in order to ahdere to the guidlines about using only core python libraries.

Adherence to the "networkx" syntax was maintained by using a test driven development process whereby failing tests on the graph class methods were introduced to check these methods for the expected result as per the networkx graph object behavior. The methods of the Graph, DiGraph, and Multigraph class along with other auxillary classes were then written to fullfil the expectations of the tests one at a time.

This style was maintained throughout the package development with the exception of the PlotWindow class which was tested manually by observing the displayed plot.

tests are found in the "tests" subdirectory and can be run from the project directory via the "run_tests.sh" script

```
./scripts/run_tests.sh
```

# Loading the package


from the "example_network.py" file in the "example_network_package" directory, the package can be loaded via:

```
from src.example_network_package import example_network as nx
```

# Creating a Graph
In order to create a graph with the package the same syntax can be used as in networkx

```
mynetwork = nx.Graph()
```

# Adding/Removing Nodes

individual nodes can be added with:

```
G.add_node(2)
```

and can then be removed with

```
G.remove_node(2)
```

nodes can also be added in batches with:

```
G.add_nodes_from([1, 2, 4, 7])
```

and can likewise be removed with

```
G.remove_nodes_from([1, 2, 4, 7])
```

in addition the presence of a node can be checked with a boolean function

```
G.has_node(2)
```

the present nodes can be listed with:

```
my_nodes = G.nodes()
```


# Adding/Removing Edges

an edge can be added between two nodes 0, 2 by

```
G.add_edge(0, 2)
```

it can then be removed similarly:

```
G.remove_edge(0, 2)
```

edges can also be added in batches with:

```
G.add_edges_from([(0,1), (1,2), (2,4)])
```

they can then also be removed in batches as follows:

```
G.remove_edges_from([(0,1), (1,2), (2,4)])
```

the presence of an edge can be checked with:

```
G.has_edge((0,2))
```

the present edges can be listed with:

```
my_edges = G.edges()
```

the edges adjacent to the node 4 can be checked with:

```
adjacent_edges = G.edges(4)
```

if an attempt is made to add an edge between nodes that do not yet exist then these nodes will be created
also if a node is removed that any edge depends on then the dependent edge will be removed as well

# Adding Metadata/ Weights

metadata can be added to a node with attribute keywords via:

```
G.add_node(0, key1="val1", key2="val2")
```

and in batches by:

```
G.add_nodes_from([(4, {key1:"val1", key2:"val2"}), (6, {key1:"val1", key2:"val2"})])
```

similarly any metadata can be added to edges via:

```
G.add_edge(0, 2, key1="val1", key2="val2")
```
```
G.add_edges_from([(0, 1, {key1:"val1", key2:"val2"}), (2, 3, {key1:"val1", key2:"val2"})])
```
weights can be added as a type of meta-data:

```
G.add_edge(0, 2, weight=4)
```

Once present a node or edges meta data can accessed or modified via subscripts:
```
old_val = G.nodes[6][key1]
```
```
G.nodes[6][key1] = "new_val"
```

```
old_val = G.edges[0, 2][key1]
```
```
G.edges[0, 2][key1] = "new_val"
```

edge meta data can also be modified in batches via:

```
nx.set_edge_attributes(G, {(0,2): {key1:"new_val1"}, (0,2): {key1:"new_val1"}})
```

# Plotting

A Tkinter plot window displaying a given graph can be draw with:

```
G.draw()
```

The window shops circles for nodes and line segments connceting the circles for edges.
The nodes are originally positioned on the vertices of a regular n-gon where n is the number of nodes in the graph.
The node positions are then adjusted for a few seconds so that nodes move toward other nodes they are connected to via edges.

# Digraphs

The DiGraph is a subclass of the Graph which is modified to pay attention to the direction of edges.
A digraph can be created via:

```
G = nx.DiGraph()
```

when it is queried for edges adjacent to a node only the outpoing edges will be returned
```
G.add_edges_from([(0,1),(1,2),(2,1)])
```
```
G.edges(1)
```
returns `[(1,2)]`

plotting the DiGraph with `G.draw()` will display arrows for the edge line segments with the arrow pointing
in the direction of the edge


# MultiGraphs
A MultiGraph is another subclass of Graph it modifies the edge methods of the graph so that multiple edges between
the same two nodes can be added. This is done by creating an edge index which is used internally for storing the edge data.

A multigraph can be created by:
```
G = nx.MultiGraph()
```

when it is queried for the edges adjacent to a node a dictionry is returned which can contain multiple entries for each node on the other end of an edge:
the dictionary has keys which are the corresponding other node values and values which are themselves dictionaries
with the edge indices as keys and attributes assignments as values

```
G.add_edges_from([(1, 2, {key1:"val1"}), (1, 2, {key1:"val2"}), (4, 1, {key1:"val3"})])
```
```
G[1]
```
returns `{2:{0: {key1:"val1"}, 1:{key1:"val2"}}, 4:{2: {key1:"val3"}}`

plotting the MultiGraph with `G.draw()` will display multiple line segments for each edge connecting two nodes


# DiMultiGraphs

The DiMultiGraph inherets from both the DiGraph and MultiGraph classes and implements both of their functionalities
it pays attention the the edge index like the multigraph but will also pay attention to the edge direction
so that queries will only return outgoing edges:

For the same example as above but in the case of the DiMultGraph we have 
```
G.add_edges_from([(1, 2, {key1:"val1"}), (1, 2, {key1:"val2"}), (4, 1, {key1:"val3"})])
```
```
G[1]
```
returns `{2:{0: {key1:"val1"}, 1:{key1:"val2"}}}`

plotting the DiMultiGraph with `G.draw()` will display multiple arrows for each edge connecting two nodes with the arrows pointing in the edge direction.

