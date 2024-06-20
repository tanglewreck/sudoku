__doc__ = """Sudoku game GUI"""
__all__ = ["SudokuGUI"]
__author__ = "Mikael Eriksson"

# import re

from tkinter import *
from tkinter import ttk

from utils import debug_msg, err_msg, sys_msg
from utils import ROOT_GEOMETRY

from sudokuWidgets import SudokuWidgets
from sudokuboard import Sudoku


class SudokuGUI():
    """A class representing the graphical interface of a sudoku game"""

    def __init__(self, sudoku_game:Sudoku, geometry:str=ROOT_GEOMETRY, debug=False):
        self.debug = debug
        self.widgets = SudokuWidgets(sudoku_game=sudoku_game, geometry=geometry, debug=self.debug)
        self.sudoku = sudoku_game
        self.board = sudoku_game.board


    def mainloop(self):
        self.widgets.root.mainloop()


    def populate(self, sudoku_game, debug=False):
        """Populate the content frame with numbers"""

        if debug:
            debug_msg(f"\n{self.board}")

        # Create a list of lists of Sudoku number labels
        L = list()
        for i in range(9):
            l = list()
            for j in range(9):
                l.append(ttk.Label(self.widgets.content, text=f"{self.board[i][j]}"))
            L.append(l)

        # Place the number labels using grid())
        for i in range(9):
            for j in range(9):
                L[i][j]['style'] = 'SudokuBoard.TLabel'
                L[i][j].grid(column=j, row=i, sticky=(E,N,W,S))
        
    
if __name__ == "__main__":
    print(__doc__)
