import networkx as nx
from pqdict import pqdict
import matplotlib.pyplot as plt


class PrimMST:
    """
    最小生成树的Prim算法的即时实现
    """
    def __init__(self, G: nx.Graph, root=0):
        n = G.number_of_nodes()

        self.__prev = [None] * n
        self.__dist2 = [float('inf')] * n
        marked = [False] * n

        # 即时策略获取生成树的权重
        self.weight = 0

        # 初始化堆和距离向量
        self.__prev[root], self.__dist2[root] = None, 0
        pq = pqdict(dict(enumerate(self.__dist2)))

        for v in pq.popkeys():
            # 标记顶点，防止重复加入 MST
            marked[v] = True
            self.weight += self.__dist2[v]

            # 将生成树的边涂红
            if v != root:
                u = self.__prev[v]
                G[u][v]['color'] = 'red'

            for w in G[v]:
                # 遍历v的所有邻居w

                if marked[w]:
                    # 跳过已经加入 MST 的顶点
                    continue

                # 缩短 w 到树的距离
                new_dist = G[v][w]['weight']
                if new_dist < self.__dist2[w]:
                    self.__dist2[w], self.__prev[w] = new_dist, v
                    pq[w] = new_dist

    @property
    def edges(self):
        """
        返回生成树的边的集合
        """
        for v in range(1, len(self.__prev)):
            yield v, self.__prev[v], self.__dist2[v]

    # @property
    # def weight(self):
    #     """
    #     延时策略返回生成树的权重
    #     """
    #     import math
    #     return math.fsum(self.__dist2)


if __name__ == "__main__":
    G = nx.read_weighted_edgelist('tinyEWG.txt', nodetype=int)
    nx.set_edge_attributes(G, 'blue', 'color')

    mst = PrimMST(G)
    for v, w, weight in mst.edges:
        print(f'{v}-{w}-{weight}')
    print(mst.weight)

    pos = nx.nx_agraph.graphviz_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    colors = nx.get_edge_attributes(G, 'color').values()
    nx.draw(G, pos, edge_color=colors, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, labels)
    plt.show()
