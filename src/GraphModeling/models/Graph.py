import matplotlib.pyplot as pyplot
import networkx
import numpy

from collections.abc import Sequence, Mapping
from numpy import random as r

class Graph:
    """ 
    The Graph class allows for the generation of directed graphs containing weights and costs.

    members:
        + edges (Sequence): a list of (from, to) node tuples
        + direction_matrix (numpy.ndarray): matrix of the directed edges between nodes
        + networkx_graph (networkx.DiGraph): networkx object representation of graph
    """
    
    def __init__(self, edges: Sequence) -> None:
        """
        Creates a new instance of the Graph class. Initializes the graph's 
        matricies based on the given general matrix.  

        Args:
            edges (Sequence): a list of edges (node from-to tuples)
        """
        self.edges: Sequence = edges
        self.connection_matrix: numpy.ndarray
        self.networkx_graph: networkx.DiGraph

        # Initialize connection matrix using the list of edges
        self._initialize_connection_matrix()

        # Initialize the networkx graph
        self._initialize_networkx_graph()

        
    def print_graph(self, picture_name: str = "", edge_labels: Mapping | None = None, suppress_text_output: bool = False) -> None:
        """
        Prints the graph using the networkx graph representation and pyplot.

        Args:
            picture_name (str, optional): The name to save the graph image as. Defaults to "".
            edge_labels (Mapping | None, optional): The dictionary of edges to labels. Defaults to None.
            suppress_text_output (bool): Supresses print statements and edge labels from being printed on the graph. Defaults to False
        """
        if(not suppress_text_output):
            print("Nodes on Graph:")
            print(f"|    {self.networkx_graph.nodes()}")
            print("Edges of Graph:")
            print(f"|    {self.networkx_graph.edges()}")
        
        #TODO: Fix positioning bug - nodes should be in counterclockwise order (should also fix color map bug)
        #TODO: Alter size of nodes and lines with size of graph
        networkx.draw_networkx(self.networkx_graph, 
            pos = networkx.circular_layout(self.networkx_graph), node_color = self.get_color_map(len(self.networkx_graph)))
        
        if edge_labels and not suppress_text_output:
            networkx.draw_networkx_edge_labels(self.networkx_graph, edge_labels = edge_labels, pos = networkx.circular_layout(self.networkx_graph))

        if picture_name != "":
            #TODO: Add a parameter to save this in the folder the .py file running the program is in or choice of location
            pyplot.savefig(picture_name) #save as png
        pyplot.show() #display

    def get_simple_paths(self, source_node: int = 0, destination_node: int | None = None) -> Sequence:
        """
        Returns an array of simple paths in the graph

        Args:
            source_node(int): the first node in the path
            destination_node(int): the last node in the path

        Returns:
            Sequence: a list of paths (a path is an array of nodes)
        """
        #TODO: Returns a generator object instead of an array
        paths = []

        if not destination_node:
            destination_node = len(Graph.get_nodes(self.edges)) - 1

        if self.networkx_graph:
            paths = networkx.all_simple_paths(self.networkx_graph, source_node, destination_node)

        return paths
    
    def get_color_map(self, n: int, s: int = 0, t: int = -1) -> Sequence:
        """
        Returns a colop mapping for each node in the graph

        Args:
            n (int): the number of nodes
            s (int, optional): The starting node. Defaults to 0.
            t (int, optional): The destination node. Defaults to -1.

        Returns:
            Sequence: a color mapping of each node in the graph
        """
        if t == -1:
            t = n - 1
        else:
             t - 1
        color_map = []
        for i in range(0,n):
            if i == s:
                color_map.append("green")
            elif i == t:
                color_map.append("red")
            else:
                color_map.append("blue")    
        return color_map
    
    def _initialize_networkx_graph(self) -> None:
        """
        Initializes the networkx graph, adding the nodes and edges of the graph 
        to the networkx object.
        """
        self.networkx_graph = networkx.DiGraph()
        # Add nodes
        self.networkx_graph.add_nodes_from(Graph.get_nodes(self.edges))
        # Add edges
        self.networkx_graph.add_edges_from(self.edges)

    def _initialize_connection_matrix(self) -> None:
        """
        Initializes the connection matrix representation of the graph using the defined edges
        for the graph.

        About Connection Matrix: 
        + We are representing a graph using an nxn square matrix, where n = number of nodes.
        + Each matrix element represents an edges between two nodes, where 1 at position M[a][b] 
        indicates that an edges exists between the nodes a and b.
        + The column of the martix represents the "from" nodes and the row represents the "to" nodes, 
        so you can represent directed graphs using the matrix.

            3x3 Example: list of edges --> [(1, 2), (1, 3)]
                     1  2  3
                 1 [[0, 1, 1],
                 2  [0, 0, 0], 
                 3  [0, 0, 0]]
        """
        # initialize matrix to nxn 0 matrix
        self.connection_matrix = Graph._gen_zero_n_square_matrix(self.edges)

        for edge in self.edges:
            self.connection_matrix[edge[0] - 1][edge[1] - 1] = 1

    # Static/Class Function
    def get_nodes(edges: Sequence) -> Sequence:
        """
        Returns a list of nodes given a list of edges

        Args:
            edges (Sequence): a list of edges, where an edge is a tuple of nodes

        Returns:
            [Sequence]: a list of nodes in the graph with edges
        """
        nodes = []

        for edge in edges:
            for node in edge:
                if node not in nodes:
                    nodes.append(node)
        # sort the nodes
        nodes.sort()
        return nodes

    # Static/Class Function
    def _gen_zero_n_square_matrix(edges: Sequence) -> numpy.ndarray:
        """
        Generates an nxn zero square matrix based on the list of edges

        Args:
            edges (Sequence): list of edges in the graph (node pairs)

        Returns:
            numpy.ndarray: an nxn zero square matrix
        """
        nodes = Graph.get_nodes(edges)
        num_nodes = len(nodes)
        return numpy.zeros((num_nodes, num_nodes))

    def get_arbitrary_graph(n: int):
        """Generates arbitrary WC graph with n nodes and no weights or costs

        Args:
            n (int): number of nodes

        Returns:
            Graph: arbitary WC graph with all (w,c) = (0,0)
        """
        graphDict = {}
        #Loop i range(0,n)
        for i in range(0,n-1):
            #Random Noe range(i,n) # of outgoing edges
            N_oe = r.randint(1,n-i) if n-i>1 else 1
            #print("i :", i, "\tN_oe: ", N_oe)
            #Choose Noe unique nodes range(1,n) delta_o[]
            delta_o = r.choice([*range(i+1,n)], N_oe, replace=False) if i!=n-1 else [n]
            #For each j in delta_o[], add edge (i,j)
            for j in delta_o:
                #TODO: Add weights and cost generation -> can only do to a WCGraph
                graphDict[i,j] = (0,0)
            #If no incoming nodes
            oneInNode = False
            for k in range(0,i):
                if((k,i) in graphDict):
                    oneInNode = True
                    break
            if not oneInNode and i != 0:
                #Choose node incoming n_in range(0,i-1)
                n_in = r.randint(0,i-1) if i>1 else 0
                #Add edge (n_in,i)
                #TODO: Add weight and const
                graphDict[n_in,i] = (0,0)
            
        graph = Graph(graphDict)
        return graph

