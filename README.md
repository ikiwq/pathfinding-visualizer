# PathfindingVisualizer
A simple tool built in python for visualizing pathfinding algorithms

#### Choose between A* star algorithm and dijkstra's algorithm.
<img src="https://github.com/ikiwq/pathfinding-visualizer/assets/110495658/9ff09939-2985-405a-91c7-44664d52ff75" width="600">

Select the algorithm by using the up and down arrow key and then press enter.

#### Place the nodes and watch the algorithm find a solution.
<img src="https://github.com/ikiwq/pathfinding-visualizer/assets/110495658/f4001e96-a1cc-4ac4-af4e-6485d0cb4991" width="600">

You can place a start node, an end node and a barrier node with the left click.
You can then press space to start the visualization.
When the visualization has run, you can press space again to return to the main menu.

## Supported Algorithms
The pathfinding visualizer can currently use these algorithms:
1. A* is a pathfinding algorithm that incorporates heuristics, allowing it to efficiently find the shortest path in a graph while considering both the cost to reach a node and an estimated cost to the goal.
2. Dijkstra's algorithm is a classic pathfinding method that systematically explores nodes in a graph based on their distance from the start point.

## Requirements
- Python 3.10 and above. Download python from the [official website](https://www.python.org/).
- Pygame. Install Pygame by running 'pip install pygame' in your terminal.

## Usage
Run in your terminal

    python main.py
