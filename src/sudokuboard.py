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

        if board is None and filename is None:
            self.board = np.zeros((9,9), dtype=int)
        elif not board is None:
            self.board = np.array(board, dtype=int)
        elif not filename is None:
            self.load_board(filename)

        if not self.validate_board(self.board, debug=debug):
            err_msg("Invalid entry/entries found – aborting")
            raise SystemExit(1)


    def __str__(self):
        return str(self.board)


    def load_board(self, filename, debug=False):
        if debug:
            debug_msg(f"filename = {filename}")

        try:
            self.board = np.loadtxt(filename, delimiter=",", dtype=int)
            if not self.validate_board(self.board):
                err_msg(f"Failed to validate board (file = \"{filename}\")")
        except ValueError:
            err_msg(f"Unable to load game file ({filename}): invalid entries found")
        except OSError as e:
            err_msg(e)


    def save_board(self, board, filename):
        try:
            np.savetxt(filename, board, delimiter=",", fmt='%d')
        except OSError as e:
            err_msg(e)


    def validate_board(self, board, debug=False):
        debug = False
        valid = True
        for row in range(9):
            if debug:
                print(board[row,])
            for col in range(9):
                if not 0 <= board[row, col] <=9:
                    err_msg(f"Invalid entry ({row}, {col}): {board[row, col]}")
                    valid = False
        return valid


    def set_value(self, row, col, value):
        try:
            if 1 <= value <= 9:
                self.board[row, col] = 9
                return True
            else:
                return False
        except (IndexError, ValueError) as e:
            err_msg(e)

