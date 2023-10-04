from typing import List, Optional, TypeVar

from stubs import Item

TNode = TypeVar("TNode", bound="Node")


class Node:
    def __init__(
            self,
            remaining_capacity: int,
            total_value: int,
            estimate: int,
            item_index: int,
            taken: bool = False,
            parent: TNode = None,
    ):
        self.left = None
        self.right = None
        self.remaining_capacity = remaining_capacity
        self.total_value = total_value
        self.estimate = estimate
        self.index = item_index
        self.parent = parent
        self.taken = taken

    def set_children(self, item: Item, consumed_capacity: Optional[float] = None):
        self.left = Node(
            remaining_capacity=self.remaining_capacity - item.weight,
            total_value=self.total_value + item.value,
            estimate=self.estimate,
            item_index=item.index + 1,
            taken=True
        )
        self.right = Node(
            remaining_capacity=self.remaining_capacity,
            total_value=self.total_value,
            estimate=self.estimate - (item.value
                                      if consumed_capacity is None
                                      else consumed_capacity),
            item_index=item.index + 1,
            taken=False
        )

    def end(self, best_estimate: int) -> bool:
        if self.remaining_capacity < 0:
            return True
        return self.estimate < best_estimate


def linear_relaxation_bound(items: List[Item], capacity: int) -> (int, List[float]):
    items = items.copy()
    capacity_consumed = [0.0] * len(items)
    items.sort(key=lambda x: x.value / x.weight, reverse=True)
    bound = 0
    remaining_capacity = capacity
    for item in items:
        if item.weight < remaining_capacity:
            bound += item.value
            remaining_capacity -= item.weight
            capacity_consumed[item.index] = item.value
        else:
            value = item.value * remaining_capacity / item.weight
            bound += value
            capacity_consumed[item.index] = value
            break

    return bound, capacity_consumed


def branch_and_bound(items: List[Item], capacity: int) -> (List[int], int):
    value = 0
    items_taken = [0] * len(items)
    bound, consumed_capacities = linear_relaxation_bound(items, capacity)
    root = Node(
        remaining_capacity=capacity,
        total_value=0,
        estimate=bound,
        item_index=0
    )
    highest_value_node = root

    def dept_first(node):
        nonlocal value, highest_value_node  # bind to outer scope
        if not node:
            return

        if not node.end(value):
            value = max(node.total_value, value)
            if node.total_value > highest_value_node.total_value:
                highest_value_node = node
                items_taken[highest_value_node.index] = int(highest_value_node.taken)
            if node.left is None:
                node.set_children(
                    items[node.index],
                    consumed_capacity=consumed_capacities[items[node.index].index]
                )
            dept_first(node.left)
            dept_first(node.right)

    dept_first(root)

    return items_taken, highest_value_node.total_value
