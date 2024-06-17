__doc__ = """sudoku graphics (tkinter) stuff"""
__author__ = "mier"
__version__ = "0.1"
__all__ = ["SudokuGame"]

import argparse
import inspect
import os
import re
import subprocess
import sys
import time

from sudokuutils import *
import sudokuwidgets 

# import glob
# import pathlib
# import shlex
# import shutil

# Root geometry
R_HEIGHT = 1000
R_WIDTH = 1500
R_X = 100
R_Y = 0
ROOT_GEOMETRY = f"{R_WIDTH}x{R_HEIGHT}+{R_X}+{R_Y}"

def foo():
    """foo function"""
    pass

class SudokuGame():

    def __init__(self, geometry=ROOT_GEOMETRY, debug=False):
        self.debug = debug

        # <Decode geometry>
        regexp = r"^(\d+)x(\d+)\+(\d+)\+(\d+)$"
        try:
            (self.root_height,
             self.root_width,
             self.root_x,
             self.root_y) = re.search(regexp, geometry).groups()
        except AttributeError as e:
            print("Unable to decode geometry argument")
            sys.exit(1)

        if self.debug:
            print(f"({__name__}) geometry: {geometry}")
            print(f"({__name__}) geometry (decoded): {self.root_height} x {self.root_width} + {self.root_x} + {self.root_y}")

        # Create and configure the tk widgets.
        # The instance variables are used inside the sudoku class 
        (self.root, self.content) = sudokuwidgets.create_widgets(geometry, debug)


    def mainloop(self):
        """Start the mainloop of the tk root widget"""
        self.root.mainloop()

