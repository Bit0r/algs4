class LinearProbing:
    def __init__(self, capacity=4):
        self._m, self._n = capacity, 0
        self._st = [None] * capacity

    def __len__(self):
        return self._n

    def __hash(self, key):
        return (hash(key) & 0x7fffffff) % self._m

    def __resize(self, capacity):
        tmp = LinearProbing(capacity)
        for ls in self._st:
            for k, v in ls:
                tmp[k] = v
        self._m, self._n, self._st = tmp._m, tmp._n, tmp._st

    def __getitem__(self, key):
        if key is None:
            raise KeyError('The Key is None')

        i = self.__hash(key)
        while self._st[i]:
            if self._st[i][0] == key:
                return self._st[i][1]
            i = (i + 1) % self._m
        else:
            raise KeyError(key)

    def __contains__(self, key):
        try:
            self[key]
            return True
        except KeyError:
            return False

    def __setitem__(self, key, value):
        if key is None:
            raise KeyError('The Key is None')

        if self._n * 2 == self._m:
            self.__resize(self._m * 2)

        i = self.__hash(key)
        while self._st[i]:
            if self._st[i][0] == key:
                self._st[i][1] = value
                break
            i = (i + 1) % self._m
        else:
            self._st[i] = [key, value]
            self._n += 1

    def __delitem__(self, key):
        if key is None:
            raise KeyError('The Key is None')

        i = self.__hash(key)
        while self._st[i]:
            if self._st[i][0] == key:
                self._st[i] = None
                self._n -= 1
                break
            i = (i + 1) % self._m
        else:
            raise KeyError(key)

        # rehash all keys in same cluster
        i = (i + 1) % self._m
        while self._st[i]:
            # delete st[i] and reinsert
            k, v = self._st[i]
            self._st[i] = None
            self._n -= 1
            self[k] = v
            i = (i + 1) % self._m

        if self._n > 0 and self._n * 8 == self._m:
            self.__resize(self._m // 2)

    def __resize(self, capacity):
        tmp = LinearProbing(capacity)
        for pair in self._st:
            if pair:
                k, v = pair
                tmp[k] = v
        self._m, self._n, self._st = tmp._m, tmp._n, tmp._st

    def __iter__(self):
        for pair in self._st:
            if pair:
                yield pair[0]


if __name__ == '__main__':
    st = LinearProbing()
    for i, k in enumerate('SEXARCHM'):
        st[k] = i
    for k in st:
        print(k, st[k])

    print('\n', st._m, st._n)
    print(st._st)
    for k in 'EXARCH':
        del st[k]
    st['S'] = 8
    print('\n', st._m, st._n)
    print(st._st)
