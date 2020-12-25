class Edge:
    """
    带权边的类
    """
    def __init__(self, v: int, w: int, weight: float):
        """
        设置边的顶点和权重
        """
        self.__v, self.__w, self.weight = v, w, weight

    @property
    def either(self):
        """
        获得边的任意一个顶点
        """
        return self.__v

    def other(self, v: int):
        """
        已经知道边的一个顶点v，获取另一个顶点w
        """
        return self.__w if v == self.__v else self.__v

    def __str__(self):
        """
        边的文字表示
        """
        return f'{self.__v}-{self.__w} {self.weight:.2f}'

    def __cmp__(self, other):
        """
        比较两条边的权重
        """
        if self.weight < other.weight:
            return -1
        elif self.weight > other.weight:
            return 1
        else:
            return 0


from collections import deque


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
