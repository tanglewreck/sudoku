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
WINDOW_SIZE = f"WIDTHxHEIGHT"



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
    parser = argparse.ArgumentParser(
                                      add_help=True,
                                      description="sudoku ftw utility"
    )
    parser.add_argument('--winsize', default=WINDOW_SIZE)
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('-f', '--filename', type=argparse.FileType('r'), default=None, required=False)
    try:
        args = parser.parse_args()
        # Return arguments as an argparse.Namespace object
        return args
    except argparse.ArgumentError as e:
        err_msg(f"Caught argparse.ArgumentError: {e}")
        pass


