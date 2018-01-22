#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################################################################
#sumaary and induction  
#1. there is a maximum number of edges between nodes n(n-1)/2
#2. there is a density of the edges, if the edges is k , then the density is k/(n(n-1)/2)
#3. if the node is fully connected, then the mininum color is number if the node in the graph node.count 
#4. rank the node by the total number of edges it has
#5. should start with the node which has the largest edges  
#1. the number of color cannot exceed n(n-1)/2, upper bound 
#####################################################################################################################


#from ortools.constraints_solver import pywrapcp
import networkx as nx 
import networkx.algorithms.approximation as apprx
import time 

def create_graph(node_count,edges):
    G = nx.Graph()
    nodes = list(range(node_count))
    G.add_nodes_from(nodes)
    G.add_edges_from(edges)
    return G

#sorte the node in the graph by it degree, how many node it connceted to  
def sorted_by_degree(graph):
    degrees = [(node, nx.degree(graph,node)) for node in graph]
    degrees = sorted(degrees, key = lambda t:-t[1])
    return degrees 

#def most_connected()
#def node_neighbour()

#cliques 
def preset(node, neighbors, presets):
    if not node in presets:
        values = sorted([presets[n] for n in neighbors if n in presets])
        value = 0
        if len(values) > 0:
            values = values + [max(values)+2] # last item is the forced max value +2
            for i in range(len(values)): # find an "emtpy slot"
                if values[i+1] - values[i] > 1:
                    value = values[i] + 1
                    break
        presets[node] = value

def preset_most_connected(graph, limit):
    degrees = sorted_by_degree(graph)

    #choose top limit connected 
    most_connected = degrees[:limit]
    
    presets = {}
    for node, degree in most_connected:
        neighbors = [n for n in graph[node]]
        print('neighbors for node', node, ':',neighbors)
        preset(node, neighbors, presets)
    
    return [(node, presets[node]) for node in presets]

def cliques_for_nodes(graph):
    return [apprx.max_clique(graph)]


#super greedy algorithms, where you only 
def super_greedy(graph,node_count):
    degrees_nodes = sorted_by_degree(graph)
    tabu = set()
    nodes = node_count
    solution = [-1]*nodes #initialize with -1 
    sloved_node = 0
    cur_color = 0 

    while(sloved_node < nodes):
        #print ("color: ", cur_color, "solved: ", sloved_node)
        for (node, degree) in degrees_nodes:
            if solution[node] == -1 and not node in tabu:
                solution[node] = cur_color
                tabu |= set(graph[node])
                sloved_node+=1
        tabu = set()        
        cur_color+=1

    print("color used in total:" , cur_color)
    return solution


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
    #every node has its own color
    #solution = range(0, node_count)

    #######################################my code start##############################################
    #create a undirected graph 
    graph_undi = create_graph(node_count,edges)
    sorted_graph = sorted_by_degree(graph_undi)
    #use super greedy algorithm
    #solution = super_greedy(graph_undi,node_count)
    
    #use conditioning programming 
    cliques_all = cliques_for_nodes(graph_undi)

    present = preset_most_connected(graph_undi,10)
    #######################################my code end##############################################

    # prepare the solution in the specified output format
    #output_data = str(node_count) + ' ' + str(0) + '\n'
    #output_data += ' '.join(map(str, solution))

    output_data = 'sorted_graph:', ' '.join(map(str, sorted_graph ))+ '\n'
    print (present)
    print("Get the cliques: ")
    print(cliques_all)

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

