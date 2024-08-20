#!/usr/bin/env python3
"""Sudoku backtracking solver"""

__version__ = "2024-08-19"

# Code by sudhanshgupta2019a
# (https://www.geeksforgeeks.org/sudoku-backtracking-7/#)
# Modified by mier to use numpy arrays and more.

import datetime
import numpy as np
import random
from utils import parse_arguments

# N is the size of the N x N matrix
N = 9

GRID_1: np.ndarray = np.array(
    [[3, 0, 6, 5, 0, 8, 4, 0, 0],
     [5, 2, 0, 0, 0, 0, 0, 0, 0],
     [0, 8, 7, 0, 0, 0, 0, 3, 1],
     [0, 0, 3, 0, 1, 0, 0, 8, 0],
     [9, 0, 0, 8, 6, 3, 0, 0, 5],
     [0, 5, 0, 0, 9, 0, 6, 0, 0],
     [1, 3, 0, 0, 0, 0, 2, 5, 0],
     [0, 0, 0, 0, 0, 0, 0, 7, 4],
     [0, 0, 5, 2, 0, 6, 3, 0, 0]]
)

GRID_2: np.ndarray = np.array(
    [[0, 0, 0, 5, 1, 0, 0, 0, 8],
     [5, 0, 0, 8, 0, 0, 0, 6, 7],
     [0, 0, 0, 0, 0, 6, 3, 0, 9],
     [3, 0, 8, 0, 7, 0, 0, 0, 0],
     [0, 5, 0, 0, 0, 0, 4, 0, 0],
     [0, 0, 0, 0, 4, 8, 0, 0, 0],
     [0, 1, 0, 0, 8, 0, 0, 7, 0],
     [0, 0, 7, 6, 9, 1, 0, 0, 0],
     [0, 9, 0, 0, 0, 0, 0, 2, 0]]
)

GRID_2_1: np.ndarray = np.array(
    [[9, 3, 6, 5, 1, 7, 2, 4, 8],
     [5, 2, 4, 8, 3, 9, 1, 6, 7],
     [8, 7, 1, 4, 2, 6, 3, 5, 9],
     [3, 4, 8, 9, 7, 5, 6, 1, 2],
     [7, 5, 9, 1, 6, 2, 4, 8, 3],
     [1, 6, 2, 3, 4, 8, 7, 9, 5],
     [4, 1, 5, 2, 8, 3, 9, 7, 6],
     [2, 8, 7, 6, 9, 1, 5, 3, 4],
     [6, 9, 3, 7, 5, 4, 8, 2, 1]]
)


GRID_3: np.ndarray = np.array(
    [[8, 4, 0, 6, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 3, 0, 5, 4, 8, 0, 0, 0],
     [0, 5, 9, 0, 1, 0, 0, 8, 0],
     [7, 0, 0, 0, 0, 0, 2, 0, 0],
     [2, 0, 4, 0, 0, 0, 0, 9, 0],
     [0, 0, 0, 0, 6, 7, 0, 2, 0],
     [0, 8, 0, 0, 0, 4, 9, 5, 0],
     [0, 0, 0, 0, 0, 0, 7, 0, 0]]
)


def valid(grid, row, col, num):
    """Check whether num can be assigned to the given row, col
       Return False if num is in the same row, column, or subgrid"""
    start_row = row - row % 3
    start_col = col - col % 3
    return not num in grid[row, :] and \
           not num in grid[:, col] and \
           not num in grid[start_row:start_row + 3, start_col:start_col + 3]


def solve(grid, row, col):
    """ solve:
        Take a partially filled-in grid and attempt
        (recursiveley) to assign values to all unassigned
        locations in such a way as to conform to 
        the Rules of Sudoku """

    # If we have reached the last column, move on to the next row 
    if col == N:
        # If we're on the last row, end the recursion
        if row == N - 1:
            return True
        else:
            row, col = (row + 1, 0)

    # Check if the current position of the grid already contains
    # a value > 0, and if it does, move on to the next column
    if grid[row, col] > 0:
        return solve(grid, row, col + 1)

    for num in range(1, N + 1):
        # Check if we can safely place a number at [row, col].
        # If we can, assign the number tentatively, and move on to the next column.
        # This is where the recursion takes place.
        if valid(grid, row, col, num):
            # Assign the num at the current row/col,
            # **assuming** the assigned num is correct
            # (if this assumption is wrong, we will end up with a
            # 'contradiction', i.e. we will end up at a position where we
            # have unsuccessfully tried to assign all numbers from 1 to 9.
            # At that point, the recursion will rewind to a point in the grid
            # where we are able to try with another number...
            grid[row][col] = num

            # Check for the next possible number in the next column
            if solve(grid, row, col + 1):
                return True

        # Our assumption was incorrect, so remove the assigned num
        # and go for next assumption with a different num value
        # print(f"not safe [{row}, {col}]: {num}")
        grid[row][col] = 0

    # If we have reached this far, the grid is unsolvable
    return False


def possibles(array: np.ndarray, row: int, col:int) -> list:
    """Return a list of possible numbers at array[row, col]"""
    possible_numbers = list()
    for num in range(1, 10):
        if valid(array, row, col, num):
            possible_numbers.append(num)
    return possible_numbers


def generate() -> np.ndarray:
    """ Initialise an empty grid (all zeros)"""
    grid: np.ndarray = np.zeros((9,9), dtype=int)

    # Randomise the first row
    grid[0] = np.random.choice(np.arange(1, 10), size=9, replace=False)
    return grid

### def generate() -> np.ndarray:
###     # grid: np.ndarray = np.zeros((81), dtype=int)
###     # Randomise 9 positions in a 1 x 81 array
###     random_positions: np.ndarray = np.random.choice(range(81), size=9, replace=False)
###
###     # Randomise the order of the numbers 1-9
###     numbers = np.random.choice(np.arange(1, 10, dtype=int), size=9, replace=False)
###
###     # Insert the numbers in the grid at the randomised positions
###     grid[random_positions] = numbers
###     return grid.reshape(9, 9)


def main():
    """main foo doc string"""
    args = parse_arguments()
    debug = args.debug

    # Load the sudoku board file, if provided on the command line
    if args.filename:
        if debug:
            debug_msg("args.filename:", args.filename.name)
        try:
            grid = np.loadtxt(args.filename.name, delimiter=",", dtype=int)
        except OSError as e:
            print(e)
    else:
        grid = generate()

    # grid = GRID_2
    # grid = grid_3 = generate()

    input_grid = grid

    # Print a list of possible numbers 
    for row in range(9):
        print(f"row: {row + 1}")
        for col in range(9):
            print(f"\tcol: {col}\t", " ".join(map(str, possibles(grid, row, col))))

    print("Input grid:",  input_grid, sep="\n", end="\n\n")
    # Solve it
    if (solve(grid, 0, 0)):
        solution = grid
        print(f"Solution:", solution, sep="\n")
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        filename = f"data/{timestamp}.sudoku"

        n_remove = 81 - 30
        remove_index = np.random.randint(0, 80, n_remove)
        #print(remove_index)
        g = grid.flatten()
        g[remove_index] = 0
        #for k in range(n_remove):
        #    g[remove_index[k]] = 0
        #print(g.reshape([9, 9]))
        np.savetxt(filename, g.reshape([9, 9]), fmt="%d", delimiter=",")
    else:
        print("no solution  exists ")
    

if __name__ == "__main__":
    main()
