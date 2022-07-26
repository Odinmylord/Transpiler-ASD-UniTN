import heapq
from collections import deque
from typing import Tuple

"""The GraphDict and Tree implementations inside this file are translated from Alberto Montresor site https://cricca.disi.unitn.it/montresor/
    the original work is available under license CC BY-SA 4.0"""


class ListOneBased(list):
    def __init__(self, *args):
        list.__init__(self, *args)

    def __getitem__(self, index):
        index = int(index)
        if index == 0:
            raise IndexError("Index 0 is not valid")
        val = list.__getitem__(self, index - 1)
        return val

    def __setitem__(self, index, value):
        index = int(index)
        list.__setitem__(self, index - 1, value)

    def __add__(self, other):
        return ListOneBased(list.__add__(self, other))


class GraphDict:
    """Implementation of a graph using a dictionary, taken from Alberto Montresor slides"""

    def __init__(self):
        self.nodes = {}
        # Aliases to stick to pseudo-code definitions
        self.insertNode = self.insert_node
        self.insertEdge = self.insert_edge
        self.V = self.vertices

    def size(self):
        return len(self.nodes)

    def vertices(self):
        return self.nodes.keys()

    def adj(self, u):
        """Takes a vertice and gives a back a list of the vertices adjacent to it
         or None if it isn't part of the graph"""
        edges_list = self.nodes.get(u, None)
        if edges_list is None:
            return None
        return set(edges_list)

    def insert_node(self, u):
        """Inserts a node, if it already is in the graph returns False"""
        if self.nodes.get(u, None) is not None:
            return False
        self.nodes[u] = {}
        return True

    def insert_edge(self, u, v, w=0):
        """Inserts an edge from the node u to the node v, is also possible to give the edge a weight"""
        self.insertNode(u)
        self.insertNode(v)
        edges_list = self.nodes.get(u, None)
        if edges_list is None:
            return False
        edges_list[v] = w
        return True


class Tree:
    """Implementation of a tree based with methods defined in Alberto Montresor's slide"""

    def __init__(self, v):
        self.parent = None
        self.left = self.right = None
        self.value = v
        self.insertLeft = self.insert_left
        self.insertRight = self.insert_right

    def insert_left(self, t):
        if self.left is None:
            t.parent = self
            self.left = t

    def insert_right(self, t):
        if self.right is None:
            t.parent = self
            self.right = t

    def delete_left(self):
        if self.left is not None:
            self.left.delete_left()
            self.left.delete_right()
            self.left = None

    def delete_right(self):
        if self.right is not None:
            self.right.delete_left()
            self.right.delete_right()
            self.right = None

    def __str__(self):
        return self.value


class Stack:

    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        return self.items.pop()

    def top(self):
        assert len(self.items) > 0
        return self.items[-1]

    def isEmpty(self) -> bool:
        return not self

    def size(self):
        return len(self.items)


class Queue(deque):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.enqueue = self.append
        self.dequeue = self.popleft

    def top(self):
        assert len(self) > 0
        return self[0]

    def isEmpty(self) -> bool:
        return not self

    def size(self):
        return len(self)


class MinPriorityQueue(list):
    """Implementation of the priority queue following Alberto Montresor slide methods.
        Note that the elements inside the queue are tuples of the type (priority, value)"""

    def __init__(self, size):
        # Takes size only for a possible implementation of the priority queue with fixed size not yet available
        super().__init__()
        heapq.heapify(self)
        self.deleteMin = self.delete_min
        self.insert = self.priority_insert

    def isEmpty(self) -> bool:
        return not self

    def min(self):
        assert not self.isEmpty()

        return heapq.nsmallest(1, self)

    def delete_min(self):
        assert not self.isEmpty()

        return heapq.heappop(self)

    def priority_insert(self, item: any, priority: int):
        element = (priority, item)
        heapq.heappush(self, element)
        return element

    def decrease(self, priority_item: Tuple[int, any], priority: int):
        assert not self.isEmpty()
        assert priority_item in self

        new_item = priority_item[1]
        self.remove(priority_item)
        heapq.heapify(self)
        return self.priority_insert(new_item, priority)
