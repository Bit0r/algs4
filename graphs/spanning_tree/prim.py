import math

import networkx as nx
from pqdict import pqdict


class PrimMST:
    """
    最小生成树的Prim算法的即时实现
    """
    def __init__(self, G: nx.Graph):
        V = G.number_of_nodes()
        self.__G = G

        self.__edge_to = [None] * V
        self.__dist_to = [float('inf')] * V
        self.__marked = [False] * V

        # 即时策略获取生成树的权重
        self.weight = 0

        self.__edge_to[0], self.__dist_to[0], self.__marked[0] = 0, 0, True
        self.__pq = pqdict(enumerate([0]))
        while self.__pq:
            self.__visit(self.__pq.pop())

    def __visit(self, v: int):
        """
        将顶点v加入生成树，同时更新数据
        """
        # 将顶点v加入生成树
        self.__marked[v] = True
        self.weight += self.__dist_to[v]

        # 考查所有v的横切边
        for w in self.__G[v]:
            # v-w已失效，即不再是横切边
            if self.__marked[w]:
                continue

            weight = self.__G.edges[v, w]['weight']
            if weight < self.__dist_to[w]:
                self.__edge_to[w], self.__dist_to[w] = v, weight
                self.__pq[w] = weight

    @property
    def edges(self):
        """
        返回生成树的边的集合
        """
        for v in range(1, len(self.__edge_to)):
            yield v, self.__edge_to[v], self.__dist_to[v]

    # @property
    # def weight(self):
    #     """
    #     延时策略返回生成树的权重
    #     """
    #     return math.fsum(self.__dist_to)


if __name__ == "__main__":
    G = nx.read_weighted_edgelist('tinyEWG.txt', nodetype=int)
    mst = PrimMST(G)
    for v, w, weight in mst.edges:
        print(f'{v}-{w}', weight)
    print(mst.weight)
