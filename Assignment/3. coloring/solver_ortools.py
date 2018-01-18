from ortools.constraint_solver import py


 #https://github.com/arielscarpinelli/discrete-optimization/blob/master/GraphColoring/solver.py
 #https://github.com/ungood/optimization/blob/master/coloring/solver.py
 #https://github.com/wypd/DiscreteOptimization



 range Slots = {0,n} #all the slot of the assemble line 
 range Configs = {...} #types of the car to produce (class1, class2, class3)
 range Options = {...} #different parts/options for the car, leather seat, moonroof, etc
 int demand[Configs] = .. #number of cars you need to produce for that type 
 int nbCars = sum(c in Config  s) demand[c]
 int lb[Options] = .. #lower bound of the options/ parts 
 int ub[Options] = .. # upper bound of the option / parts 
 int required[Options,Configs] = .. # require parts for a specific type of car 
 
 #decision variable
 var{int} line[Slots] in Configs  #for every slot of the assemnling line, what type of car you have to produce 
 #auxiliary variable 
 var(int) setup[Options,Slots] in 0,1 #setup[o,s]=1, if Slot[s] has been scheduled a car requiring Options[o]

 solve{
 	#demand constraints 
 	forall(c in Configs)
 		sum(s in Slots) (line[s] = c) = demand[c];

 	forall(s in Slots, o in Options)
 		setup[o,s] = required[o, line[s]];

 }

  