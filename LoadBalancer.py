import time
from geopy.distance import geodesic
from threading import Thread
import networkx as nx

class LoadBalancer(Thread):
    def __init__(self, buffer, nodes, stop_event):
        super().__init__()
        self.buffer = buffer
        self.nodes = nodes
        self.stop_event = stop_event
        self.graph = nx.Graph()
        self.update_network()
        self.calculate_routing_tables()

    def update_network(self):
        for node in self.nodes:
            self.graph.add_node(node.node_id, latitude=node.latitude, longitude=node.longitude, computational_power=node.computational_power, memory_size=node.memory_size)
        for i, node1 in enumerate(self.nodes):
            for j, node2 in enumerate(self.nodes):
                if i != j:
                    distance = geodesic((node1.latitude, node1.longitude), (node2.latitude, node2.longitude)).kilometers
                    self.graph.add_edge(node1.node_id, node2.node_id, weight=distance)

    def run(self):
        while not self.stop_event.is_set():
            if not self.buffer.empty():
                task = self.buffer.get()
                print(f"Task {task.task_id} added to LoadBalancer")
                self.distribute_task(task)
                if not self.buffer.full():
                    print("Buffer not full. Requesting new task generation.")
            else:
                time.sleep(1)  # Buffer is empty, wait for tasks

    # def distribute_task(self, task):
    #     nearest_node = self.choose_nearest_node(task.location)
    #     remaining_data_size = task.data_size

    #     while remaining_data_size > 0:
    #         node = self.choose_closest_available_node(nearest_node)
    #         if node is None:
    #             print("No available nodes to execute task")
    #             break

    #         data_to_assign = min(remaining_data_size, node.memory_size)
    #         remaining_data_size -= data_to_assign
    #         node.assign_task(task, data_to_assign)
    #         print(f"Task {task.task_id} partially distributed to Node {node.node_id}. Data size: {data_to_assign} MB")

    def distribute_task(self, task):
        nearest_node = self.choose_nearest_node(task.location)
        remaining_data_size = task.data_size

        while remaining_data_size > 0:
            node = self.choose_closest_available_node(nearest_node, remaining_data_size)
            if node is None:
                print("No available nodes to execute task")
                break

            data_to_assign = min(remaining_data_size, node.memory_size)
            remaining_data_size -= data_to_assign
            node.assign_task(task)
            print(f"Task {task.task_id} partially distributed to Node {node.node_id}. Data size: {data_to_assign} MB")

    def choose_nearest_node(self, location):
        nearest_node = None
        min_distance = float('inf')
        for node in self.nodes:
            distance = geodesic(location, (node.latitude, node.longitude)).kilometers
            if distance < min_distance:
                min_distance = distance
                nearest_node = node
        return nearest_node

    def choose_closest_available_node(self, nearest_node, remaining_data_size):
        min_distance = float('inf')
        closest_node = None

        for n in self.nodes:
            if n.is_available() and n.memory_size >= remaining_data_size:
                distance = self.routing_table[nearest_node.node_id]['distances'][n.node_id]
                if distance < min_distance:
                    min_distance = distance
                    closest_node = n

        if closest_node is None:
            # If no single node has enough memory, distribute across multiple nodes
            for n in self.nodes:
                if n.is_available() and n.memory_size > 0:
                    distance = self.routing_table[nearest_node.node_id]['distances'][n.node_id]
                    if distance < min_distance:
                        min_distance = distance
                        closest_node = n

        return closest_node


    def dijkstra_algorithm(self, start_node_id):
        distances = {node.node_id: float('inf') for node in self.nodes}
        predecessors = {node.node_id: None for node in self.nodes}
        distances[start_node_id] = 0
        unvisited_nodes = set(node.node_id for node in self.nodes)

        while unvisited_nodes:
            current_node_id = min(unvisited_nodes, key=lambda node_id: distances[node_id])
            unvisited_nodes.remove(current_node_id)

            for neighbor in self.graph[current_node_id]:
                tentative_distance = distances[current_node_id] + self.graph[current_node_id][neighbor]['weight']
                if tentative_distance < distances[neighbor]:
                    distances[neighbor] = tentative_distance
                    predecessors[neighbor] = current_node_id

        return distances, predecessors

    def calculate_routing_tables(self):
        self.routing_table = {}
        for node in self.nodes:
            distances, predecessors = self.dijkstra_algorithm(node.node_id)
            self.routing_table[node.node_id] = {'distances': distances, 'predecessors': predecessors}

    def print_routing_tables(self):
        for node_id in self.routing_table:
            print(f"Routing table for Node {node_id}:")
            for target_node_id in self.routing_table[node_id]['distances']:
                distance = self.routing_table[node_id]['distances'][target_node_id]
                predecessor = self.routing_table[node_id]['predecessors'][target_node_id]
                print(f"  To Node {target_node_id}: Distance = {distance:.2f}, Predecessor = {predecessor}")
            print()

