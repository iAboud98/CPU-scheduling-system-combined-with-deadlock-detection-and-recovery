from Process import Process  # -> import Process class


def parse_cpu(cpu_content):
    bursts = []
    parts = cpu_content.split(",")  # -> split based on ',' input could have this formula "R[1],4,F[2]" or just "4"
    for part in parts:  # -> divide into parts and process each part alone
        if "R[" in part or "F[" in part:  # -> if its 'R[2]' or 'F[5]' just add it to sequence list as it is
            bursts.append(part)
        else:
            bursts.append(int(part))  # -> if its '4' or any other digit, convert it to int then add it to sequence list
    return {"type": "cpu_burst", "bursts": bursts}  # -> make it in dictionary and send it


def parse_io(io_content):  # -> here the formula sent looks like this way only 'digit'
    bursts = [int(io_content)]  # -> convert it to integer
    return {"type": "io", "bursts": bursts}  # -> returned as dictionary and append it to sequence list


def process_line(line):
    try:
        columns = line.split()  # -> split line into columns
        process_id = int(columns[0])  # -> first column is set to be process id
        arrival_time = int(columns[1])  # -> second column is set to be process arrival time
        priority = int(columns[2])  # -> third column is set to be process priority

        sequence = []

        tasks = columns[3:]  # -> fourth and the rest are process bursts sequence
        for task in tasks:  # -> to check each part and process it alone
            if task.startswith("CPU"):  # -> since we have two possible parts 'CPU' and 'IO' only
                if "{" in task and "}" in task:
                    cpu_content = task.split("{")[1].split("}")[0]  # -> remove '{}'
                    sequence.append(parse_cpu(cpu_content))  # -> process on the string between '{}'
            elif task.startswith("IO"):
                if "{" in task and "}" in task:
                    io_content = task.split("{")[1].split("}")[0]
                    sequence.append(parse_io(io_content))
        p = Process(process_id, arrival_time, priority, sequence)  # -> make an instance of Process class and fill its attributes as well
        return p
    except Exception as e:  # -> handle errors while reading lines
        print(f"Error processing line: {line} - {e}")  # -> mentions which line exactly error occurs
        return None


processes = []
with open("processes.txt", "r") as file:
    for line in file:
        process = process_line(line.strip())
        if process:
            processes.append(process)  # -> append Process object to processes list
