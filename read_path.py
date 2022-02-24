import numpy as np
import matplotlib.pyplot as plt
import argparse


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

    grid = np.loadtxt("grids/" + args.filename, dtype='int8')
    print(grid)

if __name__ == '__main__':
    main()

