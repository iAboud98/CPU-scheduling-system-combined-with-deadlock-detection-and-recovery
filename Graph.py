class Graph:

    def __init__(self):
        self.graph_dic = {}

    def add_connection(self, node, edge):
        """Adds a directed edge from node to edge."""
        if node in self.graph_dic:
            self.graph_dic[node].append(edge)
        else:
            self.graph_dic[node] = [edge]

    def release_connection(self, node, edge):
        if len(self.graph_dic[node]) == 1:
            self.graph_dic.pop(node)
        else:
            self.graph_dic[node].remove(edge)

    def display(self):
        for node, edges in self.graph_dic.items():
            print(f"{node} -> {', '.join(edges)}")

