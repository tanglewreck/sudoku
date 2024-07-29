#!/usr/bin/env python3

__author__ = "Mikael Eriksson"
__version__ = 0.9
"""Sudoku
Usage: sudoku [--debug] <sudoku game file>
    <sudoku game file>  A text file representing the sudoku board; comma
                        separated; nine lines with nine entries each;
                        '0' representing an empty square; e.g.

                        1,0,3,2,0,0,0,0,9
                        0,0,0,1,0,0,0,0,0
                        0,4,0,0,0,0,1,0,0
                        0,0,1,0,3,0,0,0,2
                        0,2,0,0,7,0,0,0,0
                        0,0,0,0,0,9,0,7,0
                        8,0,0,0,0,0,0,0,0
                        0,0,7,0,0,0,5,6,0
                        0,0,2,0,0,0,3,0,1
"""

from sudoku.utils import debug_msg, err_msg, sys_msg
from sudoku.utils import parse_arguments
from sudoku.utils import ROOT_GEOMETRY

from sudoku.board import Sudoku
from sudoku.gui import SudokuGUI

DEBUG = False

def main():
    args = parse_arguments()
    if args.debug:
        sys_msg(f"{args}")

    sudoku = Sudoku(debug=args.debug)
    sudoku.load(args.filename)

    # breakpoint()
    sudokuApp = SudokuGUI(sudoku, geometry=args.geometry, debug=args.debug)
    sudokuApp.populate()
    sudokuApp.mainloop()


if __name__ == "__main__":
    main()
