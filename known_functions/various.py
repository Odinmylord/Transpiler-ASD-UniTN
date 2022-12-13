from utility.Classes import ListOneBased, MinPriorityQueue, Tree


def huffman(c: ListOneBased, f: ListOneBased, n: int):
    Q = MinPriorityQueue()
    for i in range(1, n + 1):
        Q.insert(Tree(c[i], f[i]), f[i])
    for i in range(1, n + 1):
        z1 = Q.delMin()
        z2 = Q.delMin()
        z = Tree(z1.value + z2.value, None)
        z.left = z1
        z.right = z2
        Q.insert(z, z.key)
    return Q.delMin()
