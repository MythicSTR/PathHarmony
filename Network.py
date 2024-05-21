import networkx as nx
import matplotlib.pyplot as plt

class Node:
    def __init__(self, id, ip, hostname, status):
        self.id = id
        self.ip = ip
        self.hostname = hostname
        self.status = status
    
    def __repr__(self):
        return f"Node(id={self.id}, ip='{self.ip}', hostname='{self.hostname}', status = '{self.status}')"

class Network:
    def __init__(self):
        self.graph = nx.Graph()

    def add_node(self, node):
        self.graph.add_node(node.id, ip=node.ip, hostname=node.hostname, status=node.status)

    def add_connection(self, id1, id2):
        self.graph.add_edge(id1, id2)

    def visualize(self):
        pos = nx.spring_layout(self.graph)
        nx.draw(self.graph, pos, with_labels=True, node_color='lightblue', node_size=3000, font_size=10, font_color='black')

        node_labels = {node: f"{self.graph.nodes[node]['hostname']} ({self.graph.nodes[node]['ip']})\n{self.graph.nodes[node]['status']}" for node in self.graph.nodes}

        nx.draw_networkx_labels(self.graph, pos, labels=node_labels, font_size=8)

        plt.title("Distribution System Graph")
        plt.show()

network = Network()

node1 = Node(1, "192.168.1.1", "node1", "active")
node2 = Node(2, "192.168.1.2", "node2", "inactive")
node3 = Node(3, "192.168.1.3", "node3", "active")
node4 = Node(4, "192.168.1.4", "node4", "active")

network.add_node(node1)
network.add_node(node2)
network.add_node(node3)
network.add_node(node4)

network.add_connection(1, 2)
network.add_connection(1, 3)
network.add_connection(2, 4)
network.add_connection(3, 4)

network.visualize()
