#!/usr/bin/env python3

import numpy as np
from utils import debug_msg, err_msg, sys_msg
from utils import parse_arguments


args = parse_arguments()
debug = args.debug

a = np.array([[1, 2, 3, 4, 5, 6, 7, 8, 9],
              [2, 3, 4, 5, 6, 7, 8, 9, 1],
              [3, 4, 5, 6, 7, 8, 9, 1, 2],
              [4, 5, 6, 7, 8, 9, 1, 2, 3],
              [5, 6, 7, 8, 9, 1, 2, 3, 4],
              [6, 7, 8, 9, 1, 2, 3, 4, 5],
              [7, 8, 9, 1, 2, 3, 4, 5, 6],
              [8, 9, 1, 2, 3, 4, 5, 6, 7],
              [9, 1, 2, 3, 4, 5, 6, 7, 8]])

def check_row(row: np.ndarray) -> bool:
    return len(set(row.flatten())) == len(row.flatten()):


def is_unique(array: np.ndarray) -> bool:
    elements = [n for n in array if n != 0]
    return len(elements) == len(set(elements))


def is_valid(array: np.ndarray) -> bool:
    # is_valid = True
    # status_rows = status_cols = status_blocks = list()

    # Check rows and columns
    for k in range(9):
        if not is_unique(array[k, :]) or not is_unique(array[:, k]):
            # return False
            return_status = False
        else:
            print(f"row and/or column {k} is valid: {array[k]}")
    
    # Check blocks
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            print(array[row:row + 3, col:col +3].flatten())
            if not check_row(array[row:row + 3, col:col +3].flatten()):
                # return False
                return_status = False
            else:
                print(f"block [{row}:{row + 3}, {col}:{col + 3}] is valid")
    return return_status

def main():
    if debug:
        if is_valid:
            debug_msg("Grid is valid")
        else:
           debug_msg("Grid is not valid")


if __name__ == "__main__":
    main()
