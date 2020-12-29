from collections import deque

import networkx as nx


class BellmanFordQueue:
    """
    寻找最短路径的基于队列的bellman-ford算法
    """
    def __init__(self, DG: nx.DiGraph, s: int):
        """
        初始化起点和有向图
        """
        self.__V = V = DG.number_of_nodes()
        self.__DG = DG
        self.__s = s

        self.dist_to = [float('inf')] * V
        self.__edge_to = [None] * V

        self.__queue = deque()
        self.__on_queue = [False] * V

        self.__cnt = 0
        self.cycle = None

        self.dist_to[s] = 0

        self.__queue.append(s)
        self.__on_queue[s] = True
        # 在队列不为空且没有负权环时循环
        while self.__queue and not self.has_negative_cycle:
            v = self.__queue.popleft()
            self.__on_queue[v] = False
            self.__relax(v)

        # assert self.__check()

    def __relax(self, v: int):
        """
        能够检测负权环的放松函数
        """
        for w in self.__DG[v]:
            if self.dist_to[w] > self.dist_to[v] + self.__DG[v][w]['weight']:
                self.dist_to[w] = self.dist_to[v] + self.__DG[v][w]['weight']
                self.__edge_to[w] = v

                # 将放松成功且尚未在队列中的顶点w入队
                if not self.__on_queue[w]:
                    self.__queue.append(w)
                    self.__on_queue[w] = True

            # 每放松V次就进行一次检查
            self.__cnt += 1
            if self.__cnt % self.__V == 0:
                self.__find_negative_cycle()
                if self.has_negative_cycle:
                    return

    def __find_negative_cycle(self):
        """
        寻找负权环
        """
        spt = nx.DiGraph(
            list(map(lambda e: (e[1], e[0]), enumerate(self.__edge_to))))
        try:
            self.cycle = nx.find_cycle(spt)
        except:
            pass

    @property
    def has_negative_cycle(self):
        """
        是否有负权环
        """
        return self.cycle is not None

    def path_to(self, v: int):
        """
        获得s->v的最短路径
        """
        if self.cycle:
            raise Exception('存在负权环，没有最短路径')

        stack = deque()

        while v != self.__s:
            stack.appendleft(v)
            u = self.__edge_to[v]
            v = u
        stack.appendleft(v)

        return stack

    def __check(self):
        """
        检查每一条从v到w有向边e是否符合：
            dist_to[w] <= dist_to[v] + e.weight
        """
        for v, w in self.__DG.edges:
            if self.dist_to[w] > self.dist_to[v] + self.__DG[v][w]['weight']:
                return False

        return True


if __name__ == "__main__":
    DG = nx.read_weighted_edgelist('tinyEWDnc.txt',
                                   create_using=nx.DiGraph,
                                   nodetype=int)
    sp = BellmanFordQueue(DG, 0)
    # print(sp.path_to(4))
    print(sp.cycle)
