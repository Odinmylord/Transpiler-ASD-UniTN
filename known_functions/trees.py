from Classes import Tree

"""The known_functions inside this file are translated from Alberto Montresor site 
https://cricca.disi.unitn.it/montresor/ the original work is available under license CC BY-SA 4.0 """


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


def insertNode(T: Tree, k, v):
    p = None  # Padre
    u = T
    while u is not None and u.key != k:  # Cerca posizione inserimento
        p = u
        u = (u.left if k < u.key else u.right)
    if u is not None and u.key == k:
        u.value = v  # Chiave già presente
    else:
        new = Tree(k, v)  # Crea un nodo coppia chiave-valore
        link(p, new, k)
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