from collections import deque

from .edge import Edge


class WeightedGraph:
    """
    带权重的图
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
                self.add_edge(Edge(v, w, weight))

    def __init_adj(self, V: int):
        """
        初始化领接表
        """
        self.V, self.E = V, 0
        self.adj = tuple(map(lambda _: deque(), range(V)))

    def add_edge(self, e: Edge):
        """
        添加一条边到图
        """
        v = e.either
        w = e.other(v)

        self.adj[v].append(e)
        self.adj[w].append(e)
        self.E += 1

    @property
    def edges(self):
        """
        图中的所有边
        """
        edges = deque()

        for v in range(self.V):
            for e in self.adj[v]:
                if e.other(v) > v:
                    edges.append(e)

        return edges

    def __str__(self):
        """
        领接表的字符串表示
        """
        string = ''

        for v in range(self.V):
            string_v = f'{v} : '
            for e in self.adj[v]:
                string_v += f'{e.other(v)} {e.weight:.2f}, '
            string += string_v[:-2] + '\n'

        return string


if __name__ == "__main__":
    WG = WeightedGraph(filename='tinyEWG.txt')
    print(*map(str, WG.edges), sep='\n')
    print(WG)
