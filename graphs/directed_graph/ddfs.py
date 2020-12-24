import matplotlib.pyplot as plt
import networkx as nx


class DirectedDFS:
    """
    有向图的DFS
    """
    def __init__(self, DG: nx.DiGraph, s: int = None, sources: list = None):
        """
        初始化搜索
        """
        self.__marked = [False] * DG.number_of_nodes()
        self.__DG = DG
        if s is not None:
            self.__dfs(s)
        elif sources is not None:
            for s in sources:
                if not self.__marked[s]:
                    self.__dfs(s)
        else:
            raise TypeError('必须传入参数 s 或 sources 的其中之一')

    def __dfs(self, v: int):
        """
        深度优先搜索
        """
        self.__marked[v] = True
        for w in self.__DG[v]:
            if not self.__marked[w]:
                self.__dfs(w)

    def marked(self, v: int):
        """
        查看顶点v是否被标记
        """
        return self.__marked[v]


if __name__ == "__main__":
    DG = nx.read_edgelist('tinyDG.txt', create_using=nx.DiGraph, nodetype=int)
    reachable = DirectedDFS(DG, s=2)

    for v in DG.nodes:
        if reachable.marked(v):
            print(v, end=' ')

    pos = nx.nx_agraph.graphviz_layout(DG)
    nx.draw_networkx(DG, pos)
    plt.show()
