from collections import namedtuple
from typing import Any

class Knapsack:
    def __init__(self, items: namedtuple, capacity: int) -> None:
        self._items = items
        self.capacity = capacity
        self.w = [0] * len(self._items)
        self.v = [0] * len(self._items)
        self.wj()

    def wj(self) -> None:
        for item in self._items:
            self.w[item.index] = item.weight
            self.v[item.index] = item.value

class Oracle:
    def __init__(self) -> None:
        self._o = [[0]]
        
    def __call__(self, k: int, j: int) -> int | None:
        try:
            return self._o[k][j]
        except IndexError:
            return None

        
oracle = Oracle()

def O(knapsack: Knapsack, k: int, j:int) -> int: 
    global oracle
    if j == 0:
        return 0
    elif knapsack.w[j] <= k:
        return max(
            oracle(k, j-1) or O(knapsack, k, j-1),
            knapsack.v[j] + oracle(k - knapsack.w[j], j) or O(knapsack, k - knapsack.w[j], j)
        )
    else:
        oracle(k, j-1) or O(knapsack, k, j-1)


def main(items: namedtuple, capacity: int):
    global oracle
    knapsack = Knapsack(items, capacity)
    oracle = Oracle()

