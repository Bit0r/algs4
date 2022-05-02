from __future__ import annotations

import builtins
from dataclasses import dataclass
from typing import Any, List


def len(obj):
    if obj:
        return builtins.len(obj)
    else:
        return 0


class BST:
    """
    二叉搜索树
    """
    @dataclass
    class Node:
        """
        二叉搜索树的结点类
        """
        key: Any
        value: Any
        count: int = 1
        left: BST.Node = None
        right: BST.Node = None

        __len__ = lambda self: self.count

        def update(self):
            self.count = 1 + len(self.left) + len(self.right)

    def __init__(self):
        self.root = None

    __len__ = lambda self: len(self.root)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = key.start, key.stop

            def getkeys(root: BST.Node):
                """
                按照键大小，利用中序遍历入队
                """
                if root is None:
                    return

                if start < root.key:
                    yield from getkeys(root.left)
                if start <= root.key <= stop:
                    yield root.key
                if stop > root.key:
                    yield from getkeys(root.right)

            return getkeys(self.root)

        cur = self.root
        while cur:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return cur.value

        raise KeyError(key)

    def __setitem__(self, key, value):
        new_node = self.Node(key, value)
        if self.root is None:
            self.root = new_node
            return

        path = []
        cur = self.root
        while cur:
            path.append(cur)
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                cur.value = value
                return

        if key < path[-1].key:
            path[-1].left = new_node
        else:
            path[-1].right = new_node

        self.root = self._update_path(path)

    @staticmethod
    def _update_path(path: List[Node]):
        for root in reversed(path):
            root.update()
        return root

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def min(self):
        """
        返回最小键
        """
        if self.root is None:
            return None

        cur = self.root
        while cur.left:
            cur = cur.left
        return cur.key

    def max(self):
        """
        返回最大键
        """
        if self.root is None:
            return None

        cur = self.root
        while cur.right:
            cur = cur.right
        return cur.key

    def floor(self, key):
        """
        找出小于等于key的最大键
        """
        if self.root is None:
            return

        cur, candidate = self.root, None
        while cur:
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                candidate = cur.key
                cur = cur.right
            else:
                return key
        return candidate

    def ceiling(self, key):
        """
        找出大于等于key的最小键
        """
        if self.root is None:
            return

        cur, candidate = self.root, None
        while cur:
            if key < cur.key:
                candidate = cur.key
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                return key
        return candidate

    def select(self, k):
        """
        找出排名为k的键
        """
        if len(self) < k or k < 1:
            raise IndexError('index out of range')

        cur = self.root
        while True:
            t = len(cur.left) + 1
            if k < t:
                cur = cur.left
            elif k > t:
                k -= t
                cur = cur.right
            else:
                return cur.key

    def rank(self, key):
        """
        找出key在树中的排名
        """
        cur, k = self.root, 0
        while cur:
            t = len(cur.left) + 1
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                k += t
                cur = cur.right
            else:
                k += t
                return k
        raise KeyError(key)

    def delete_min(self):
        """
        删除最小结点
        """
        self.root, node_min = self.__delete_min(self.root)
        return node_min.key, node_min.value

    @classmethod
    def __delete_min(cls, root: Node):
        """
        删除以root为根的子树中的最小结点
        返回新root和被删的node
        """
        if root is None:
            return None, None
        elif root.left is None:
            return root.right, root

        path = []
        cur = root
        while cur.left:
            path.append(cur)
            cur = cur.left

        path[-1].left = cur.right
        cls._update_path(path)
        return root, cur

    def __delitem__(self, key):
        path = []
        cur = self.root
        while cur:
            path.append(cur)
            if key < cur.key:
                cur = cur.left
            elif key > cur.key:
                cur = cur.right
            else:
                path.pop()
                break
        else:
            raise KeyError(key)

        if cur.left and cur.right:
            # 如果左右孩子都有，则用后继代替自己，然后删除后继
            new_right, root = self.__delete_min(cur.right)
            root.left, root.right = cur.left, new_right
        else:
            # 如果只有一个子树，则用该子树替代自己
            root = cur.left or cur.right

        if path:
            # 如果路径不为空，则将新子树连接到父节点上
            parent = path[-1]
            if cur is parent.left:
                parent.left = root
            else:
                parent.right = root

        # 从新子树向上回溯并更新
        path.append(root)
        self.root = self._update_path(path)

    def __iter__(self):
        def __iter(root: BST.Node):
            """
            将以root为根的树按照中序遍历入队
            """
            if root is None:
                return

            yield from __iter(root.left)
            yield root.key
            yield from __iter(root.right)

        return __iter(self.root)

    def draw(self, filename='bst.png'):
        from pygraphviz import AGraph
        G = AGraph()
        G.node_attr['shape'] = 'circle'

        none_count = 0

        def __draw_edge(node0: BST.Node, node1: BST.Node):
            """
            画一条从node0到node1边
            """
            nonlocal none_count
            if node1:
                G.add_edge(node0.key, node1.key)
            else:
                none_node = f'None{none_count}'
                G.add_node(none_node, shape='point')
                G.add_edge(node0.key, none_node)
                none_count += 1

        def __draw(root: BST.Node):
            """
            画出以root为根的子树
            """
            if root is None:
                return

            __draw(root.left)
            __draw_edge(root, root.left)
            __draw_edge(root, root.right)
            __draw(root.right)

        __draw(self.root)
        G.layout('dot')
        G.draw(filename)


if __name__ == "__main__":
    st = BST()
    for i, k in enumerate('HSEXARCMGZD'):
        st[k] = i
    for k in st:
        print(k, st[k])
    print('\n', len(st), '\n')
    print(*st['E':'X'], end='\n\n')
    print(st.floor('G'), st.floor('*'), st.ceiling('G'), end='\n\n')
    print(st.select(6), st.rank('H'))
    st.draw()
    del st['E']
    st.draw('bst1.png')
    del st['H']
    st.draw('bst2.png')
