import time

class Node:
    def __init__(self, node_id, latitude, longitude, computational_power, memory_size, stop_event):
        self.node_id = node_id
        self.latitude = latitude
        self.longitude = longitude
        self.computational_power = computational_power
        self.memory_size = memory_size
        self.current_memory_usage = 0
        self.tasks = []  # List of tasks assigned to the node
        self.routing_table = {}  # Routing table for the node
        self.stop_event = stop_event

    def is_available(self):
        return self.current_memory_usage < self.memory_size

    def run(self):
        while not self.stop_event.is_set():
            if self.tasks:
                task, data_size = self.tasks.pop(0)
                print(f"Node {self.node_id} executing Task {task.task_id}")
                self.execute_task(task, data_size)
                print(f"Node {self.node_id} completed Task {task.task_id}")
                self.current_memory_usage -= data_size
            else:
                time.sleep(2)  # No task assigned, wait

    def assign_task(self, task, data_size):
        self.current_memory_usage += data_size
        self.tasks.append((task, data_size))

    def execute_task(self, task, data_size):
        time.sleep(task.duration)  # Simulating task execution
