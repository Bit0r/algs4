from collections import deque

import matplotlib.pyplot as plt
import networkx as nx
from pqdict import pqdict


class DijkstraSP:
    """
    最短路径的Dijkstra算法
    """
    def __init__(self, DG: nx.DiGraph, s: int):
        """
        dijkstra 算法
        """
        self.__DG = DG
        self.__s = s
        n = DG.number_of_nodes()

        self.__prev = [None] * n
        self.dist2 = [float('inf')] * n
        self.dist2[s] = 0

        # 将距离向量建堆
        pq = pqdict(dict(enumerate(self.dist2)))

        # 循环弹出距离最近的顶点和距离
        for v in pq.popkeys():
            # 将最短路径经过的边的颜色改为红色
            if v != s:
                u = self.__prev[v]
                self.__DG[u][v]['color'] = 'red'

            # 缩短 v 所有的邻居 w 的距离
            for w in self.__DG[v]:
                new_dist = self.dist2[v] + self.__DG[v][w]['weight']
                if new_dist < self.dist2[w]:
                    # 更新w的入边和距离
                    pq[w] = new_dist
                    self.dist2[w], self.__prev[w] = new_dist, v

        # 断言条件
        assert self.__check()

    def path2(self, v: int):
        """
        获得s->v的最短路径
        """
        stack = deque()

        while v != self.__s:
            stack.appendleft(v)
            u = self.__prev[v]
            v = u
        stack.appendleft(v)

        return stack

    def __check(self):
        """
        检查每一条从v到w有向边e是否符合:
            dist2[w] <= dist2[v] + e.weight
        """
        for v, w in self.__DG.edges:
            if self.dist2[w] > self.dist2[v] + self.__DG[v][w]['weight']:
                return False

        return True


if __name__ == "__main__":
    DG = nx.read_weighted_edgelist('tinyEWD.txt',
                                   create_using=nx.DiGraph,
                                   nodetype=int)
    nx.set_edge_attributes(DG, 'blue', 'color')

    sp = DijkstraSP(DG, 0)
    for v in DG.nodes:
        print(*sp.path2(v))

    pos = nx.nx_agraph.graphviz_layout(DG)
    labels = nx.get_edge_attributes(DG, 'weight')
    colors = nx.get_edge_attributes(DG, 'color').values()
    nx.draw(DG, pos, edge_color=colors, with_labels=True)
    nx.draw_networkx_edge_labels(DG, pos, labels, label_pos=0.7)
    plt.show()
