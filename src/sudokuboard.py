__doc__ = """sudoku graphics (tkinter) stuff"""
__author__ = "mier"
__version__ = "0.1"
__all__ = ["Sudoku"]

import argparse
import inspect
import numpy as np
import os
import re
import subprocess
import sys
import time

from utils import debug_msg, err_msg, sys_msg

# import glob
# import pathlib
# import shlex
# import shutil


class Sudoku():

    def __init__(self, board=None, filename=None, debug=False):
        self.debug = debug

#        if not filename is None:
#            self.load_board(filename)
#        elif not board is None:
#            self.board = np.array(board, dtype=int)
#        else:
#            self.board = np.zeros((9,9), dtype=int)
#
#        if not self.validate_board():
#            err_msg("Invalid entry/entries found – aborting")
#            raise SystemExit(1)


    def __str__(self):
        return str(self.board)


    def load_board(self, filename, debug=False):
        if filename is None:
            self.board = np.zeros((9, 9), dtype=int)
        else:
            if self.debug:
                debug_msg(f"filename = {filename}")
            try:
                self.board = np.loadtxt(filename, delimiter=",", dtype=int)
                if not self.validate_format():
                    err_msg("Invalid board entry/entries found – aborting")
                    raise SystemExit(1)
                if not self.validate_board():
                    sys_msg("Invalid row found")
            except ValueError as e:
                err_msg(f"Unable to load game file ({filename}): invalid entries found ({e})")
                raise SystemExit(1)
            except OSError as e:
                err_msg(e)
                raise SystemExit(1)


    def save_board(self, filename):
        try:
            np.savetxt(filename, self.board, delimiter=",", fmt='%d')
        except OSError as e:
            err_msg(e)

    def validate_format(self):
        """Check that the board contains only integers btw. 0 and 9"""
        for row in range(9):
            if self.debug:
                sys_msg(f"{self.board[row,]}")
            for col in range(9):
                if not 0 <= self.board[row, col] <=9:
                    err_msg(f"Invalid entry ({row}, {col}): {self.board[row, col]}")
                    return False
        return True

    def validate_board(self):
        """Check that each square contains a number btw. 0 (representing an
        empty square) and 9"""

        def validate_row(row):
            """Check that a row contains at most one instance of a number
            (excluding the number zeror, representing an empty square"""
            valid = True
            try:
                # Count the number of occurrences of 0's, 1's, etc.
                count = {}
                for col in range(10):
                    count[col] = 0
                for col in self.board[row]:
                    count[col] += 1
                for col in range(1,10):
                    if self.debug:
                        sys_msg(f"row = {row}, column = {col}, count = {count[col]}")
                    if count[col] > 1:
                        sys_msg(f"row = {row + 1} not valid")
                        valid = False
            except IndexError as e:
                err_msg(e)
            return valid

        valid = True
        for row in range(9):
            if not validate_row(row):
                valid = False
        return valid


    def set_value(self, row:int, col:int, value):
        try:
            if 1 <= value <= 9:
                self.board[row, col] = 9
                return True
            else:
                return False
        except (IndexError, ValueError) as e:
            err_msg(e)

    def get_value(self, row:int, col:int):
        pass
