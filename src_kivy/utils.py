__doc__ = """Utility functions"""
__author__ = "mier"
__version__ = "0.1"
__all__ = ["debug_msg",
           "err_msg",
           "sys_msg",
           "parse_arguments", 
           "WINDOW_SIZE"]

import argparse
import inspect
import sys

# import os
# import re
# import subprocess
# import time

# import glob
# import pathlib
# import shlex
# import shutil


# Root window geometry
HEIGHT = 600
WIDTH = 1000
WINDOW_SIZE = f"{WIDTH}x{HEIGHT}"


def debug_msg(*args):
    """Utility function. Prints debugging info on stderr"""
    msg = ' '.join(args)
    caller = inspect.stack()[1].function
    if caller == "<module>":
        caller = "main"
    print(f"({caller}) {msg}", file=sys.stderr)


def err_msg(*args):
    """Utility function. Prints a message on stderr"""
    msg = ' '.join(args)
    caller = inspect.stack()[1].function
    if caller == "<module>":
        caller = "main"
    print(f"({caller}) {msg}", file=sys.stderr)


def sys_msg(*args):
    """Utility function. Prints a message on stdout"""
    msg = ' '.join(args)
    caller = inspect.stack()[1].function
    if caller == "<module>":
        caller = "main"
    print(f"({caller}) {msg}", file=sys.stdout)


def parse_arguments():
    """Parse command line options and positional arguments"""
    parser = argparse.ArgumentParser(add_help=True,
                                     description="sudoku game",
                                     prog="sudoku"
    )
    help_dict = {
        'debug': 'Print debug info',
        'filename': """Path to a file containing a sudoku grid – nine rows and
                       nine columns, each containing a comma-separated,
                       list of integers (0-9, where 0 means an empty square""",
        'nremove': "Number of squares to remove from the completed grid "
                   "(roughly: level of difficulty)",
        'save': "Save the generated grid to disk",
        'verbose': "Enable verbose output",
        'winsize': f"Window size; default={WINDOW_SIZE}"
    }

    parser.add_argument('--winsize',
                        default=WINDOW_SIZE,
                        help=help_dict['winsize'])
    parser.add_argument('-d', '--debug',
                        default=False,
                        action='store_true',
                        help=help_dict['debug'])
    parser.add_argument('-n', '--nremove',
                        default=50,
                        type=int,
                        help=help_dict['nremove'])
    parser.add_argument('-s', '--save',
                        default=False,
                        action='store_true',
                        help=help_dict['save'])
    parser.add_argument('-v', '--verbose',
                        default=False,
                        action='store_true',
                        help=help_dict['verbose'])
    parser.add_argument('-f', '--filename',
                        type=argparse.FileType('r'),
                        default=None,
                        required=False,
                        help=help_dict['filename'],
                        metavar="path")
    try:
        args = parser.parse_args()
        # Return arguments as an argparse.Namespace object
        return args
    except argparse.ArgumentError as e:
        err_msg(f"Caught argparse.ArgumentError: {e}")
        pass


