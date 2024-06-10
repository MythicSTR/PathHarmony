import threading
import time
import math

class Node:
    def __init__(self, node_id, computational_power, memory_size, longitude, latitude):
        self.node_id = node_id
        self.computational_power = computational_power
        self.memory_size = memory_size
        self.longitude = longitude
        self.latitude = latitude
        self.available = True
        self.tasks = []

    def assign_task(self, task):
        self.tasks.append(task)
        self.memory_size -= task.data_size
        self.available = False
        print(f"Task {task.task_id} assigned to Node {self.node_id} with data size: {task.data_size} MB")

    def execute_task(self, task):
        print(f"Node {self.node_id} executing Task {task.task_id}")
        time.sleep(task.duration)
        self.tasks.remove(task)
        self.memory_size += task.data_size
        self.available = True
        print(f"Node {self.node_id} completed Task {task.task_id}")

    def is_available(self):
        return self.available and self.memory_size > 0

class Task:
    def __init__(self, task_id, duration, data_size, location):
        self.task_id = task_id
        self.duration = duration
        self.data_size = data_size
        self.location = location

class LoadBalancer(threading.Thread):
    def __init__(self, nodes):
        threading.Thread.__init__(self)
        self.nodes = nodes
        self.tasks = []
        self.graph = self.build_graph()
        self.routing_table = self.build_routing_table()

    def run(self):
        while True:
            if self.tasks:
                task = self.tasks.pop(0)
                self.distribute_task(task)
            time.sleep(1)

    def build_graph(self):
        graph = {}
        for node in self.nodes:
            graph[node.node_id] = {}
            for other_node in self.nodes:
                if node.node_id != other_node.node_id:
                    distance = self.calculate_distance(node, other_node)
                    graph[node.node_id][other_node.node_id] = {'weight': distance}
        return graph

    def calculate_distance(self, node1, node2):
        lon1, lat1, lon2, lat2 = map(math.radians, [node1.longitude, node1.latitude, node2.longitude, node2.latitude])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = 6371 * c  # Radius of earth in kilometers
        return distance

    def build_routing_table(self):
        routing_table = {}
        for node in self.nodes:
            distances, predecessors = self.dijkstra(node.node_id)
            routing_table[node.node_id] = {'distances': distances, 'predecessors': predecessors}
        return routing_table

    def dijkstra(self, start_node_id):
        distances = {node.node_id: float('inf') for node in self.nodes}
        predecessors = {node.node_id: None for node in self.nodes}
        distances[start_node_id] = 0
        unvisited = {node.node_id for node in self.nodes}

        while unvisited:
            current_node_id = min(unvisited, key=lambda node_id: distances[node_id])
            unvisited.remove(current_node_id)

            for neighbor, data in self.graph[current_node_id].items():
                new_distance = distances[current_node_id] + data['weight']
                if new_distance < distances[neighbor]:
                    distances[neighbor] = new_distance
                    predecessors[neighbor] = current_node_id

        return distances, predecessors

    def choose_nearest_node(self, location):
        min_distance = float('inf')
        nearest_node = None

        for node in self.nodes:
            distance = self.calculate_geo_distance(location, (node.latitude, node.longitude))
            if distance < min_distance:
                min_distance = distance
                nearest_node = node

        return nearest_node

    def calculate_geo_distance(self, loc1, loc2):
        lon1, lat1, lon2, lat2 = map(math.radians, [loc1[1], loc1[0], loc2[1], loc2[0]])
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = 6371 * c  # Radius of earth in kilometers
        return distance

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
            task_part = Task(task.task_id, task.duration, data_to_assign, task.location)
            node.assign_task(task_part)
            print(f"Task {task.task_id} partially distributed to Node {node.node_id}. Data size: {data_to_assign} MB")
            threading.Thread(target=node.execute_task, args=(task_part,)).start()

    def add_task(self, task):
        self.tasks.append(task)
        print(f"Task {task.task_id} added to LoadBalancer")
