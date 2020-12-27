from collections import deque

from .directed_edge import DirectedEdge


class WeightedDigraph:
    """
    带权重的有向图
    """
    def __init__(self, V: int = 0, filename: str = None):
        """
        创建一个空图或从文件读入图
        """
        if V != 0:
            self.__init_adj(V)
        elif filename is None:
            raise TypeError('必需有一个初始化参数')

        with open(filename) as file:
            self.__init_adj(int(file.readline()))
            E = int(file.readline())

            for _ in range(E):
                v, w, weight = file.readline().split()
                v, w = int(v), int(w)
                weight = float(weight)
                self.add_edge(DirectedEdge(v, w, weight))

    def __init_adj(self, V: int):
        """
        初始化领接表
        """
        self.V, self.E = V, 0
        self.adj = tuple(map(lambda _: deque(), range(V)))

    def add_edge(self, e: DirectedEdge):
        """
        添加一条有向边到图
        """
        self.adj[e.v].append(e)
        self.E += 1

    @property
    def edges(self):
        """
        返回所有有向边
        """
        for v in range(self.V):
            for e in self.adj[v]:
                yield e

    def __str__(self):
        """
        领接表的字符串表示
        """
        string = ''

        for v in range(self.V):
            string_v = f'{v} : '
            for e in self.adj[v]:
                string_v += f'{e.w} {e.weight:.2f}, '
            string += string_v[:-2] + '\n'

        return string


if __name__ == "__main__":
    WDG = WeightedDigraph(filename='tinyEWD.txt')
    print(*map(str, WDG.edges), sep='\n')
    print(WDG)
