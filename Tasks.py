import random
import time
from threading import Thread

class Task:
    def __init__(self, task_id, duration):
        self.task_id = task_id
        self.duration = duration
        self.start_time = None
        self.end_time = None

    def execute(self):
        self.start_time = time.time()
        time.sleep(self.duration)
        self.end_time = time.time()
        start_time_str = time.strftime("%H:%M:%S", time.localtime(self.start_time))
        end_time_str = time.strftime("%H:%M:%S", time.localtime(self.end_time))
        print(f"Task {self.task_id} started at {start_time_str} and ended at {end_time_str}.")

class TaskGenerator:
    def __init__(self, max_duration, num_tasks):
        self.max_duration = max_duration
        self.num_tasks = num_tasks
        self.task_buffer = []

    def generate_tasks(self):
        for i in range(self.num_tasks):
            duration = random.randint(1, self.max_duration)
            task = Task(i, duration)
            self.task_buffer.append(task)

    def get_next_task(self):
        if len(self.task_buffer) > 0:
            return self.task_buffer.pop(0)
        else:
            return None

    def execute_tasks(self):
        for task in self.task_buffer:
            print(f"Task {task.task_id} will take {task.duration} seconds to complete.")
        print("Executing tasks...")
        threads = []
        for task in self.task_buffer:
            thread = Thread(target=task.execute)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

# Example usage
max_duration = 5  # Maximum duration of a task
num_tasks = 3      # Number of tasks to generate

task_generator = TaskGenerator(max_duration, num_tasks)
task_generator.generate_tasks()

task_generator.execute_tasks()


"""
Sample Output
Task 0 will take 3 seconds to complete.
Task 1 will take 2 seconds to complete.
Task 2 will take 2 seconds to complete.
Executing tasks...
Task 1 started at 12:56:48 and ended at 12:56:50.
Task 2 started at 12:56:48 and ended at 12:56:50.
Task 0 started at 12:56:48 and ended at 12:56:51.
"""
