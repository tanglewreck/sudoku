#!/usr/bin/env python3
"""Example grids"""

__version__ = "2024-08-21"

import numpy as np

GRID_1: np.ndarray = np.array(
    [[3, 0, 6, 5, 0, 8, 4, 0, 0],
     [5, 2, 0, 0, 0, 0, 0, 0, 0],
     [0, 8, 7, 0, 0, 0, 0, 3, 1],
     [0, 0, 3, 0, 1, 0, 0, 8, 0],
     [9, 0, 0, 8, 6, 3, 0, 0, 5],
     [0, 5, 0, 0, 9, 0, 6, 0, 0],
     [1, 3, 0, 0, 0, 0, 2, 5, 0],
     [0, 0, 0, 0, 0, 0, 0, 7, 4],
     [0, 0, 5, 2, 0, 6, 3, 0, 0]]
)

GRID_2: np.ndarray = np.array(
    [[0, 0, 0, 5, 1, 0, 0, 0, 8],
     [5, 0, 0, 8, 0, 0, 0, 6, 7],
     [0, 0, 0, 0, 0, 6, 3, 0, 9],
     [3, 0, 8, 0, 7, 0, 0, 0, 0],
     [0, 5, 0, 0, 0, 0, 4, 0, 0],
     [0, 0, 0, 0, 4, 8, 0, 0, 0],
     [0, 1, 0, 0, 8, 0, 0, 7, 0],
     [0, 0, 7, 6, 9, 1, 0, 0, 0],
     [0, 9, 0, 0, 0, 0, 0, 2, 0]]
)

GRID_2_1: np.ndarray = np.array(
    [[9, 3, 6, 5, 1, 7, 2, 4, 8],
     [5, 2, 4, 8, 3, 9, 1, 6, 7],
     [8, 7, 1, 4, 2, 6, 3, 5, 9],
     [3, 4, 8, 9, 7, 5, 6, 1, 2],
     [7, 5, 9, 1, 6, 2, 4, 8, 3],
     [1, 6, 2, 3, 4, 8, 7, 9, 5],
     [4, 1, 5, 2, 8, 3, 9, 7, 6],
     [2, 8, 7, 6, 9, 1, 5, 3, 4],
     [6, 9, 3, 7, 5, 4, 8, 2, 1]]
)


GRID_3: np.ndarray = np.array(
    [[8, 4, 0, 6, 0, 0, 0, 0, 1],
     [0, 0, 0, 0, 0, 0, 0, 0, 0],
     [0, 3, 0, 5, 4, 8, 0, 0, 0],
     [0, 5, 9, 0, 1, 0, 0, 8, 0],
     [7, 0, 0, 0, 0, 0, 2, 0, 0],
     [2, 0, 4, 0, 0, 0, 0, 9, 0],
     [0, 0, 0, 0, 6, 7, 0, 2, 0],
     [0, 8, 0, 0, 0, 4, 9, 5, 0],
     [0, 0, 0, 0, 0, 0, 7, 0, 0]]
)


