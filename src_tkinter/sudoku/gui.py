__doc__ = """Sudoku game GUI"""
__all__ = ["SudokuGUI"]
__author__ = "Mikael Eriksson"

# import re

from tkinter import *
from tkinter import ttk

from . utils import debug_msg, err_msg, sys_msg
from . utils import ROOT_GEOMETRY

from . widgets import SudokuWidgets
from . board import Sudoku


class SudokuGUI():
    """A class representing the graphical interface of a sudoku game"""

    def __init__(self, sudoku:Sudoku, geometry:str=ROOT_GEOMETRY, debug=False):
        self.debug = debug
        self.sudoku = sudoku
        self.board = self.sudoku.board
        self.widgets = SudokuWidgets(geometry=geometry, debug=self.debug)


    def mainloop(self):
        self.widgets.root.mainloop()


    def numkeypad(self):
        pass
        
    def populate(self):
        """Populate the content frame with numbers"""

        def change_text(m,n):
            """Call-back function for the board buttons; changes the text 
            of the button to the current value of 'current_number'"""
            self.board_buttons[m][n]['text'] = self.widgets.current_number.get()
            

        if self.debug:
            debug_msg(f"\n{self.sudoku.board}")

        # Create a list of lists of Sudoku number labels (buttons)
        self.board_buttons = list()
        for i in range(9):
            l = list()
            for j in range(9):
                l.append(ttk.Button(self.widgets.content,
                                    command=lambda m=i, n=j: change_text(m,n),
                                    text=f"{self.sudoku.board[i][j]}"
                                    )
                         )
            self.board_buttons.append(l)

        # Place the number labels (buttons) using grid())
        for i in range(9):
            for j in range(9):
                self.board_buttons[i][j]['style'] = 'SudokuBoard_boardbutton.TButton'
                self.board_buttons[i][j].grid(column=j, row=i, sticky=(E,N,W,S))

    
if __name__ == "__main__":
    print(__doc__)
