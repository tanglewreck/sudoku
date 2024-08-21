#!/usr/bin/env python3
"""Sudoku backtracking solver"""

__version__ = "2024-08-20"
__all__ = ['generate', 'print_possibles', 'save_to_disk', 'solver']

# Code by sudhanshgupta2019a
# (https://www.geeksforgeeks.org/sudoku-backtracking-7/#)
# Modified by mier to use numpy arrays and more.

import datetime
import numpy as np
from utils import parse_arguments, debug_msg, err_msg, sys_msg

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


# GRID_SIZE is the number of rows and columns of the grid
# GRID_ROWS and GRID_COLUMNS are the number of rows and columns in each subgrid
GRID_SIZE = 9
GRID_ROWS = GRID_COLS = 3


def _valid(grid: np.ndarray=None, row: int=0, col: int=0, num: int=0):
    """Check whether num can be assigned to the given row, col
       Returns False if num is in the same row, column, or subgrid"""
    start_row = row - row % GRID_ROWS
    start_col = col - col % GRID_COLS
    return not num in grid[row, :] and \
           not num in grid[:, col] and \
           not num in grid[start_row:start_row + 3, start_col:start_col + 3]


def _solver(grid: np.ndarray, row: int, col: int) -> bool:
    """ solver:
        Take a partially filled-in grid and attempt
        (recursiveley) to assign values to all unassigned
        locations in such a way as to conform to 
        the Rules of Sudoku """

    # If we have reached (more specifically, if we have *gone beyond*)
    # the last column, move on to the first column of the next row.
    if col == GRID_SIZE:
        # If we're on the last row, end the recursion
        if row == GRID_SIZE - 1:
            return True
        else:
            row, col = (row + 1, 0)

    # Check if the current position of the grid already contains
    # a value > 0, and if it does, move on to the next column
    if grid[row, col] > 0:
        return _solver(grid, row, col + 1)

    for num in range(1, 10):
        # Check if we can safely place a number at [row, col].
        # If we can, assign the number tentatively, and move on to the next column.
        # This is where the recursion takes place.
        if _valid(grid, row, col, num):
            # Assign the num at the current row/col,
            # **assuming** the assigned num is correct
            # (if this assumption is wrong, we will end up with a
            # 'contradiction', i.e. we will end up at a position where we
            # have unsuccessfully tried to assign all numbers from 1 to 9.
            # At that point, the recursion will rewind to a point in the grid
            # where we are able to try with another number...
            ### grid[row][col] = num
            grid[row, col] = num

            # Check for the next possible number in the next column
            if _solver(grid, row, col + 1):
                return True

        # Our assumption was incorrect, so remove the assigned num
        # and go for next assumption with a different num value
        # print(f"not safe [{row}, {col}]: {num}")
        grid[row, col] = 0

    # If we have reached this far, the grid is unsolvable
    return False


def solver(grid: np.ndarray) -> bool:
    """Wraps _solver()"""
    # return grid if _solver(grid, 0, 0) else None
    # return grid if _solver(grid, 0, 0) else np.zeros([GRID_SIZE, GRID_SIZE])
    return _solver(grid, 0, 0)


def _possibles(grid: np.ndarray, row: int, col:int) -> list:
    """Return a list of possible numbers at grid[row, col]"""
    possible_numbers = []
    if grid[row, col] == 0:
        for num in range(1, 10):
            if _valid(grid, row, col, num):
                # print(num, "is valid at", row, col)
                possible_numbers.append(num)
    return possible_numbers


def print_possibles(grid: np.ndarray) -> None:
    """For each square in the grid, print what numbers
       can possibly be placed there"""
    for row in range(GRID_SIZE):
        print(f"row: {row + 1}")
        for col in range(GRID_SIZE):
            print(f"\tcol: {col + 1}\t", " ".join(map(str, _possibles(grid, row, col))))


def _remove_squares(grid: np.ndarray, n_remove: int=30) -> np.ndarray:
    # Generate random positions to remove from the grid
    remove_index = np.random.choice(np.arange(81), size=n_remove, replace=False)
    # Flatten the grid so that we can easily remove (i.e. set to zero)
    # the desired number of squares
    g = grid.flatten()
    # Assign zero to the randomised positions...
    g[remove_index] = 0
    # ... and return a properly shaped (i.e. a 2-D) grid
    return g.reshape([GRID_SIZE, GRID_SIZE])


def generate(n_remove: int=50) -> np.ndarray:
    """Generate a sudoku puzzle"""
    while True:
        # Create an "empty" (i.e. filled with zeros) 9 x 9 grid
        g: np.ndarray = np.zeros((9,9), dtype=int)
        # Randomise the first row
        g[0] = np.random.choice(np.arange(1, 10), size=9, replace=False)
        # Solve the grid
        if solver(g):
            solution = g
            # Remove squares to make the grid a sudoku puzzle
            puzzle = _remove_squares(solution, n_remove)
            break
        else:
            err_msg(f"WARNING: Cannot solve this grid: {g}. Trying again...")
    return puzzle, solution

### # ALTERNATE implementation:
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

def save_to_disk(grid: np.ndarray, path: str = None) -> bool:
    """Save a grid to disk. If no path is provided, the
       grid is saved to 'data/<timestamp>', where
       timestamp = '<year>-<month>-<day>.<hour>.<minute>.<second>'"""
    if not path:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H.%M.%S")
        path = f"data/{timestamp}.sudoku"
    try:
        np.savetxt(path, grid, fmt="%d", delimiter=",")
    except (OSError) as e:
        print(str(e))


def main():
    """main foo doc string"""
    args = parse_arguments()

    # Load the sudoku board file, if provided on the command line
    if args.filename:
        if args.debug:
            debug_msg("args.filename:", args.filename.name)
        try:
            puzzle = np.loadtxt(args.filename.name, delimiter=",", dtype=int)
            # Make a deep copy of the puzzle and solve it
            solution = np.copy(puzzle)
            if not solver(solution):
                err_msg(f"Cannot solve this puzzle: \n{puzzle}")
        except OSError as e:
            print(e)
    # If there's no filename, generate a random puzzle
    else:
        puzzle, solution = generate(n_remove=args.nremove)
        # Save the puzzle to file
        if args.save:
            save_to_disk(puzzle)

    if args.verbose:
        print_possibles(puzzle)
    if args.solution:
        print("Puzzle:", puzzle, sep="\n")
        print("Solution:", solution, sep="\n")


if __name__ == "__main__":
    main()
