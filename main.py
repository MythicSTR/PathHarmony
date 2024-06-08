from Tasks import TaskGenerator, Task
from LoadBalancer import LoadBalancer
from Node import Node
from queue import Queue
import time
from threading import Event, Thread
from Network import Network

def main():
    buffer_size = 10
    buffer = Queue(buffer_size)
    stop_event = Event()

    # Node locations (latitude and longitude)
    node_locations = {
        1: (40.7128, -74.0060),  # New York
        2: (34.0522, -118.2437), # Los Angeles
        3: (41.8781, -87.6298),  # Chicago
        4: (29.7604, -95.3698)   # Houston
    }

    # Node computational power and memory size
    node_specs = {
        1: (4, 400),   # Computational Power: 4, Memory Size: 400 MB
        2: (8, 500),  # Computational Power: 8, Memory Size: 500 MB
        3: (6, 600),  # Computational Power: 6, Memory Size: 600 MB
        4: (10, 100)  # Computational Power: 10, Memory Size: 100 MB
    }

    nodes = [Node(node_id, *node_locations[node_id], *node_specs[node_id], stop_event) for node_id in node_locations]

    # Print node properties
    for node in nodes:
        print(f"Node {node.node_id} properties:")
        print(f"  Available: {node.is_available()}")
        print(f"  Tasks: {node.tasks}")
        print(f"  Computational Power: {node.computational_power}")
        print(f"  Memory Size: {node.memory_size}")
        print(f"  Longitude: {node.longitude}")
        print(f"  Latitude: {node.latitude}")
        print()

    load_balancer = LoadBalancer(buffer, nodes, stop_event)
    load_balancer.calculate_routing_tables()
    load_balancer.print_routing_tables()
    
    task_generator = TaskGenerator(buffer_size, buffer, stop_event, node_locations)

    try:
        for node in nodes:
            Thread(target=node.run).start()  # Start a separate thread for each node
        load_balancer.start()
        task_generator.start()

        while not stop_event.is_set():
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping...")
        stop_event.set()
        for node in nodes:
            node.join()  # Wait for node threads to finish
        load_balancer.join()
        task_generator.join()

if __name__ == "__main__":
    main()
