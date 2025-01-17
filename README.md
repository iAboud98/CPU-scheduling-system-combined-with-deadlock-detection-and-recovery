# CPU Scheduling and Deadlock Simulation

This repository contains the implementation of a **CPU Scheduling and Deadlock Detection and Recovery System** as part of the ENCS3390: Operating System Concepts course (Fall 2024). The project simulates process execution using priority scheduling with round-robin, detects deadlocks, and applies recovery strategies.

## Features

1. **CPU Scheduling**:
   - Implements **priority scheduling with round-robin**.
   - Simulates processes with CPU bursts and I/O bursts.
   - Generates a Gantt chart to visualize process execution.

2. **Deadlock Detection and Recovery**:
   - Detects deadlock situations using a chosen detection algorithm.
   - Handles recovery through strategies like process termination or resource preemption.
   - Reports all deadlock states and the applied recovery methods.

3. **Performance Metrics**:
   - Calculates **average waiting time** and **average turnaround time** for all processes.
   - Handles I/O bursts concurrently, ensuring accurate simulation.

4. **Customizable Input**:
   - Processes are defined in a text file, with details like arrival time, priority, and resource requests.

## Input Format

The input file should list processes in the following format:

```
[PID] [Arrival Time] [Priority] [Sequence of CPU and IO bursts]
```

### Example:
```
0 0 1 CPU{R[1], 50, F[1]}
1 5 1 CPU{20} IO{30} CPU{20, R[2], 30, F[2], 10}
```

### Explanation:
- **Process 0**: Arrives at time 0, priority 1, requests resource 1, executes for 50 units, releases resource 1, and terminates.
- **Process 1**: Arrives at time 5, priority 1, alternates between CPU and I/O bursts, and requests/releases resources.

## Simulation Details

- **Context Switching**: Negligible context switch time.
- **Time Representation**: Simple time counter tracks simulation time.
- **Resource Requests**: Processes wait in a queue if requested resources are unavailable.
- **Deadlock Recovery**: Implements recovery mechanisms upon deadlock detection.


## Authors and Acknowledgments

This project was developed as part of the ENCS3390 course at the Department of Electrical & Computer Engineering.

---
