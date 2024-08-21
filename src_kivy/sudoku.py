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

__version__ = "2024-08-21"

import functools
# import string
import sys
import numpy as np

from utils import debug_msg, err_msg  #, sys_msg
from utils import parse_arguments

# from typing import
from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ColorProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget


# from solver import generate, print_possibles, solver
import solver

import kivy
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# <ENVIRONMENT VARIABLES>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
import os

# NOTE: KIVY_HOME must be set *before* kivy is imported,
# thereby breaking PEP8 (E402)
os.environ['KIVY_HOME'] = "./.kivy"
HOME = os.environ['HOME']  # Needed for the path to the kivy config file

# Make kivy ignore command-line arguments so that we don't have to put '--'
# before our own options/arguments
os.environ['KIVY_NO_ARGS'] = 'yes'

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# </ENVIRONMENT VARIABLES>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# <KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Read the (local) configuration files and change stuff to our liking.
# NOTE: Changes require a restart to take effect
Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")
Config.set('kivy', 'exit_on_escape', 1)
Config.set('kivy', 'log_enable', 1)
Config.set('kivy', 'window_icon', "data/mier_347x437.jpg")
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 1000)
# Config.set('graphics', 'height', 480)
# Config.set('graphics', 'width', 800)
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'position', 'custom')  # auto|custom
Config.set('graphics', 'left', 100)         # ignored when 'position' == 'auto'
Config.set('graphics', 'top', 100)          # ignored when 'position' == 'auto'
Config.set('kivy', 'log_level', "warning")  # debug|info|warning|error|critical
Config.write()

# Config.set('modules', 'monitor', '')
# Config.set('modules', 'touchring', '')
kivy.require("2.0.0")
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# </KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


class ButtonBG(Widget):
    """Button background"""
    def __init__(self):
        super(ButtonBG, self).__init__()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
        with self.canvas:
            Color(1, 1, 1, 0.3)
            Rectangle(pos=self.pos, size=self.size)
        self.background_color = (1, 1, 1, 1)


class NumberPadButton(Button):
    """Number pad buttons"""
    pass
    # def __init__(self, **kwargs):
    #    super(NumberPadButton, self).__init__(**kwargs)


class GridButton(Button):
    """Sudoku grid buttons"""
    pass


class SudokuBlock(GridLayout):
    """The sudoku grid buttons are wrapped within 3 x 3 GridLayouts"""
    def __init__(self, **kwargs):
        super(SudokuBlock, self).__init__(**kwargs)


class RootWidget(GridLayout):
    """RootWidget: Sudoku grid with a numerical keypad on the right"""
    # note = False
    the_grid = ListProperty()
    active_number = NumericProperty()
    active_number_string = StringProperty()

    def __init__(self, grid: np.ndarray = None, debug: bool = None) -> None:
        super(RootWidget, self).__init__()

        self.debug = debug
        self.grid = grid
        self.build_the_grid()
        # self.add_gridbutton()

        if self.debug:
            print(self.grid)

    def build_the_grid(self):
        """Build the grid widget tree"""
        # Add a 3 by 3 GridLayout widget
        self.sudokugrid = GridLayout(
            cols=3,
            rows=3,
            orientation="lr-tb",
            size_hint_x=3 / 8
        )
        # Add grid buttons with text set to the corresponding
        # self.grid[index] value. Also bind each button to the
        # 'update_gridbutton' function.
        for n in range(3):
            for m in range(3):
                sudoku_block = SudokuBlock(orientation='lr-tb')  # SudokuBlocks
                self.sudokugrid.add_widget(sudoku_block)
                for i in range(3):
                    for j in range(3):
                        # Index in the grand total GridLayout
                        index = (n * 3 + i, m * 3 + j)
                        grid_button = GridButton(disabled=False)
                        # Bind the GridButton to a function which updates the
                        # label text to the active number:
                        grid_button.bind(
                            on_release=functools.partial(
                                self.update_grid_button,
                                index=index
                            )
                        )

                        # If the number at position 'index' is set
                        # (i.e. is not zero), update the text of the
                        # corresponding GridButton and disable it:
                        if self.grid[index]:
                            grid_button.text = str(self.grid[index])
                            grid_button.disabled = True
                        # Add the GridButton to the SudokuBlock
                        sudoku_block.add_widget(grid_button)
        # Add the finalised sudoku grid (GridLayout) to the RootWidget
        self.add_widget(self.sudokugrid)

    # Update the GridButton text with the active number
    def update_grid_button(self, instance: GridButton, index: tuple) -> None:
        if self.debug:
            print("index: ", index)
            print("instance.text (pre):", instance.text)
            print(f"self.grid[{index}]:", self.grid[index])
            print(f"self.ids.active_number.text:", self.ids.active_number.text)
            print(self.grid)
        if self.ids.active_number.text:
            self.grid[index] = int(self.ids.active_number.text)
            instance.text = str(self.ids.active_number.text)
            # print("active_number: ", self.ids.active_number.text)
        else:
            self.grid[index] = 0
            instance.text = ""

        if self.debug:
            print("instance.text (post):", instance.text)

    # Quit the application (triggered by the Quit button)
    def do_quit(self, *args):
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)


class SudokuApp(App):
    """SudokuApp"""

    def __init__(self, grid: np.ndarray = np.zeros((9, 9), dtype=int),
                 debug: bool = None) -> None:
        super(SudokuApp, self).__init__()
        self.debug = debug  # gets passed on to RootWidget
        self.grid = grid  # gets passed on to RootWidget
        self.kv_file = "kv/sudoku.kv"  # the kv file is in a separate directory

    def build(self):
        self.root = RootWidget(self.grid, self.debug)
        return self.root

    def on_start(self):
        pass

    def on_stop(self):
        print("Bye bye!")


if __name__ == "__main__":
    # Parse and get command line arguments
    args = parse_arguments()
    debug = args.debug

    # Load the sudoku grid file, if provided on the command line
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
    SudokuApp(puzzle, debug=debug).run()
