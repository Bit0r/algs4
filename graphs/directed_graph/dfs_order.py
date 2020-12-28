import networkx as nx
from collections import deque


class DepthFirstOrder:
    """
    docstring
    """
    def __init__(self, DG: nx.DiGraph):
        """
        docstring
        """
        self.pre, self.post, self.reverse_post = deque(), deque(), deque()
        self.__marked = [False] * DG.number_of_nodes()
        self.__DG = DG
        for v in DG.nodes:
            if not self.__marked[v]:
                self.__dfs(v)

    def __dfs(self, v: int):
        self.pre.append(v)

        self.__marked[v] = True
        for w in self.__DG[v]:
            if not self.__marked[w]:
                self.__dfs(w)

        self.post.append(v)
        self.reverse_post.appendleft(v)


if __name__ == "__main__":
    DG = nx.read_edgelist('tinyDAG.txt', create_using=nx.DiGraph, nodetype=int)
    order = DepthFirstOrder(DG)
    print(order.pre, order.post, order.reverse_post, sep='\n')
