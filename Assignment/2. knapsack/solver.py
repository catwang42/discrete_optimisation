#!/usr/bin/python
# -*- coding: utf-8 -*-

from collections import namedtuple
import copy
import sys
import numpy as np


Item = namedtuple("Item", ['index', 'value', 'weight','density'])
value = 0 
weight = 0 
taken = []

def density(item):
    return 1.0* item.value/item.weight

##############################################
#Dynamic Programming 
#O(k,j) denote the optimal solution 
#############################################
def greedyAlgo(items,capacity):
    
    global value
    global weight
    global taken
            
    for item in items:
        if weight + item.weight <= capacity:
            taken[item.index] = 1
            value += item.value
            weight += item.weight
        

##########################################################################
#Branch and Bound
# 1.apply linear relaxation to find the optimal estimation on sub-problem 
# 2.use depth first search 
# 3.use good first search 
##########################################################################
bestValue = 0 
Node = namedtuple("Node",["bestEstimate","value","weight","taken","depth"])

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

#########################
#depth first searc 
#########################
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


#########################
#best first search 
#########################

def BFS(items,capacity,bfsQueue):
    
    global bestValue
    global taken
    
    #dequeue node with highest value
    while len(bfsQueue):
                
        maxBestEstimateIndex, maxBestEstimate = max(enumerate(bfsQueue),key=lambda x:x[1].bestEstimate)
        curNode = bfsQueue.pop(maxBestEstimateIndex) 
        curValue = curNode.value
        curWeight = curNode.weight
        depth = curNode.depth
        tmpTaken = curNode.taken
        
        bestEstimate = getEstimate(items, capacity, curValue, curWeight,depth)
        
        if curWeight > capacity or bestEstimate == 0 or bestValue >= bestEstimate:
            continue
        
        if depth < len(items) -1:
            
            bfsQueue.append(Node(getEstimate(items,capacity,curValue+items[depth+1].value,curWeight+items[depth+1].weight,depth+1),
                                 curValue+items[depth+1].value,
                                 curWeight+items[depth+1].weight,
                                 tmpTaken + (0b1 << depth + 1),depth+1))
            bfsQueue.append(Node(getEstimate(items,capacity,curValue,curWeight,depth+1),
                                 curValue,
                                 curWeight,
                                 tmpTaken,depth+1))
            
            continue
            
            
        elif depth == len(items)-1:
            if curValue > bestValue:
                bestValue = curValue
                taken=[int(bit,2) for bit in format(tmpTaken,"#0"+str(len(items)+2)+"b")[:1:-1]]
            
    else:
        return bestValue               



# linear relaxation
def bbAlgo(items,capacity,searchpattern):
    
    global value
    global weight 
    global taken
    
    print 'start branch and bounce Algorithm'
    
    if searchpattern == "dfs":
        tmpTaken = taken[:]
        
        tmpTaken[0] = 1
        left_val = DFS(items,capacity,tmpTaken,items[0].value,items[0].weight,0)
        
        tmpTaken[0] = 0    
        right_val = DFS(items,capacity,tmpTaken,0,0,0)
        
        value = max(left_val,right_val)
         
        
    if searchpattern == 'bfs':
        bfsQueue = []
        
        bfsQueue.append(Node(getEstimate(items,capacity,items[0].value,items[0].weight,0),
                             items[0].value,items[0].weight,0b1,0))
        bfsQueue.append(Node(getEstimate(items,capacity,0,0,0),
                             0,0,0b0,0))
        
        value = BFS(items,capacity,bfsQueue)
        
    return    

def chooseAlgo(items,capacity):
    
    global value
    global taken
    
    #greedyAlgo(items,capacity)
    bbAlgo(items,capacity,"dfs")
    #bbAlgo(items,capacity,"bfs")
   
    
    # prepare the solution in the specified output format
    output_data = str(value) + ' ' + str(1) + '\n'
    output_data += ' '.join(map(str, taken))
    return output_data

###################################################
# Validate the algorithms 
###################################################
def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    global taken
    # parse the input
    lines = input_data.split('\n')

    firstLine = lines[0].split()
    item_count = int(firstLine[0]) 
    capacity = int(firstLine[1])

    items = []

    for i in range(1, item_count+1):
        line = lines[i]
        parts = line.split()
        items.append(Item(i-1, int(parts[0]), int(parts[1]),float(parts[0])/float(parts[1])))


    #Code gose here 
    taken = [0]*len(items)
    return chooseAlgo(items,capacity)


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
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/ks_4_0)')

