from collections import namedtuple
from typing import List
import numpy as np

Item = namedtuple("Item", ['index', 'value', 'weight'])

def dynamic_programming(items: List[Item], capacity: int) -> (List[Item], int):
    """
    Dynamic programming solution.
    @param items The items that can be added
    @param apacity Capacity of the knapsack
    @retuns items, value The items taken and the total value
    """
    items_taken: List[Item] = []
    value = 0

    o = np.zeros(shape=(capacity, len(items)))

    def O(k: int, j: int) -> int:
        """
        Calculate o at a given capacity and item.
        @param k capacity
        @param j item index
        """
        if o[k][j] != 0:
            return o[k][j]
        if j == 0:
            return 0
        elif items[j].weight <= k:
            not_taken = O(k, j-1)
            taken = items[j].value + O(k - items[j].weight, j - 1)

            o[k][j-1] = not_taken
            o[k][j] = taken

            if taken > not_taken:
                items_taken.push(items[j])
                return taken
            return not_taken
        else:
            return O(k, j - 1)
        
    O(capacity, len(items))
    
    return items_taken, value