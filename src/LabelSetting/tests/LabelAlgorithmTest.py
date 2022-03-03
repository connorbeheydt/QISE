
import sys
import networkx
from types import LambdaType
from src.GraphModeling.models.Graph import Graph
from src.GraphModeling.models.WCGraph import WCGraph
from src.LabelSetting.Models.LabelAlgorithm import LabelAlgorithm

from src.GraphModeling.tests.WCGraphTest import print_graph_details, print_matrix

def print_test_results(labels: LabelAlgorithm, destination_node: int):
    for node, label in labels.node_labels.items():
        print(f"|   Labels for node {node}:")
        print(f"|   |   {label.labels}")
        print(f"|   Paths for node {node}: ")
        print(f"|   |   {label.paths}")
        print(f"|   Untreated nodes: {label.get_untreated_nodes()}\n")

    efficient_labels = labels.node_labels[destination_node].get_efficient_labels()
    print(f"|   Efficient labels for the destination node:\n|   |   {efficient_labels}\n")
    print(f"|   Efficient Paths:")
    for node in efficient_labels.keys():
        print(f"|    |   {labels.node_labels[destination_node].paths[node]}")

def setup(graph: WCGraph) -> LabelAlgorithm:
    labels = LabelAlgorithm()

    print(graph.connection_matrix)
    print(graph.weight_matrix)
    print(graph.cost_matrix)

    for node_index in Graph.get_nodes(graph.edges):
        # find the incoming and outgoing nodes of the current node
        print(f"Incoming Nodes for node {node_index}: {graph.get_incoming_nodes(node_index)}")
        print(f"Outgoing Nodes for node {node_index}: {graph.get_outgoing_nodes(node_index)}")
    
    return labels

def test_graph_v1(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print("\nLabel Algorithm v1\n")
    labels = setup(graph)

    labels.run_algorithm_v1(graph, source_node, weight)

    print_test_results(labels, destination_node)

def test_graph_v2(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print("\nLabel Algorithm v2\n")
    labels = setup(graph)

    labels.run_algorithm_v2(graph, source_node, weight)

    print_test_results(labels, destination_node)

def test_graph_v3(graph: WCGraph, source_node: int, destination_node: int, weight: int):
    print("\nLabel Algorithm - Generate all possible labels\n")
    labels = setup(graph)

    labels.gen_all_possible_labels(graph, source_node, weight)

    print_test_results(labels, destination_node)

def test_1():
    graph = WCGraph({
        #edge    constraint
        #s  t    w  c
        (0, 1): (1, 1),
        (1, 2): (2, 5),
        (0, 3): (1, 1),
        (1, 3): (2, 2),
        (1, 4): (2, 8),
        (2, 4): (7, 2),
        (3, 4): (6, 2),
        (0, 2): (0, 1),
        (2, 3): (1, 1),
        (3, 5): (2, 3),
        (5, 6): (1, 1)
    })

    test_graph_v1(graph, source_node = 0, destination_node = 6, weight = 6)
    test_graph_v2(graph, source_node = 0, destination_node = 6, weight = 6)
    test_graph_v3(graph, source_node = 0, destination_node = 6, weight = 6)

    print("\ngraph:\n")

    graph.print_graph()

def test_2():
    graph = WCGraph({
        #edge    constraint
        #s  t    w  c
        (0, 1): (1, 1),
        (1, 2): (2, 5),
        (0, 3): (1, 1),
        (1, 3): (2, 2),
        (1, 4): (2, 8),
        (2, 4): (7, 2),
        (3, 4): (6, 2),
        (0, 2): (0, 1),
        (2, 3): (1, 1),
        (3, 5): (2, 3),
        (5, 6): (1, 1),
        (0, 6): (6, 10),
        (4, 5): (1, 1)
    })

    graph.print_graph()

    test_graph_v2(graph, source_node = 0, destination_node = 6, weight = 6)

def test_3():
    graph: WCGraph = WCGraph.get_arbitrary_graph(n = 50, mean_weight = 10, mean_cost = 5)

    try:
        test_graph_v2(graph, source_node = 0, destination_node = 49, weight = 49) 
    except Exception as error:
        graph.save_to_json("LabelAlgorithm_LargeGraph_Crash")
        print(f"Error: {error.__doc__}. Saving graph.")
    except:
        graph.save_to_json("LabelAlgorithm_LargeGraph_UnexpectedCrash")
        print(f"Unexpected error: {sys.exc_info()[0]}")

    print("\ngraph:\n")
    graph.print_graph(show_minimal_output=True)

def test_load(graph_name: str):
    graph: WCGraph = WCGraph.load_json_graph(graph_name)
    
    try:
        test_graph_v2(graph, source_node = 0, destination_node = 49, weight  =49)
    except:
        graph.print_graph(show_minimal_output=True)
        print(f"\n\nnum cycles: {len(list(networkx.simple_cycles(graph.networkx_graph)))}")
        print_matrix(graph.connection_matrix)


def main():
    print("Label Algorithm Test ------------------------------------")

    # Basic graph tests
    #test_1()
    #test_2()

    # Large graph test
    #test_3()

    # Test loaded graph
    test_load("LabelAlgorithm_LargeGraph_UnexpectedCrash")


if __name__ == "__main__":
    main()