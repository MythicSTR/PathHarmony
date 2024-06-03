from Network import *
from Tasks import *

class LoadBalancer:
    def __init__(self, network):
        self.network = network

    def find_closest_node(self, current_node_id, remaining_nodes):
        closest_node_id = None
        min_distance = float('inf')
        for node_id in remaining_nodes:
            if node_id != current_node_id:
                path = self.network.graph.nodes[current_node_id]['routing_table'].get(node_id, [])
                if path:
                    distance = self.network.calculate_geographical_distance(current_node_id, path[-1])
                    if distance < min_distance:
                        min_distance = distance
                        closest_node_id = node_id
        return closest_node_id

    def distribute_task(self, task):
        remaining_data_size = task.data_size
        selected_nodes = []
        current_node_id = None

        # Find the initial closest node to distribute the task
        for node_id, node_data in self.network.graph.nodes(data=True):
            if node_data['status'] == 'active':
                current_node_id = node_id
                selected_nodes.append(current_node_id)
                remaining_data_size -= min(node_data['memory'], remaining_data_size)
                break

        # Continue to find the closest nodes until the data is fully distributed
        while remaining_data_size > 0:
            remaining_nodes = [node_id for node_id, node_data in self.network.graph.nodes(data=True) if node_data['status'] == 'active' and node_id not in selected_nodes]
            current_node_id = self.find_closest_node(current_node_id, remaining_nodes)
            if current_node_id is None:
                break
            selected_nodes.append(current_node_id)
            node_data = self.network.graph.nodes[current_node_id]
            remaining_data_size -= min(node_data['memory'], remaining_data_size)

        return selected_nodes

    def execute_task(self, task):
        nodes = self.distribute_task(task)
        print(f"Task {task.task_id} with data size {task.data_size} MB is distributed among nodes: {nodes}")

# Example usage
network = Network()

# Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
node1 = Node(1, "192.168.1.1", "node1", "active", 37.7749, -122.4194, 10, 32)  # San Francisco, CA
node2 = Node(2, "192.168.1.2", "node2", "inactive", 34.0522, -118.2437, 8, 16)  # Los Angeles, CA
node3 = Node(3, "192.168.1.3", "node3", "active", 40.7128, -74.0060, 15, 64)  # New York, NY
node4 = Node(4, "192.168.1.4", "node4", "active", 41.8781, -87.6298, 20, 128)  # Chicago, IL

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
max_data_size = 500  # Maximum data size of a task in MB
num_tasks = 3  # Number of tasks to generate

task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
task_generator.generate_tasks()

for task in task_generator.task_buffer:
    load_balancer.execute_task(task)
