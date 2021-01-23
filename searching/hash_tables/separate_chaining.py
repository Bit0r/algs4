from collections import deque


class SeparateChaining:
    def __init__(self, capacity=4):
        self._m, self._n = capacity, 0
        self._st = list(map(lambda _: deque(), range(capacity)))

    def __hash(self, key):
        # h = hash(key)
        # h ^= (h >> 20) ^ (h >> 12) ^ (h >> 7) ^ (h >> 4)
        # return h & (self._m - 1)
        return (hash(key) & 0x7fffffff) % self._m

    def __len__(self):
        return self._n

    def __getitem__(self, key):
        ls = self._st[self.__hash(key)]
        for k, v in ls:
            if k == key:
                return v
        else:
            raise KeyError(key)

    def __setitem__(self, key, value):
        if key is None:
            raise KeyError('The Key is None')

        if self._n == self._m:
            self.__resize(self._m * 2)

        ls = self._st[self.__hash(key)]
        for pair in ls:
            if pair[0] == key:
                pair[1] = value
                break
        else:
            ls.appendleft([key, value])
            self._n += 1

    def __delitem__(self, key):
        if key is None:
            raise KeyError('The Key is None')

        ls = self._st[self.__hash(key)]
        i = 0
        for k, _ in ls:
            if k == key:
                break
            else:
                i += 1
        else:
            raise KeyError(key)
        del ls[i]
        self._n -= 1

        if self._m > 4 and 4 * self._n <= self._m:
            self.__resize(self._m // 2)

    def __iter__(self):
        for ls in self._st:
            for k, _ in ls:
                yield k

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __resize(self, capacity):
        tmp = SeparateChaining(capacity)
        for ls in self._st:
            for k, v in ls:
                tmp[k] = v
        self._m, self._n, self._st = tmp._m, tmp._n, tmp._st


if __name__ == "__main__":
    st = SeparateChaining()
    for i, k in enumerate('SEXARCHM'):
        st[k] = i
    for k in st:
        print(k, st[k])

    print('\n', st._m, st._n)
    for ls in st._st:
        print(ls)

    for k in 'EXARCH':
        del st[k]
    st['S'] = 8
    print('\n', st._m, st._n)
    for ls in st._st:
        print(ls)
