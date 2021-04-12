from __future__ import annotations

import re


class SuffixArray:
    class Suffix:
        def __init__(self, text, index):
            self.__text = text
            self._index = index

        def __lt__(self, other: SuffixArray.Suffix):
            if self is other:
                return False

            for i in range(min(len(self), len(other))):
                if self[i] < other[i]:
                    return True
                elif self[i] > other[i]:
                    return False
            else:
                return len(self) < len(other)

        def __len__(self):
            return len(self.__text) - self._index

        def __getitem__(self, index):
            return self.__text[self._index + index]

        def __str__(self):
            return self.__text[self._index:]

    def __init__(self, text: str) -> None:
        self.__suffixes = list(
            map(lambda i: SuffixArray.Suffix(text, i), range(len(text))))
        self.__suffixes.sort()

    def __len__(self):
        return len(self.__suffixes)

    def __getitem__(self, index: int):
        return str(self.__suffixes[index])

    def index(self, i: int):
        '''
        获取第 i 个后缀在原串中的偏移量

        Parameters
        ----------
        i : int
            后缀数组的元素索引

        Returns
        -------
        int
            子串的偏移量
        '''
        return self.__suffixes[i]._index

    def lcp(self, i: int):
        '''
        获取第 i 个后缀与第 i + 1 个后缀之间的最长公共前缀

        Parameters
        ----------
        i : int
            后缀数组的元素索引

        Returns
        -------
        int
            最长重复前缀的长度
        '''
        return self.__lcp_suffix(self.__suffixes[i], self.__suffixes[i + 1])

    @staticmethod
    def __lcp_suffix(s: SuffixArray.Suffix, t: SuffixArray.Suffix):
        n = min(len(s), len(t))
        for i in range(n):
            if s[i] != t[i]:
                return i
        else:
            return n

    def rank(self, query: str):
        '''
        查询字符串 query 在后缀数组中的位置

        Parameters
        ----------
        query : str
            查询字符串

        Returns
        -------
        int
            后缀数组中的位置
        '''
        left, right = 0, len(self) - 1
        while left <= right:
            middle = (left + right) // 2
            cmp = self.__compare(query, self.__suffixes[middle])
            if cmp < 0:
                right = middle - 1
            elif cmp > 0:
                left = middle + 1
            else:
                return middle
        else:
            return left

    @staticmethod
    def __compare(query: str, suffix: SuffixArray.Suffix):
        n = min(len(query), len(suffix))
        for i in range(n):
            if query[i] < suffix[i]:
                return -1
            elif query[i] > suffix[i]:
                return 1
        else:
            return len(query) - len(suffix)


if __name__ == '__main__':
    with open('abra.txt') as file:
        s = re.sub(r'\s+', r' ', file.read()).strip()
    sa = SuffixArray(s)
    print('  i ind lcp rnk select')
    print('---------------------------')

    for i in range(len(sa)):
        index = sa.index(i)
        rank = sa.rank(s[index:])
        ith = f'"{s[index:min(index+50,len(s))]}"'
        if i == len(sa) - 1:
            print(f'{i:3} {index:3}   - {rank:3} {ith}')
        else:
            lcp = sa.lcp(i)
            print(f'{i:3} {index:3} {lcp:3} {rank:3} {ith}')
