import networkx as nx


class AcyclicSP:
    """
    有向无环图的最长路径算法
    """
    def __init__(self, DG: nx.Graph, s: int):
        """
        先进行拓扑排序，然后按拓扑顺序放松每一条边
        """
        V = DG.number_of_nodes()
        order = nx.topological_sort(DG)

        self.__DG = DG
        self.__edge_to = [None] * V
        self.dist_to = [-float('inf')] * V
        self.__s = s

        self.dist_to[s] = 0
        for v in order:
            self.__relax(v)

        assert self.__check()

    def __relax(self, v: int):
        """
        放松顶点v的全部有向边v->w
        """
        for w in self.__DG[v]:
            if self.dist_to[w] < self.dist_to[v] + self.__DG[v][w]['weight']:
                self.dist_to[w] = self.dist_to[v] + self.__DG[v][w]['weight']
                self.__edge_to[w] = v

    def path_to(self, v: int):
        """
        获得s->v的最长路径
        """
        from collections import deque
        stack = deque()

        while v != self.__s:
            stack.appendleft(v)
            u = self.__edge_to[v]
            v = u
        stack.appendleft(v)

        return stack

    def __check(self):
        """
        检查每一条从v到w有向边e是否符合：
            dist_to[w] >= dist_to[v] + e.weight
        """
        for v, w in self.__DG.edges:
            if self.dist_to[w] < self.dist_to[v] + self.__DG[v][w]['weight']:
                return False

        return True


if __name__ == "__main__":
    DG = nx.read_weighted_edgelist('tinyEWDAG.txt',
                                   create_using=nx.DiGraph,
                                   nodetype=int)
    sp = AcyclicSP(DG, 5)
    print(sp.path_to(0))
