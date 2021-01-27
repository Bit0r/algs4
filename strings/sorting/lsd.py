def lsd_sort(a):
    # ASCII alphabet size
    r = 128
    aux = [None] * len(a)
    count = [0] * (r + 1)

    for d in range(len(a[0]) - 1, -1, -1):
        for i in range(r + 1):
            count[i] = 0

        # compute frequency counts
        for string in a:
            count[ord(string[d]) + 1] += 1

        # compute cumulates
        for i in range(r):
            count[i + 1] += count[i]

        # move data
        for string in a:
            index = ord(string[d])
            aux[count[index]] = string
            count[index] += 1

        # copy back
        for i in range(len(a)):
            a[i] = aux[i]


if __name__ == '__main__':
    with open('words3.txt') as file:
        ls = file.read().split()
        lsd_sort(ls)
        print(ls)

    def check(a):
        for i in range(len(a) - 1):
            if a[i] > a[i + 1]:
                return False
        else:
            return True

    assert check(ls)
