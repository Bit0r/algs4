def quick_sort(a, left: int = None, right: int = None):
    def exch(i, j):
        a[i], a[j] = a[j], a[i]

    def median3(i, j, k):
        if a[i] < a[j]:
            if a[j] < a[k]:
                a[i], a[j], a[k] = a[j], a[i], a[k]
            elif a[i] < a[k]:
                a[i], a[j], a[k] = a[k], a[i], a[j]
            else:
                a[i], a[j], a[k] = a[i], a[k], a[j]
        elif a[i] < a[k]:
            pass
        elif a[j] < a[k]:
            a[i], a[j], a[k] = a[k], a[j], a[i]
        else:
            a[i], a[j], a[k] = a[j], a[k], a[i]

    def insert_sort(left, right):
        for i in range(left, right + 1):
            for j in range(i, left, -1):
                if a[j - 1] <= a[j]:
                    break
                exch(j, j - 1)

    if left is None:
        left, right = 0, len(a) - 1

    n = right - left + 1
    if n <= 8:
        insert_sort(left, right)
        return
    else:
        median3(left, (left + right) // 2, right)

    i, j = left, right + 1
    p, q = left + 1, right
    v = a[left]
    while True:
        i += 1
        while a[i] < v:
            i += 1

        j -= 1
        while a[j] > v:
            j -= 1

        if i == j and a[i] == v:
            exch(p, i)
            p += 1
        if i >= j:
            break

        exch(i, j)
        if a[i] == v:
            exch(p, i)
            p += 1
        if a[j] == v:
            exch(q, j)
            q -= 1

    i = j + 1
    for k in range(left, p):
        exch(k, j)
        j -= 1
    for k in range(right, q, -1):
        a[i], a[k] = a[k], a[i]
        i += 1

    if left < j:
        quick_sort(a, left, j)
    if i < right:
        quick_sort(a, i, right)


if __name__ == '__main__':
    import numpy as np
    a = np.random.randint(5, size=100)
    # a = np.zeros(100, dtype=int)
    print(a)
    quick_sort(a)
    print(a)
