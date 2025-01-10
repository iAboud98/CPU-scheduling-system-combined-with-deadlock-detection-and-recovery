class Graph:

    def __init__(self):
        self.graph_dic = {}

    def add_connection(self, node, edge):
        if node in self.graph_dic:
            self.graph_dic[node].append(edge)
        else:
            self.graph_dic[node] = [edge]

        if edge in self.graph_dic and node in self.graph_dic[edge]:
            if len(self.graph_dic[edge]) == 1:
                self.graph_dic.pop(edge)
            else:
                self.graph_dic[edge].remove(node)

    def release_connection(self, node, edge):
        if len(self.graph_dic[node]) == 1:
            self.graph_dic.pop(node)
        else:
            self.graph_dic[node].remove(edge)

    def detect_cycle_util(self, node, visited, rec_stack):
        """Utility function to detect cycles using DFS."""
        visited.add(node)
        rec_stack.add(node)

        for neighbor in self.graph_dic.get(node, []):
            if neighbor not in visited:
                if self.detect_cycle_util(neighbor, visited, rec_stack):
                    return True
            elif neighbor in rec_stack:
                return True

        rec_stack.remove(node)
        return False

    def deadlock_detection(self):
        """Detects deadlocks (cycles) in the graph."""
        visited = set()
        rec_stack = set()

        for node in self.graph_dic:
            if node not in visited:
                if self.detect_cycle_util(node, visited, rec_stack):
                    return True
        return False

    def display(self):
        for node, edges in self.graph_dic.items():
            print(f"{node} -> {', '.join(edges)}")
