__doc__ = """Utility functions"""
__author__ = "mier"
__version__ = "0.1"
__all__ = ["debug_msg", "err_msg", "parse_arguments", "sys_msg"]

import argparse
import inspect
import os
import re
import subprocess
import sys
import time

# import glob
# import pathlib
# import shlex
# import shutil

def debug_msg(msg=None):
    """Utility function. Prints debugging info on stderr"""
    caller = inspect.stack()[1].function
    print(f"({caller}) {msg}", file=sys.stderr)


def err_msg(msg=None):
    """Utility function. Prints a message on stderr"""
    caller = inspect.stack()[1].function
    print(f"({caller}) {msg}", file=sys.stderr)


def sys_msg(msg=None):
    """Utility function. Prints a message on stdout"""
    caller = inspect.stack()[1].function
    print(f"({caller}) {msg}", file=sys.stdout)


def parse_arguments():
    """Parse command line options and positional arguments"""
    parser = argparse.ArgumentParser(
                                      add_help=True,
                                      description="sudoku ftw utility"
    )
    parser.add_argument('-d', '--debug', default=False, action='store_true')
    parser.add_argument('filename')
    try:
        args = parser.parse_args()
        # Return arguments as an argparse.Namespace object
        return args
    except argparse.ArgumentError as e:
        err_msg(f"Caught argparse.ArgumentError: {e}")
        pass


