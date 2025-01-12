from read_from_file import processes
from ResourceManager import ResourceManager
from Graph import Graph
import copy
from itertools import groupby
from collections import Counter

QUANTUM = 2

processes_num = len(processes)

copy_processes = copy.deepcopy(processes)
resource_manager = ResourceManager()

current_time = 0

CPU_running = []
CPU_ready = []
CPU_waiting = []
IO_running = []
deadlock_processes = []
quantum = QUANTUM

RGA = Graph()


def deadlock_recovery(list_of_processes):
    for process in CPU_waiting[:]:
        if (process.priority == min(p.priority for p in CPU_waiting)) and (
                any(process.pid == p.pid for p in list_of_processes)):
            print(f"pid terminated -> {process.pid}")
            resource_manager.release_all_resources(process.pid)
            RGA.release_process("P" + str(process.pid))
            CPU_waiting.remove(process)
            processes.remove(process)
            for p in copy_processes:
                if p.pid == process.pid:
                    fresh_process = p
            processes.append(fresh_process)
            deadlock_processes.clear()
            deadlock_processes.append(fresh_process)
            break


Gantt_chart = []
running = []
waiting_q = []
io_q = []
rsc_q = []

while processes:

    for process in processes:
        if process.arrival_time == current_time:
            CPU_ready.append(process)

    if CPU_ready:
        for process in CPU_ready[:]:
            if process.sequence[0]['type'] == 'io':
                IO_running.append(process)
                CPU_ready.remove(process)

    if CPU_waiting:
        CPU_waiting.sort(key=lambda p: p.priority)

        for process in CPU_waiting[:]:
            flag = True
            i = 0
            while not isinstance(process.sequence[0]['bursts'][i], int):
                resource_operation, resource_number = process.analyze_input()
                if resource_operation == 'request':
                    r = resource_manager.request_resource(resource_number)
                    if r is not None and not r.is_available():
                        flag = False
                i += 1

            if flag:
                CPU_ready.append(process)
                CPU_waiting.remove(process)
                break

    if deadlock_processes:
        CPU_ready.append(deadlock_processes[0])
        deadlock_processes.pop(0)

    while not CPU_running and CPU_ready:
        for process in CPU_ready:
            if process.priority == min(p.priority for p in CPU_ready):
                CPU_running.append(process)
                CPU_ready.remove(process)
                break

        while CPU_running[0].sequence[0]['bursts']:
            if isinstance(CPU_running[0].sequence[0]['bursts'][0], int):
                break
            else:
                operation_type, resource_number = CPU_running[0].analyze_input()
                r = resource_manager.request_resource(resource_number)
                if operation_type == 'request':
                    if r is None:
                        resource_manager.add_resource(resource_number)
                        r = resource_manager.request_resource(resource_number)
                        RGA.add_connection("R" + str(r.resource_number), "P" + str(CPU_running[0].pid))
                        resource_manager.assign_resource(resource_number, CPU_running[0].pid)
                    else:
                        if r.is_available():
                            RGA.add_connection("R" + str(r.resource_number), "P" + str(CPU_running[0].pid))
                            resource_manager.assign_resource(resource_number, CPU_running[0].pid)
                        else:
                            RGA.add_connection("P" + str(CPU_running[0].pid), "R" + str(r.resource_number))
                            deadlock_flag, deadlock_processes = RGA.deadlock_detection()
                            CPU_waiting.append(CPU_running[0])
                            CPU_running.pop(0)
                            if deadlock_flag:
                                deadlock_recovery(deadlock_processes)
                            break
                elif operation_type == 'free':
                    RGA.release_connection("R" + str(r.resource_number), "P" + str(CPU_running[0].pid))
                    r.free_resource()
                CPU_running[0].sequence[0]['bursts'].pop(0)

    if CPU_running:
        Gantt_chart.append(f"P{CPU_running[0].pid}")
    else:
        Gantt_chart.append("idle")

    if CPU_ready:
        waiting_q.append([f"P{p.pid}" for p in CPU_ready])
    else:
        waiting_q.append("idle")
    if IO_running:
        io_q.append([f"P{p.pid}" for p in IO_running])
    else:
        io_q.append("idle")
    if CPU_waiting:
        rsc_q.append([f"P{p.pid}" for p in CPU_waiting])
    else:
        rsc_q.append("idle")

    if IO_running:
        for process in IO_running[:]:
            process.sequence[0]['bursts'][0] -= 1
            if process.sequence[0]['bursts'][0] == 0:
                process.sequence.pop(0)
                CPU_ready.append(process)
                IO_running.remove(process)

        # 1: bursts = [] handeled ///// 2: bursts = [number] /////// 3: -> waiting  handeled (no quantum)

    # print(quantum)
    if CPU_running:  # 3

        if not CPU_running[0].sequence[0]['bursts']:  # 1
            CPU_running[0].sequence.pop(0)
            if not CPU_running[0].sequence:
                index = [i for i, process in enumerate(processes) if process.pid == CPU_running[0].pid][0]
                processes.pop(index)
            else:
                CPU_ready.append(CPU_running[0])
            CPU_running.pop(0)
        else:  # 2

            CPU_running[0].sequence[0]['bursts'][0] -= 1
            quantum -= 1

            if (quantum == 0) and (CPU_running[0].sequence[0]['bursts'][0] != 0):
                CPU_ready.append(CPU_running[0])
                CPU_running.pop(0)
                quantum = QUANTUM

            # 1: bursts = []  handeled /////////// 2: = bursts = [ resource ]

            elif CPU_running[0].sequence[0]['bursts'][0] == 0:

                CPU_running[0].sequence[0]['bursts'].pop(0)

                if not CPU_running[0].sequence[0]['bursts']:  # 1
                    CPU_running[0].sequence.pop(0)
                    if not CPU_running[0].sequence:
                        index = [i for i, process in enumerate(processes) if process.pid == CPU_running[0].pid][0]
                        processes.pop(index)
                    else:
                        CPU_ready.append(CPU_running[0])
                    CPU_running.pop(0)
                    quantum = QUANTUM
                else:  # 2
                    while CPU_running[0].sequence[0]['bursts']:
                        if isinstance(CPU_running[0].sequence[0]['bursts'][0], int):
                            break
                        else:
                            op_type, r_number = CPU_running[0].analyze_input()
                            r = resource_manager.request_resource(r_number)
                            if op_type == 'request':
                                if r is None:
                                    resource_manager.add_resource(r_number)
                                    r = resource_manager.request_resource(r_number)
                                    RGA.add_connection("R" + str(r.resource_number), "P" + str(CPU_running[0].pid))
                                    resource_manager.assign_resource(r_number, CPU_running[0].pid)
                                else:
                                    if r.is_available():
                                        RGA.add_connection("R" + str(r.resource_number), "P" + str(CPU_running[0].pid))
                                        resource_manager.assign_resource(r_number, CPU_running[0].pid)
                                    else:
                                        RGA.add_connection("P" + str(CPU_running[0].pid), "R" + str(r.resource_number))
                                        deadlock_flag, deadlock_processes = RGA.deadlock_detection()
                                        CPU_waiting.append(CPU_running[0])
                                        CPU_running.pop(0)
                                        quantum = QUANTUM
                                        if deadlock_flag:
                                            deadlock_recovery(deadlock_processes)
                                        break
                            elif op_type == 'free':
                                RGA.release_connection("R" + str(r.resource_number), "P" + str(CPU_running[0].pid))
                                r.free_resource()
                            CPU_running[0].sequence[0]['bursts'].pop(0)

                    if CPU_running and not CPU_running[0].sequence[0]['bursts']:  # 1
                        CPU_running[0].sequence.pop(0)
                        if not CPU_running[0].sequence:
                            index_v2 = [i for i, process in enumerate(processes) if process.pid == CPU_running[0].pid][
                                0]
                            processes.pop(index_v2)
                        else:
                            CPU_ready.append(CPU_running[0])
                        CPU_running.pop(0)
                        quantum = QUANTUM

                    if quantum == 0:
                        quantum = QUANTUM

    current_time += 1

result = [f"{key}({len(list(group))})" for key, group in groupby(Gantt_chart)]
print(result)


def flatten_and_count(lst):
    flat_list = []  # Temporary list to store flattened items
    # Flatten the list and count occurrences of 'P' items
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_and_count(item))  # Recursive call to flatten nested lists
        elif isinstance(item, str) and item.startswith("P"):  # Only process 'P' items
            flat_list.append(item)
    return flat_list


def process_queue(queue):
    # Flatten the queue
    flat_list = flatten_and_count(queue)
    # Count occurrences
    count = Counter(flat_list)
    return dict(count)


# Process each queue and print results
waiting_count = process_queue(waiting_q)
io_count = process_queue(io_q)
rsc_count = process_queue(rsc_q)
running_count = process_queue(Gantt_chart)
total_turnaround = sum([waiting_count[process] for process in waiting_count]) + sum([io_count[process] for process in io_count]) + sum([rsc_count[process] for process in rsc_count]) + sum([running_count[process] for process in running_count])

print(f"Average Waiting Time -> {sum([waiting_count[process] for process in waiting_count]) / len(waiting_count)}")
print(f"Average Turn-around Time -> {total_turnaround/processes_num}")

