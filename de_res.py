import numpy as np
import matplotlib.pyplot as plt

DE_RES_FACTOR = 5

def de_res(filename):
    grid = np.loadtxt("grids/" + filename, dtype='int8')
    low_res_length = int(len(grid) / DE_RES_FACTOR)


    low_res_grid = np.zeros((low_res_length, low_res_length))

    # Loop through grid by 5's and check if any are blocked
    for x in range(0, len(grid), DE_RES_FACTOR):
        for y in range(0, len(grid), DE_RES_FACTOR):
            is_blocked = False

            for i in range(5):
                if is_blocked:
                    break
                for j in range(5):
                    if (grid[x+i, y+j] == 1):
                        is_blocked = True
                        low_res_grid[int(x / DE_RES_FACTOR), int(y / DE_RES_FACTOR)] = 1
                        break

    
            
    plt.imsave("grids/" + filename + "_lres.png", low_res_grid)
    np.savetxt("grids/" + filename + "_lres", low_res_grid.astype(int), fmt="%i")
    return low_res_grid

def main():
    de_res("grid_txt")



if __name__ == '__main__':
    main()