import matplotlib.pyplot as plt
import networkx as nx


class CC:
    """
    寻找连通分量
    """
    def __init__(self, G: nx.Graph):
        """
        建立图的连通分量信息
        """
        self.__marked = [False] * G.number_of_nodes()
        self.__G = G

        self.__component = [None] * G.number_of_nodes()
        self.__count = 0

        for v in range(G.number_of_nodes()):
            if not self.__marked[v]:
                self.__dfs(v)
                self.__count += 1

    def __dfs(self, v: int):
        """
        深度搜索极大连通子图
        """
        self.__marked[v] = True
        self.__component[v] = self.__count
        for w in self.__G[v]:
            if not self.__marked[w]:
                self.__dfs(w)

    def connected(self, v: int, w: int):
        """
        检验两个顶点是否连通
        """
        return self.__component[v] == self.__component[w]

    @property
    def count(self):
        """
        连通分量的数量
        """
        return self.__count

    @property
    def components(self):
        """
        返回所有连通分量
        """
        return tuple(self.__component)


if __name__ == "__main__":
    with open('tinyG.txt') as f:
        G = nx.Graph()
        f.readline()
        E = int(f.readline())
        for i in range(E):
            G.add_edge(*map(int, f.readline().split()))

    cc = CC(G)
    print(cc.count)
    print(cc.components)

    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx(G, pos=pos)
    plt.show()
    # plt.savefig('tinyG.png')
