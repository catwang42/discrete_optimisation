#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################################################################
#sumaary and induction  
#1. there is a maximum number of edges between nodes n(n-1)/2
#2. there is a density of the edges, if the edges is k , then the density is k/(n(n-1)/2)
#3. if the node is fully connected, then the mininum color is number if the node in the graph node.count 
#4. rank the node by the total number of edges it has
#5. should start with the node which has the largest edges  
#
#
from ortools.constraints_col

########################################################################################################################

####################################################################################################################################
#1. the number of color cannot exceed n(n-1)/2, upper bound 
#2. the 
#3. 
####################################################################################################################################

################################################################################################################################
#decision variables 
#constraints / redundant constraints / global constraints / symmetrces breaking 
#objective functions 
################################################################################################################################


################################################################################################################################
#generic algorithms with local serach 
################################################################################################################################
Nodes 
int node_color 
list edges 
int index 

Goups 
int num_nodes 
int num_edges
int color_edge 



#read solution and convert color to number 
def readMap(nodes):
    color_map = []
    #color_num = 0
    color_num = -1
    result = []

    for node_color in nodes:
        if not node_color in color_map:
            color_num = color_num +1 
            color_map[node_color] = color_num
        result.append(color_map[node_color])

def cp_solver(edges, node_count):
    print("start solving the problem...")

    color_upper_bound = (node_count)*(node_count-1)/2
    colors = range(0, color_upper_bound)
    nodes = range(0,node_count)







def solve_it(input_data):
    # Modify this code to run your optimization algorithm

    # parse the input
    lines = input_data.split('\n')

    first_line = lines[0].split()
    node_count = int(first_line[0])
    edge_count = int(first_line[1])

    edges = []
    for i in range(1, edge_count + 1):
        line = lines[i]
        parts = line.split()
        edges.append((int(parts[0]), int(parts[1])))
    
    # build a trivial solution
    # every node has its own color
    solution = range(0, node_count)

    

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    output_data += ' '.join(map(str, solution))
    output_data += '\n' + ' '.join(str(x) for x in edges) 

    return output_data


import sys

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        file_location = sys.argv[1].strip()
        with open(file_location, 'r') as input_data_file:
            input_data = input_data_file.read()
        print(solve_it(input_data))
    else:
        print('This test requires an input file.  Please select one from the data directory. (i.e. python solver.py ./data/gc_4_1)')

