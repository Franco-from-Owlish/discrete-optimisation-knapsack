#!/usr/bin/python
# -*- coding: utf-8 -*-

from solutions import (
    dynamic_programming,
    greedy,
    branch_and_bound,
)
from stubs import Item


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    item_count = int(first_line[0])
    capacity = int(first_line[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1])))

    optimised = False

    if capacity < 500000:
        taken, value = dynamic_programming(items, capacity)
        optimised = True
    elif item_count < 400:
        taken, value = branch_and_bound(items, capacity)
        optimised = True
    else:
        taken, value = greedy(items, capacity)
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(int(optimised)) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py '
              './data/ks_4_0)')

