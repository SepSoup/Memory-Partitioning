import time
from typing import List, Optional
from collections import deque

waiting_processes = deque()


class Process:
    def __init__(self, size: int, process_id: int, time_needed: float):
        self.process_id = process_id
        self.size = size
        self.size_on_memory = 0
        self.partition: Optional["Partition"] = None
        self.time_needed = time_needed

    def enter_into_partition(self, partition: "Partition", size_of_blocks: int):
        self.partition = partition
        self.size_on_memory = min(size_of_blocks, self.size)

    def exit_from_partition(self):
        self.partition = None
        self.size_on_memory = 0


class Partition:
    def __init__(self, size: int, partition_id: int):
        self.partition_id = partition_id
        self.size = size
        self.currently_occupied = 0
        self.process: Optional[Process] = None

    def add_new_process(self, process: Process):
        if self.process is None:
            self.process = process
            self.currently_occupied = min(process.size, self.size)
            process.enter_into_partition(self, self.currently_occupied)
        else:
            waiting_processes.append(process)

    def remove_current_process(self):
        if self.process:
            self.process.exit_from_partition()
            self.process = None
            self.currently_occupied = 0
        if waiting_processes:
            next_process = waiting_processes.popleft()
            self.add_new_process(next_process)

    def get_queue(self) -> List[Process]:
        return list(waiting_processes)


def main():
    processes: List[Process] = []
    partitions: List[Partition] = []

    # Input
    process_count = int(input("Please Enter the process count: "))
    partition_count = int(input("Please Enter the partition count: "))
    memory_size = int(input("Please Enter the Memory Size (MB): "))

    for i in range(process_count):
        size = int(input(f"Enter the process {i + 1} size (MB): "))
        time_needed = float(
            input(f"Enter the process {i + 1} time needed (in seconds): ")
        )
        process = Process(size, i + 1, time_needed)
        processes.append(process)

    total_size = 0
    for i in range(partition_count):
        size = int(input(f"Enter the partition {i + 1} size (MB): "))
        if total_size + size > memory_size:
            print("Error! Total size of partitions is bigger than Memory size!")
            return
        total_size += size
        partition = Partition(size, i + 1)
        partitions.append(partition)

    partitions.sort(key=lambda x: x.size)

    for process in processes:
        placed = False
        for partition in partitions:
            if process.size <= partition.size and partition.process is None:
                partition.add_new_process(process)
                placed = True
                break
        if not placed:
            waiting_processes.append(process)

    total_used = sum(partition.currently_occupied for partition in partitions)

    start_time = time.time()
    total_execution_time = 0.0
    while any(partition.process for partition in partitions) or waiting_processes:
        for partition in partitions:
            if partition.process:
                print(
                    f"Executing Process P{partition.process.process_id} in Partition {partition.partition_id} for {partition.process.time_needed} seconds."
                )
                process_time_needed = partition.process.time_needed
                time.sleep(process_time_needed)
                partition.remove_current_process()
                total_execution_time += process_time_needed
    end_time = time.time()
    total_running_time = end_time - start_time

    time_utilization = (total_execution_time / total_running_time) * 100

    print("\nProcesses are placed on memory")
    print("---------- Memory Information ----------")
    print(f"Memory Size: {memory_size}MB")
    print(f"Used Size: {total_used}MB")
    print(f"Remaining Size: {memory_size - total_used}MB")
    print(f"Utilization: {(total_used / memory_size) * 100}%")
    print(f"Total Time Needed for Processes: {total_execution_time} seconds")
    print(f"Total Running Time of Application: {total_running_time} seconds")
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
    if not waiting_processes:
        print("[]")
    else:
        print("[", end="")
        for j, proc in enumerate(waiting_processes):
            if j != len(waiting_processes) - 1:
                print(f"P{proc.process_id} - ", end="")
            else:
                print(f"P{proc.process_id}]", end="")
        print()


if __name__ == "__main__":
    main()
