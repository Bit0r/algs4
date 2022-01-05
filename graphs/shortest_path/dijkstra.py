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

        self.__edge_to = [None] * n
        self.dist_to = [float('inf')] * n
        self.dist_to[s] = 0

        # 将距离向量建堆
        pq = pqdict(dict(enumerate(self.dist_to)))

        # 循环弹出距离最近的顶点和距离
        for v, min_dist in pq.popitems():
            self.dist_to[v] = min_dist

            # 将最小生成树的边的颜色改为红色
            if v != s:
                u = self.__edge_to[v]
                self.__DG[u][v]['color'] = 'red'

            # 缩短 v 所有的邻居 w 的距离
            for w in self.__DG[v]:
                new_dist = self.dist_to[v] + self.__DG[v][w]['weight']
                if new_dist < self.dist_to[w]:
                    # 更新w的入边和距离
                    pq[w] = new_dist
                    self.dist_to[w], self.__edge_to[w] = new_dist, v

        # 断言条件
        assert self.__check()

    def path_to(self, v: int):
        """
        获得s->v的最短路径
        """
        stack = deque()

        while v != self.__s:
            stack.appendleft(v)
            u = self.__edge_to[v]
            v = u
        stack.appendleft(v)

        return stack

    def __check(self):
        """
        检查每一条从v到w有向边e是否符合:
            dist_to[w] <= dist_to[v] + e.weight
        """
        for v, w in self.__DG.edges:
            if self.dist_to[w] > self.dist_to[v] + self.__DG[v][w]['weight']:
                return False

        return True


if __name__ == "__main__":
    DG = nx.read_weighted_edgelist('tinyEWD.txt',
                                   create_using=nx.DiGraph,
                                   nodetype=int)
    nx.set_edge_attributes(DG, 'blue', 'color')
    sp = DijkstraSP(DG, 0)
    for v in DG.nodes:
        print(*sp.path_to(v))

    pos = nx.nx_agraph.graphviz_layout(DG)
    edges = DG.edges
    edge_color = [DG[u][v]['color'] for u, v in edges]
    labels = nx.get_edge_attributes(DG, 'weight')
    nx.draw_networkx(DG, pos, edge_color=edge_color)

    plt.show()
