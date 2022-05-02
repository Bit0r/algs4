from __future__ import annotations

from dataclasses import dataclass
from typing import List

from searching.binary_search_trees.bst import BST, len


class AVL(BST):
    @dataclass
    class Node(BST.Node):
        height: int = 0
        left: AVL.Node = None
        right: AVL.Node = None

        @property
        def factor(self):
            return self.get_height(self.left) - self.get_height(self.right)

        def update(self):
            super().update()
            self.height = 1 + max(self.get_height(self.left),
                                  self.get_height(self.right))

        @staticmethod
        def get_height(root: AVL.Node):
            return root.height if root else -1

    @staticmethod
    def _update_path(path: List[Node]):
        for idx in range(len(path) - 1, -1, -1):
            root = path[idx]

            root.update()
            root = AVL.balance(root)

            if idx > 0:
                parent = path[idx - 1]
                if root.key < parent.key:
                    parent.left = root
                else:
                    parent.right = root

        return root

    @staticmethod
    def balance(root: Node):
        if root.factor == 2:
            # L型树
            if root.left.factor < 0:
                # 将LR调整为LL
                root.left = AVL.__rotate_left(root.left)
            if root.left.factor >= 0:
                # 调整LL平衡
                root = AVL.__rotate_right(root)
        elif root.factor == -2:
            # R型树
            if root.right.factor > 0:
                # 将RL调整为RR
                root.right = AVL.__rotate_right(root.right)
            if root.right.factor <= 0:
                # 调整RR平衡
                root = AVL.__rotate_left(root)
        return root

    @staticmethod
    def __rotate_left(root: Node):
        pivot = root.right
        root.right, pivot.left = pivot.left, root
        root.update()
        pivot.update()
        return pivot

    @staticmethod
    def __rotate_right(root: Node):
        pivot = root.left
        root.left, pivot.right = pivot.right, root
        root.update()
        pivot.update()
        return pivot


if __name__ == "__main__":
    st = AVL()
    for i, k in enumerate('ACDKJGE'):
        st[k] = i
    for k in st:
        print(k, st[k])
    print()
    print(*st['C':'F'], end='\n\n')
    print(st.floor('F'), st.floor('*'), st.ceiling('H'), end='\n\n')
    print(st.select(6), st.rank('E'))
    st.draw(filename='avl.png')
    del st['J']
    st.draw('avl1.png')
    del st['D']
    st.draw('avl2.png')
