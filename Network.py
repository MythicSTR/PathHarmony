# import networkx as nx
# import matplotlib.pyplot as plt
# from geopy.distance import geodesic

# class Node:
#     def __init__(self, id, ip, hostname, status, latitude, longitude):
#         self.id = id
#         self.ip = ip
#         self.hostname = hostname
#         self.status = status
#         self.latitude = latitude
#         self.longitude = longitude
#         self.routing_table = {}  # Initialize an empty routing table
    
#     def __repr__(self):
#         return (f"Node(id={self.id}, ip='{self.ip}', hostname='{self.hostname}', status='{self.status}', "
#                 f"latitude={self.latitude}, longitude={self.longitude})")

# class Network:
#     def __init__(self):
#         self.graph = nx.Graph()
    
#     def add_node(self, node):
#         self.graph.add_node(node.id, ip=node.ip, hostname=node.hostname, status=node.status, 
#                             latitude=node.latitude, longitude=node.longitude, routing_table=node.routing_table)
    
#     def add_connection(self, id1, id2):
#         distance = self.calculate_geographical_distance(id1, id2)
#         self.graph.add_edge(id1, id2, weight=distance)
    
#     def calculate_geographical_distance(self, id1, id2):
#         node1 = self.graph.nodes[id1]
#         node2 = self.graph.nodes[id2]
#         coords_1 = (node1['latitude'], node1['longitude'])
#         coords_2 = (node2['latitude'], node2['longitude'])
#         distance_km = geodesic(coords_1, coords_2).km
#         scaled_distance = distance_km / 100  # Scaling factor to keep distances manageable
#         return scaled_distance
    
#     def visualize(self):
#         pos = nx.spring_layout(self.graph)
#         nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_color='black')
        
#         edge_labels = nx.get_edge_attributes(self.graph, 'weight')
#         nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        
#         node_labels = {node: f"{self.graph.nodes[node]['hostname']} ({self.graph.nodes[node]['ip']})\n"
#                              f"{self.graph.nodes[node]['status']}\n"
#                              f"({self.graph.nodes[node]['latitude']}, {self.graph.nodes[node]['longitude']})" 
#                       for node in self.graph.nodes}
#         nx.draw_networkx_labels(self.graph, pos, labels=node_labels, font_size=8)
        
#         plt.title("Distribution System Graph")
#         plt.show()
    
#     def update_routing_tables(self):
#         for node in self.graph.nodes:
#             lengths, paths = nx.single_source_dijkstra(self.graph, node, weight='weight')
#             for target_node in self.graph.nodes:
#                 self.graph.nodes[node]['routing_table'][target_node] = paths.get(target_node, [])
    
#     def print_routing_tables(self):
#         for node in self.graph.nodes:
#             print(f"Routing table for Node {node}:")
#             for target, path in self.graph.nodes[node]['routing_table'].items():
#                 print(f"  To Node {target}: Path = {path}")

# # Create the network
# network = Network()

# # Add nodes with geographical coordinates (latitude, longitude)
# node1 = Node(1, "192.168.1.1", "node1", "active", 37.7749, -122.4194)  # San Francisco, CA
# node2 = Node(2, "192.168.1.2", "node2", "inactive", 34.0522, -118.2437)  # Los Angeles, CA
# node3 = Node(3, "192.168.1.3", "node3", "active", 40.7128, -74.0060)  # New York, NY
# node4 = Node(4, "192.168.1.4", "node4", "active", 41.8781, -87.6298)  # Chicago, IL

# network.add_node(node1)
# network.add_node(node2)
# network.add_node(node3)
# network.add_node(node4)

# # Add connections, weights will be calculated based on geographical distance
# network.add_connection(1, 2)
# network.add_connection(1, 3)
# network.add_connection(2, 4)
# network.add_connection(3, 4)

# # Visualize the network
# network.visualize()

# # Update routing tables
# network.update_routing_tables()

# # Print routing tables
# network.print_routing_tables()

# # Calculate and print geographical distances between nodes
# print("Geographical Distances:")
# for id1 in network.graph.nodes:
#     for id2 in network.graph.nodes:
#         if id1 != id2:
#             distance = network.calculate_geographical_distance(id1, id2)
#             print(f"Distance between Node {id1} and Node {id2}: {distance:.2f}")

import networkx as nx
import matplotlib.pyplot as plt
from geopy.distance import geodesic

class Node:
    def __init__(self, id, ip, hostname, status, latitude, longitude, computational_power, memory):
        self.id = id
        self.ip = ip
        self.hostname = hostname
        self.status = status
        self.latitude = latitude
        self.longitude = longitude
        self.computational_power = computational_power
        self.memory = memory
        self.routing_table = {}  # Initialize an empty routing table
        self.is_busy = False  # New attribute to track if the node is busy with a task

    def __repr__(self):
        return (f"Node(id={self.id}, ip='{self.ip}', hostname='{self.hostname}', status='{self.status}', "
                f"latitude={self.latitude}, longitude={self.longitude}, computational_power={self.computational_power}, memory={self.memory}, "
                f"is_busy={self.is_busy})")

class Network:
    def __init__(self):
        self.graph = nx.Graph()
    
    def add_node(self, node):
        self.graph.add_node(node.id, ip=node.ip, hostname=node.hostname, status=node.status, 
                            latitude=node.latitude, longitude=node.longitude, computational_power=node.computational_power, 
                            memory=node.memory, routing_table=node.routing_table)
    
    def add_connection(self, id1, id2):
        distance = self.calculate_geographical_distance(id1, id2)
        self.graph.add_edge(id1, id2, weight=distance)
    
    def calculate_geographical_distance(self, id1, id2):
        node1 = self.graph.nodes[id1]
        node2 = self.graph.nodes[id2]
        coords_1 = (node1['latitude'], node1['longitude'])
        coords_2 = (node2['latitude'], node2['longitude'])
        distance_km = geodesic(coords_1, coords_2).km
        scaled_distance = distance_km / 100  # Scaling factor to keep distances manageable
        return scaled_distance
    
    def visualize(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_color='black')
        
        edge_labels = nx.get_edge_attributes(self.graph, 'weight')
        nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=edge_labels)
        
        node_labels = {node: f"{self.graph.nodes[node]['hostname']} ({self.graph.nodes[node]['ip']})\n"
                             f"{self.graph.nodes[node]['status']}\n"
                             f"({self.graph.nodes[node]['latitude']}, {self.graph.nodes[node]['longitude']})" 
                      for node in self.graph.nodes}
        nx.draw_networkx_labels(self.graph, pos, labels=node_labels, font_size=8)
        
        plt.title("Distribution System Graph")
        plt.show()
    
    def update_routing_tables(self):
        for node in self.graph.nodes:
            lengths, paths = nx.single_source_dijkstra(self.graph, node, weight='weight')
            for target_node in self.graph.nodes:
                self.graph.nodes[node]['routing_table'][target_node] = paths.get(target_node, [])
    
    def print_routing_tables(self):
        for node in self.graph.nodes:
            print(f"Routing table for Node {node}:")
            for target, path in self.graph.nodes[node]['routing_table'].items():
                print(f"  To Node {target}: Path = {path}")

# # Create the network
# network = Network()

# # Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
# node1 = Node(1, "192.168.1.1", "node1", "active", 37.7749, -122.4194, 10, 32)  # San Francisco, CA
# node2 = Node(2, "192.168.1.2", "node2", "inactive", 34.0522, -118.2437, 8, 16)  # Los Angeles, CA
# node3 = Node(3, "192.168.1.3", "node3", "active", 40.7128, -74.0060, 15, 64)  # New York, NY
# node4 = Node(4, "192.168.1.4", "node4", "active", 41.8781, -87.6298, 20, 128)  # Chicago, IL

# network.add_node(node1)
# network.add_node(node2)
# network.add_node(node3)
# network.add_node(node4)

# # Add connections, weights will be calculated based on geographical distance
# network.add_connection(1, 2)
# network.add_connection(1, 3)
# network.add_connection(2, 4)
# network.add_connection(3, 4)

# # Visualize the network
# network.visualize()

# # Update routing tables
# network.update_routing_tables()

# # Print routing tables
# network.print_routing_tables()

# # Calculate and print geographical distances between nodes
# print("Geographical Distances:")
# for id1 in network.graph.nodes:
#     for id2 in network.graph.nodes:
#         if id1 != id2:
#             distance = network.calculate_geographical_distance(id1, id2)
#             print(f"Distance between Node {id1} and Node {id2}: {distance:.2f}")
