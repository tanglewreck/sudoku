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
def is_safe(grid, row, col, num):
  
    # If num is in the same row, return False 
    if num in grid[row]:
        return False

    # If num is in the same col, return False 
    if num in grid[:, col]:
        return False

    # If num is in the same subgrid, return False 
    startRow = row - row % 3
    startCol = col - col % 3
    if num in grid[startRow:startRow + 3, startCol:startCol + 3]:
        return False
#     for i in range(3):
#         for j in range(3):
#             if grid[i + startRow][j + startCol] == num:
#                 return False

    # All the above checks are go, so return True:
    return True


# solve_sudolu:
#   Takes a partially filled-in grid and attempts
#   (recursiveley) to assign values to all unassigned
#   locations in such a way to meet the requirements for
#   a Sudoku solution (non-duplication across rows,
#   columns, and subgrids)
def solve_sudoku(grid, row, col):
  
    # Check if we have reached index [8, 9] (0 indexed matrix)
    # If we habe, return true to avoid further backtracking
    if (row == N - 1 and col == N):
        return True
      
    # Check if column value is 9; if so, move on to
    # the beginning of the next row 
    if col == N:
        row = row + 1
        col = 0

    # Check if the current position of the grid already contains
    # a value > 0, and if it does, iterate for the next column
    if grid[row, col] > 0:
        return solve_sudoku(grid, row, col + 1)

    for num in range(1, N + 1):
        # Check if we can safely place the num (1-9) in the
        # given row/ col. If it is, move on to the next column
        if is_safe(grid, row, col, num):
            # Assign the num at the current row/col,
            # assuming the assigned num is correct
            grid[row][col] = num

            # Check for the next possible number in the next column
            if solve_sudoku(grid, row, col + 1):
                return True

        # Our assumption was incorrect, so remove the assigned num
        # and go for next assumption with a different num value
        grid[row][col] = 0

    return False


# Driver Code
def main():

    # 0 means unassigned cells
    grid_1 = [[3, 0, 6, 5, 0, 8, 4, 0, 0],
              [5, 2, 0, 0, 0, 0, 0, 0, 0],
              [0, 8, 7, 0, 0, 0, 0, 3, 1],
              [0, 0, 3, 0, 1, 0, 0, 8, 0],
              [9, 0, 0, 8, 6, 3, 0, 0, 5],
              [0, 5, 0, 0, 9, 0, 6, 0, 0],
              [1, 3, 0, 0, 0, 0, 2, 5, 0],
              [0, 0, 0, 0, 0, 0, 0, 7, 4],
              [0, 0, 5, 2, 0, 6, 3, 0, 0]]
    
    grid_2: np.ndarray = np.array([[0, 0, 0, 5, 1, 0, 0, 0, 8],
                                   [5, 0, 0, 8, 0, 0, 0, 6, 7],
                                   [0, 0, 0, 0, 0, 6, 3, 0, 9],
                                   [3, 0, 8, 0, 7, 0, 0, 0, 0],
                                   [0, 5, 0, 0, 0, 0, 4, 0, 0],
                                   [0, 0, 0, 0, 4, 8, 0, 0, 0],
                                   [0, 1, 0, 0, 8, 0, 0, 7, 0],
                                   [0, 0, 7, 6, 9, 1, 0, 0, 0],
                                   [0, 9, 0, 0, 0, 0, 0, 2, 0]])

    grid_3: np.ndarray = np.zeros((9, 9), dtype=int)
    grid_3_flat = grid_3.flatten()
    positions = np.random.choice(range(81), size=9, replace=False)
    nums = np.random.choice(range(1, 10), size=9, replace=False)
    for k, pos in enumerate(positions):
        grid_3_flat[pos] = nums[k]
        # print(grid_3_flat[int(pos)])
        # grid_3.flat[pos] = np.random.choice(1,10)
    grid_3 = grid_3_flat.reshape(9, 9)
    # print(grid_3)
    # index = {0: 0, 1:0, 2: 0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
    # index_x1 = np.random.choice(range(9))
    # print(index.keys())

    grid_array = np.array(grid_1)
    grid_array = grid_3
    print("Input array:",  grid_array, sep="\n", end="\n\n")
    # raise SystemExit(0, "ok")
    if (solve_sudoku(grid_array, 0, 0)):
        # printing(grid_array)
        print("Output array:", grid_array, sep="\n")
    else:
        print("no solution  exists ")
    
    
if __name__ == "__main__":
    main()
