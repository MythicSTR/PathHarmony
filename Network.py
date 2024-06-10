# import networkx as nx
# import matplotlib.pyplot as plt
# from geopy.distance import geodesic

# class Network:
#     def __init__(self):
#         self.graph = nx.Graph()

#     def add_node(self, node):
#         print(node)
#         print(node.node_id)
#         self.graph.add_node(node.node_id, **node.__dict__)

#     def add_connection(self, node1_id, node2_id):
#         self.graph.add_edge(node1_id, node2_id)

#     def visualize(self):
#         pos = nx.spring_layout(self.graph)
#         nx.draw(self.graph, pos, with_labels=True)
#         plt.show()

#     # def update_routing_tables(self):
#     #     for node in self.graph.nodes:
#     #         paths = nx.single_source_dijkstra_path(self.graph, node)
#     #         self.graph.nodes[node]['routing_table'] = paths

#     # def print_routing_tables(self):
#     #     for node in self.graph.nodes:
#     #         print(f"Routing table for Node {node}:")
#     #         for destination, path in self.graph.nodes[node]['routing_table'].items():
#     #             print(f"  To Node {destination}: Path = {path}")


import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic
import mplcursors  # To enable hover functionality

class Network:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node.node_id, **node.__dict__)

    def add_connection(self, node1_id, node2_id):
        node1 = self.graph.nodes[node1_id]
        node2 = self.graph.nodes[node2_id]
        distance = geodesic((node1['latitude'], node1['longitude']), (node2['latitude'], node2['longitude'])).kilometers
        self.graph.add_edge(node1_id, node2_id, weight=distance)

    def visualize(self):
        pos = nx.spring_layout(self.graph)

        # Draw nodes and edges
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10)
        labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels)

        fig, ax = plt.subplots()
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=500, font_size=10, ax=ax)
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=labels, ax=ax)

        # Add hover functionality
        cursor = mplcursors.cursor(ax.collections[0], hover=True)

        @cursor.connect("add")
        def on_add(sel):
            node_id = list(self.graph.nodes)[sel.target.index]
            node_data = self.graph.nodes[node_id]
            sel.annotation.set_text(f"Node {node_id}\n"
                                    f"Comp Power: {node_data['computational_power']}\n"
                                    f"Memory: {node_data['memory_size']} MB\n"
                                    f"Lat: {node_data['latitude']}\n"
                                    f"Lon: {node_data['longitude']}\n"
                                    f"Available: {node_data['available']}")

        plt.show()
