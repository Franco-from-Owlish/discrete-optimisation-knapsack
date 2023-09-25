from typing import List

from stubs import Item


class Node:
    def __init__(
            self,
            remaining_capacity: int,
            total_value: int,
            estimate: int,
            item_index: int
    ):
        self.left = None
        self.right = None
        self.remaining_capacity = remaining_capacity
        self.total_value = total_value
        self.estimate = estimate
        self.index = item_index

    def set_children(self, item: Item):
        self.left = Node(
            remaining_capacity=self.remaining_capacity-item.weight,
            total_value=self.total_value+item.value,
            estimate=self.estimate,
            item_index=item.index
        )
        self.right = Node(
            remaining_capacity=self.remaining_capacity,
            total_value=self.total_value,
            estimate=self.estimate-item.value,
            item_index=item.index
        )

    def end(self, best_estimate: int) -> bool:
        return self.remaining_capacity < 0 or self.estimate < best_estimate


def linear_relaxation_bound(items: List[Item], capacity: int) -> int:
    items.sort(key=lambda x: x.value / x.weight)
    bound = 0
    remaining_capacity = capacity
    for item in items:
        if item.weight < remaining_capacity:
            bound += item.value
            remaining_capacity -= item.weight
        else:
            bound += item.value * remaining_capacity/item.weight
            break

    return bound


def bound_and_bound(items: List[Item], capacity: int) -> (List[int], int):
    bound = linear_relaxation_bound(items, capacity)
    root = Node(
        remaining_capacity=capacity,
        total_value=0,
        estimate=bound,
        item_index=0
    )

    def create_tree(node: Node, index: int):
        node.set_children(items[index])
        if index < len(items):
            node.left.set_children(items[index+1])
            node.right.set_children(items[index+1])

    def dept_first(node):
        if node and not node.end(bound):
            dept_first(node.left)
            dept_first(node.right)


