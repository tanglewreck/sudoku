#!/usr/bin/env python3

import inspect
import math
import numpy as np
import os
import re
import sys
from functions import *

DEBUG = False

def read_game_file(filename=None, debug=DEBUG):
    rows = []
    try:
        # with open("../dn_2024-06-11_hard.sudoku", 'r') as f:
        with open(filename, 'r') as f:
            while row := f.readline():
                nrow = list(map(int, re.findall(r"\d+", row)))
                rows.append(nrow)
            if debug:
                for row in rows:
                    debug_msg(row)
    except OSError as e:
        err_msg(e)
    return np.array(rows)


def print_board(board):
    print(" – – – – – – – – – – – –")
    for i, row in enumerate(board):
        # print(row)
        s = "| "
        for j, element in enumerate(row):
            s += str(element) + " "
            if (j + 1) % 3 == 0:
                s += "| "
        print(s)
        if (i + 1) % 3 == 0:
            print(" – – – – – – – – – – – –")

def main():
    args = parse_arguments()
    board = read_game_file(args.filename, debug=args.debug)

    blocks = []
    blocks.append(board[0:3, 0:3])
    blocks.append(board[0:3, 3:6])
    blocks.append(board[0:3, 6:9])

    blocks.append(board[3:6, 0:3])
    blocks.append(board[3:6, 3:6])
    blocks.append(board[3:6, 6:9])

    blocks.append(board[6:9, 0:3])
    blocks.append(board[6:9, 3:6])
    blocks.append(board[6:9, 6:9])

    for k, block in enumerate(blocks): 
        # print(block, end='    ')
        if k % 3 == 0:
            print()
        print(block)




if __name__ == "__main__":
    main()
