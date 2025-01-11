class Process:

    def __init__(self, pid, arrival_time, priority, sequence):
        self.pid = pid
        self.arrival_time = arrival_time
        self.priority = priority
        self.sequence = sequence

    def print_process(self):
        print(f"Process ID: {self.pid}, Arrival Time: {self.arrival_time}, Priority: {self.priority}, Sequence: "
              f"{self.sequence}")

    def analyze_input(self):
        if 'R' in self.sequence[0]['bursts'][0]:
            operation = 'request'
        else:
            operation = 'free'
        number = int((self.sequence[0]['bursts'][0].split('[')[1]).split(']')[0])

        return operation, number

