from collections import namedtuple
from typing import List
import numpy as np

from stubs import Item

def dynamic_programming(items: List[Item], capacity: int) -> (List[Item], int):
    """
    Dynamic programming solution.
    @param items The items that can be added
    @param apacity Capacity of the knapsack
    @retuns items, value The items taken and the total value
    """
    items_taken = [0]*len(items)
    value = 0

    o = {}

    def O(k: int, j: int) -> int:
        """
        Calculate o at a given capacity and item.
        @param k capacity
        @param j item index
        """
        if k in o and j in o[k]:
            return o[k][j]
        if j == 0:
            return 0
        elif items[j-1].weight <= k:
            not_taken = O(k, j-1)
            taken = items[j-1].value + O(k - items[j-1].weight, j - 1)

            if k not in o:
                o[k] = {}
            o[k][j-1] = not_taken
            o[k][j] = taken

            print(f"k={k}, j={j}, item={items[j-1]}, taken={taken}, not_taken={not_taken}")

            if taken >= not_taken:
                items_taken[items[j-1].index] = 1
                return taken
            return not_taken
        else:
            return O(k, j - 1)
        
    value = O(capacity, len(items))

    print(o)
    
    return items_taken, value