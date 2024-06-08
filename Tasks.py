import time
import random
from threading import Thread

class TaskGenerator(Thread):
    def __init__(self, buffer_size, buffer, stop_event, node_locations):
        super().__init__()
        self.buffer = buffer
        self.buffer_size = buffer_size
        self.stop_event = stop_event
        self.node_locations = node_locations

    def run(self):
        task_id = 0
        while not self.stop_event.is_set():
            if self.buffer.full():
                time.sleep(1)  # Buffer is full, wait
            else:
                task = self.generate_task(task_id)
                self.buffer.put(task)
                print(f"Generated Task {task.task_id} with duration {task.duration} s, data size {task.data_size} MB, and location {task.location}")
                task_id += 1
                time.sleep(5)  # Delay task generation by 5 seconds

    def generate_task(self, task_id):
        duration = random.randint(1, 5)
        data_size = random.randint(100, 1000)
        location = random.choice(list(self.node_locations.values()))  # Choose a random node location
        return Task(task_id, duration, data_size, location)

class Task:
    def __init__(self, task_id, duration, data_size, location):
        self.task_id = task_id
        self.duration = duration
        self.data_size = data_size
        self.location = location