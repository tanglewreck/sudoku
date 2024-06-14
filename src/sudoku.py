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
        with open("../dn_2024-06-11_hard.sudoku", 'r') as f:
            while row := f.readline():
                nrow = list(map(int, re.findall(r"\d+", row)))
                rows.append(nrow)
            if debug:
                for row in rows:
                    debug_msg(row)
    except OSError as e:
        err_msg(e)
    return rows


def main():
    args = parse_arguments()
    rows = read_game_file(args.filename, debug=args.debug)

    print(rows)

if __name__ == "__main__":
    main()
