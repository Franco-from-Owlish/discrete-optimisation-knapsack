from typing import List

from stubs import Item


def greedy(items: List[Item], capacity: int) -> (List[Item], int):
    items.sort(key=lambda x : x.value/x.weight)

    value = 0
    weight = 0
    taken = [0]*len(items)
    
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight

    return taken, value
