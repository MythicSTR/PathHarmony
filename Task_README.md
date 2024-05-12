# Task Execution Simulator

This Python program simulates the execution of tasks in a distributed computing environment. It includes a Task class to represent individual tasks, a TaskGenerator class to create and manage tasks, and a main function to demonstrate the task execution process.

Task Class

## Task(task_id, duration)

    task_id (int): The unique identifier of the task.
    duration (int): The duration of the task in seconds.

## Attributes

    task_id (int): The unique identifier of the task.
    duration (int): The duration of the task in seconds.
    start_time (float): The time when the task execution started.
    end_time (float): The time when the task execution ended.

## Methods

    execute(): Executes the task by sleeping for the specified duration and recording the start and end times.

## TaskGenerator Class
## TaskGenerator(max_duration, num_tasks)

    max_duration (int): The maximum duration of a task in seconds.
    num_tasks (int): The number of tasks to generate.

## Attributes

    max_duration (int): The maximum duration of a task in seconds.
    num_tasks (int): The number of tasks to generate.
    task_buffer (list): A list to store generated tasks.

## Methods

    generate_tasks(): Generates random tasks with durations between 1 and max_duration.
    get_next_task(): Retrieves the next task from the task buffer.
    execute_tasks(): Executes all generated tasks concurrently using threads.

## Main Function

    Generates a TaskGenerator instance with specified parameters.
    Generates tasks using generate_tasks() method.
    Executes tasks using execute_tasks() method.