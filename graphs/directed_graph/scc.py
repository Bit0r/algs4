import networkx as nx


class SCC:
    """
    [summary]
    有向图的强连通分量
    """
    def __init__(self, DG: nx.DiGraph):
        post = self.getpost(DG.reverse())
        seq = sorted(DG.nodes, key=post.__getitem__, reverse=True)
        self.calc_cc(DG, seq=seq)

    def dfs(self,
            DG: nx.DiGraph,
            seq=None,
            visited=None,
            init=None,
            previsit=None,
            postvisit=None):

        visited = visited if visited else [False] * DG.number_of_nodes()

        def explore(v):
            visited[v] = True
            if previsit:
                previsit(v)
            for w in DG[v]:
                if not visited[w]:
                    explore(w)
            if postvisit:
                postvisit(v)

        seq = seq if seq else DG.nodes
        for v in seq:
            if not visited[v]:
                if init:
                    init(v)
                explore(v)

    def calc_cc(self, DG: nx.DiGraph, seq=None):
        self.cc = [None] * DG.number_of_nodes()
        self.cc_cnt = 0

        def init(_):
            self.cc_cnt += 1

        def previsit(v):
            self.cc[v] = self.cc_cnt

        self.dfs(DG, seq=seq, init=init, previsit=previsit)

    def getpost(self, DG: nx.DiGraph):
        post = [None] * DG.number_of_nodes()
        visited = [False] * DG.number_of_nodes()
        clock = 0

        def init(_):
            nonlocal clock, visited
            clock = 0
            visited[:] = [False] * DG.number_of_nodes()

        def previsit(_):
            nonlocal clock
            clock += 1

        def postvisit(v):
            previsit(v)
            post[v] = clock

        self.dfs(DG,
                 visited=visited,
                 init=init,
                 previsit=previsit,
                 postvisit=postvisit)
        return post


if __name__ == '__main__':
    DG = nx.read_edgelist('tinyDG.txt', create_using=nx.DiGraph, nodetype=int)
    scc = SCC(DG)
    print(scc.cc_cnt)
    print(*scc.cc)
