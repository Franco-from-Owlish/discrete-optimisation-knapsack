from typing import List

import numpy as np

from stubs import Item


def dynamic_programming(items: List[Item], capacity: int) -> (List[Item], int):
    """
    Dynamic programming solution.
    @param items: The items that can be added
    @param capacity: Capacity of the knapsack
    @returns items, value The items taken and the total value
    """
    items_taken = [0] * len(items)
    value = 0

    o = np.ndarray((capacity + 1, len(items) + 1), dtype=int)

    def oracle(k: int, j: int) -> int:
        """
        Calculate o for a given capacity and item.
        @param k capacity
        @param j item index
        """
        if o[k][j] != 0:
            return o[k][j]
        if j == 0:
            return 0
        elif items[j - 1].weight <= k:
            not_taken = oracle(k, j - 1)
            taken = items[j - 1].value + oracle(k - items[j - 1].weight, j - 1)

            o_kj = max(taken, not_taken)
            o[k, j] = o_kj
            return o_kj
        else:
            return oracle(k, j - 1)

    for k in range(capacity + 1):
        value = oracle(k, len(items))

    k = capacity
    for j in range(len(items), 0, -1):
        if o[k, j] != o[k, j - 1]:
            items_taken[items[j-1].index] = 1
            k -= items[j - 1].weight

    # validate
    total_value = 0
    for idx, chosen in enumerate(items_taken):
        total_value += chosen * items[idx].value

    assert total_value == value

    return items_taken, value
