import matplotlib.pyplot as plt
import networkx as nx


class TwoColor:
    """
    双色问题
    """
    def __init__(self, G: nx.Graph):
        """
        初始化标记数组，同时开始搜索
        """
        self.__G = G
        self.__marked = [False] * G.number_of_nodes()
        self.__color = [False] * G.number_of_nodes()
        self.__is_two_colorable = True

        for v in G.nodes:
            if not self.__marked[v]:
                self.__dfs(v)

    def __dfs(self, v: int):
        """
        深度搜索进行染色确定二分图
        """
        self.__marked[v] = True
        for w in self.__G[v]:
            if not self.__marked[w]:
                self.__color[w] = not self.__color[v]
                self.__dfs(w)
            # 如果其邻居已被搜索过，但颜色和本顶点一样，则其不是二分图
            elif self.__color[w] == self.__color[v]:
                self.__is_two_colorable = False

    @property
    def is_bipartite(self):
        """
        是否为二分图
        """
        return self.__is_two_colorable

    @property
    def color(self):
        """
        颜色数组的视图
        """
        return list(map(lambda red: 'r' if red else 'b', self.__color))


if __name__ == "__main__":
    with open('twoColor.txt') as f:
        G = nx.Graph()
        f.readline()
        E = int(f.readline())
        for i in range(E):
            G.add_edge(*map(int, f.readline().split()))

    two_color = TwoColor(G)
    print(two_color.is_bipartite)
    pos = nx.nx_agraph.graphviz_layout(G)
    nx.draw_networkx(G,
                     pos=pos,
                     nodelist=range(G.number_of_nodes()),
                     node_color=two_color.color)
    plt.show()
