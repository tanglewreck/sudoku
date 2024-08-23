#!/usr/bin/env python3

# ----------------------------------------
# sudoku.py –
# ----------------------------------------
'''
sudoku.py – sudoku implemented in kivy

Sudoku puzzles are either loaded from file (using option '-f' or '--filename')
or generated from scratch.

    Usage: sudoku [-h] [-d] [-n NREMOVE] [-s] [-v] [-f path] [--solution]

    Command line options:

    -h, --help            Show this help message and exit
    -d, --debug           Print debug info
    -s, --save            Save the generated grid to disk
    -v, --verbose         Enable verbose output
    -n NREMOVE, --nremove NREMOVE
                          Number of squares to remove from the
                          completed grid (roughly: level of difficulty)
    -f path, --filename path
                        Name of file containing a sudoku grid – nine rows and
                        nine columns, each row containing a comma-separated,
                        list of integers (0-9, where 0 means an empty square
  --solution            Reveal the solution

'''

# Run 'pycodestyle --ignore=E501,E402 --show-source main.py' to
# check PEP8 compliancy (ignoring E501 because it's stupid
# and E402 because we have to; see NOTE below).

__version__ = "2024-08-23"

import os
# NOTE: KIVY_HOME must be set *before* kivy is imported
os.environ['KIVY_HOME'] = f"{os.getcwd()}/.kivy"
# Make kivy ignore command-line arguments 
os.environ['KIVY_NO_ARGS'] = 'yes'

import numpy as np

import kivy
from kivy.config import Config
from kivy.core.window import Window

import solver
from sudoku import SudokuApp
from utils import debug_msg, err_msg, sys_msg, parse_arguments

# Window.size = (1500, 600)

if __name__ == "__main__":
    # Parse and get command line arguments
    args = parse_arguments()
    debug = args.debug

    # Load the sudoku grid file, if provided on the command line
    # otherwise generate a random puzzle
    if args.filename:
        if debug:
            debug_msg("args.filename:", args.filename.name)
        try:
            puzzle = np.loadtxt(args.filename.name, delimiter=",", dtype=int)
            solution = np.copy(puzzle)
            if not solver.solver(solution):
                err_msg(f"Unable to solve this puzzle: \n{puzzle}")
        except OSError as e:
            print(e)
    else:
        puzzle, solution = solver.generate(args.nremove)
        if args.save:
            solver.save_to_disk(puzzle)

    # Print possible values
    if args.verbose:
        solver.print_possibles(puzzle)

    # Reveal the solution
    if args.solution:
        print("Puzzle:", puzzle, sep="\n")
        print("Solution:", solution, sep="\n")

    # Start the app
    SudokuApp(puzzle, solution).run()
