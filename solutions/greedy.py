from typing import List

from solutions import base
from stubs import Item


def greedy(items: List[Item], capacity: int) -> (List[Item], int):
    items.sort(key=lambda x: x.value/x.weight, reverse=True)

    return base(items, capacity)
