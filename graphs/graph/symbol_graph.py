from .graph import Graph


class SymbolGraph:
    """
    使用符号作为顶点的图
    """
    def __init__(self, filename: str, sep: str):
        """
        根据filename指定的文件构造图，使用sep来分隔顶点
        """
        # 构造从字符串到索引的映射
        self.__symbol_table = {}
        file = open(filename)
        for line in file:
            # 为每个不同的字符串关联一个索引
            for key in line.strip().split(sep):
                if key not in self.__symbol_table:
                    self.__symbol_table[key] = len(self.__symbol_table)

        # 构造从索引到字符串的映射
        V = len(self.__symbol_table)
        self.__keys = [None] * V
        for key, index in self.__symbol_table.items():
            self.__keys[index] = key

        file.seek(0)

        # 构造普通的数字作为顶点的图
        self.G = Graph(V=V)
        for line in file:
            # 将每行的第一个顶点v与该行的其它顶点w相连
            ls = line.strip().split(sep)
            v = self.__symbol_table[ls[0]]
            for key in ls[1:]:
                w = self.__symbol_table[key]
                self.G.add_edge(v, w)

        file.close()

    def contains(self, key: str):
        """
        key是一个顶点吗？
        """
        return key in self.__symbol_table

    def get_vertex_index(self, key: str):
        """
        顶点key的索引
        """
        return self.__symbol_table[key]

    def get_vertex_name(self, v: int):
        """
        索引v的顶点名
        """
        return self.__keys[v]


if __name__ == "__main__":
    SG = SymbolGraph('routes.txt', ' ')
    print(SG.G)
    print(SG.get_vertex_index('JFK'))
    print(SG.get_vertex_name(5))
