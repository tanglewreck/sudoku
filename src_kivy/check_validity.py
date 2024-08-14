#!/usr/bin/env python3

import numpy as np
import random
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
    return len(set(row.flatten())) == len(row.flatten())


def is_unique(array: np.ndarray) -> bool:
    elements = [n for n in array if n != 0]
    return len(elements) == len(set(elements))


def is_valid(array: np.ndarray) -> bool:
    # return_status = True
    # status_rows = status_cols = status_blocks = list()

    # Check rows and columns
    for k in range(9):
        if not is_unique(array[k, :]) or not is_unique(array[:, k]):
            # return False
            return_status = False
        else:
            # print(f"row and/or column {k} is valid: {array[k]}")
            pass
    
    # Check blocks
    for row in range(0, 9, 3):
        for col in range(0, 9, 3):
            # print(array[row:row + 3, col:col +3].flatten())
            print(f"checking block [{row}:{row + 3}, {col}:{col + 3}]")
            if not check_row(array[row:row + 3, col:col +3].flatten()):
                # print("block not valid")
                return False
                # return_status = False
            #else:
            #    print(f"block [{row}:{row + 3}, {col}:{col + 3}] is valid")
    return True

def generate() -> np.ndarray:
    # Generate a random 9x9 array
    # array = np.random.choice(range(1, 10), size=(9,9), replace=True)
    # print(f"array {array} is valid?", is_valid(array))
    return np.random.choice(range(1, 10), size=(9,9), replace=True)


def gen():
    A = np.zeros((9, 9), dtype=int)
    # Randomise the first line
    A[0] = np.random.choice(range(1,10), size=9, replace=False)

    for r in range(1,9):    # rows
        for c in range(9):  # cols
            col_nums = A[:, c]    # numbers in this column
            row_nums = A[r, :]    # numbers on this row
            # row_col_nums = set(col_nums + row_nums)
            row_col_nums = set(list(col_nums) + list(row_nums))
            row_col_nums.discard(0)
            possibles = list(set(range(1, 10)).difference(row_col_nums))
            ## print(r, c, "possibles:", possibles)
            if len(possibles) > 0:
                random_int = np.random.choice(possibles)
            else:
                return A, False
                # random_int = 0
            ## print("np.random.choice: ", random_int) 
            # print("np.random.choice: ", np.random.choice(possibles, size=1))
            # print(k, c, s)
            # A[r, c] = np.random.choice(list(possibles))
            A[r, c] = random_int
            # print(A[r, c])
            #
    # print(is_valid(A))
    return A, is_valid(A)


def main():
    k = 0
    valid = False
    while not valid:
        k = k + 1 
        print(k)
        (A, valid) = gen()
        if valid:
            print("valid")
            print(A)
        else:
            print(k)
    #    a = generate()
    #    # if valid := is_valid(a):
    #    if is_valid(a):
    #        print(f"Iteration #{k} valid")
    #        print(a)
    #break

    if debug:
        if valid:
            debug_msg("Grid is valid")
        else:
           debug_msg("Grid is not valid")


if __name__ == "__main__":
    main()
