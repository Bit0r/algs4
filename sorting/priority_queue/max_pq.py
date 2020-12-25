class MaxPQ:
    """
    最大堆
    """
    def __init__(self):
        """
        初始化堆数组
        """
        self.__pq = [None] * 2
        self.size = 0

    def __swim(self, i: int):
        """
        上浮某个元素
        """
        while i > 1 and self.__less(i // 2, i):
            self.__exch(i // 2, i)
            i //= 2

    def __sink(self, i: int):
        """
        下沉某个元素
        """
        while 2 * i <= self.size:
            j = i * 2
            if j != self.size and self.__less(j, j + 1):
                j += 1
            if self.__less(j, i):
                break
            self.__exch(i, j)
            i = j

    def insert(self, elem):
        """
        插入一个元素
        """
        self.size += 1
        self.__pq[self.size] = elem
        self.__swim(self.size)

        # 当完全占用空间时，空间加倍
        if self.size + 1 == len(self.__pq):
            self.__resize(len(self.__pq) * 2)

    def del_max(self):
        """
        删除最大值
        """
        max = self.__pq[1]

        # 将最后一个元素提升到顶部
        self.__pq[1] = self.__pq[self.size]

        # 删掉最后一个元素
        self.__pq[self.size] = None  # 防止对象游离
        self.size -= 1

        # 对顶部元素进行下称
        self.__sink(1)

        # 当空间占用为1/4时，空间减半
        if self.size > 0 and self.size + 1 == len(self.__pq) // 4:
            self.__resize(len(self.__pq) // 2)
        return max

    @property
    def is_empty(self):
        """
        优先队列是否为空
        """
        return self.size == 0

    def __resize(self, n: int):
        """
        调整数组容量
        """
        new_pq = [None] * n
        for i in range(self.size + 1):
            new_pq[i] = self.__pq[i]
        self.__pq = new_pq

    def __less(self, i: int, j: int):
        """
        比较堆数组中的第i和j个元素
        """
        return self.__pq[i] < self.__pq[j]

    def __exch(self, i: int, j: int):
        """
        交换堆数组中的第i和j个元素
        """
        self.__pq[i], self.__pq[j] = self.__pq[j], self.__pq[i]


if __name__ == "__main__":
    max_pq = MaxPQ()
    sequence = 'P R I O * R * * I * T * Y * * * Q U E * * * U * E'.split()
    for elem in sequence:
        if elem == '*':
            print(max_pq.del_max(), end=' ')
        else:
            max_pq.insert(elem)
