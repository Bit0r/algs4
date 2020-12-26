import heapq
import math
from collections import deque

import networkx as nx
from networkx.utils.union_find import UnionFind


class KruskalMST:
    """
    最小生成树的Kruskal实现
    """
    def __init__(self, G: nx.Graph):
        V = G.number_of_nodes()

        self.edges = deque()

        self.weight = 0

        pq = list(map(lambda e: (e[2], e[:2]), G.edges.data('weight')))
        heapq.heapify(pq)
        uf = UnionFind()

        while len(self.edges) < V - 1:
            e = heapq.heappop(pq)
            v, w = e[1]

            if uf[v] == uf[w]:
                continue

            uf.union(v, w)
            weight = e[0]
            self.weight += weight

            self.edges.append((v, w, weight))

    # @property
    # def weight(self):
    #     """
    #     延时策略返回生成树的权重
    #     """
    #     return math.fsum(map(lambda e: e[0], self.__mst))


if __name__ == "__main__":
    G = nx.read_weighted_edgelist('tinyEWG.txt', nodetype=int)
    mst = KruskalMST(G)
    print(*mst.edges, sep='\n')
    print(mst.weight)
