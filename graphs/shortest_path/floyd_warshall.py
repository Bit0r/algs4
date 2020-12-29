import networkx as nx
import numpy as np


class FloydWarshall:
    """
    求任意两点间的最短路径的floyd-warshall算法
    """
    def __init__(self, DG: nx.DiGraph):
        """
        初始化距离数组和路径数组
        """
        self.dist = nx.to_numpy_array(DG,
                                      nodelist=range(DG.number_of_nodes()),
                                      nonedge=np.inf)
        self.path = np.full_like(self.dist, -1, dtype=int)
        np.fill_diagonal(self.dist, 0)

        # 对于从每条从u到w的路径，在其中加入一个点v进行中转
        for v in DG.nodes:
            for u in DG.nodes:
                for w in DG.nodes:
                    # 如果从u->v->w比以前的u->w路径要短，则在u之后插入v
                    if self.dist[u, w] > self.dist[u, v] + self.dist[v, w]:
                        self.dist[u, w] = self.dist[u, v] + self.dist[v, w]
                        self.path[u, w] = v

    def path_from_to(self, s: int, t: int):
        """
        从起点s到终点t的最短路径
        """
        v = s

        while v != -1:
            yield v
            v = self.path[v, t]
        yield t

    def dist_from_to(self, s: int, t: int):
        """
        从起点s到终点t的最短路径长度
        """
        return self.dist[s, t]


if __name__ == "__main__":
    DG = nx.read_weighted_edgelist('tinyEWD.txt',
                                   create_using=nx.DiGraph,
                                   nodetype=int)
    floyd_warshall = FloydWarshall(DG)
    print(*floyd_warshall.path_from_to(0, 1), '\tdistance:',
          floyd_warshall.dist_from_to(0, 1))
    print(*floyd_warshall.path_from_to(6, 5), '\tdistance:',
          floyd_warshall.dist_from_to(6, 5))
