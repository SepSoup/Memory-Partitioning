import time
import random
from typing import List, Optional
from collections import deque
import matplotlib.pyplot as plt

# For single queue
waiting_processes_single_queue = deque()

class Process:
    def __init__(self, size: int, process_id: int, time_needed: float):
        self.process_id = process_id
        self.size = size
        self.size_on_memory = 0
        self.partition: Optional["Partition"] = None
        self.time_needed = time_needed
        self.waiting_time = 0.0

    def enter_into_partition(self, partition: "Partition"):
        self.partition = partition
        self.size_on_memory = min(partition.size, self.size)

    def exit_from_partition(self):
        self.partition = None
        self.size_on_memory = 0


class Partition:
    def __init__(self, size: int, partition_id: int):
        self.partition_id = partition_id
        self.size = size
        self.currently_occupied = 0
        self.process: Optional[Process] = None
        self.waiting_processes: List[Process] = []

    def add_new_process(self, process: Process, use_single_queue=False):
        if self.process is None:
            self.process = process
            self.currently_occupied = min(process.size, self.size)
            process.enter_into_partition(self)
        else:
            if use_single_queue:
                waiting_processes_single_queue.append(process)
            else:
                self.waiting_processes.append(process)

    def remove_current_process(self, use_single_queue=False):
        if self.process:
            self.process.exit_from_partition()
            self.process = None
            self.currently_occupied = 0
            if use_single_queue:
                if waiting_processes_single_queue:
                    next_process = waiting_processes_single_queue.popleft()
                    self.add_new_process(next_process, use_single_queue)
            else:
                if self.waiting_processes:
                    next_process = self.waiting_processes.pop(0)
                    self.add_new_process(next_process)

    def get_queue(self) -> List[Process]:
        return self.waiting_processes


def generate_random_processes(process_count: int):
    processes = []
    for i in range(process_count):
        size = random.randint(10, 100)  # Random size between 10MB and 100MB
        time_needed = random.uniform(1, 10)  # Random time needed between 1 and 10 seconds
        processes.append(Process(size, i + 1, time_needed))
    return processes


def generate_random_partitions(partition_count: int, memory_size: int):
    partitions = []
    total_size = 0
    for i in range(partition_count):
        remaining_memory = memory_size - total_size
        if remaining_memory <= 0:
            break
        size = random.randint(10, remaining_memory // (partition_count - i))  # Random size ensuring total size <= memory_size
        total_size += size
        partitions.append(Partition(size, i + 1))
    return partitions, total_size


def best_fit_allocation(processes: List[Process], partitions: List[Partition], use_single_queue=False):
    partitions.sort(key=lambda x: x.size)

    for process in processes:
        placed = False
        for partition in partitions:
            if process.size <= partition.size:
                if partition.process is None:
                    partition.add_new_process(process, use_single_queue)
                    placed = True
                    break
                elif not use_single_queue:
                    partition.add_new_process(process, use_single_queue)
                    placed = True
                    break
        if not placed and use_single_queue:
            waiting_processes_single_queue.append(process)


def simulate_execution(partitions: List[Partition], use_single_queue=False):
    start_time = time.time()
    total_execution_time = 0.0
    total_waiting_time = 0.0

    while any(partition.process or partition.waiting_processes for partition in partitions) or (use_single_queue and waiting_processes_single_queue):
        for partition in partitions:
            if partition.process:
                process_time_needed = partition.process.time_needed
                waiting_time_before_execution = partition.process.waiting_time
                print(f"Executing Process P{partition.process.process_id} in Partition {partition.partition_id} for {process_time_needed} seconds.")
                time.sleep(process_time_needed)
                partition.remove_current_process(use_single_queue)
                total_execution_time += process_time_needed
                total_waiting_time += waiting_time_before_execution

        # Update waiting time for processes in queue
        for partition in partitions:
            if partition.process:
                for process in partition.get_queue():
                    process.waiting_time += partition.process.time_needed

        if use_single_queue:
            for process in waiting_processes_single_queue:
                process.waiting_time += process_time_needed

    end_time = time.time()
    total_running_time = end_time - start_time

    return total_execution_time, total_running_time, total_waiting_time


def plot_comparison(single_queue_data, multi_queue_data):
    labels = ['Total Execution Time', 'Total Running Time', 'Total Waiting Time', 'Time Utilization']

    single_queue_values = [single_queue_data['execution_time'], single_queue_data['running_time'], single_queue_data['waiting_time'], single_queue_data['utilization']]
    multi_queue_values = [multi_queue_data['execution_time'], multi_queue_data['running_time'], multi_queue_data['waiting_time'], multi_queue_data['utilization']]

    x = range(len(labels))
    width = 0.35

    fig, ax = plt.subplots()
    ax.bar(x, single_queue_values, width, label='Single Queue')
    ax.bar([p + width for p in x], multi_queue_values, width, label='Multi Queue')

    ax.set_xlabel('Metrics')
    ax.set_ylabel('Values')
    ax.set_title('Comparison of Single Queue and Multi Queue')
    ax.set_xticks([p + width / 2 for p in x])
    ax.set_xticklabels(labels)
    ax.legend()

    plt.show()


def main():
    memory_size = int(input("Please Enter the Memory Size (MB): "))
    partition_count = int(input("Please Enter the partition count: "))
    process_count = random.randint(10, 20)  # Random process count between 10 and 20

    processes = generate_random_processes(process_count)
    partitions, total_partition_size = generate_random_partitions(partition_count, memory_size)

    print(f"\nGenerated {process_count} processes:")
    for process in processes:
        print(f"Process {process.process_id}: Size = {process.size}MB, Time Needed = {process.time_needed:.2f} seconds")

    print(f"\nGenerated {partition_count} partitions:")
    for partition in partitions:
        print(f"Partition {partition.partition_id}: Size = {partition.size}MB")

    if total_partition_size > memory_size:
        print("Error! Total size of partitions is bigger than Memory size!")
        return

    # Multi-queue simulation
    print("\nSimulation with Multiple Queues:")
    best_fit_allocation(processes, partitions)
    total_used = sum(partition.currently_occupied for partition in partitions)
    total_execution_time, total_running_time, total_waiting_time = simulate_execution(partitions)

    time_utilization = (total_execution_time / (total_running_time + total_waiting_time)) * 100 if (total_running_time + total_waiting_time) != 0 else 0

    multi_queue_data = {
        'execution_time': total_execution_time,
        'running_time': total_running_time,
        'waiting_time': total_waiting_time,
        'utilization': time_utilization
    }

    print("\nProcesses are placed on memory")
    print("---------- Memory Information (Multi-Queue) ----------")
    print(f"Memory Size: {memory_size}MB")
    print(f"Used Size: {total_used}MB")
    print(f"Remaining Size: {memory_size - total_used}MB")
    print(f"Utilization: {(total_used / memory_size) * 100:.2f}%")
    print(f"Total Time Needed for Processes: {total_execution_time:.2f} seconds")
    print(f"Total Running Time of Application: {total_running_time:.2f} seconds")
    print(f"Total Waiting Time: {total_waiting_time:.2f} seconds")
    print(f"Time Utilization: {time_utilization:.2f}%")

    for i, partition in enumerate(partitions):
        print(f"\n---- Partition {i + 1}:")
        print(f"Size: {partition.size}MB")
        if partition.process:
            print(f"Current Process: P{partition.process.process_id}")
            print(f"Process Size: {partition.process.size}MB")
            print(f"Time Needed: {partition.process.time_needed} seconds")
        else:
            print("Current Process: NONE")

        print(f"Queue for Partition {i + 1}:")
        queue = partition.get_queue()
        if queue:
            for proc in queue:
                print(f"- Process P{proc.process_id} - Time Needed: {proc.time_needed} seconds")
        else:
            print("Empty")

    # Single queue simulation
    print("\nSimulation with Single Queue:")
    for partition in partitions:
        partition.process = None
        partition.waiting_processes = []

    best_fit_allocation(processes, partitions, use_single_queue=True)
    total_used = sum(partition.currently_occupied for partition in partitions)
    total_execution_time, total_running_time, total_waiting_time = simulate_execution(partitions, use_single_queue=True)

    time_utilization = (total_execution_time / (total_running_time + total_waiting_time)) * 100 if (total_running_time + total_waiting_time) != 0 else 0

    single_queue_data = {
        'execution_time': total_execution_time,
        'running_time': total_running_time,
        'waiting_time': total_waiting_time,
        'utilization': time_utilization
    }

    print("\nProcesses are placed on memory")
    print("---------- Memory Information (Single Queue) ----------")
    print(f"Memory Size: {memory_size}MB")
    print(f"Used Size: {total_used}MB")
    print(f"Remaining Size: {memory_size - total_used}MB")
    print(f"Utilization: {(total_used / memory_size) * 100:.2f}%")
    print(f"Total Time Needed for Processes: {total_execution_time:.2f} seconds")
    print(f"Total Running Time of Application: {total_running_time:.2f} seconds")
    print(f"Total Waiting Time: {total_waiting_time:.2f} seconds")
    print(f"Time Utilization: {time_utilization:.2f}%")

    for i, partition in enumerate(partitions):
        print(f"\n---- Partition {i + 1}:")
        print(f"Size: {partition.size}MB")
        if partition.process:
            print(f"Current Process: P{partition.process.process_id}")
            print(f"Process Size: {partition.process.size}MB")
            print(f"Time Needed: {partition.process.time_needed} seconds")
        else:
            print("Current Process: NONE")

    print("\nShared Waiting Queue: ", end="")
    if not waiting_processes_single_queue:
        print("[]")
    else:
        print("[", end="")
        for j, proc in enumerate(waiting_processes_single_queue):
            if j != len(waiting_processes_single_queue) - 1:
                print(f"P{proc.process_id} - ", end="")
            else:
                print(f"P{proc.process_id}]", end="")
        print()

    # Plot comparison
    plot_comparison(single_queue_data, multi_queue_data)


if __name__ == "__main__":
    main()
