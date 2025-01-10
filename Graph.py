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

    def display(self):
        for node, edges in self.graph_dic.items():
            print(f"{node} -> {', '.join(edges)}")
