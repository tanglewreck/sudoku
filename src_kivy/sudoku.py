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
import kivy
import numpy as np

import solver
from utils import debug_msg, err_msg, sys_msg, parse_arguments

from kivy.app import App
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

kivy.require("2.0.0")


class NumberPadButton(Button):
    """Number pad buttons"""


class GridButton(Button):
    """Sudoku grid buttons"""


class SudokuBlock(GridLayout):
    """The sudoku grid buttons are wrapped within 3 x 3 GridLayouts"""


class RootWidget(GridLayout):
    """RootWidget: Sudoku grid with a numerical keypad on the right"""

    def __init__(self, puzzle: np.ndarray, solution: np.ndarray) -> None:
        super().__init__()

        self.puzzle: np.ndarray = puzzle
        self.solution: np.ndarray = solution

        # Create the sudoku grid containing 9 x 9 kivy Buttons
        # whose text is updated with the text of the current_number
        # (set by the numbuttons) Label.
        self.build_the_grid()


    def build_the_grid(self):
        """Creates a 3 by 3 grid of 3 by 3 GridLayout widgets. Each layout 'square'
           contains a SudokuBlock widget (inherits BoxLayout)"""
        self.sudokugrid = GridLayout(
            cols=3,
            rows=3,
            orientation = "lr-tb",
            size_hint_x = 25 / 100
        )
        # Add grid buttons with text set to value of self.puzzle[index].
        # Also bind each button to 'self.update_gridbutton()'.
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
                        if self.puzzle[row, col]:
                            grid_button.text = str(self.puzzle[row, col])
                            grid_button.disabled = True
                        # Add the GridButton to the SudokuBlock
                        sudoku_block.add_widget(grid_button)
        # Add the finalised sudoku grid (GridLayout) to the RootWidget
        self.add_widget(self.sudokugrid)

    def update_grid_button(self, instance: GridButton, row: int, col: int) -> None:
        """Update the GridButton text with the active number
           Also update the puzzle array at that location"""
        if self.ids.active_number.text:
            self.puzzle[row, col] = np.int64(self.ids.active_number.text)
            instance.text = self.ids.active_number.text
        else:
            self.puzzle[row, col] = 0
            instance.text = ""

        # Is the puzzle completed?
        # if self.puzzle.all() == self.solution.all():
        if np.array_equal(self.puzzle, self.solution):
            sys_msg(self.puzzle)
            print()
            sys_msg(self.solution)
            sys_msg("You got it!")
            self.ids.instructions_header.text = "[b][color=#ff2000][size=50]Grattis![/size][/color][/b]"
            self.ids.instructions_body.text = "[b][color=#ff2000]Klicka på 'Nytt spel' för att spela igen[/color][/b]"


    def do_quit(self):  # , *args):
        """Quit the application (triggered by the Quit button)"""
        sys_msg("See ya!")
        raise SystemExit(0)

    def do_restart(self):
        sys_msg("New game coming up")
        # subprocess.run("python main.py", shell=True)


class SudokuApp(App):
    """SudokuApp inherits kivy.app.App"""
    def __init__(self, puzzle: np.ndarray = np.zeros((9, 9), dtype=int),
                 solution: np.ndarray = np.zeros((9, 9), dtype=int)) -> None:
        super().__init__()
        self.puzzle = puzzle        # passed on to RootWidget
        self.solution = solution    # passed on to RootWidget
        self.kv_file = "kv/sudoku.kv"  # the kv file is in a separate directory
        self.actions = []           # stack for undo functionality

    def build(self):
        """Build the widget tree"""
        self.root = RootWidget(self.puzzle, self.solution)
        return self.root

    def on_start(self):
        """Do stuff when the app starts"""

    def on_stop(self):
        """Do stuff when the app quits"""
        print("Bye bye!")


if __name__ == "__main__":
    print("(You'd be better off running main.py...")
    pass
