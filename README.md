# Memory Allocation Simulation

This project simulates memory allocation using both single queue and multi-queue strategies. It generates random processes and partitions, allocates them using the best-fit algorithm, and compares the performance of both strategies.

## Table of Contents
- [Memory Allocation Simulation](#memory-allocation-simulation)
  - [Table of Contents](#table-of-contents)
  - [Overview](#overview)
  - [Features](#features)
  - [Requirements](#requirements)

## Overview

This project simulates memory allocation for processes using both single queue and multi-queue strategies. It includes:
- Generating random processes with random memory requirements and execution times.
- Generating random memory partitions.
- Allocating processes to partitions using the best-fit algorithm.
- Simulating the execution of processes.
- Comparing the performance of single queue and multi-queue strategies.
- Plotting the comparison results.

## Features

- Random generation of processes and partitions.
- Best-fit allocation algorithm.
- Single queue and multi-queue simulation.
- Performance metrics: total execution time, total running time, total waiting time, and time utilization.
- Visualization of the comparison results.

## Requirements

- Python 3.x
- `matplotlib` library

To install `matplotlib`, run:
```sh
pip install matplotlib
