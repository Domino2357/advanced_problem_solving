#!/usr/bin/env python
from copy import *

import argparse as ap
import math
import heapq as hq
import io
# to start with, we will need matplotlib.pyplot
import numpy as np
from matplotlib import animation
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider
import random

from numpy.random.mtrand import rand


paths = dict()

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


def find_intital_path(maze, starting_node, goal_node, extend=False):
    '''
    Considering walls and the outer frame, returns the possible neighbour nodes of a given coordinate.
    :param node: the node as (x,y) tuple/coordinate for which possible neighbours shall be determined
    :param maze: a two-dim array containing the characters as in the maze file.
    :return: list of neighbour coordinate pairs
    '''
    (s_x,s_y)=starting_node
    (g_x,g_y)=goal_node
    global paths
    
    xdir = 1 if (g_x - s_x > 0) else -1
    ydir = 1 if (g_y - s_y > 0) else -1

    if extend:
        if 0 <= s_x-xdir < len(maze[0]) and 0 <= s_y-ydir < len(maze[0]):
            starting_node = random.choice([(s_x-xdir, s_y), (s_x, s_y-ydir)])
    n_path = [starting_node]
    loop = True

    while loop:
        (c_x, c_y) = n_path[len(n_path)-1]
        opts = []
        if c_x != g_x:
            opts.append((c_x+xdir, c_y))
        
        if c_y != g_y:
            opts.append((c_x, c_y+ydir))
                
        if opts:
            n_path.append(random.choice(opts))
        else: 
            loop = False
    return n_path


def path_cost(maze, path):
    cost = 0
    number_of_walls = 0
    for point in path:
        x, y = point
        cost += 1
        if maze[x][y] == 1:
            number_of_walls += 1
            cost += len(maze)*len(maze)/number_of_walls
    return cost


def find_neighbor(maze, work_path, len_new_path, extend=False):
    starting_index = random.randint(0, len(work_path) - 1 - len_new_path)
    end_index = starting_index + len_new_path
    new_path_piece = find_intital_path(maze, work_path[starting_index], work_path[end_index], extend)
    if not len(new_path_piece) == len_new_path:
        new_path = [x for x in work_path[0:starting_index]] + new_path_piece + [x for x in work_path[end_index+1:]]
    else:
        new_path = [x for x in work_path[0:starting_index+1]] + new_path_piece + [x for x in work_path[end_index+1:]]
    return new_path


def update_T(param_T, t):
    return param_T/(t+1)


def sim_annealing_search(maze, starting_node, goal_node, param_T=10):
    '''
    :param maze: a two-dim array containing the characters as in the maze file.
    :param heuristic: a function that takes two corrdinate pairs an returns an approx. distance
    :return: shortest path found ...list of coord. pairs
    '''
    num_generations = 0
    final_path = []
    while num_generations < 30:
        path = find_intital_path(maze, starting_node, goal_node)
        cost = path_cost(maze, path)
        check_for_walls = 5
        for i in range(500):
            extend = False
            if i%check_for_walls == 0 and i != 0:
                # hasn't reached Manhatten distance, i.e., shotest path yet '
                if cost > len(maze)+len(maze):
                    extend = True
                    check_for_walls = check_for_walls/2
            candidate = find_neighbor(maze, path, 4, extend)
            new_cost = path_cost(maze, candidate)

            if cost > new_cost:
                path = candidate
                cost = new_cost
            if param_T != 0:
                if random.uniform(0, 1) < math.exp((cost - new_cost) / param_T):
                    path = candidate
                    cost = new_cost
            param_T = update_T(param_T, i)
        if num_generations == 0:
            final_path = path
        else:
            if path_cost(maze, final_path) > cost:
                final_path = path
        num_generations +=1
        param_T = 10
    print(final_path)
    print(cost)
    
def main():
    # Start from your command line:
    # C:/ProgramData/Anaconda3/python.exe "c:/Users/marcr/Desktop/Master 1/APSS/Exercises/Exercise 1/astar-maze-template.py" hard.maze
    # parser = ap.ArgumentParser(description="A Maze Solver based on AStar.")
    # parser.add_argument("mazefile", type=str, help="filename of the the maze file to load")
    # args = parser.parse_args()

    # 1. load the maze
    maze, starting_node, goal_node = load_maze_file("hard.maze")
    
    maze = numeric_maze(maze)

    # 2. call simulated annealing
    sim_annealing_search(maze, starting_node, goal_node)


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

### Combines a maze with a the path in the val position
def maze_with_path(maze,path_key):
    '''
    :param maze: a two-dim array containing the numbers encoding the maze
    :param path_key: the key of the desired path in the global paths variable
    '''
    mazeviz = maze.copy()    
    ## reset maze
    for row in range(len(mazeviz)):
        for cell in range(len(mazeviz[row])):
            if mazeviz[row][cell] == 4:
                mazeviz[row][cell] = 0
            if mazeviz[row][cell] == 5:
                mazeviz[row][cell] = 1

    ## print current path
    for row in range(len(mazeviz)):
        for cell in range(len(mazeviz[row])):
            if mazeviz[row][cell] == 0:
                if paths[path_key]:
                    if (row,cell) in paths[path_key]:
                        mazeviz[row][cell] = 4
            if mazeviz[row][cell] == 1:
                if paths[path_key] and (row,cell) in paths[path_key]:
                    mazeviz[row][cell] = 5
    return mazeviz


### Visualizes the global paths on the maze
def viz_maze(maze,size):
    '''
    :param maze: a two-dim array containing the numbers encoding the maze
    :param size: the number of iterations to display
    '''
   
    plt.rcParams["figure.figsize"] = [7.50, 3.50]
    plt.rcParams["figure.autolayout"] = True
    fig, ax = plt.subplots()
    img = ax.imshow(numeric_maze(maze))

    
    axcolor = 'yellow'
    ax_slider = plt.axes([0.20, 0.01, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(ax_slider, 'Slide->', 1, size, valstep=1)

    def generate_path(val):
        mazeviz = maze_with_path(maze,val)
        ax.imshow(mazeviz)
        fig.canvas.draw_idle()
    slider.on_changed(generate_path)
    plt.show()


if __name__ == "__main__":
    main()


# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# import time

# fig = plt.figure()
# ax1 = fig.add_subplot(1,1,1)

# def animate(i):
#     pullData = open("sampleText.txt","r").read()
#     dataArray = pullData.split('\n')
#     xar = []
#     yar = []
#     for eachLine in dataArray:
#         if len(eachLine)>1:
#             x,y = eachLine.split(',')
#             xar.append(int(x))
#             yar.append(int(y))
#     ax1.clear()
#     ax1.plot(xar,yar)
# ani = animation.FuncAnimation(fig, animate, interval=1000)
# plt.show()


