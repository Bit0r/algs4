class DirectedEdge:
    """
    带权重的有向边
    """
    def __init__(self, v: int, w: int, weight: float):
        """
        初始化边的起点和终点，以及权重
        """
        self.v, self.w, self.weight = v, w, weight

    def __str__(self):
        """
        边的字符串表示
        """
        return f'{self.v}->{self.w} {self.weight}'


if __name__ == "__main__":
    e = DirectedEdge(1, 3, 0.5)
    print(e)
