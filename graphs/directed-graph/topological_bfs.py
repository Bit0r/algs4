from collections import deque

import matplotlib.pyplot as plt
import networkx as nx


def topological_sort(DG: nx.DiGraph):
    """
    对有向图进行拓扑排序
    """
    V = DG.number_of_nodes()

    # 保存所有顶点的入度
    in_degree = list(map(DG.in_degree, range(V)))

    # 将所有起点加入一个队列
    sources = deque()
    for v in range(V):
        if in_degree[v] == 0:
            sources.append(v)

    order = deque()

    # 当起点队列不为空时循环
    while sources:

        # 将一个起点出队，并将其保存到排序结果的队列中
        v = sources.popleft()
        order.append(v)

        # 将该起点的所有的出边删除，即所有邻居的入度减1
        for w in DG[v]:
            in_degree[w] -= 1

            # 将删除这个点后的图上的新起点入队
            if in_degree[w] == 0:
                sources.append(w)

    return order if len(order) == V else None


if __name__ == "__main__":
    DG = nx.read_edgelist('tinyDAG.txt', create_using=nx.DiGraph, nodetype=int)
    print(topological_sort(DG))
    pos = nx.nx_agraph.graphviz_layout(DG)
    nx.draw_networkx(DG, pos)
    plt.show()
