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


class RedBlackBST:
    """
    左倾红黑树
    """
    RED, BLACK = True, False

    @dataclass
    class Node:
        """
        红黑树的结点
        """
        key: Any  # 结点的键
        value: Any  # 结点的值
        left: RedBlackBST.Node = None  # 左子结点
        right: RedBlackBST.Node = None  # 右子结点
        count: int = 1  # 子树大小
        color: bool = True  # 父链接的颜色

        __len__ = lambda self: self.count

    @staticmethod
    def __is_red(node: Node):
        """
        检查node的父链接是否为红色
        """
        if node is None:
            return False
        return node.color == RedBlackBST.RED

    @staticmethod
    def __is_black(node: Node):
        """
        检查node的父链接是否为黑色
        """
        if node is None:
            return True
        return node.color == RedBlackBST.BLACK

    @staticmethod
    def __rotate_left(root: Node):
        """
        对以root为根的子树进行左旋转
        """
        new_root = root.right
        # 移动子树
        root.right, new_root.left = new_root.left, root
        # 改变颜色
        new_root.color, root.color = root.color, RedBlackBST.RED
        # 改变大小
        new_root.count, root.count = root.count, 1 + len(root.left) + len(
            root.right)
        return new_root

    @staticmethod
    def __rotate_right(root: Node):
        """
        对以root为根的子树进行右旋转
        """
        new_root = root.left
        root.left, new_root.right = new_root.right, root
        root.color, new_root.color = RedBlackBST.RED, root.color
        root.count, new_root.count = len(root.left) + len(
            root.right) + 1, root.count

    @staticmethod
    def __flip_colors(root: Node):
        """
        对以root为根且为中键的3-结点进行分裂操作
        """
        root.color = RedBlackBST.RED
        root.left.color, root.right.color = RedBlackBST.BLACK, RedBlackBST.BLACK

    def __init__(self):
        self.root = None

    __len__ = lambda self: len(self.root)

    def __setitem__(self, key, value):
        new_node = self.Node(key, value)
        if self.root is None:
            self.root = new_node
            self.root.color = self.BLACK
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

        while len(stack) > 1:
            h = stack.popleft()
            if self.__is_red(h.right) and self.__is_black(h.left):
                h = self.__rotate_left(h)
            if self.__is_red(h.left) and self.__is_red(h.left.left):
                h = self.__rotate_right(h)
            if self.__is_red(h.left) and self.__is_red(h.right):
                self.__flip_colors(h)
            h.count = len(h.left) + len(h.right) + 1

            if h.key < stack[0].key:
                stack[0].left = h
            else:
                stack[0].right = h

        root = stack.popleft()
        if self.__is_red(root.right) and self.__is_black(root.left):
            root = self.__rotate_left(root)
        if self.__is_red(root.left) and self.__is_red(root.left.left):
            root = self.__rotate_right(root)
        if self.__is_red(root.left) and self.__is_red(root.right):
            self.__flip_colors(root)
        root.color = self.BLACK
        root.count = len(root.left) + len(root.right) + 1
        self.root = root

    def draw(self, filename='rb_bst.png'):
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
                color = 'red' if node1.color == self.RED else 'black'
                G.add_edge(node0.key, node1.key, color=color)
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
    rb_bst = RedBlackBST()
    for i, k in enumerate('ACEHRS'):
        rb_bst[k] = i
    rb_bst.draw()
