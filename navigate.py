from move_wrapper import move_to_coordinate
import copy
from grid import grid
import matplotlib.pyplot as plt
import numpy as np
import argparse
import time
from de_res import de_res
from move_wrapper import move_amt, turn
from detect_stop import detect_stop


DEBUG = True
DE_RES_FACTOR = 5
X_OFFSET = 12
GOAL = (16, 6)
DIAG_DIST = np.sqrt(DE_RES_FACTOR**2 + DE_RES_FACTOR**2)

class Node:
    def __init__(self, x, y, parent, f, g, h):
        self.x = x
        self.y = y
        self.parent = parent
        self.f = f
        self.g = g
        self.h = h

    def __str__(self):
        return "({}, {}, {}, {}, {})".format(self.x, self.y, self.f, self.g, self.h)

    def __repr__(self):
        return "({}, {}, {}, {}, {})".format(self.x, self.y, self.f, self.g, self.h)

# Checks if a given coordinate is outside of the bounds of the grid
def is_out_of_bounds(x, y, de_res):
    if de_res:
        return (x < 0 or y < 0 or x >= 20 or y >= 20)
    else:
        return (x < 0 or y < 0 or x > 99 or y > 99)

# Checks to see if any of the surrounding nodes is blocked.
# Returns True if surrounding node is blocked, False if not
def is_blocked(x, y, course, de_res):
    if is_out_of_bounds(x, y, de_res):
        return True

    points = [-1, 1]
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 or j == 0) and (not is_out_of_bounds(x + i, y + 1, de_res)) and course[x + i, y + j] == 1:
                count += 1
    return count >= 2

# Calculates Manhattan Distance for two nodes on the grid
def manhattan_dist(cur_x, cur_y, goal_x, goal_y):
    return np.sqrt((cur_x - goal_x)**2 + (cur_y - goal_y)**2)

# Generates all surrounding children for a node. Checks for validity along the way
# Returns a list of all children nodes
def generate_children(node, course, open, closed, goal, de_res):
    children = []

    for i in range(-1, 2):
        for j in range(-1, 2):
            if (i == 0 and j == 0):
                continue
            
            # Generate node values
            cur_x = node.x + i
            cur_y = node.y + j
            if i == 0 or j == 0:
                cur_g = node.g + DE_RES_FACTOR
            else:
                cur_g = node.g + DIAG_DIST
            cur_h = manhattan_dist(cur_x, cur_y, goal[0], goal[1]) 
            cur_f = cur_g + cur_h

            new_node = Node(cur_x, cur_y, node, cur_f, cur_g, cur_h)

            if new_node.x == goal[0] and new_node.y == goal[1]:
                if DEBUG:
                    print("reached goal")
                return [Node(goal[0], goal[1], node, -1, -1, -1)]

            # Check to see if there is a shorter path to current node through different parent
            skip_node = False
            if is_blocked(new_node.x, new_node.y, course, de_res) or course[new_node.x, new_node.y] == 1:
                if DEBUG:
                    print("({}, {}) skipped from blocked".format(new_node.x, new_node.y))
                continue

            for closed_node in closed:
                if closed_node.x == new_node.x and closed_node.y == new_node.y:
                    skip_node = True
                    if DEBUG:
                        print("({}, {}) skipped from close".format(new_node.x, new_node.y))
                    break
                else:
                    for open_node in open:
                        if open_node.x == new_node.x and open_node.y == new_node.y:
                            if DEBUG:
                                print("({}, {}) skipped from open".format(new_node.x, new_node.y))

                            skip_node = True
                            break

                    if skip_node:
                        break

            

            if skip_node:
                continue

            children.append(new_node)
    
    return children




# Finds the shortest path from the start to the end using A* algorithm
def find_path(course, goal, de_res):
    start_node = Node(X_OFFSET, 0, None, 0, 0, 0)

    open = [start_node]
    closed = []

    while len(open) > 0:
        min_f = open[0].f
        min_f_idx = 0
        for i, node in enumerate(open):
            if node.f < min_f:
                min_f = node.f
                min_f_idx = i
        
        q = open.pop(min_f_idx)

        children = generate_children(q, course, open, closed, goal, de_res)

        if len(children) == 1 and children[0].f == -1:
            closed.append(q)
            closed.append(children[0])
            break
        open = open + children
        if DEBUG:
            print(children)

        closed.append(q)
        if DEBUG:
            print("Added ({}, {}, {})".format(q.x, q.y, q.f))


    
    return closed

def print_list(nodes):
    for node in nodes:
        print("({}, {})".format(node.x, node.y))

def find_angle(first, second):
    x_dif = second[0] - first[0]
    y_dif = second[1] - first[1]
    difs = (x_dif, y_dif)

    if difs == (0, 1):
        angle = 0
    elif difs == (1, 1):
        angle = 45
    elif difs == (1, 0):
        angle = 90
    elif difs == (1, -1):
        angle = 135
    elif difs == (0, -1):
        angle = 180
    elif difs == (-1, -1):
        angle = 225
    elif difs == (-1, 0):
        angle = 270
    elif difs == (-1, 1):
        angle = 315
    
    print(angle)
    return angle



def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--filename',
        help='Filename to save grid into.',
        required=False,
        default=""
    )  
    parser.add_argument(
        '--deres',
        help='LowerResolution of Grid',
        action='store_true',
        required=False,
        default=False
    ),
    parser.add_argument(
        '--goal',
        nargs=2,
        type=int,
        required=True
    )
    args = parser.parse_args()

    # Load in grid, if not predetermined, generate grid
    if args.filename == "":
        filename = "grid_txt"
        course = grid(filename)
    else:
        filename = args.filename
        course = np.loadtxt("grids/" + filename, dtype='int8')
    
    # If option is chosen, deres grid by a factor of 5
    if args.deres:
        course = de_res(filename)
        goal = (int(args.goal[0] / DE_RES_FACTOR), int(args.goal[1] / DE_RES_FACTOR))
    else:
        goal = tuple(args.goal)

    # Find shortest path
    closed_list = find_path(course, goal, args.deres)

    # Trace path out in file
    solved_grid = np.copy(course)
    last_node = closed_list[len(closed_list) - 1]
    solved_grid[last_node.x, last_node.y] = 2
    parent = last_node.parent
    print("({}, {})".format(last_node.x, last_node.y))
    path = [(last_node.x, last_node.y)]

    while parent != None:
        path.append((parent.x, parent.y))
        print("({}, {})".format(parent.x, parent.y))
        solved_grid[parent.x, parent.y] = 2
        parent = parent.parent

    # Save plot and data for reference
    plt.imsave("grids/" + filename + "_solved" + ".png", solved_grid)
    np.savetxt("grids/" + filename + "_solved", solved_grid.astype(int), fmt="%i")

    # Read path and move car accordingly
    path = path[::-1]
    move_inputs = []

    counter = 1
    cur_angle = 0
    last_point = path[0]
    for point in path[1:]:
        new_angle = find_angle(last_point, point)
        if new_angle == cur_angle:
            counter += 1
        else:
            move_inputs.append(("move", counter * 5))
            counter = 1
            move_inputs.append(("turn", cur_angle, new_angle))
            cur_angle = new_angle
        last_point = point
    
    move_inputs.append(("move", counter * 5 + 5))

    for move in move_inputs:
        if move[0] == "move":
            move_amt(move[1])
        else:
            turn(move[1], move[2])

    



if __name__ == '__main__':
    main()







