import networkx as nx
from networkx.utils.union_find import UnionFind
import matplotlib.pyplot as plt


class KruskalMST:
    """
    最小生成树的Kruskal实现
    """
    def __init__(self, G: nx.Graph):
        n = G.number_of_nodes()

        # 初始化边表
        self.edges = []
        # 初始化总权值
        self.weight = 0

        edges = sorted(G.edges,
                       key=lambda e: G.edges[e]['weight'],
                       reverse=True)
        uf = UnionFind()

        while len(self.edges) < n - 1:
            v, w = edges.pop()

            if uf[v] == uf[w]:
                # 如果已在同一个连通部件中，则此边作废
                continue

            # 将该边加入生成树，同时更新总权值
            uf.union(v, w)
            weight = G[v][w]['weight']
            self.weight += weight

            # 将该边的颜色改为红色
            G[v][w]['color'] = 'red'

            self.edges.append((v, w, weight))

    # @property
    # def weight(self):
    #     """
    #     延时策略返回生成树的权重
    #     """
    #     import math
    #     from operator import itemgetter
    #     return math.fsum(map(itemgetter(2), self.edges))


if __name__ == "__main__":
    G = nx.read_weighted_edgelist('tinyEWG.txt', nodetype=int)
    nx.set_edge_attributes(G, 'blue', 'color')

    mst = KruskalMST(G)
    print(*mst.edges, sep='\n')
    print(mst.weight)

    pos = nx.nx_agraph.graphviz_layout(G)
    labels = nx.get_edge_attributes(G, 'weight')
    colors = nx.get_edge_attributes(G, 'color').values()
    nx.draw(G, pos, edge_color=colors, with_labels=True)
    nx.draw_networkx_edge_labels(G, pos, labels)
    plt.show()
