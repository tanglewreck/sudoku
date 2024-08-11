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
    if len(set(row.flatten())) == len(row.flatten()):
        return True
    else:
        return False


is_valid = True
for row in range(9):
    if not check_row(a[row]):
        is_valid = False
    else:
        print(f"row {row} is valid: {a[row]}")

for col in range(9):
    if not check_row(a[:, col]):
        is_valid = False
    else:
        print(f"col {col} is valid: {a[col]}")

for row in range(0, 9, 3):
    for col in range(0, 9, 3):
        print(a[row:row + 3, col:col +3].flatten())
        if not check_row(a[row:row + 3, col:col +3].flatten()):
            is_valid = False

if debug:
    if is_valid:
        debug_msg("Grid is valid")
    else:
       debug_msg("Grid is not valid")
