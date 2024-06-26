# import random
# import time
# from LoadBalancer import Node, Task, LoadBalancer
# from Network import *

# def main():
#     # Example usage
#     network = Network()

#     # Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
#     node1 = Node(1, 4, 400, -74.0060, 40.7128)
#     node2 = Node(2, 8, 500, -118.2437, 34.0522)
#     node3 = Node(3, 6, 600, -87.6298, 41.8781)
#     node4 = Node(4, 10, 100, -95.3698, 29.7604)

#     network.add_node(node1)
#     network.add_node(node2)
#     network.add_node(node3)
#     network.add_node(node4)

#     # Add connections, weights will be calculated based on geographical distance
#     network.add_connection(1, 2)
#     network.add_connection(1, 3)
#     network.add_connection(1, 4)
#     network.add_connection(2, 3)
#     network.add_connection(2, 4)
#     network.add_connection(3, 4)

#     # Visualize the network
#     network.visualize()


#     nodes = [
#         Node(1, 4, 400, -74.0060, 40.7128),
#         Node(2, 8, 500, -118.2437, 34.0522),
#         Node(3, 6, 600, -87.6298, 41.8781),
#         Node(4, 10, 100, -95.3698, 29.7604)
#     ]

#     lb = LoadBalancer(nodes)
#     lb.start()

#     for node in nodes:
#         print(f"Node {node.node_id} properties:")
#         print(f"  Available: {node.available}")
#         print(f"  Tasks: {node.tasks}")
#         print(f"  Computational Power: {node.computational_power}")
#         print(f"  Memory Size: {node.memory_size}")
#         print(f"  Longitude: {node.longitude}")
#         print(f"  Latitude: {node.latitude}")
#         print()

#     for node in nodes:
#         print(f"Routing table for Node {node.node_id}:")
#         distances = lb.routing_table[node.node_id]['distances']
#         predecessors = lb.routing_table[node.node_id]['predecessors']
#         for dest, dist in distances.items():
#             pred = predecessors[dest]
#             print(f"  To Node {dest}: Distance = {dist:.2f}, Predecessor = {pred}")
#         print()

#     task_id = 0
#     while True:
#         task_duration = random.randint(1, 5)
#         task_data_size = random.randint(50, 700)
#         task_location = (random.uniform(29.0, 42.0), random.uniform(-118.0, -74.0))
#         task = Task(task_id, task_duration, task_data_size, task_location)
#         print(f"Generated Task {task_id} with duration {task_duration} s, data size {task_data_size} MB, and location {task_location}")
#         lb.add_task(task)
#         task_id += 1
#         time.sleep(1.5)  # Slow down task generation for clarity

# if __name__ == "__main__":
#     main()



import random
import time
from LoadBalancer import Node, Task, LoadBalancer
from Network import Network

def main():
    # Example usage
    network = Network()

    # Add nodes with geographical coordinates (latitude, longitude), computational power, and memory
    node1 = Node(1, 4, 400, -74.0060, 40.7128)
    node2 = Node(2, 8, 500, -118.2437, 34.0522)
    node3 = Node(3, 6, 600, -87.6298, 41.8781)
    node4 = Node(4, 10, 100, -95.3698, 29.7604)

    network.add_node(node1)
    network.add_node(node2)
    network.add_node(node3)
    network.add_node(node4)

    # Add connections, weights will be calculated based on geographical distance
    network.add_connection(1, 2)
    network.add_connection(1, 3)
    network.add_connection(1, 4)
    network.add_connection(2, 3)
    network.add_connection(2, 4)
    network.add_connection(3, 4)

    # Visualize the network
    network.visualize()

    nodes = [node1, node2, node3, node4]

    lb = LoadBalancer(nodes)
    lb.start()

    for node in nodes:
        print(f"Node {node.node_id} properties:")
        print(f"  Available: {node.available}")
        print(f"  Tasks: {node.tasks}")
        print(f"  Computational Power: {node.computational_power}")
        print(f"  Memory Size: {node.memory_size}")
        print(f"  Longitude: {node.longitude}")
        print(f"  Latitude: {node.latitude}")
        print()

    for node in nodes:
        print(f"Routing table for Node {node.node_id}:")
        distances = lb.routing_table[node.node_id]['distances']
        predecessors = lb.routing_table[node.node_id]['predecessors']
        for dest, dist in distances.items():
            pred = predecessors[dest]
            print(f"  To Node {dest}: Distance = {dist:.2f}, Predecessor = {pred}")
        print()

    task_id = 0
    while True:
        task_duration = random.randint(1, 5)
        task_data_size = random.randint(50, 700)
        task_location = (random.uniform(29.0, 42.0), random.uniform(-118.0, -74.0))
        task = Task(task_id, task_duration, task_data_size, task_location)
        print(f"Generated Task {task_id} with duration {task_duration} s, data size {task_data_size} MB, and location {task_location}")
        lb.add_task(task)
        task_id += 1
        time.sleep(1.5)  # Slow down task generation for clarity

if __name__ == "__main__":
    main()

