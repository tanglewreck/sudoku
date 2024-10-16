#!/usr/bin/env python3

__version__ = "2024-08-23"

import numpy as np
import os
# NOTE: KIVY_HOME must be set *before* kivy is imported.
#       This is not PEP8 compliant.
os.environ['KIVY_HOME'] = f"{os.getcwd()}/.kivy"
# Make kivy ignore command-line arguments 
os.environ['KIVY_NO_ARGS'] = 'yes'

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

    # Save the puzzle to disk
    if args.save:
        solver.save_to_disk(puzzle)

    # Read the local kivy config
    # Config.read(f"{os.environ['HOME']}/Proj/sudoku/src_kivy/.kivy/config.ini")
    Config.read(f"{os.environ['PWD']}/.kivy/config.ini")

    # Start the app
    SudokuApp(puzzle, solution).run()
