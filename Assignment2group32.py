""""
Maze search using Greedy Best First Search Algorithm
----------------------------------------------------
Configurations:
Map size - number of hexagonal coordinates
Rubbish Coordinates 
Number of rooms with rubbish
Disposal Coordinates
Number of rooms with disposal
Agent Bin Size or Weight limit
Rubbish Weight and Size
Agent Starting Coordinate
Generate Disposal and Rubbish incl. weight,size randomly across the map. 
Select clockwise or anticlockwise search (either may be more suited based on the scenario)

Further modifications possible to implement:
larger cost coverage - larger radius
Agent carries more than one bin

Features:
Agent can select from adjacent rubbish that fits among several

"""
import random
#generate the coordinates relative to a hexagonal coordinate mapping
#Initialize size and weight to 0, cost default 2. x,y,s,w,c,d 0=False 1=True for disposal
def generateHexagonCoordinates(length, height):
    coordinates = []
    counter = 0
    i = 0
    for x in range(0, length):
        if counter % 2 == 0 and counter != 0:
            i = i + 1
        for y in range((height - 1) - i, -1 - i, -1):
            coordinates.append([x, y, 0, 0, 2, 0])  
        counter += 1

    return coordinates

#fill in the rubbish in state_space_coordinates
def fill_size_weight(coordinates, x, y, size, weight):
    for i in range(len(coordinates)):
        if coordinates[i][0] == x and coordinates[i][1] == y:
            coordinates[i][2] = size
            coordinates[i][3] = weight
            break

    return coordinates
#set disposal nodes
def disposalCoordinates(coordinates, x, y):
    for i in range(len(coordinates)):
        if coordinates[i][0] == x and coordinates[i][1] == y:
            coordinates[i][5] = 1
            break
        
    return coordinates

#randomize rubbish incl size, weight and disposal coordinates 
def generateRandom(state_space_coordinates, num_disposal, num_rubbish, max_r_size, max_r_weight):
    
    dp = random.sample(state_space_coordinates, num_disposal)
    for i in dp:
        disposalCoordinates(state_space_coordinates, i[0], i[1])
    temp = [x for x in state_space_coordinates if x not in dp]
    rb = random.sample(temp, num_rubbish)
    for r in rb:
        fill_size_weight(state_space_coordinates, r[0], r[1], random.choice(range(1,max_r_size)), random.choice(range(1,max_r_weight)))
    return state_space_coordinates

#Inidivual coordinates stored as node
class Node:
  def __init__(self, x, y, parent_x = None, parent_y = None ):
    self.x = x
    self.y = y
    self.children = []
    self.weight = 0
    self.size = 0
    self.cost = 0
    
  def addChildren(self, children):
      self.children.extend(children)
  def set_size(self, size):
      self.size = size
  def set_weight(self, weight):
      self.weight = weight
  def set_cost(self, cost):
      self.cost = cost
        
#Agent class, carries bin of size and weight
class Agent:
    def __init__(self, name, bin_max_size, bin_max_weight):
        self.name = name
        self.bin_max_size = bin_max_size
        self.bin_max_weight = bin_max_weight
        self.binSize = []
        self.binWeight = []
        
    def addRubbishSize(self, size):
        self.binSize.append(size)
    def addRubbishWeight(self, weight):
        self.binWeight.append(weight)
    def remainingSize(self):
        rsize = self.bin_max_size - sum(self.binSize)
        return rsize
    def remainingWeight(self):
        rweight = self.bin_max_weight - sum(self.binWeight)
        return rweight
    def disposeRubbish(self):
        self.binSize.clear()
        self.binWeight.clear()
        
#Expand and return children of a node
def expandAndReturnChildren(state_space_coordinates, node):
    children = []
    
    for i in adjacentCoordinate(node.x,node.y):
        for z in state_space_coordinates:
            if i[0] == z[0] and i[1] == z[1]:
                #add the adhacent nodes to the children list
                children.append(Node(z[0],z[1], node.x, node.y))
                break
    for j in children: #set the nodes cost size and weight
        for [x,y,s,w,c,d] in state_space_coordinates: 
          if x == j.x and y == j.y: 
            j.set_cost(c)
            j.set_size(s)
            j.set_weight(w)
    return children
#set clockwise or anticlockwise rotation
def sequenceSelection(rotation, x, y):
    if rotation == "anticlockwise":
        return [x,y-1],[x+1,y-1],[x+1,y],[x,y+1],[x-1,y+1],[x-1,y]
    if rotation == "clockwise":
        return [x,y-1],[x-1,y],[x-1,y+1],[x,y+1],[x+1,y],[x+1,y-1]

#generate the coordinates in sequence 
# default - anticlockwise [down,down-right,up-right,up,up-left,down-left]
def adjacentCoordinate(x,y):
    adj = []
    adj.extend(sequenceSelection("anticlockwise", x, y))
    return adj
    
#function to generate map cost (rubbish search)
def generateMapCostRubbish(state_space_coordinates):
    #in place tweaking
    for i in state_space_coordinates:
        i[4] = 2
    for i in state_space_coordinates:
        if i[2] != 0 and i[3] != 0: #if node is rubbish
            i[4] = 0
            for [j,k] in adjacentCoordinate(i[0], i[1]): #loop thorugh adjacent nodes
                for l in (state_space_coordinates):
                    if l[0] == j and l[1] == k and l[4] != 0:
                        l[4] = 1
                        break
    return state_space_coordinates

#function to generate map cost (disposal search)
#when generate disposal search, rubbish cost stays 0 but disposal cost set to -1
def generateMapCostDisposal(state_space_coordinates):
    for i in state_space_coordinates:
        i[4] = 2
    for i in state_space_coordinates:
        if i[2] != 0 and i[3] != 0:   #rubbish cannot be a disposal node
            i[4] = 0
        elif i[5] == 1: #is disposal
            i[4] = -1
            for [j,k] in adjacentCoordinate(i[0], i[1]):
                for l in (state_space_coordinates):
                    if l[0] == j and l[1] == k and (l[4] != 0 and l[4] != -1): 
                        l[4] = 1
                        break
    return state_space_coordinates

#removes rubbish, set size and weight to 0.
def removeRubbish(state_space_coordinates, x ,y):
    for i in state_space_coordinates:
        if i[0] == x and i[1] == y:
            i[2] = 0
            i[3] = 0
            i[4] = 2
            break
"""
main function for greedy best first search
main goal: clear all rubbish in the given state space
sub goal 1: find rubbish
sub goal 2: find disposal
"""

def gbfs (state_space_coordinates, agent, initial_x, initial_y):
    #print("executed")
    frontier = []
    explored = []
    solution_path = []
    total_rubbish = []
    cost = 0
    steps = 0
    found_goal = False
    searching_for_rubbish = True
    searching_for_disposal = False
    frontier.append(Node(initial_x, initial_y, None))
    solution_path.append([initial_x,initial_y])
    print("###############################################################")
    print(agent.name, "has entered the maze at", initial_x, ",", initial_y)
    while not found_goal:      
        #goal test if all rubbish cleared
        if all(c[2] == 0 and c[3] == 0 for c in state_space_coordinates):
            found_goal = True
            break
        else:
            searching_for_rubbish = True
        while searching_for_rubbish or searching_for_disposal:
            
            if searching_for_rubbish == True:
                generateMapCostRubbish(state_space_coordinates)
                #print(agent.name," is looking for rubbish!!")
            if searching_for_disposal == True:
                generateMapCostDisposal(state_space_coordinates)
                #print(agent.name, "is now searching for a disposal!")
            
            children = expandAndReturnChildren(state_space_coordinates, frontier[0])
            frontier[0].addChildren(children)
            explored.append(frontier[0])
            print("                                                    ")
            print("Exploring node:", frontier[0].x,",", frontier[0].y)
            print("Cleared rubbish:", len(total_rubbish))
            est = int(((sum(agent.binSize)+sum(agent.binWeight))/(agent.bin_max_size+agent.bin_max_weight))*100)
            print("Rubbish Bin Capacity:", "[",est,"% ]")
            print("Remaining Bin Space:", "Size",agent.remainingSize(),"Weight", agent.remainingWeight())
            #print(state_space_coordinates)
            print("---------------------------------------")
            del frontier[0]
            
            #variables
            found_rubbish = False
            found_disposal = False
            rubbish_nodes = []
            smallest_value = None
            gbf = None
            
            for child in children:
                if not any((child.x == e.x and child.y == e.y) for e in explored): #avoid loopy
                    # greedy search. 
                    if smallest_value is None or child.cost < smallest_value:
                        
                        if child.cost == -1:
                            disposal_node = child
                            found_disposal = True
                            
                        if child.cost == 0:
                            rubbish_nodes.append(child)
                            found_rubbish = True
                            
                        elif child.cost > 0:
                            smallest_value = child.cost 
                            gbf = child
                            
                            
            if found_rubbish == True and found_disposal == False: #if there is rubbish
                for i,r in enumerate(rubbish_nodes):
                    print("Rubbish found! At coordinate", r.x,",", r.y)
                    if r.size <= agent.remainingSize()  and r.weight <= agent.remainingWeight():
                        
                        #pickup rubbish
                        agent.addRubbishSize(r.size)
                        agent.addRubbishWeight(r.weight)
                        print("Rubbish of Size", r.size, "m^3 and Weight", r.weight, "kg collected!" )
                        total_rubbish.append([r.size, r.weight])
                        #clear rubbish from coordinates
                        removeRubbish(state_space_coordinates, r.x, r.y)
                        searching_for_disposal = True
                        searching_for_rubbish = False
                        solution_path.append([r.x,r.y])
                        frontier.append(r) 
                        explored.clear()
                        steps += 1
                        print(agent.name, "needs to find a disposal now!")
                        break
                    else:
                        #case where rubbish does not fit
                        print("Does not fit the bin! Poor", agent.name, "!")
                        if gbf is not None:
                            if i == len(rubbish_nodes) - 1 and r == rubbish_nodes[i]:
                                solution_path.append([gbf.x, gbf.y])
                                frontier.append(gbf)
                                steps += 1
                        #case where ronny is cornered by trash that he cant carry (stuck). rare scenario but it happens
                        if gbf is None:
                            frontier.append(explored[-1])
                            explored.clear()
            #greedy expand. (not rubbish or diisposal)
            elif found_rubbish == False and found_disposal == False:
                
                if gbf is not None:
                    if gbf.cost == 1:
                        print(agent.name, "smells something nearby!! Moving closer...")
                    else:
                        print("No rubbish or disposal nearby,", agent.name,"moves to the next best room!")
                    cost += gbf.cost #stores the cost (heuristic summation)
                    solution_path.append([gbf.x,gbf.y])
                    frontier.append(gbf)
                    steps += 1
                elif gbf is None: #scenario where agent searched all surroundings( all in explored list)
                    print("Ronny has explored all around him, time to try again")
                    frontier.append(explored[-1])
                    explored.clear()
            # agent found a disposal
            elif found_disposal == True:
                print("Disposal Found at", disposal_node.x,",", disposal_node.y, "!")
                solution_path.append([disposal_node.x,disposal_node.y])
                print("Emptied rubbish in bin of Size", sum(agent.binSize), "m^3 and Weight", sum(agent.binWeight),"kg")
                print(agent.name, "looks for more rubbish!")
                agent.disposeRubbish()
                frontier.append(disposal_node)
                searching_for_disposal = False
                explored.clear()
                steps += 1
                
    print("")
    print(agent.name, "has cleared all the rubbish!! Hooray")
    print("################################################")
    return solution_path, total_rubbish, cost, steps
            

#create the state_space, set size (length, height)
state_space_coordinates = generateHexagonCoordinates(9, 6)
#manually set rubbish and disposal
#set rubbish
fill_size_weight(state_space_coordinates, 0, 0, 1, 10)
fill_size_weight(state_space_coordinates, 1, 2, 3, 30)
fill_size_weight(state_space_coordinates, 2, 2, 1, 5)
fill_size_weight(state_space_coordinates, 3, 3, 1, 5)
fill_size_weight(state_space_coordinates, 3, 0, 3, 5)
fill_size_weight(state_space_coordinates, 4, 1, 2, 10)
fill_size_weight(state_space_coordinates, 4, -1, 1, 20)
fill_size_weight(state_space_coordinates, 6, 1, 2, 10)
fill_size_weight(state_space_coordinates, 6, -2, 2, 5)
fill_size_weight(state_space_coordinates, 7, 2, 1, 30)
fill_size_weight(state_space_coordinates, 7, -1, 2, 20)
fill_size_weight(state_space_coordinates, 8, 0, 3, 10)
#set disposal
disposalCoordinates(state_space_coordinates, 2, -1 )
disposalCoordinates(state_space_coordinates, 8, -4)
disposalCoordinates(state_space_coordinates, 5, 3)

#randomize disposal, rubbish (coordinates, no.disposal, no.rubbish, rubbish size, rubbish weight)
#generateRandom(state_space_coordinates, 5, 5, 4, 30)

#create agent object with name, bin size limit, bin weight limit
agent = Agent("Ronny",5,40)
#initalize starting coordinates
initial_x = 0
initial_y = 5
#return and print solution
[solution_path, total_rubbish, cost, steps] = gbfs(state_space_coordinates, agent, initial_x, initial_y)
print("")
print("Solution path: ", solution_path)
print("")
print("Rubbish disposed [size,weight] in sequence: ", total_rubbish)
print("Number of rubbish: ", len(total_rubbish))
print("")
print("Total cost: ", cost)
print("Total Steps: ", steps)
           