from collections import deque


class Digraph:
    """
    有向图
    """
    def __init__(self, V: int):
        """
        初始化一副有向图
        """
        self.__V, self.__E = V, 0
        self.adj = list(map(lambda _: deque(), range(V)))

    def add_edge(self, v: int, w: int):
        """
        添加一条有向边
        """
        self.adj[v].append(w)
        self.__E += 1

    def reverse(self):
        """
        本图的反向图
        """
        R = Digraph(self.__V)
        for v in range(self.__V):
            for w in self.adj[v]:
                R.add_edge(w, v)
        return R
