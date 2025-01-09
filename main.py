from read_from_file import processes

QUANTUM = 2

resources = {
    1: -1,
    2: -1,
    3: -1,
    4: -1,
    5: -1
}


def request_resource(process, r_number):
    if (resources[r_number] == -1) or (resources[r_number] == process.pid):
        return True
    else:
        return False


current_time = 0

CPU_running = []
CPU_ready = []
CPU_waiting = []
IO_running = []
quantum = QUANTUM

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
                    available = request_resource(process, resource_number)
                    if not available:
                        flag = False
                i += 1

            if flag:
                CPU_ready.append(process)
                CPU_waiting.remove(process)
                break

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
                if operation_type == 'request':
                    if request_resource(CPU_running[0], resource_number):
                        resources[resource_number] = CPU_running[0].pid
                    else:
                        CPU_waiting.append(CPU_running[0])
                        CPU_running.pop(0)
                        break
                elif operation_type == 'free':
                    resources[resource_number] = -1
                CPU_running[0].sequence[0]['bursts'].pop(0)

    time_line = [
        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29,
        30,
        31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58,
        59, 60,
        61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88,
        89, 90, 91, 92, 93, 94, 95, 96, 97, 98, 99, 100, 110, 111, 112, 120, 125, 130, 135, 140
    ]

    # time_line = [
    #     0, 10, 15, 20, 30, 35, 40, 50, 60, 70, 80, 90, 120, 130, 150, 160
    # ]

    if current_time in time_line:
        print(f"current time -> {current_time}")
        print(f"cpu_running -> {[process.pid for process in CPU_running]}")
        print(f"cpu_ready -> {[process.pid for process in CPU_ready]}")
        print(f"cpu_waiting -> {[process.pid for process in CPU_waiting]}")
        print(f"io_running -> {[process.pid for process in IO_running]}")
        print(f"resources -> {resources}")
        print(f"quantum -> {quantum}")
        print("-----------------------------------------------------------------")

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
                            if op_type == 'request':
                                if request_resource(CPU_running[0], r_number):
                                    resources[r_number] = CPU_running[0].pid
                                else:
                                    CPU_waiting.append(CPU_running[0])
                                    CPU_running.pop(0)
                                    quantum = QUANTUM
                                    break
                            elif op_type == 'free':
                                resources[r_number] = -1
                            CPU_running[0].sequence[0]['bursts'].pop(0)

                    if CPU_running and not CPU_running[0].sequence[0]['bursts']:  # 1
                        CPU_running[0].sequence.pop(0)
                        if not CPU_running[0].sequence:
                            index_v2 = [i for i, process in enumerate(processes) if process.pid == CPU_running[0].pid][0]
                            processes.pop(index_v2)
                        else:
                            CPU_ready.append(CPU_running[0])
                        CPU_running.pop(0)
                        quantum = QUANTUM

                    if quantum == 0:
                        quantum = QUANTUM

    current_time += 1
