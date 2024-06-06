# from Network import *
# from Tasks import *
# import geopy.distance
# import time
# from threading import Thread, Lock
# from queue import Queue

# class LoadBalancer:
#     def __init__(self, network):
#         self.network = network
#         self.lock = Lock()
#         self.task_queue = Queue()
#         self.active_tasks = []

#     def find_nearest_node(self, task_location):
#         nearest_node_id = None
#         min_distance = float('inf')

#         for node_id, node_data in self.network.graph.nodes(data=True):
#             if node_data['status'] == 'active' and not node_data.get('is_busy', False):
#                 node_location = (node_data['latitude'], node_data['longitude'])
#                 distance = geopy.distance.geodesic(task_location, node_location).kilometers
#                 if distance < min_distance:
#                     min_distance = distance
#                     nearest_node_id = node_id

#         return nearest_node_id

#     def distribute_task(self, task):
#         task_location = (task.latitude, task.longitude)
#         nearest_node_id = self.find_nearest_node(task_location)
#         selected_nodes = []

#         if nearest_node_id is not None:
#             remaining_data_size = task.data_size

#             # Distribute data starting from the nearest node
#             nodes_to_consider = [nearest_node_id] + [node_id for node_id in self.network.graph.nodes if node_id != nearest_node_id]
#             for node_id in nodes_to_consider:
#                 node_data = self.network.graph.nodes[node_id]
#                 if node_data['status'] == 'active' and not node_data.get('is_busy', False):
#                     data_to_assign = min(remaining_data_size, node_data['memory'])
#                     remaining_data_size -= data_to_assign
#                     node_data['memory'] -= data_to_assign  # Update node's memory
#                     selected_nodes.append((node_id, data_to_assign))
#                     if remaining_data_size == 0:
#                         break

#             # Update node status to indicate they're busy
#             for node_id, _ in selected_nodes:
#                 self.network.graph.nodes[node_id]['is_busy'] = True

#         return selected_nodes

#     def execute_task_on_node(self, task, node_id, data_size):
#         start_time = time.time()
#         # Simulate task execution time
#         time.sleep(task.duration)
#         end_time = time.time()
#         with self.lock:
#             # Reset node status after task completion
#             self.network.graph.nodes[node_id]['is_busy'] = False
#             # Restore node's memory
#             self.network.graph.nodes[node_id]['memory'] += data_size
#         print(f"Task {task.task_id} completed on Node {node_id}. Data size processed: {data_size} MB. Start time: {start_time}, End time: {end_time}")

#     def execute_task(self, task):
#         nodes = self.distribute_task(task)
#         if nodes:
#             print(f"Task {task.task_id} with data size {task.data_size} MB is distributed among nodes: {nodes}")
#             threads = []
#             for node_id, data_size in nodes:
#                 thread = Thread(target=self.execute_task_on_node, args=(task, node_id, data_size))
#                 thread.start()
#                 threads.append(thread)
#             for thread in threads:
#                 thread.join()
#             print(f"Task {task.task_id} completed successfully.")
#         else:
#             print(f"No available node found to execute Task {task.task_id}")

#     def check_and_execute_tasks(self):
#         while not self.task_queue.empty():
#             task = self.task_queue.get()
#             self.execute_task(task)
#             self.task_queue.task_done()

#     def run(self, tasks):
#         for task in tasks:
#             self.task_queue.put(task)
        
#         # Create worker threads
#         worker_threads = []
#         for _ in range(len(tasks)):
#             worker_thread = Thread(target=self.check_and_execute_tasks)
#             worker_thread.start()
#             worker_threads.append(worker_thread)
        
#         for worker_thread in worker_threads:
#             worker_thread.join()

# # Example usage
# network = Network()

# # Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
# node1 = Node(1, "192.168.1.1", "node1", "active", 37.7749, -122.4194, 10, 300)  # San Francisco, CA
# node2 = Node(2, "192.168.1.2", "node2", "inactive", 34.0522, -118.2437, 8, 100)  # Los Angeles, CA
# node3 = Node(3, "192.168.1.3", "node3", "active", 40.7128, -74.0060, 15, 200)  # New York, NY
# node4 = Node(4, "192.168.1.4", "node4", "active", 41.8781, -87.6298, 20, 400)  # Chicago, IL

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
# max_data_size = 1000  # Maximum data size of a task in MB
# num_tasks = 3  # Number of tasks to generate

# task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
# task_generator.generate_tasks()

# # Run the LoadBalancer with the generated tasks
# load_balancer.run(task_generator.task_buffer)

# from Network import *
# from Tasks import *
# import geopy.distance
# import time
# from threading import Thread, Lock, Condition
# from queue import Queue

# class LoadBalancer:
#     def __init__(self, network):
#         self.network = network
#         self.lock = Lock()
#         self.condition = Condition(self.lock)
#         self.task_queue = Queue()
#         self.active_tasks = []

#     def find_nearest_node(self, task_location):
#         nearest_node_id = None
#         min_distance = float('inf')

#         for node_id, node_data in self.network.graph.nodes(data=True):
#             if node_data['status'] == 'active' and not node_data.get('is_busy', False):
#                 node_location = (node_data['latitude'], node_data['longitude'])
#                 distance = geopy.distance.geodesic(task_location, node_location).kilometers
#                 if distance < min_distance:
#                     min_distance = distance
#                     nearest_node_id = node_id

#         return nearest_node_id

#     def distribute_task(self, task):
#         task_location = (task.latitude, task.longitude)
#         nearest_node_id = self.find_nearest_node(task_location)
#         selected_nodes = []

#         if nearest_node_id is not None:
#             remaining_data_size = task.data_size

#             # Distribute data starting from the nearest node
#             nodes_to_consider = [nearest_node_id] + [node_id for node_id in self.network.graph.nodes if node_id != nearest_node_id]
#             for node_id in nodes_to_consider:
#                 node_data = self.network.graph.nodes[node_id]
#                 if node_data['status'] == 'active' and not node_data.get('is_busy', False):
#                     data_to_assign = min(remaining_data_size, node_data['memory'])
#                     remaining_data_size -= data_to_assign
#                     node_data['memory'] -= data_to_assign  # Update node's memory
#                     selected_nodes.append((node_id, data_to_assign))
#                     if remaining_data_size == 0:
#                         break

#             # Update node status to indicate they're busy
#             for node_id, _ in selected_nodes:
#                 self.network.graph.nodes[node_id]['is_busy'] = True

#         return selected_nodes

#     def execute_task_on_node(self, task, node_id, data_size):
#         start_time = time.time()
#         # Simulate task execution time
#         time.sleep(task.duration)
#         end_time = time.time()
#         with self.lock:
#             # Reset node status after task completion
#             self.network.graph.nodes[node_id]['is_busy'] = False
#             # Restore node's memory
#             self.network.graph.nodes[node_id]['memory'] += data_size
#             self.condition.notify_all()  # Notify other threads that a node is available
#         print(f"Task {task.task_id} completed on Node {node_id}. Data size processed: {data_size} MB. Start time: {start_time}, End time: {end_time}")

#     def execute_task(self, task):
#         with self.lock:
#             nodes = self.distribute_task(task)
#         if nodes:
#             print(f"Task {task.task_id} with data size {task.data_size} MB is distributed among nodes: {nodes}")
#             threads = []
#             for node_id, data_size in nodes:
#                 thread = Thread(target=self.execute_task_on_node, args=(task, node_id, data_size))
#                 thread.start()
#                 threads.append(thread)
#             for thread in threads:
#                 thread.join()
#             print(f"Task {task.task_id} completed successfully.")
#         else:
#             print(f"No available node found to execute Task {task.task_id}")

#     def worker(self):
#         while True:
#             task = self.task_queue.get()
#             if task is None:
#                 break
#             self.execute_task(task)
#             self.task_queue.task_done()

#     def run(self, tasks):
#         num_workers = len(self.network.graph.nodes)  # Number of worker threads
#         threads = []

#         for i in range(num_workers):
#             thread = Thread(target=self.worker)
#             thread.start()
#             threads.append(thread)

#         for task in tasks:
#             self.task_queue.put(task)

#         self.task_queue.join()

#         for i in range(num_workers):
#             self.task_queue.put(None)

#         for thread in threads:
#             thread.join()

# # Example usage
# network = Network()

# # Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
# node1 = Node(1, "192.168.1.1", "node1", "active", 37.7749, -122.4194, 10, 300)  # San Francisco, CA
# node2 = Node(2, "192.168.1.2", "node2", "inactive", 34.0522, -118.2437, 8, 100)  # Los Angeles, CA
# node3 = Node(3, "192.168.1.3", "node3", "active", 40.7128, -74.0060, 15, 200)  # New York, NY
# node4 = Node(4, "192.168.1.4", "node4", "active", 41.8781, -87.6298, 20, 400)  # Chicago, IL

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
# max_data_size = 1000  # Maximum data size of a task in MB
# num_tasks = 3  # Number of tasks to generate

# task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
# task_generator.generate_tasks()

# # Run the LoadBalancer with the generated tasks
# load_balancer.run(task_generator.task_buffer)


from Network import *
from Tasks import *
import geopy.distance
import time
from threading import Thread, Lock, Condition
from queue import Queue

class LoadBalancer:
    def __init__(self, network):
        self.network = network
        self.lock = Lock()
        self.condition = Condition(self.lock)
        self.task_queue = Queue()
        self.active_tasks = []

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
        selected_nodes = []

        if nearest_node_id is not None:
            remaining_data_size = task.data_size

            # Distribute data starting from the nearest node
            nodes_to_consider = [nearest_node_id] + [node_id for node_id in self.network.graph.nodes if node_id != nearest_node_id]
            for node_id in nodes_to_consider:
                node_data = self.network.graph.nodes[node_id]
                if node_data['status'] == 'active' and not node_data.get('is_busy', False):
                    data_to_assign = min(remaining_data_size, node_data['memory'])
                    remaining_data_size -= data_to_assign
                    node_data['memory'] -= data_to_assign  # Update node's memory
                    selected_nodes.append((node_id, data_to_assign))
                    if remaining_data_size == 0:
                        break

            # Update node status to indicate they're busy
            for node_id, _ in selected_nodes:
                self.network.graph.nodes[node_id]['is_busy'] = True

        return selected_nodes

    def execute_task_on_node(self, task, node_id, data_size):
        start_time = time.time()
        # Simulate task execution time
        time.sleep(task.duration)
        end_time = time.time()
        with self.lock:
            # Reset node status after task completion
            self.network.graph.nodes[node_id]['is_busy'] = False
            # Restore node's memory
            self.network.graph.nodes[node_id]['memory'] += data_size
            self.condition.notify_all()  # Notify other threads that a node is available
        print(f"Task {task.task_id} completed on Node {node_id}. Data size processed: {data_size} MB. Start time: {start_time}, End time: {end_time}")

    def execute_task(self, task):
        while True:
            with self.lock:
                nodes = self.distribute_task(task)
                if nodes:
                    print(f"Task {task.task_id} with data size {task.data_size} MB is distributed among nodes: {nodes}")
                    break
                else:
                    # Wait for a node to become available
                    self.condition.wait()

        threads = []
        for node_id, data_size in nodes:
            thread = Thread(target=self.execute_task_on_node, args=(task, node_id, data_size))
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()
        print(f"Task {task.task_id} completed successfully.")

    def worker(self):
        while True:
            task = self.task_queue.get()
            if task is None:
                break
            self.execute_task(task)
            self.task_queue.task_done()

    def run(self, tasks):
        num_workers = len(self.network.graph.nodes)  # Number of worker threads
        threads = []

        for i in range(num_workers):
            thread = Thread(target=self.worker)
            thread.start()
            threads.append(thread)

        for task in tasks:
            self.task_queue.put(task)

        self.task_queue.join()

        for i in range(num_workers):
            self.task_queue.put(None)

        for thread in threads:
            thread.join()

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

# Run the LoadBalancer with the generated tasks
load_balancer.run(task_generator.task_buffer)
