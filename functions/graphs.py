from Classes import ListOneBased, GraphDict


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
