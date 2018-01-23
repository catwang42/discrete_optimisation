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
from ortools.constraint_solver import pywrapcp
from ortools.constraint_solver import solver_parameters_pb2
import networkx as nx 
import networkx.algorithms.approximation as apxa
import time 

#created a undirected graph 
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

#for the most connected nodes, preset color for them 
#set limited manually, top 10
def most_connected_node(graph, limit):
    degrees = sorted_by_degree(graph)
    most_connected = degrees[: limit] 

    preset_colors = {}
    for node, degree in most_connected:
        neighbours = [n for n in graph[node]]
        setcolor(node, neighbours, preset_colors)
    return [(node, preset_colors[node]) for node in preset_colors]

#set color for the node with the highest degree
def setcolor(node,neighbours, preset_colors):
    if node not in preset_colors:
        #loops throught all the neighbours, see if any color in already in the preset color list
        values = sorted([preset_colors[n] for n in neighbours if n in preset_colors])
        value = 0  #preset color to 0 
        if len(values) > 0:
            values = values + [max(values)+2] #force the last item to be value+2, enable to find the slot
            for i in range(len(values)):
                if values[i+1] - values[i] > 1:
                    value = values[i] +1 
                    break 
        preset_colors[node] = value

#chekcing the cliques
def cliques_in_nodes(graph):
    return [apxa.max_clique(graph)]


def super_greedy(graph,node_count):
    #remove the top limited degree of nodes 
    #remove the ones in cliques
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

    #print("color used in total:" , cur_color)
    return solution
    #use this as upper bound 
    #return cur_color

def remap(nodes):
    color_map = {}
    current_color = -1
    result = []
    
    for node_color in nodes:
        # read the color of the map and conver it to number 
        if not node_color in color_map:
            current_color = current_color + 1
            color_map[node_color] = current_color
        result.append(color_map[node_color])
    
    return result

    cp_solve(edges, node_count, cliques, presets)

def cp_solver(edges, node_count, presets,lower,upper):
    '''
    #using constraint programming solver only 
    solver = pywrapcp.Solver("coloring")

    for edge in edges:
        solver.Add(node_color_arry[edge[0]] != node_color_arry[edge[1]])
    '''

    
    parameters = pywrapcp.Solver.DefaultSolverParameters()
    solver = pywrapcp.Solver('simple_CP', parameters)
    #colors = list(range(node_count))
    nodes = list(range(node_count))
    node_color_list = [solver.IntVar(0, node_count-1,'color%i' % i) for i in nodes] 
   
    # solver.Add(obj == max(node_color_list)+1)
    ###############constraints####################################################################
    #1.all the nodes in the cliques are different 

    #2.symemetrics breaking 
    #for node in nodes:  


    #3.different color in the edge list 
    for edge in edges:
        solver.Add(node_color_list[edge[0]] != node_color_list[edge[1]])

    #4.check the node's color are the same for the most connected nodes 
    for (node, value) in presets:
        solver.Add(node_color_list[node] == value)
    #################################################matrix dose not work################################################
    obj = solver.IntVar(lower, upper, "obj")
    solver.Add(obj == max(node_color_list)+1)
    objective = solver.Minimize(obj,1)

    solution = solver.Assignment()
    solution.AddObjective(obj)
    solution.Add(node_color_list)
    

    collector = solver.LastSolutionCollector(solution)
    #search_log = solver.SearchLog(100, obj)

    
    solver.Solve(solver.Phase(node_color_list,
                            solver.INT_VAR_SIMPLE,
                            solver.ASSIGN_MIN_VALUE),
                            [objective, collector])
    
    '''
    decision_builder = solver.Phase(node_color_list, 
                                    solver.CHOOSE_FIRST_UNBOUND,
                                    solver.ASSIGN_MIN_VALUE)
    collector = solver.LastSolutionCollector()
    collector.Add(node_color_list)
    collector.AddObjective(obj)
    solver.Solve(decision_builder,[objective,collector])
    '''
    print("cost:", collector.ObjectiveValue(0))
    print([(collector.Value(0, node_color_list[node])) for node in nodes])

    best_solution = collector.SolutionCount() - 1
    solution_node = [collector.Value(best_solution, node_color_list[node]) for node in nodes]


    return solution_node
    '''
    nodes_colors = [[solver.BoolVar('n%s_c%s' % (node,color))for color in colors] for node in nodes]
    obj = solver.IntVar(1, max_allowed_colors,'object') 
    for node in nodes:
        node_colors = nodes_colors[node]
        solver.Add(solver.Sum(node_colors) == 1 ) # one constraint 1 color per node
        for color in colors:
            solver.Add( obj >= color*node_colors[color] ) # symmetries breaking 


    for edge in edges:
        left = nodes_colors[edge[0]] 
        right = nodes_colors[edge[1]]
        for color in colors:
            solver.Add ( left[color] + right[color] <= 1  ) # Different colors for the linked node 

    
    for (node, value) in presets:
        for color in colors:
            solver.Add(nodes_colors[node][color] == (color == value)) 
            #check if the node are color the same as in the preset color 

    #################################################################################################

  
    db = solver.Phase(node_color_arry,
                      solver.CHOOSE_FIRST_UNBOUND,
                      solver.ASSIGN_MIN_VALUE)

    solver.NewSearch(db)
    solver.NextSolution()

    solution = [sum([color for color in colors if node_colors[color].Value()]) for node_colors in nodes_colors]

    solver.EndSearch()
    
  
    print ("WallTime:", solver.WallTime())
                           
    return remap(solution)
    #eturn nodes_colors
   '''

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
    #solution = range(0, node_count)
   
    #######################################my code start##############################################
    #create a undirected graph 
    graph_undi = create_graph(node_count,edges)
    #use super greedy algorithm
    solution_upper = super_greedy(graph_undi,node_count)
    upperbound = max(solution_upper) + 1   
    preset_colors = most_connected_node(graph_undi,10)
    #cliques = cliques_in_nodes(graph_undi)
    max_edges = node_count*(node_count-1)
    lowerbound = int(0.1*(edge_count/max_edges)*node_count)
     
    solution = cp_solver(edges, node_count, preset_colors,lowerbound,upperbound)

    #######################################my code end##############################################

    # prepare the solution in the specified output format
    output_data = str(node_count) + ' ' + str(0) + '\n'
    #output_data += ' '.join(map(str, solution))
    
    #print(preset_colors)
    
    print(lowerbound)
    print(upperbound)
    print(solution_upper)
    print("lala")
    print(max(solution))
    #return output_data


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

