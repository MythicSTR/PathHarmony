# import random
# import time
# from threading import Thread

# class Task:
#     def __init__(self, task_id, duration, data_size):
#         self.task_id = task_id
#         self.duration = duration
#         self.data_size = data_size
#         self.start_time = None
#         self.end_time = None

#     def execute(self):
#         self.start_time = time.time()
#         time.sleep(self.duration)
#         self.end_time = time.time()
#         start_time_str = time.strftime("%H:%M:%S", time.localtime(self.start_time))
#         end_time_str = time.strftime("%H:%M:%S", time.localtime(self.end_time))
#         print(f"Task {self.task_id} (Data Size: {self.data_size} MB) started at {start_time_str} and ended at {end_time_str}.")

# class TaskGenerator:
#     def __init__(self, max_duration, max_data_size, num_tasks):
#         self.max_duration = max_duration
#         self.max_data_size = max_data_size
#         self.num_tasks = num_tasks
#         self.task_buffer = []

#     def generate_tasks(self):
#         for i in range(self.num_tasks):
#             duration = random.randint(1, self.max_duration)
#             data_size = random.randint(1, self.max_data_size)
#             task = Task(i, duration, data_size)
#             self.task_buffer.append(task)

#     def get_next_task(self):
#         if len(self.task_buffer) > 0:
#             return self.task_buffer.pop(0)
#         else:
#             return None

#     def execute_tasks(self):
#         for task in self.task_buffer:
#             print(f"Task {task.task_id} will take {task.duration} seconds to complete and has a data size of {task.data_size} MB.")
#         print("Executing tasks...")
#         threads = []
#         for task in self.task_buffer:
#             thread = Thread(target=task.execute)
#             thread.start()
#             threads.append(thread)
#         for thread in threads:
#             thread.join()

# # Example usage
# max_duration = 5  # Maximum duration of a task in seconds
# max_data_size = 500  # Maximum data size of a task in MB
# num_tasks = 3  # Number of tasks to generate

# task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
# task_generator.generate_tasks()

# task_generator.execute_tasks()

# """
# Sample Output
# Task 0 will take 3 seconds to complete and has a data size of 200 MB.
# Task 1 will take 2 seconds to complete and has a data size of 150 MB.
# Task 2 will take 2 seconds to complete and has a data size of 300 MB.
# Executing tasks...
# Task 1 (Data Size: 150 MB) started at 12:56:48 and ended at 12:56:50.
# Task 2 (Data Size: 300 MB) started at 12:56:48 and ended at 12:56:50.
# Task 0 (Data Size: 200 MB) started at 12:56:48 and ended at 12:56:51.
# """

import random
import time
from threading import Thread

class Task:
    def __init__(self, task_id, duration, data_size):
        self.task_id = task_id
        self.duration = duration
        self.data_size = data_size
        self.start_time = None
        self.end_time = None
        self.location, self.latitude, self.longitude = self.select_random_location()

    def select_random_location(self):
        # Dictionary of real-world locations with latitude and longitude coordinates
        locations = {
            "New York, USA": (40.7128, -74.0060),
            "London, UK": (51.5074, -0.1278),
            "Tokyo, Japan": (35.6895, 139.6917),
            "Paris, France": (48.8566, 2.3522),
            "Sydney, Australia": (-33.8688, 151.2093),
            "Rio de Janeiro, Brazil": (-22.9068, -43.1729),
            "Moscow, Russia": (55.7558, 37.6173),
            # Add more locations as needed...
        }
        location = random.choice(list(locations.keys()))
        latitude, longitude = locations[location]
        return location, latitude, longitude

    def execute(self):
        self.start_time = time.time()
        time.sleep(self.duration)
        self.end_time = time.time()
        start_time_str = time.strftime("%H:%M:%S", time.localtime(self.start_time))
        end_time_str = time.strftime("%H:%M:%S", time.localtime(self.end_time))
        print(f"Task {self.task_id} (Data Size: {self.data_size} MB) started at {start_time_str} and ended at {end_time_str}. Location: {self.location} (Latitude: {self.latitude}, Longitude: {self.longitude})")

class TaskGenerator:
    def __init__(self, max_duration, max_data_size, num_tasks):
        self.max_duration = max_duration
        self.max_data_size = max_data_size
        self.num_tasks = num_tasks
        self.task_buffer = []

    def generate_tasks(self):
        for i in range(self.num_tasks):
            duration = random.randint(1, self.max_duration)
            data_size = random.randint(1, self.max_data_size)
            task = Task(i, duration, data_size)
            self.task_buffer.append(task)

    def get_next_task(self):
        if len(self.task_buffer) > 0:
            return self.task_buffer.pop(0)
        else:
            return None

    def execute_tasks(self):
        for task in self.task_buffer:
            print(f"Task {task.task_id} will take {task.duration} seconds to complete and has a data size of {task.data_size} MB.")
        print("Executing tasks...")
        threads = []
        for task in self.task_buffer:
            thread = Thread(target=task.execute)
            thread.start()
            threads.append(thread)
        for thread in threads:
            thread.join()

# # Example usage
# max_duration = 5  # Maximum duration of a task in seconds
# max_data_size = 500  # Maximum data size of a task in MB
# num_tasks = 3  # Number of tasks to generate

# task_generator = TaskGenerator(max_duration, max_data_size, num_tasks)
# task_generator.generate_tasks()

# task_generator.execute_tasks()

"""
Sample Output
Task 0 will take 3 seconds to complete and has a data size of 200 MB.
Task 1 will take 2 seconds to complete and has a data size of 150 MB.
Task 2 will take 2 seconds to complete and has a data size of 300 MB.
Executing tasks...
Task 1 (Data Size: 150 MB) started at 12:56:48 and ended at 12:56:50.
Task 2 (Data Size: 300 MB) started at 12:56:48 and ended at 12:56:50.
Task 0 (Data Size: 200 MB) started at 12:56:48 and ended at 12:56:51.
"""
