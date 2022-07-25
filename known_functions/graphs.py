from Classes import ListOneBased, GraphDict
import new_functions.useful_functions

"""The known_functions inside this file are translated from Alberto Montresor site https://cricca.disi.unitn.it/montresor/
    the original work is available under license CC BY-SA 4.0"""

# Start of CC function for connected components
def cc(G: GraphDict):
    id = ListOneBased(["__" for _ in range(G.size())])
    for u in G.V():
        id[u] = 0
    counter = 0
    for u in G.V():
        if id[u] == 0:
            counter = counter + 1
            ccdfs(G, counter, u, id)
    return id


def ccdfs(G: GraphDict, counter: ListOneBased, u: int, id: ListOneBased):
    id[u] = counter
    for v in G.adj(u):
        if id[v] == 0:
            ccdfs(G, counter, v, id)
# end of CC function for connected components

# start of functions to find cycles inside graphs

def hasCycleRec(G: GraphDict, u: int, p: int, visited: ListOneBased):
    visited[u] = True
    for v in new_functions.useful_functions.subtract_lists(G.adj(u), [p]):
        if visited[v]:
            return True
        elif hasCycleRec(G, v, u, visited):
            return True
    return False


def hasCycle(G: GraphDict):
    visited = ListOneBased(["__" for _ in range(G.size() + 1)])
    for u in G.V():
        visited[u] = False
    for u in G.V():
        if not visited[u]:
            if hasCycleRec(G, u, None, visited):
                return True
    return False
# end of functions to find cycles inside graphs
