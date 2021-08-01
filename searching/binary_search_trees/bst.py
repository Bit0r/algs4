from __future__ import annotations

import builtins
from collections import deque
from dataclasses import dataclass
from typing import Any


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

    def __init__(self):
        self.root = None

    __len__ = lambda self: len(self.root)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop = key.start, key.stop

            def getkeys(root: self.Node):
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

        stack = deque()
        cur = self.root
        while cur:
            if key < cur.key:
                stack.appendleft(cur)
                cur = cur.left
            elif key > cur.key:
                stack.appendleft(cur)
                cur = cur.right
            else:
                cur.value = value
                return

        if key < stack[0].key:
            stack[0].left = new_node
        else:
            stack[0].right = new_node

        for parent in stack:
            parent.count += 1

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

    @staticmethod
    def __delete_min(root: Node):
        """
        删除以root为根的子树中的最小结点
        """
        if root is None:
            return None, None
        elif root.left is None:
            return root.right, root

        stack = deque()
        cur = root
        while cur.left:
            stack.appendleft(cur)
            cur = cur.left

        stack[0].left = cur.right
        for parent in stack:
            parent.count -= 1
        return root, cur

    def __delitem__(self, key):
        stack = deque()
        cur = self.root
        while cur and cur.key != key:
            stack.appendleft(cur)
            if key < cur.key:
                cur = cur.left
            else:
                cur = cur.right

        if cur is None:
            raise KeyError(key)

        new_right, tmp = self.__delete_min(cur.right)
        if tmp:
            tmp.left, tmp.right = cur.left, new_right

        if cur is stack[0].left:
            stack[0].left = tmp
        else:
            stack[0].right = tmp

        for parent in stack:
            parent.count -= 1

    def __iter__(self):
        def __iter(root: self.Node):
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

        def __draw_edge(node0: self.Node, node1: self.Node):
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

        def __draw(root: self.Node):
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
    for i, k in enumerate('SEXARCHM'):
        st[k] = i
    for k in st:
        print(k, st[k])
    print()
    print(*st['E':'X'], end='\n\n')
    print(st.floor('G'), st.floor('*'), st.ceiling('G'), end='\n\n')
    print(st.select(6), st.rank('H'))
    st.draw()
    del st['E']
    st.draw('bst1.png')
