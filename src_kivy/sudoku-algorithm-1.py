#!/usr/bin/env python3
"""Sudoku backtracking solver"""

__version__ = "2024-08-14"

# Code by sudhanshgupta2019a
# (https://www.geeksforgeeks.org/sudoku-backtracking-7/#)
# Modified by mier to use numpy arrays and more.

import numpy as np

# N is the size of the N x N matrix
N = 9

# Check whether num can be assigned to the given row, col
# (without breaking the Rules)
def is_safe(grid, row, col, num):

    """ Return False if num is in the same row, column, or subgrid"""
    start_row = row - row % 3
    start_col = col - col % 3
    return not num in grid[row, :] and \
           not num in grid[:, col] and \
           not num in grid[start_row:start_row + 3, start_col:start_col + 3]


def solve_sudoku(grid, row, col):
    """ solve_sudoku:
        Take a partially filled-in grid and attempt
        (recursiveley) to assign values to all unassigned
        locations in such a way as to conform to 
        the Rules of Sudoku """

    # Check if we have reached index [8, 9] (the next
    # to last row/last column).
    # If we have, return true to avoid further backtracking
    if (row, col) == (N - 1, N):
        return True

    # Check if column value is 9; if so, move on to
    # the beginning of the next row
    if col == N:
        (row, col) = (row + 1, 0)

    # Check if the current position of the grid already contains
    # a value > 0, and if it does, move on to the next column
    if grid[row, col] > 0:
        return solve_sudoku(grid, row, col + 1)

    for num in range(1, N + 1):
        # Check if we can safely place the num (1 thru 9) in the
        # given row/col. If we can, assign it to the current
        # row/col and move on to the next column
        if is_safe(grid, row, col, num):
            # Assign the num at the current row/col,
            # **assuming** the assigned num is correct
            # (if this assumption is wrong, we will end up with a
            # 'contradiction', i.e. we will end up at a position where we
            # have unsuccessfully tried to assign all numbers from 1 to 9.
            # At that point, the recursion will rewind to a point in the grid
            # where we are able to try with another number...
            grid[row][col] = num

            # Check for the next possible number in the next column
            if solve_sudoku(grid, row, col + 1):
                return True

        # Our assumption was incorrect, so remove the assigned num
        # and go for next assumption with a different num value
        # print(f"not safe [{row}, {col}]: {num}")
        grid[row][col] = 0

    return False


def generate() -> np.ndarray:
    """ Initialise an empty grid (all zeros)"""
    grid: np.ndarray = np.zeros((9,9), dtype=int)

    # Randomise the first row
    grid[0] = np.random.choice(np.arange(1, 10), size=9, replace=False)
    return grid

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
    """main"""
    # 0 means unassigned cells
###     grid_1 = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
###               [5, 2, 0, 0, 0, 0, 0, 0, 0],
###               [0, 8, 7, 0, 0, 0, 0, 3, 1],
###               [0, 0, 3, 0, 1, 0, 0, 8, 0],
###               [9, 0, 0, 8, 6, 3, 0, 0, 5],
###               [0, 5, 0, 0, 9, 0, 6, 0, 0],
###               [1, 3, 0, 0, 0, 0, 2, 5, 0],
###               [0, 0, 0, 0, 0, 0, 0, 7, 4],
###               [0, 0, 5, 2, 0, 6, 3, 0, 0]]
###
###     grid_2: np.ndarray = np.array([[0, 0, 0, 5, 1, 0, 0, 0, 8],
###                                    [5, 0, 0, 8, 0, 0, 0, 6, 7],
###                                    [0, 0, 0, 0, 0, 6, 3, 0, 9],
###                                    [3, 0, 8, 0, 7, 0, 0, 0, 0],
###                                    [0, 5, 0, 0, 0, 0, 4, 0, 0],
###                                    [0, 0, 0, 0, 4, 8, 0, 0, 0],
###                                    [0, 1, 0, 0, 8, 0, 0, 7, 0],
###                                    [0, 0, 7, 6, 9, 1, 0, 0, 0],
###                                    [0, 9, 0, 0, 0, 0, 0, 2, 0]])
###
###     grid_3: np.ndarray = np.zeros((9, 9), dtype=int)
###     grid_3_flat = grid_3.flatten()
###
###     grid_4: np.ndarray = np.array([[8, 4, 0, 6, 0, 0, 0, 0, 1],
###                                    [0, 0, 0, 0, 0, 0, 0, 0, 0],
###                                    [0, 3, 0, 5, 4, 8, 0, 0, 0],
###                                    [0, 5, 9, 0, 1, 0, 0, 8, 0],
###                                    [7, 0, 0, 0, 0, 0, 2, 0, 0],
###                                    [2, 0, 4, 0, 0, 0, 0, 9, 0],
###                                    [0, 0, 0, 0, 6, 7, 0, 2, 0],
###                                    [0, 8, 0, 0, 0, 4, 9, 5, 0],
###                                    [0, 0, 0, 0, 0, 0, 7, 0, 0]])

    # positions = np.random.choice(range(81), size=9, replace=False)
    # nums = np.random.choice(range(1, 10), size=9, replace=False)
    # for k, pos in enumerate(positions):
    #    grid_3_flat[pos] = nums[k]
    #    # print(grid_3_flat[int(pos)])
    #    # grid_3.flat[pos] = np.random.choice(1,10)
    # grid_3 = grid_3_flat.reshape(9, 9)
    # print(grid_3)
    # index = {0: 0, 1:0, 2: 0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    # index_x1 = np.random.choice(range(9))
    # print(index.keys())

    # grid_array = np.array(grid_1)
    # grid_array = grid_3

    # Initialise the array with all blanks (zeros)
    grid_array = np.zeros([9, 9], dtype=int)

    # Randomise the first row
    grid_array[0] = np.random.choice(np.arange(1, 10), size=9, replace=False)

    # Generate a grid
    grid_array = generate()
    # grid_array = grid_4
    print("In:",  grid_array, sep="\n", end="\n\n")
    # raise SystemExit(0, "ok")
    if solve_sudoku(grid_array, 0, 0):
        # printing(grid_array)
        print("Out:", grid_array, sep="\n")
    else:
        print("no solution  exists ")


if __name__ == "__main__":
    main()
