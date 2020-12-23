from collections import deque

from networkx import nx
from networkx.drawing.nx_agraph import to_agraph


class UF:
    """
    并查算法
    """
    def __init__(self, N: int):
        """
        初始化N个触点
        """
        self.__count = N
        self.__component = list(range(N))
        self.__size = [1] * N

    def union(self, p: int, q: int):
        """
        连接p和q
        """
        i = self.find(p)
        j = self.find(q)

        # 如果p和q已经属于一个集合，则直接返回
        if i == j:
            return

        # 将小集合并入大集合中
        if self.__size[i] < self.__size[j]:
            self.__component[i] = j
            self.__size[j] += self.__size[i]
        else:
            self.__component[j] = i
            self.__size[i] += self.__size[j]
        # 集合数量减少1
        self.__count -= 1

    def find(self, p: int):
        """
        查找p所在集合的标识符
        """
        # 使用一个队列，保存搜索路径
        path = deque()

        while p != self.__component[p]:
            path.append(p)
            p = self.__component[p]

        for v in path:
            self.__component[v] = p

        return p

    def connected(self, p: int, q: int):
        """
        检测p和q是否连通
        """
        return self.find(p) == self.find(q)

    @property
    def count(self):
        """
        连通分量的数量
        """
        return self.__count

    @property
    def forest(self):
        """
        返回归并后产生的森林
        """
        return tuple(self.__component)


if __name__ == "__main__":
    with open('tinyUF.txt') as f:
        N = int(f.readline())
        uf = UF(N)
        for i in range(N):
            p, q = tuple(map(int, f.readline().split()))
            if not uf.connected(p, q):
                uf.union(p, q)
                print(p, q)

            # 画出每次联合后的森林图像
            G = nx.Graph(list(enumerate(uf.forest)))
            A = to_agraph(G)
            A.node_attr['shape'] = 'circle'
            A.layout()
            A.draw(f'{i}-{p}-{q}.png')

    print(uf.count, 'components')
