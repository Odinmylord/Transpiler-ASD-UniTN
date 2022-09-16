from Classes import Tree

"""The known_functions inside this file are translated from Alberto Montresor site 
https://cricca.disi.unitn.it/montresor/ the original work is available under license CC BY-SA 4.0 """
BLACK = 0
RED = 1


def count(T: Tree):
    """Function that counts the number of nodes in a binary tree"""
    if T == None:
        return 0
    else:
        Cl = count(T.left())
        Cr = count(T.right())
        return Cl + Cr + 1


# SET OF FUNCTIONS THAT ONLY WORK WITH BINARY SEARCH TREES

def lookupNode(T: Tree, k):
    if T == None or T.key == k:
        return T
    else:
        return lookupNode((T.left if k < T.key else T.right), k)


def successorNode(t: Tree):
    if t == None:
        return t
    if t.right != None:  # Caso 1
        return min(t.right)
    else:  # Caso 2
        p = t.parent
        while p != None and t == p.right:
            t = p
            p = p.parent
        return p


def predecessorNode(t: Tree):
    if t == None:
        return t
    if t.left != None:  # Caso 1
        return max(t.left)
    else:  # Caso 2
        p = t.parent
        while p != None and t == p.left:
            t = p
            p = p.parent
        return p


def min(T: Tree):
    u = T
    while u.left != None:
        u = u.left
    return u


def max(T: Tree):
    u = T
    while u.right != None:
        u = u.right
    return u


def insertNode(T: Tree, k, v):  # Capire perché si rompe e va in un loop infinito
    p = None  # Padre
    u = T
    while u is not None and u.key != k:  # Cerca posizione inserimento
        p = u
        u = (u.left if k < u.key else u.right)
    if u is not None and u.key == k:
        u.value = v  # Chiave già presente
    else:
        new = Tree(v, k)  # Crea un nodo coppia chiave-valore (inverted v and k)
        link(p, new, k)
        balanceInsert(new)  # Didn't change this part hoping that it won't cause problems to non red-black trees
        if p is None:
            T = new  # Primo nodo ad essere inserito
    return T  # Restituisce albero non modificato o nuovo nodo


def link(p: Tree, u: Tree, k):
    if u is not None:
        u.parent = p  # Registrazione padre
    if p is not None:
        if k < p.key:
            p.left = u  # Attaccato come figlio sinistro
        else:
            p.right = u  # Attaccato come figlio destro


# RED-BLACK TREES FUNCTIONS

def balanceInsert(t: Tree):
    t.color = RED
    while t != None:
        p = t.parent  # Padre
        n = (p.parent if p != None else None)  # Nonno
        z = (None if n == None else (n.right if n.left == p else n.left))  # Zio


def rotateLeft(x: Tree):
    y = x.right
    p = x.parent
    x.right = y.left  # II sottoalbero B diventa figlio destro di x
    if y.left != None:
        y.left.parent = x
    y.left = x  # x diventa figlio sinistro di y
    x.parent = y
    y.parent = p  # y diventa figlio di p
    if p != None:
        if p.left == x:
            p.left = y
        else:
            p.right = y
    return y


def rotateRight(x: Tree):
    y = x.left
    p = x.parent
    x.left = y.right  # II sottoalbero B diventa figlio sinistro di x
    if y.right != None:
        y.right.parent = x
    y.right = x  # x diventa figlio destro di y
    x.parent = y
    y.parent = p  # Change parent of y as parent of x
    if p != None:
        if p.right == x:
            p.right = y
        else:
            p.left = y
    return y
