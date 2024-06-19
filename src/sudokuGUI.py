"""Sudoku game GUI"""

__all__ = ["SudokuGUI"]
__author__ = "Mikael Eriksson"

# import re

from tkinter import *
from tkinter import ttk

from utils import debug_msg, err_msg, sys_msg
from utils import ROOT_GEOMETRY

import widgets 


class SudokuGUI():

    def __init__(self, sudoku_game, geometry=ROOT_GEOMETRY, debug=False):
        widgets.validate_geometry(geometry, debug=debug)
        (self.root, self.content) = widgets.create_widgets(geometry=geometry, debug=debug)
        self.sudoku = sudoku_game
        self.debug = debug
        self.board = sudoku_game.board


    def mainloop(self):
        self.root.mainloop()


    def populate(self, sudoku_game, debug=False):
        board = self.board
        if debug:
            debug_msg(f"\n{board}")
        # A list of lists of Sudoku number labels
        L = list()
        for i in range(9):
            l = list()
            for j in range(9):
                l.append(ttk.Label(self.content, text=f"{board[i][j]}"))
            L.append(l)

        # Place the numbers 
        for i in range(9):
            for j in range(9):
                L[i][j]['style'] = 'SudokuBoard.TLabel'
                L[i][j].grid(column=j, row=i, sticky=(E,N,W,S))
        
    
if __name__ == "__main__":
    # (root, content) = create_widgets()
    # root.mainloop()
    print(__doc__)
