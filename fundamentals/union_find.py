from networkx import nx
from networkx.drawing.nx_agraph import to_agraph


class UF:
    """
    并查集
    """
    def __init__(self, n: int):
        """
        初始化一个有n颗树的森林
        """
        self.__cnt = n
        self.__forest = [-1] * n

    def union(self, p: int, q: int):
        """
        连接p和q
        """
        root1 = self.find(p)
        root2 = self.find(q)

        # 如果p和q已经属于同一颗树，则直接返回
        if root1 == root2:
            return

        # 将小集合并入大集合中
        if self.__forest[root1] < self.__forest[root2]:
            self.__forest[root1] += self.__forest[root2]
            self.__forest[root2] = root1
        else:
            self.__forest[root2] += self.__forest[root1]
            self.__forest[root1] = root2

        # 集合数量减少1
        self.__cnt -= 1

    def find(self, p: int):
        """
        查找p所在树的根
        """

        # 查找树根
        root = p
        while self.__forest[root] >= 0:
            root = self.__forest[root]

        # 压缩路径
        while self.__forest[p] >= 0:
            self.__forest[p], p = root, self.__forest[p]

        return root

    def connected(self, p: int, q: int):
        """
        检测p和q是否连通
        """
        return self.find(p) == self.find(q)

    @property
    def cnt(self):
        """
        连通分量的数量
        """
        return self.__cnt

    @property
    def forest(self):
        """
        返回归并后产生的森林
        """
        return tuple(self.__forest)


if __name__ == "__main__":
    with open('tinyUF.txt') as f:
        n = int(f.readline())
        uf = UF(n)
        G = nx.Graph()

        for i in range(n):
            p, q = tuple(map(int, f.readline().split()))
            uf.union(p, q)

            # 画出每次联合后的森林图像
            G.clear()
            G.add_nodes_from(range(n))
            G.add_edges_from(
                filter(lambda pair: pair[1] > 0, enumerate(uf.forest)))
            A = to_agraph(G)
            A.node_attr['shape'] = 'circle'
            A.layout()
            A.draw(f'{i}-{p}-{q}.png')

    print(uf.cnt, 'components')
