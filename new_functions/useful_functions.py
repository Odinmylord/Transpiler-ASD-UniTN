def subtract_lists(l1, l2):
    return [x for x in set(l1) if x not in set(l2)]


def swap(list_to_swap, i: int, j: int):
    list_to_swap[i], list_to_swap[j] = list_to_swap[j], list_to_swap[i]


def copy(s):
    return s.copy()
