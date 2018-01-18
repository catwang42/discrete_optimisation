#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import copy
import sys

#add performance ratio to rank the list 
Item = namedtuple("Item", ['index', 'value', 'weight', 'ratio'])

#set recursive limitation 
sys.setrecursionlimit(100000)


def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0]) 
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]), float(parts[0])/float(parts[1])))

    value = 0
    weight = 0
    taken = [0]*len(items)    
  
    #my code 
    items = sorted(items, key=lambda item:item.ratio, reverse=True)
    taken = [0] * len(items)  # it takes items in-order until the knapsack is full

    ###############################################################################################
    # parameter for the DFS
    #node -> node starting from level 0 
    #depth -> the possible depth of the tree, the total number of item you need to search 
    #taken -> how many items are already in the bag 
    #value -> current value in the bag 
    #room -> the capability/room left in the bag 
    #items -> data input 
    #max_value -> optimal estimation 
    #best_taklen-> what to take into the bag 
    #use linear relaxation to get the optimistic estimation of the current bag estimate -= float(weight_sum - room) / last_weight * last_value
    ##############################################################################################
    (value, best_taken) = depthFirst(0, item_count, taken, 0, capacity, items, 0, [])
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, best_taken))
    return output_data


def depthFirst(node, depth, taken, value, room, items, max_value, best_taken):
    """
    :rtype : object
    """
    
    if node == depth:
        if value > max_value:
            max_value = value
            best_taken = copy.copy(taken)
        return max_value, best_taken
   
    
    estimate = value
    weight_sum = 0
    last_weight = 0
    last_value = 0
    for i in range(node, depth):
        if weight_sum < room:
            weight_sum += items[i].weight
            last_weight = items[i].weight
            estimate += items[i].value
            last_value = items[i].value
        else:
            break
            
    if last_weight > 0:
        estimate -= float(weight_sum - room) / last_weight * last_value
    else:
        estimate -= weight_sum

    if estimate <= max_value:
        return max_value, best_taken

    if node < depth:
        # go left
        taken[items[node].index] = 1
        value += items[node].value
        room -= items[node].weight
        if room >= 0:
            (max_value, best_taken) = depthFirst(node + 1, depth, taken, value, room, items, max_value,
                                                 best_taken)
        # backtracking
        taken[items[node].index] = 0
        value -= items[node].value
        room += items[node].weight
        # go right
        (max_value, best_taken) = depthFirst(node + 1, depth, taken, value, room, items, max_value,
                                             best_taken)
    return max_value, best_taken



if __name__ == '__main__':
    #import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

