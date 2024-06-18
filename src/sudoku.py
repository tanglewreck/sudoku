#!/usr/bin/env python3

import inspect
import math
import numpy as np
import os
import re
import sys

import utils
from utils import debug_msg, err_msg, sys_msg
from utils import ROOT_GEOMETRY
from sudokuboard import Sudoku

DEBUG = False

def read_game_file(filename=None, debug=DEBUG):
    try:
        return np.loadtxt(filename, delimiter=",", dtype=int)
    except ValueError as e:
        err_msg(f"{e}")
        return None
    except OSError as e:
        err_msg(e)
        return None


def print_board(board):
    print(" – – – – – – – – – – – –")
    for i, row in enumerate(board):
        # print(row)
        s = "| "
        for j, element in enumerate(row):
            s += str(element) + " "
            if (j + 1) % 3 == 0:
                s += "| "
        print(s)
        if (i + 1) % 3 == 0:
            print(" – – – – – – – – – – – –")

def main():
    args = utils.parse_arguments()
#     board = read_game_file(args.filename, debug=args.debug)
#     if board is None:
#        err_msg(f"Could not read board from {args.filename}")
#        raise SystemExit(1)

#    blocks = []
#    for i in range(0,9,3):
#        for j in range(0,9,3):
#            blocks.append(board[i:i+3, j:j+3])
#
#     blocks.append(board[0:3, 0:3])
#     blocks.append(board[0:3, 3:6])
#     blocks.append(board[0:3, 6:9])
# 
#     blocks.append(board[3:6, 0:3])
#     blocks.append(board[3:6, 3:6])
#     blocks.append(board[3:6, 6:9])
# 
#     blocks.append(board[6:9, 0:3])
#     blocks.append(board[6:9, 3:6])
#     blocks.append(board[6:9, 6:9])
#
#    for k, block in enumerate(blocks): 
#        # print(block, end='    ')
#        if k % 3 == 0:
#            print()
#        print(block)

    # sudoku = Sudoku(board=board, geometry=args.geometry, debug=args.debug)
    sudoku = Sudoku(geometry=args.geometry, debug=args.debug)
    sudoku.load_board(args.filename, debug=args.debug)
    if sudoku.validate_board(sudoku.board):
        print(sudoku)
    else:
        err_msg("Invalid board")
        raise SystemExit(1)

    # root = Tk()
    # root.title("sudoku ftw!")
    # app = SudokuGUI(root, sudoku)
    # root.mainloop()
    sudoku.mainloop()





if __name__ == "__main__":
    main()
