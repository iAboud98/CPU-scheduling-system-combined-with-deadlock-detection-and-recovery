from read_from_file import processes


def get_process(processes, dead_process):
    pid = int(dead_process[1:])
    for process in processes:
        if pid == process.pid:
            return process


class Graph:  # -> Graph to implement Resource graph allocator

    def __init__(self):  # -> instructor method to make graph dictionary P/R : [processes/resources]
        self.graph_dic = {}

    def add_connection(self, node, edge):  # -> add vertexes and edges
        if node in self.graph_dic:
            self.graph_dic[node].append(edge)
        else:
            self.graph_dic[node] = [edge]

        if edge in self.graph_dic and node in self.graph_dic[edge]:
            if len(self.graph_dic[edge]) == 1:
                self.graph_dic.pop(edge)
            else:
                self.graph_dic[edge].remove(node)

    def release_connection(self, node, edge):  # -> remove connections
        if len(self.graph_dic[node]) == 1:
            self.graph_dic.pop(node)
        else:
            self.graph_dic[node].remove(edge)

    def detect_cycle_util(self, node, visited, rec_stack, cycle_nodes):  # -> Breadth First Search algorithm to detect if  cycle occurs in graph
        visited.add(node)
        rec_stack.add(node)

        for neighbor in self.graph_dic.get(node, []):
            if neighbor not in visited:
                if self.detect_cycle_util(neighbor, visited, rec_stack, cycle_nodes):
                    if node not in cycle_nodes:
                        cycle_nodes.append(node)
                    return True
            elif neighbor in rec_stack:
                cycle_nodes.append(neighbor)
                cycle_nodes.append(node)
                return True

        rec_stack.remove(node)
        return False

    def release_process(self, process):  # -> Method used when terminating a process, delete all vertexes and edges attached to it
        if process in self.graph_dic:
            self.graph_dic.pop(process)

        nodes_to_update = list(self.graph_dic.keys())
        for node in nodes_to_update:
            if process in self.graph_dic[node]:
                self.graph_dic[node].remove(process)
                if not self.graph_dic[node]:
                    self.graph_dic.pop(node)

    def deadlock_detection(self):  # -> the main BFS method
        visited = set()
        rec_stack = set()
        cycle_nodes = []
        processes_list = []
        for node in self.graph_dic:
            if node not in visited:
                if self.detect_cycle_util(node, visited, rec_stack, cycle_nodes):  # -> to save processes which caused deadlock
                    dead_processes = [n for n in cycle_nodes if n.startswith('P')]
                    dead_processes = list(dict.fromkeys(dead_processes))  # Remove duplicates while preserving order
                    for process in dead_processes:
                        processes_list.append(get_process(processes, process))
                    return True, processes_list
        return False, processes_list

    def display(self):  # -> print the graph
        for node, edges in self.graph_dic.items():
            print(f"{node} -> {', '.join(edges)}")
