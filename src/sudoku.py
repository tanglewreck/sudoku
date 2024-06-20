#!/usr/bin/env python3

# import inspect
# import math
# import numpy as np
# import os
# import re
# import sys

from utils import debug_msg, err_msg, sys_msg
from utils import ROOT_GEOMETRY
from utils import parse_arguments
from sudokuboard import Sudoku
from sudokuGUI import SudokuGUI
from widgets import SudokuWidgets

DEBUG = False

def main():
    args = parse_arguments()

    sudoku = Sudoku(debug=args.debug)
    sudoku.load_board(args.filename, debug=args.debug)
    if sudoku.validate_board(sudoku.board):
        print(sudoku)
    else:
        err_msg("Invalid board")
        raise SystemExit(1)

    app = SudokuGUI(sudoku_game=sudoku, geometry=args.geometry, debug=args.debug)
    app.populate(sudoku, debug=args.debug)
    app.mainloop()

    # app2 = SudokuWidgets(sudoku_game=sudoku, geometry=args.geometry, debug=args.debug)
    # app2.mainloop()

if __name__ == "__main__":
    main()
