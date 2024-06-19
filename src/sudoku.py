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
from sudokuGUI import SudokuGUI

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

    sudoku = Sudoku(debug=args.debug)
    sudoku.load_board(args.filename, debug=args.debug)
    if sudoku.validate_board(sudoku.board):
        print(sudoku)
    else:
        err_msg("Invalid board")
        raise SystemExit(1)

    # root = Tk()
    # root.title("sudoku ftw!")
    app = SudokuGUI(sudoku, geometry=args.geometry, debug=args.debug)
    app.populate(sudoku, debug=args.debug)
    app.mainloop()





if __name__ == "__main__":
    main()
