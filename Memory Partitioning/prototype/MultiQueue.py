import time
from typing import List, Optional


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

    def add_new_process(self, process: Process):
        if self.process is None:
            self.process = process
            self.currently_occupied = min(process.size, self.size)
            process.enter_into_partition(self)
        else:
            self.waiting_processes.append(process)

    def remove_current_process(self):
        if self.process:
            self.process.exit_from_partition()
            self.process = None
            self.currently_occupied = 0
            if self.waiting_processes:
                next_process = self.waiting_processes.pop(0)
                self.add_new_process(next_process)

    def get_queue(self) -> List[Process]:
        return self.waiting_processes


def collect_input():
    process_count = int(input("Please Enter the process count: "))
    partition_count = int(input("Please Enter the partition count: "))
    memory_size = int(input("Please Enter the Memory Size (MB): "))

    processes = []
    for i in range(process_count):
        size = int(input(f"Enter the process {i + 1} size (MB): "))
        time_needed = float(
            input(f"Enter the process {i + 1} time needed (in seconds): ")
        )
        processes.append(Process(size, i + 1, time_needed))

    partitions = []
    total_size = 0
    for i in range(partition_count):
        size = int(input(f"Enter the partition {i + 1} size (MB): "))
        if total_size + size > memory_size:
            print("Error! Total size of partitions is bigger than Memory size!")
            return None, None, None
        total_size += size
        partitions.append(Partition(size, i + 1))

    return processes, partitions, memory_size


def best_fit_allocation(processes: List[Process], partitions: List[Partition]):
    partitions.sort(key=lambda x: x.size)

    for process in processes:
        placed = False
        for partition in partitions:
            if process.size <= partition.size:
                if partition.process is None:
                    partition.add_new_process(process)
                    placed = True
                    break
                else:
                    partition.add_new_process(process)
                    placed = True
                    break
        if not placed:
            print(f"No suitable partition found for Process P{process.process_id}")


def simulate_execution(partitions: List[Partition]):
    start_time = time.time()
    total_execution_time = 0.0
    total_waiting_time = 0.0

    while any(partition.process or partition.waiting_processes for partition in partitions):
        for partition in partitions:
            if partition.process:
                process_time_needed = partition.process.time_needed
                waiting_time_before_execution = partition.process.waiting_time
                print(
                    f"Executing Process P{partition.process.process_id} in Partition {partition.partition_id} for {process_time_needed} seconds."
                )
                time.sleep(process_time_needed)
                partition.remove_current_process()
                total_execution_time += process_time_needed
                total_waiting_time += waiting_time_before_execution

        for partition in partitions:
            if partition.process:
                for process in partition.get_queue():
                    process.waiting_time += partition.process.time_needed

    end_time = time.time()
    total_running_time = end_time - start_time

    return total_execution_time, total_running_time, total_waiting_time


def main():
    processes, partitions, memory_size = collect_input()
    if not processes or not partitions:
        return

    best_fit_allocation(processes, partitions)

    total_used = sum(partition.currently_occupied for partition in partitions)
    total_execution_time, total_running_time, total_waiting_time = simulate_execution(partitions)

    time_utilization = (
        (total_execution_time / (total_running_time + total_waiting_time)) * 100
        if (total_running_time + total_waiting_time) != 0
        else 0
    )

    print("\nProcesses are placed on memory")
    print("---------- Memory Information ----------")
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
                print(
                    f"- Process P{proc.process_id} - Time Needed: {proc.time_needed} seconds"
                )
        else:
            print("Empty")


if __name__ == "__main__":
    main()
