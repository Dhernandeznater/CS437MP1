import picar_4wd as fc
import numpy as np
import picamera
import matplotlib.pyplot as plt
import time
from PIL import Image
from tflite_runtime.interpreter import Interpreter
import argparse


import cv2 

# Checks if a given coordinate is outside of the bounds of the grid
def is_out_of_bounds(x, y):
    return (x < 0 or y < 0 or x > 99 or y > 99)

def grid(filename):
    step = 1 # angle step 
    zero_angle = -12
    grid = np.zeros((100,100)) #100cm by 100cm grid
    prev_dist_large = False
    cur_dist_large = False

    # Initial point
    dist = fc.get_distance_at(-73)
    last_point = (int(np.sin(np.radians((-73)))) + 49, int(np.cos(np.radians(-73))))

    for i in range (-60, 60, 8): 
        dist_arr = []
        for trial in range(15):
            dist_arr.append(fc.get_distance_at(i + zero_angle))
        dist = max(dist_arr)
        x = int(dist * np.sin(np.radians((i + zero_angle) * 1))) + 49
        y = int(dist * np.cos(np.radians((i + zero_angle) * 1)))


        if x > 99 or y > 99: # if outside of the range, just change to the max
            last_point = (x, y)
            previ_dist_large = True
            continue

        grid[x, y] = 1 # if object detected then change to 1

        x_dif = x - last_point[0]
        y_dif = y - last_point[1]
        point_dist = np.sqrt(x_dif**2 + y_dif**2)
        if point_dist < 15:
            prev_dis_large = False
            if x_dif == 0:
                if y < last_point[0]:
                    grid[x, y:last_point[1]] = [1] * y_dif
                else:
                    grid[x, last_point[1]:y] = [1] * y_dif
            else:
                slope = y_dif / x_dif
                for j in range(x_dif):
                    new_x = last_point[0] + j + 1
                    new_y = int(last_point[1] + (j + 1) * slope)
                    if new_x > 99 or new_y > 99:
                        continue
                    grid[new_x, new_y] = 1
        else:
            if prev_dist_large and not is_out_of_bounds(last_point[0], last_point[1]):
                grid[last_point[0], last_point[1]] = 0

            prev_dist_large = True

        last_point = (x, y)

    print(grid)
    # cv2.imwrite(filename + ".png", grid)
    plt.imsave("grids/" + filename + ".png", grid, origin='lower')
    np.savetxt("grids/" + filename, grid[::-1].astype(int), fmt="%i")
    return grid

def main():
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument(
        '--filename',
        help='Filename to save grid into.',
        required=False,
        default="grid_txt"
    )
    args = parser.parse_args()

    grid(args.filename)

if __name__ == '__main__':
    main()





 

