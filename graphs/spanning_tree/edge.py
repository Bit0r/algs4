from functools import total_ordering


@total_ordering
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

    def __lt__(self, other):
        """
        比较两条边的权重
        """
        return self.weight < other.weight

    def __eq__(self):
        """
        两边是否相等
        """
        return self.weight == self.weight


if __name__ == "__main__":
    e1 = Edge(1, 3, 1.2)
    e2 = Edge(2, 5, 4.5)
    print(e1 < e2, e1, e2, sep='\n')
