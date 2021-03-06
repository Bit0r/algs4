from collections import deque


class Graph:
    """
    领接表实现的图
    """
    def __init__(self, filename: str = None, V: int = 0):
        """
        从一个文件中读取一幅图，或者构造一个空图
        """
        if V != 0:
            self.__init_adj(V)
            return

        with open(filename) as f:
            self.__init_adj(int(f.readline()))

            E = int(f.readline())
            for i in range(E):
                self.add_edge(*map(int, f.readline().split()))

    def __init_adj(self, V: int):
        """
        初始化领接表
        """
        self.V, self.E = V, 0
        self.adj = tuple(map(lambda _: deque(), range(self.V)))

    def add_edge(self, v: int, w: int):
        """
        添加边v-w
        """
        self.adj[v].append(w)
        self.adj[w].append(v)
        self.E += 1

    def __str__(self):
        """
        将图转化为字符串
        """
        return '\n'.join(
            map(lambda v: f'{v} : ' + ' '.join(map(str, self.adj[v])),
                range(self.V)))

    def degree(self, v: int):
        """
        计算v的度数
        """
        return len(self.adj[v])

    @property
    def max_degree(self):
        """
        所有顶点的最大度数
        """
        return max(map(self.degree, range(self.V)))

    @property
    def avg_degree(self):
        """
        所有顶点的平均度数
        """
        return 2 * self.E / self.V

    @property
    def self_loops(self):
        """
        自环个数
        """
        count = 0
        for v in range(self.V):
            for w in self.adj[v]:
                if v == w:
                    count += 1
        return count // 2


if __name__ == '__main__':
    g = Graph(filename='tinyG.txt')
    print(g)
    print(g.degree(1))
    print(g.max_degree)
    print(g.avg_degree)
    print(g.self_loops)
