#!/usr/bin/env python
import argparse as ap
import math
import heapq as hq
import io


def load_maze_file(maze_filename):
    '''
    Simply read in the maze as 2-dim array.
    :param maze_filename:
    :return: a two-dim array containing the same characters as in the maze file.
    '''
    maze = []
    starting_node = None
    goal_node = None

    # we find M and C here already as we traverse the file anyway

    with io.open(maze_filename, 'r') as mazefile:
        row_counter = 0
        for row in mazefile:
            if not row.startswith("#"):
                row_list = row.strip().split(sep=',')
                maze.append(row_list)
                if "M" in row_list:
                    starting_node = (row_counter, row_list.index("M"))
                if "C" in row_list:
                    goal_node = (row_counter, row_list.index("C"))
                row_counter += 1

    if starting_node == None:
        print("Could not find Mouse in maze: " + maze_filename)
        exit(1)
    if goal_node == None:
        print("Could not find Cheese in maze: " + maze_filename)
        exit(1)

    return maze, starting_node, goal_node


def neighbors(node, maze):
    '''
    Considering walls and the outer frame, returns the possible neighbor nodes of a given coordinate.
    :param node: the node as (x,y) tuple/coordinate for which possible neighbors shall be determined
    :param maze: a two-dim array containing the characters as in the maze file.
    :return: list of neighbor coordinate pairs
    '''
    (x, y) = node
    neighbor_pos = []

    if x > 0 and maze[x-1][y] != 1:
        neighbor_pos.append((x-1, y))
    if y > 0 and maze[x][y-1] != 1:
        neighbor_pos.append((x, y-1))
    if 0 <= x < len(maze)-1 and maze[x+1][y] != 1:
        neighbor_pos.append((x+1, y))
    if 0 <= y < len(maze)-1 and maze[x][y+1] != 1:
        neighbor_pos.append((x, y+1))

    return neighbor_pos


def reconstruct_path(origins, node):
    '''
    Starting from node, reconstruct the chosen path 
    :param origins: a dict that stores for each node, the node from which it has been reached
    :param nod: the node from which the path shall be reconstructed
    '''
    path = [node]

    while node in origins.keys():
        node = origins[node]
        path.append(node)

    path.reverse()

    return path

def distance(node1, node2):
    (x1, y1) = node1
    (x2, y2) = node2
    return abs(x1-x2) + abs(y1-y2)

def dummy_heuristic(point, goal):
    (p_x, p_y) = point
    (g_x, g_y) = goal
    # manhatten distance
    return abs(p_x - g_x) + abs(p_y - g_y)


def astar_search(maze, start, goal, heuristic=dummy_heuristic):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :param heuristic: a function that takes two corrdinate pairs an returns an approx. distance
    :return: shortest path found ...list of coord. pairs
    '''
    set_of_points = {start}
    # initialize g values
    g_values = {}
    f_values = {}
    came_from = {}
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            point = (i, j)
            if maze[i][j] != 1:
                if point == start:
                    g_values.update({start: 0})
                    f_values.update({start: heuristic(start, goal)})
                else:
                    g_values.update({point: math.inf})
                    f_values.update({point: math.inf})

    # TODO fix infinite loop
    while set_of_points:
        minimal_f = math.inf
        for point in set_of_points:
            if f_values[point] < minimal_f:
                minimal_f = f_values[point]
                current = point
        set_of_points.remove(current)
        if current == goal:
            # success
            return reconstruct_path(came_from, goal)
        g_value = g_values[current]
        for neighbor in neighbors(current, maze):
            tentative_g_value = g_value + distance(current, neighbor)
            if tentative_g_value < g_values[neighbor]:
                # shorter path has been found!
                if neighbor not in set_of_points:
                    set_of_points.update({neighbor})
                came_from.update({neighbor: current})
                g_values[neighbor] = tentative_g_value
                f_values[neighbor] = tentative_g_value + heuristic(neighbor, goal)
    return []


def main():

    maze, starting_node, goal_node = load_maze_file("exercise.maze")

    maze = numeric_maze(maze)

    # 2. call AStar with different heuristics to see the effects ;)
    shortest_path = astar_search(maze, starting_node, goal_node, heuristic=dummy_heuristic)

    print("Path:")
    print(shortest_path)

    print_maze(maze, shortest_path)

def print_maze(maze, path=None):
    out = ""
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if path:
                if (i,j) in path:
                    out += " X "
                else:
                    out += " " + str(maze[i][j]) + " "
            else:
                out += " " + str(maze[i][j]) + " "
        out += "\n"
    print(out)


### Encodes the maze in numeric values for display
def numeric_maze(maze):
    '''
    :param maze: a two-dim array containing the numbers encoding the maze
    '''
    mazeviz = maze.copy()
    for row in range(len(mazeviz)):
        for cell in range(len(mazeviz[row])):
            if mazeviz[row][cell] == "E":
                mazeviz[row][cell] = 0
            if mazeviz[row][cell] == "W":
                mazeviz[row][cell] = 1
            if mazeviz[row][cell] == "M":
                mazeviz[row][cell] = 2
            if mazeviz[row][cell] == "C":
                mazeviz[row][cell] = 3
    return mazeviz


if __name__ == "__main__":
    main()
