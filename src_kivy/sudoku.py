#!/usr/bin/env python3
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
__all__ = ['SudokuApp']
__version__ = "2024-08-21"

import functools
import os
import sys
import kivy
import numpy as np

from kivy.app import App
from kivy.config import Config
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

# from kivy.core.window import Window
# from kivy.graphics import Color, Rectangle
# from kivy.properties import ColorProperty
# from kivy.properties import ObjectProperty
# from kivy.uix.behaviors import ButtonBehavior
# from kivy.uix.anchorlayout import AnchorLayout
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.label import Label
# from kivy.uix.widget import Widget


import solver
from utils import debug_msg, err_msg, sys_msg, parse_arguments

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# <ENVIRONMENT VARIABLES>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

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
# NOTE: This code might probaly better be moved to its own file,
#     which can be run when needed (+TODO-list)
Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")
Config.set('kivy', 'exit_on_escape', 1)
Config.set('kivy', 'log_enable', 1)
Config.set('kivy', 'window_icon', "data/mier_347x437.jpg")
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 1500)
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


class NumberPadButton(Button):
    """Number pad buttons"""


class GridButton(Button):
    """Sudoku grid buttons"""


class SudokuBlock(GridLayout):
    """The sudoku grid buttons are wrapped within 3 x 3 GridLayouts"""


class RootWidget(GridLayout):
    """RootWidget: Sudoku grid with a numerical keypad on the right"""
    # note = False
    # the_grid = ListProperty()
    # active_number = NumericProperty()
    # active_number_string = StringProperty()

    def __init__(self, grid: np.ndarray = np.zeros([9, 9])) -> None:
        super().__init__()

        self.grid: np.ndarray = grid
        # Create the sudoku grid containing 9 x 9 kivy Buttons
        # whose text is updated with the text of the current_number
        # (set by the numbuttons) Label.
        self.build_the_grid()

        # Create a string of possibles
        if self.ids.possibles:
            possibles_list = solver.print_possibles(self.grid)  
            possibles_str = ""
            for row, possibles_row in enumerate(possibles_list):
                possibles_str += f"[b]Row {row}:[/b]\n"
                for col, possibles in enumerate(possibles_row):
                    possibles_str += f"    col {col}: {possibles}\n"
            self.ids.possibles.text = possibles_str

    def build_the_grid(self):
        """Build the grid widget tree
        
           Adds a 3 by 3 GridLayout widget. Each layout 'square'
           contains a SudokuBlock widget (inherits BoxLayout)"""
        self.sudokugrid = GridLayout(
            cols=3,
            rows=3,
            orientation = "lr-tb",
            size_hint_x = 25 / 100
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
                        row = n * 3 + i
                        col = m * 3 + j
                        grid_button = GridButton(disabled=False)
                        # Bind the GridButton to a function which updates the
                        # label text to the active number:
                        grid_button.bind(
                            on_release=functools.partial(
                                self.update_grid_button,
                                row=row,
                                col=col
                            )
                        )

                        # If the number at position 'index' is set
                        # (i.e. is not zero), update the text of the
                        # corresponding GridButton and disable it:
                        if self.grid[row, col]:
                            grid_button.text = str(self.grid[row, col])
                            grid_button.disabled = True
                        # Add the GridButton to the SudokuBlock
                        sudoku_block.add_widget(grid_button)
        # Add the finalised sudoku grid (GridLayout) to the RootWidget
        self.add_widget(self.sudokugrid)

    def update_grid_button(self, instance: GridButton, row: int, col: int) -> None:
        """Update the GridButton text with the active number"""
        if self.ids.active_number.text:
            self.grid[row, col] = np.int64(self.ids.active_number.text)
            instance.text = str(self.ids.active_number.text)
            # print("active_number: ", self.ids.active_number.text)
        else:
            self.grid[row, col] = 0
            instance.text = ""

    def do_quit(self):  # , *args):
        """Quit the application (triggered by the Quit button)"""
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)


class SudokuApp(App):
    """SudokuApp inherits kivy.app.App"""
    def __init__(self, grid: np.ndarray = np.zeros((9, 9), dtype=int)) -> None:
        super().__init__()
        self.grid = grid  # gets passed on to RootWidget
        self.kv_file = "kv/sudoku.kv"  # the kv file is in a separate directory

    def build(self):
        """Build the widget tree"""
        self.root = RootWidget(self.grid)
        return self.root

    def on_start(self):
        """Do stuff when the app starts"""

    def on_stop(self):
        """Do stuff when the app quits"""
        print("Bye bye!")


if __name__ == "__main__":
    pass
