#!/usr/bin/env python
import argparse as ap
import math
import heapq as hq
import io

from numpy.random.mtrand import rand, random, randint


def load_maze_file(maze_filename):
    '''
    Simply read in the maze as 2-dim array.
    :param maze_filename:
    :return: a two-dim array containing the same characters as in the maze file.
    '''
    maze = []

    with io.open(maze_filename, 'r') as mazefile:
        for row in mazefile:
            if not row.startswith("#"):
                maze.append(row.strip().split(sep=','))

    return maze


def neighbors(node, maze):
    '''
    Considering walls and the outer frame, returns the possible neighbor nodes of a given coordinate.
    :param node: the node as (x,y) tuple/coordinate for which possible neighbors shall be determined
    :param maze: a two-dim array containing the characters as in the maze file.
    :return: list of neighbor coordinate pairs
    '''
    (x, y) = node
    neighbor_pos = []

    if x > 0 and maze[x - 1][y] != 'W':
        neighbor_pos.append((x - 1, y))
    if y > 0 and maze[x][y - 1] != 'W':
        neighbor_pos.append((x, y - 1))
    if 0 <= x < len(maze) - 1 and maze[x + 1][y] != 'W':
        neighbor_pos.append((x + 1, y))
    if 0 <= y < len(maze) - 1 and maze[x][y + 1] != 'W':
        neighbor_pos.append((x, y + 1))

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


def astar_search(maze, heuristic=dummyheuristic):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :param heuristic: a function that takes two corrdinate pairs an returns an approx. distance
    :return: shortest path found ...list of coord. pairs
    '''
    return []


def main():
    parser = ap.ArgumentParser(description="A Maze Solver based on AStar.")
    parser.add_argument("mazefile", type=str, help="filename of the the maze file to load")
    args = parser.parse_args()

    # 1. load the maze
    maze = load_maze_file(args.mazefile)

    # 2. call AStar with different heuristics to see the effects ;)
    shortest_path = astar_search(maze, heuristic=dummyheuristic)

    print("Path:")
    print(shortest_path)

    print_maze(maze, shortest_path)


def print_maze(maze, path=None):
    out = ""
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            if path:
                if (i, j) in path:
                    out += " X "
                else:
                    out += " " + str(maze[i][j]) + " "
            else:
                out += " " + str(maze[i][j]) + " "
        out += "\n"
    print(out)


if __name__ == "__main__":
    main()
