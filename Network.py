import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

class Network:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node.node_id, **node.__dict__)

    def add_connection(self, node1_id, node2_id):
        self.graph.add_edge(node1_id, node2_id)

    def visualize(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True)
        plt.show()

    def update_routing_tables(self):
        for node in self.graph.nodes:
            paths = nx.single_source_dijkstra_path(self.graph, node)
            self.graph.nodes[node]['routing_table'] = paths

    def print_routing_tables(self):
        for node in self.graph.nodes:
            print(f"Routing table for Node {node}:")
            for destination, path in self.graph.nodes[node]['routing_table'].items():
                print(f"  To Node {destination}: Path = {path}")
