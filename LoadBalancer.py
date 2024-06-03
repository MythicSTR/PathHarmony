# from Network import *
# from Tasks import *
# import geopy.distance

# class LoadBalancer:
#     def __init__(self, network):
#         self.network = network

#     def find_nearest_node(self, task_location):
#         nearest_node_id = None
#         min_distance = float('inf')

#         for node_id, node_data in self.network.graph.nodes(data=True):
#             if node_data['status'] == 'active':
#                 node_location = (node_data['latitude'], node_data['longitude'])
#                 distance = geopy.distance.geodesic(task_location, node_location).kilometers
#                 if distance < min_distance:
#                     min_distance = distance
#                     nearest_node_id = node_id

#         return nearest_node_id

#     def distribute_task(self, task):
#         task_location = (task.latitude, task.longitude)
#         nearest_node_id = self.find_nearest_node(task_location)

#         if nearest_node_id is not None:
#             return [nearest_node_id]

#         return []

#     def execute_task(self, task):
#         nodes = self.distribute_task(task)
#         print(f"Task {task.task_id} with data size {task.data_size} MB is distributed among nodes: {nodes}")

# # Example usage
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

# # Create the LoadBalancer
# load_balancer = LoadBalancer(network)

# # Generate and execute tasks
# max_duration = 5  # Maximum duration of a task in seconds
# max_data_size = 500  # Maximum data size of a task in MB
# num_tasks = 3  # Number of tasks to generate

# task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
# task_generator.generate_tasks()

# for task in task_generator.task_buffer:
#     load_balancer.execute_task(task)

from Network import *
from Tasks import *
import geopy.distance
import time

class LoadBalancer:
    def __init__(self, network):
        self.network = network

    def find_nearest_node(self, task_location):
        nearest_node_id = None
        min_distance = float('inf')

        for node_id, node_data in self.network.graph.nodes(data=True):
            if node_data['status'] == 'active' and not node_data.get('is_busy', False):
                node_location = (node_data['latitude'], node_data['longitude'])
                distance = geopy.distance.geodesic(task_location, node_location).kilometers
                if distance < min_distance:
                    min_distance = distance
                    nearest_node_id = node_id

        return nearest_node_id

    def distribute_task(self, task):
        task_location = (task.latitude, task.longitude)
        nearest_node_id = self.find_nearest_node(task_location)

        if nearest_node_id is not None:
            selected_nodes = [nearest_node_id]
            remaining_data_size = task.data_size

            # Distribute data based on available memory of nodes
            for node_id in selected_nodes:
                node_data = self.network.graph.nodes[node_id]
                data_to_assign = min(remaining_data_size, node_data['memory'])
                remaining_data_size -= data_to_assign
                node_data['memory'] -= data_to_assign  # Update node's memory
                if remaining_data_size == 0:
                    break

            # If data remains, distribute it to additional nodes
            if remaining_data_size > 0:
                remaining_nodes = [node_id for node_id in self.network.graph.nodes if node_id not in selected_nodes]
                for node_id in remaining_nodes:
                    node_data = self.network.graph.nodes[node_id]
                    data_to_assign = min(remaining_data_size, node_data['memory'])
                    remaining_data_size -= data_to_assign
                    node_data['memory'] -= data_to_assign  # Update node's memory
                    selected_nodes.append(node_id)
                    if remaining_data_size == 0:
                        break

            # Update node status to indicate they're busy
            for node_id in selected_nodes:
                self.network.graph.nodes[node_id]['is_busy'] = True

            return selected_nodes

        return []


    def execute_task(self, task):
        nodes = self.distribute_task(task)
        if nodes:
            print(f"Task {task.task_id} with data size {task.data_size} MB is distributed among nodes: {nodes}")
            # Simulate task execution time
            time.sleep(task.duration)
            # Reset node status after task completion
            for node_id in nodes:
                self.network.graph.nodes[node_id]['is_busy'] = False
            print(f"Task {task.task_id} completed successfully.")
        else:
            print(f"No available node found to execute Task {task.task_id}")

# Example usage
network = Network()

# Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
node1 = Node(1, "192.168.1.1", "node1", "active", 37.7749, -122.4194, 10, 300)  # San Francisco, CA
node2 = Node(2, "192.168.1.2", "node2", "inactive", 34.0522, -118.2437, 8, 100)  # Los Angeles, CA
node3 = Node(3, "192.168.1.3", "node3", "active", 40.7128, -74.0060, 15, 200)  # New York, NY
node4 = Node(4, "192.168.1.4", "node4", "active", 41.8781, -87.6298, 20, 400)  # Chicago, IL

network.add_node(node1)
network.add_node(node2)
network.add_node(node3)
network.add_node(node4)

# Add connections, weights will be calculated based on geographical distance
network.add_connection(1, 2)
network.add_connection(1, 3)
network.add_connection(2, 4)
network.add_connection(3, 4)

# Visualize the network
network.visualize()

# Update routing tables
network.update_routing_tables()

# Print routing tables
network.print_routing_tables()

# Create the LoadBalancer
load_balancer = LoadBalancer(network)

# Generate and execute tasks
max_duration = 5  # Maximum duration of a task in seconds
max_data_size = 1000  # Maximum data size of a task in MB
num_tasks = 3  # Number of tasks to generate

task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
task_generator.generate_tasks()

for task in task_generator.task_buffer:
    load_balancer.execute_task(task)
