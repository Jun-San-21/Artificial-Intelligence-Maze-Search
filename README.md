
# MazeClearing: Greedy Best-First Search for Clearing Rubbish
The project aims to clear out rubbish of different size and weight from various rooms in an optimal and efficient manner using the Greedy Best-First Search Algorithm. The agent is given a rubbish bin with specific size and weight limitations. The goal is to find the most efficient path to visit all rooms with rubbish and dipose of them at designated disposal rooms. The agents movement is guided with a heuristic-based approach, prioritizing steps that appear closer to a goal. The Greedy Best-First search algorithm allows the agent to find the most optimal path while adhering to the constraints. 

## Installation
1. download the script file
2. run the file on any IDE of choice

# Execution

**Step 1: Initialize the hexagonal map dimension**

The function ```generateHexagonCoordinates(length,height)``` generates coordinates given following a hexagonal map plotting scheme. The function takes input paramenters length and height which can be adjusted to desired map dimension. 

The returned value of the function should then be stored into the ```state_space_coordinates``` variable. 

Note: the list returns a list of coordinate values with additional integer values where an element for an x, y coordinate will look like ```[x, y, 0, 0, 2, 0]``` by default. The values are represented as (x coordinate, y coordinate, rubbish size, rubbish weight, cost, disposal). These values will be adjusted later on.

**Step 2: Set coordinates of rubbish**

To add rubbish into the set of coordinates, you must first determine the size and weight values of the rubbish. The units are in m^3 and kg respectively. As long as a state_space_coordinate holds a size and weight value, it is considered a rubbish.

To add size and weight values to coordinates:

Call the ```fill_size_weight(coordinates, x, y, size, weight)``` function. To set the parameter values:

- *coordinates* - input state_space_coordinate
- *x* - the x coordinate of where the rubbish lies
- *y* - the y coordinate of where the rubbish lies
- *size* - size of the rubbish in m^3
- *weight* - weight of the rubbish in kg

The function can be called as many times as desired with different parameter values to add multiple and various rubbish values. The function updates the values in the ```state_space_coordinates``` as mentioned in Step 1. 

**Step 3: Set coordinates of disposals**

Simmilar to adding rubbish, for disposals,
call the ```disposalCoordinates(coordinates, x, y)``` function. Since disposals have no value,
set ```coordinates``` as ```state_space_coordinates``` and insert ```x``` coordinate and ```y``` coordinate of where you would like the disposal to be. 

*Note: Disposals cannot have the same coordinates as rubbish.*

**Step 4: Create the Agent Object**

To create your agent, store
```Agent(name, bin_max_size, bin_max_weight)```
into a variable. 

- *name* - the agents name of choice
- *bin_max_size* - the size limit the agents bin may carry
- *bin_max_weight* - the weight limit the agents bin may carry

*Note: Make sure no size and weight value of a rubbish created earlier does not exceed the set agent ```bin_max_size``` and ```bin_max_weight```
as the algorithm may not run properly.* 

**Step 5: Set the starting coordinate of the agent**

To set the starting point of the agent, store the x integer and y integer coordinate respectively into variable ```initial_x``` and ```initial_y```.

**Step 6: Call the main function**

Now that all values have been set, call the main function; ```gbfs(state_space_coordinates, agent, initial_x, initial_y)``` where

- *state_space_coordinates* - the state_space_coordinates after rubbish and disposals have been set. 
- *agent* - the agent object 
- *initial_x* - starting x coordinate of agent
- *initial_y* - starting y coordinate of agent

**Step 7: Run the script**

Once the script is executed, the console will display the output for each step that indicates:
- Exploring Node
- Cleared Rubbish
- Rubbish Bin Capacity
- Remaining Bin Space
- Description 

and the algorithm will return

- Solution path
- Rubbish disposed in sequence
- Number of rubbish
- Total cost
- Total steps

## Additional Information

**Alternative approach**

Instead of manually setting every coordinate with rubbish and disposal including the size and weight values, these values may be randomly generated if you would like observe how the algorithm solves for different occasions and scenarios. 

To do this, call the ```generateRandom(state_space_coordinates, num_disposal, num_rubbish, max_r_size, max_r_weight)``` function,

- *state_space_coordinate* - the default state space coordinate after calling *generateHexagonCoordinates()*
- *num_disposal* - number of disposals
- *num_rubbish* - number of rubbish
- *max_r_size* - maximum rubbish size
- *max_r_weight* - maximum rubbish weight

These will randomize the placement of disposals and rubbish along with the rubbish size and weight in the ```state_space_coordinates``` list. 

**Configurations**

The list of user configurations for the algorithm include

- Map size - number of hexagonal coordinates
- Rubbish Coordinates 
- Number of rooms with rubbish
- Disposal Coordinates
- Number of rooms with disposal
- Agent Bin Size or Weight limit
- Rubbish Weight and Size
- Agent Starting Coordinate
- Generate Disposal and Rubbish incl. weight,size randomly across the map. 
- Select clockwise or anticlockwise search (either may be more suited based on the scenario):

By default, the agent expands in an anticlockwise sequence rotation of DOWN, DOWN-RIGHT, UP-RIGHT, UP, UP-LEFT, DOWN-LEFT.
To change the search in a clockwise sequence, 
```
def adjacentCoordinate(x,y):
    adj = []
    adj.extend(sequenceSelection("anticlockwise", x, y))
    return adj
```
set the "anticlockwise" value to "clockwise" in this function. The agent will then search in the clockwise sequence as the algorithm may benefit from one or the other. 

**Default values for the assignment**

```
state_space_coordinates = generateHexagonCoordinates(9, 6)
```

```
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
disposalCoordinates(state_space_coordinates, 2, -1 )
disposalCoordinates(state_space_coordinates, 8, -4)
disposalCoordinates(state_space_coordinates, 5, 3)
```
```agent = Agent("Ronny",5,40)```

```initial_x = 0```

```initial_y = 5```

### Credits

Team Members:

Alkin Wong

## Authors

Tan Jun San







