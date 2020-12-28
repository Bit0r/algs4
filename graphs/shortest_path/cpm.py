import networkx as nx

with open('jobsPC.txt') as file:
    DG = nx.DiGraph()
    n = int(file.readline())
    s, t = 2 * n, 2 * n + 1

    for task in range(n):
        a = file.readline().split()
        DG.add_weighted_edges_from([(task, task + n, float(a[0])),
                                    (s, task, 0), (task + n, t, 0)])

        for successor in a[2:]:
            successor = int(successor)
            DG.add_edge(task + n, successor, weight=0)

lp = nx.dag_longest_path(DG)
time = nx.dag_longest_path_length(DG)
print(lp[1:-1:2], time, sep='\n')
