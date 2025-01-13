from read_from_file import processes
from ResourceManager import ResourceManager
from Graph import Graph
import copy
from itertools import groupby
from collections import Counter
import matplotlib.pyplot as plt

QUANTUM = 10

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
                                print(f"Deadlock Processes -> {' ,'.join(f'P{p.pid}' for p in deadlock_processes)}")
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


    if CPU_running:

        if not CPU_running[0].sequence[0]['bursts']:  # 1
            CPU_running[0].sequence.pop(0)
            if not CPU_running[0].sequence:
                index = [i for i, process in enumerate(processes) if process.pid == CPU_running[0].pid][0]
                processes.pop(index)
            else:
                CPU_ready.append(CPU_running[0])
            CPU_running.pop(0)
        else:

            CPU_running[0].sequence[0]['bursts'][0] -= 1
            quantum -= 1

            if (quantum == 0) and (CPU_running[0].sequence[0]['bursts'][0] != 0):
                CPU_ready.append(CPU_running[0])
                CPU_running.pop(0)
                quantum = QUANTUM

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
                                            print(f"Deadlock Processes -> {' ,'.join(f'P{p.pid}' for p in deadlock_processes)}")
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

                    if CPU_running:
                        if isinstance(CPU_running[0].sequence[0]["bursts"][0], int) and quantum == 0:
                            CPU_ready.append(CPU_running[0])
                            CPU_running.pop(0)

                    if quantum == 0:
                        quantum = QUANTUM

    current_time += 1

def flatten_and_count(lst):
    flat_list = []
    for item in lst:
        if isinstance(item, list):
            flat_list.extend(flatten_and_count(item))
        elif isinstance(item, str) and item.startswith("P"):
            flat_list.append(item)
    return flat_list


def process_queue(queue):
    flat_list = flatten_and_count(queue)
    count = Counter(flat_list)
    return dict(count)


def print_gantt_chart(gantt):
    from itertools import groupby
    process_durations = [(key, len(list(group))) for key, group in groupby(gantt)]

    start_time = 0
    print("Gantt Chart Representation:")
    print("-" * 80)
    for process, duration in process_durations:
        print(f"{process} : {start_time} -> {start_time + duration}")
        start_time += duration
    print("-" * 80)


def plot_gantt_chart(gantt, waiting_count, total_turnaround, processes_num):
    process_durations = [(key, len(list(group))) for key, group in groupby(gantt)]

    fig, ax = plt.subplots(figsize=(10, 1.5))
    ax.set_ylim(-0.07, 0.35)
    ax.set_xlim(0, sum(duration for _, duration in process_durations))

    start_time = 0
    for process, duration in process_durations:
        ax.broken_barh([(start_time, duration)], (0.1, 0.1), facecolors='#89CFF0', edgecolor='black', linewidth=2)
        ax.text(start_time + duration / 2, 0.15, process, ha='center', va='center', color='black', fontsize=12)
        start_time += duration

    ax.set_yticks([])
    tick_positions = [0] + [sum(duration for _, duration in process_durations[:i]) for i in
                            range(1, len(process_durations) + 1)]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_positions)

    for position in tick_positions[1:-1]:
        ax.axvline(x=position, color='lightgray', linewidth=1, linestyle='--', ymin=0, ymax=1)

    ax.spines['top'].set_color('black')
    ax.spines['right'].set_color('black')
    ax.spines['left'].set_color('black')
    ax.spines['bottom'].set_color('black')
    ax.spines['top'].set_linewidth(2)
    ax.spines['right'].set_linewidth(2)
    ax.spines['left'].set_linewidth(2)
    ax.spines['bottom'].set_linewidth(2)

    plt.title("Gantt Chart", fontsize=14, color='black', fontweight='bold')
    average_waiting_time = sum([waiting_count[process] for process in waiting_count]) / processes_num
    average_turnaround_time = total_turnaround / processes_num
    plt.figtext(0.5, 0.1, f"Average Waiting Time = {average_waiting_time:.2f}", ha="center", fontsize=12, color='black')
    plt.figtext(0.5, 0.07, f"Average Turn-around Time = {average_turnaround_time:.2f}", ha="center", fontsize=12,
                color='black')

    plt.grid(False)
    plt.tight_layout()
    plt.show()


waiting_count = process_queue(waiting_q)
io_count = process_queue(io_q)
rsc_count = process_queue(rsc_q)
running_count = process_queue(Gantt_chart)
total_turnaround = sum([waiting_count[process] for process in waiting_count]) + sum(
    [io_count[process] for process in io_count]) + sum([rsc_count[process] for process in rsc_count]) + sum(
    [running_count[process] for process in running_count])
plot_gantt_chart(Gantt_chart, waiting_count, total_turnaround, processes_num)
print("-" * 80) \
 \
