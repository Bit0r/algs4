import networkx as nx
import matplotlib.pyplot as plt


class Cycle:
    """
    检测G是否带环
    """
    def __init__(self, G: nx.Graph):
        """
        检测环的存在
        """
        self.__marked = [False] * G.number_of_nodes()
        self.__has_cycle = False
        self.__G = G

        # 对所有的极大连通子图进行搜索
        for v in range(G.number_of_nodes()):
            if not self.__marked[v]:
                self.__dfs(v, v)

    def __dfs(self, v: int, u: int):
        """利用深度优先搜索确定是否有环

        Parameters
        ----------
        v : int
            开始搜索的顶点

        u : int
            搜索路径的上一个顶点
        """
        self.__marked[v] = True
        for w in self.__G[v]:
            if not self.__marked[w]:
                self.__dfs(w, v)
            elif w != u:
                self.__has_cycle = True

    @property
    def has_cycle(self):
        """
        是否有环
        """
        return self.__has_cycle


if __name__ == "__main__":
    with open('tree.txt') as f:
        G = nx.Graph()
        f.readline()
        E = int(f.readline())
        for i in range(E):
            G.add_edge(*map(int, f.readline().split()))

    print(Cycle(G).has_cycle)

    pos = nx.nx_agraph.graphviz_layout(G, prog='dot')
    nx.draw_networkx(G, pos=pos)
    plt.show()
    # plt.savefig('tree.png')