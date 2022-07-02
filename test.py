from Classes import Tree


def isPlumpRec(T: Tree, l: int):
    size = 1 if T.left is not None else 0 + 1 if T.right is not None else 0
    if size < 2 ** (l - 1):
        return False
    return isPlumpRec(T.left, l + 1) and isPlumpRec(T.right, l + 1)
