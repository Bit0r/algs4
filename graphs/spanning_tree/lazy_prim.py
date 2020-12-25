import heapq
from collections import deque

import networkx as nx

from .edge import Edge


class LazyPrimMST:
    """
    最小生成树的Prim算法的延迟实现
    """
    def __init__(self, G: nx.Graph):
        """
        初始化图和优先队列
        """
        self.__V = G.number_of_nodes()
        self.__G = G
        self.__pq = []
        self.__marked = [False] * self.__V
        self.mst = deque()

        # 即时策略维护树的总权重
        self.weight = 0

        self.__visit(0)

        while self.__pq:
            e = heapq.heappop(self.__pq)

            v = e.either
            w = e.other(v)

            if self.__marked[v] and self.__marked[w]:
                continue

            self.mst.append(e)
            self.weight += e.weight

            if self.__marked[v]:
                self.__visit(w)
            else:
                self.__visit(v)

    def __visit(self, v: int):
        """
        标记顶点v并将所有连接v但未被标记的顶点的边加入优先队列
        """
        self.__marked[v] = True
        for w in self.__G[v]:
            if not self.__marked[w]:
                e = Edge(v, w, self.__G.edges[v, w]['weight'])
                heapq.heappush(self.__pq, e)

    # @property
    # def weight(self):
    #     """
    #     延时策略获取树的总权重
    #     """
    #     return sum(map(lambda e: e.weight, self.mst))


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    G = nx.read_weighted_edgelist('tinyEWG.txt', nodetype=int)
    lazy_prim_mst = LazyPrimMST(G)
    for e in lazy_prim_mst.mst:
        print(e)
    print(lazy_prim_mst.weight)
