from __future__ import annotations


class LRUCache:
    """
    docstring
    """
    class Node:
        """
        docstring
        """
        def __init__(self,
                     item,
                     prev: LRUCache.Node = None,
                     next: LRUCache.Node = None):
            """
            docstring
            """
            self.item, self.prev, self.next = item, prev, next

    def __init__(self):
        """
        docstring
        """
        self.head = self.tail = None
        self.st = {}

    def access(self, item):
        """
        LRU访问策略
        """
        try:
            node = self.st[item]

            if node is self.head:
                # 如果node已经在头部，则直接返回
                return
            elif node is self.tail:
                # 如果node在尾部，则将链表尾部前移
                self.tail = self.tail.prev
                self.tail.next = None
            else:
                # node在中间，删除此结点，同时连接左右两个结点
                node.next.prev, node.prev.next = node.prev, node.next

            # 将node设为新的头
            node.prev, node.next = None, self.head
            self.head.prev = node
            self.head = node
        except KeyError:
            node = self.Node(item, next=self.head)
            self.st[item] = node
            if self.head:
                self.head.prev = node
                self.head = node
            else:
                self.head = self.tail = node

    def remove(self):
        """
        从双链表的尾部移除元素
        """
        if self.head is None:
            # 链表有0个结点
            return
        elif self.head is self.tail:
            # 链表只有1个结点
            tmp = self.head
            self.head = self.tail = None
        else:
            # 链表有多个结点
            tmp = self.tail
            self.tail = self.tail.prev
            self.tail.next = None

        del self.st[tmp.item]
        return tmp.item


if __name__ == "__main__":
    lru = LRUCache()
    lru.access(1)
    lru.access(2)
    lru.access(1)
    lru.access(3)
    print(lru.remove())
    print(lru.remove())
    lru.access(4)
    print(lru.remove())
    print(lru.remove())
    print(lru.remove())
