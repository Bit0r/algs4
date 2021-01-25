from collections import deque

import networkx as nx


class BreathFirstPaths:
    """
    深度优先搜索寻路
    """
    def __init__(self, G: nx.Graph, s: int):
        """
        初始化图和起点
        """
        self.dist_to = [None] * G.number_of_nodes()
        self._edge_to = [None] * G.number_of_nodes()
        self.__s = s
        self.__G = G
        self.__bfs()

    def __bfs(self):
        """
        以s为起点，进行广度优先搜索
        """
        queue = deque()
        self.dist_to[self.__s] = 0
        queue.append(self.__s)
        while queue:
            v = queue.popleft()
            for w in self.__G[v]:
                if self.dist_to[w] is None:
                    self._edge_to[w], self.dist_to[w] = v, self.dist_to[v] + 1
                    queue.append(w)

    def has_path_to(self, v: int):
        """
        是否有从s到v的路径
        """
        return self.dist_to[v] is not None

    def path_to(self, v: int):
        """
        获得从s到v的一条简单路径
        """
        path = deque()

        u = v
        while u != self.__s:
            path.appendleft(u)
            u = self._edge_to[u]

        path.appendleft(self.__s)
        return iter(path)


if __name__ == "__main__":
    # 读取测试集
    G = nx.Graph()
    with open('tinyCG.txt') as f:
        V = int(f.readline())
        E = int(f.readline())
        for i in range(E):
            G.add_edge(*map(int, f.readline().split()))

    A = nx.nx_agraph.to_agraph(G)
    A.node_attr['shape'] = 'circle'
    A.layout()
    A.draw('cg.png')

    paths = BreathFirstPaths(G, 0)

    # 循环打印输出从s到任意v的一条简单路径
    for v in range(G.number_of_nodes()):
        print(*paths.path_to(v), ':', paths.dist_to[v])

    # 输出搜索路径的生成树
    T = nx.Graph()
    for v, u in enumerate(paths._edge_to):
        # 树的根节点没有父链接，所以要排除
        if u is not None:
            # print(u, v)
            T.add_edge(u, v)

    TA = nx.nx_agraph.to_agraph(T)
    TA.node_attr['shape'] = 'circle'
    TA.layout('dot')
    TA.draw('cg-tree.png')
