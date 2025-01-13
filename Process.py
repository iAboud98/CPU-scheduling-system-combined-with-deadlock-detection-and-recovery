class Process:  # -> Process class made to save attributes, print them and to apply functions on process

    def __init__(self, pid, arrival_time, priority, sequence):
        self.pid = pid  # -> Process ID
        self.arrival_time = arrival_time  # -> Arrival Time
        self.priority = priority  # -> Priority
        self.sequence = sequence  # -> Sequence

    def print_process(self):  # -> Method to print process attributes
        print(f"Process ID: {self.pid}, Arrival Time: {self.arrival_time}, Priority: {self.priority}, Sequence: "
              f"{self.sequence}")

    def analyze_input(self):  # -> Method to analyze the first index in process sequence
        if 'R' in self.sequence[0]['bursts'][0]:
            operation = 'request'  # -> request operation like : R[1], R[2], R[.....]
        else:
            operation = 'free'  # -> free operation like : F[1], F[2], F[......]
        number = int((self.sequence[0]['bursts'][0].split('[')[1]).split(']')[0])  # -> to get the numeric value inside

        return operation, number  # -> return both operation and number

