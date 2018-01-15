#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import copy
import sys
import numpy as np


Item = namedtuple("Item", ['index', 'value', 'weight'])
value = 0 
weight = 0 
taken = []

def density(item):
    return 1.0* item.value/item.weight


##############################################
#Branch and Bound
#############################################
bestValue = 0 
Treenode = namedtuple("Item", ['bestEstimate', 'value', 'weight', 'taken','depth'])

def getEstimate(items,capacity,curVal,curWeight,depth):
    bestEstimate = 0
    bestTempVal = 0 

    if depth < len(items)-1:
        tempItems = sorted(items[depth+1:],key = density,reverse = True)
        for index, item in enumerate(tempItems,start=0):
            if curWeight + item.weight <= capacity:
                bestTempVal += item.value 
                curWeight += item.weight
            else:
                break
        
        bestTempVal += (1.0(capacity - curWeight)/tempItems[index].weight*tempItems[index].value)
        bestEstimate = curVal + bestTempVal
    else: 
        bestEstimate = curVal

    return bestEstimate

#depth first 
def DFS(items,capacity,tempTaken,curVal,curWeight,depth):
    global bestValue
    global taken 

    if curWeight > capacity:
        return 0 

    #get best estimation for the highest possible value 
    #use linear relaxation 
    if bestValue >= getEstimate(items,capacity,curVal,curWeight,depth):
        return 0

    if depth <= len(items) -1:
        #take the left path 
        tempTaken[depth+1] = 1
        #increment the current value and weight 
        leftValue = DFS(items, capacity, tempTaken, 
                        curVal+items[depth+1].value,curWeight+items[depth+1].weight,
                        depth+1)

        tempTaken[depth+1] = 0 
        rightValue = DFS(items,capacity,tempTaken,curWeight,curWeight,depth+1)

    elif depth == len(item)-1:
        if curVal > bestValue:
            bestValue = curVal
            taken = tempTaken[:]
        return curVal







#best first 
def BFS(item,capacity,tempTaken,curVal,curWeight,depth):


#least discrepancy 

###################################################
# Validate the algorithms 
###################################################
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
        items.append(Item(i-1, int(parts[0]), int(parts[1])))


    #Code gose here 


    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, best_taken))
    return output_data





if __name__ == '__main__':
    #import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        if file_location == './data/ks_10000_0':
            print(file_location," name", type(file_location))
        else:
            print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

