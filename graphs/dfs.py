from collections import deque

import networkx as nx
from networkx.drawing.nx_agraph import to_agraph


class DepthFirstPaths:
    """
    深度优先搜索寻路
    """
    def __init__(self, G: nx.Graph, s: int):
        """
        初始化图和起点
        """
        self.__marked = [False] * G.number_of_nodes()
        self.__edge_to = [None] * G.number_of_nodes()
        self.__s = s
        self.__G = G
        self.__dfs(self.__s)

    def __dfs(self, v: int):
        """
        以v为起点，进行深度优先搜索
        """
        self.__marked[v] = True
        for w in self.__G[v]:
            if not self.__marked[w]:
                self.__edge_to[w] = v
                self.__dfs(w)

    def has_path_to(self, v: int):
        """
        是否有从s到v的路径
        """
        return self.__marked[v]

    def path_to(self, v: int):
        """
        获得从s到v的一条简单路径
        """
        path = deque()

        u = v
        while u != self.__s:
            path.appendleft(u)
            u = self.__edge_to[u]

        path.appendleft(self.__s)
        return path

    @property
    def path_tree(self):
        """
        返回搜索树数组的副本
        """
        return self.__edge_to.copy()


if __name__ == "__main__":
    # 读取测试集
    G = nx.Graph()
    with open('tinyCG.txt') as f:
        E = int(f.readline())
        s = int(f.readline())
        for i in range(E):
            G.add_edge(*map(int, f.readline().split()))

    A = to_agraph(G)
    A.node_attr['shape'] = 'circle'
    A.layout()
    A.draw('cg.png')

    paths = DepthFirstPaths(G, s)

    # 循环打印输出从s到任意v的一条简单路径
    for v in range(G.number_of_nodes()):
        print(paths.path_to(v))

    # 输出搜索路径的生成树
    T = nx.Graph()
    for v, u in enumerate(paths.path_tree):
        # 树的根节点没有父链接，所以要排除
        if u is not None:
            # print(u, v)
            T.add_edge(u, v)

    TA = to_agraph(T)
    TA.node_attr['shape'] = 'circle'
    TA.layout()
    TA.draw('cg-tree.png')
