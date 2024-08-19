#!/usr/bin/env python3
'''
Run 'pycodestyle --ignore=E501,E402 --show-source main.py' to
check for PEP8 compliancy (ignoring E501 because it's stupid
and E402 because we have to; see NOTE below).
'''

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# <ENVIRONMENT VARIABLES>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
import os

# NOTE: KIVY_HOME must be set *before* kivy is imported,
# thereby breaking the PEP8 recommendation to put
# module level imports at the top (E402):
os.environ['KIVY_HOME'] = "./.kivy"
HOME = os.environ['HOME']  # Needed for the path to the kivy config file

# Make kivy ignore command-line arguments so that we don't have to put '--'
# before our own options/arguments
os.environ['KIVY_NO_ARGS'] = 'yes'

# os.environ['KIVY_WINDOW'] = 'x11'
# os.environ['KIVY_WINDOW'] = 'egl_rpi'
# import pygame
# os.environ['KIVY_WINDOW'] = 'pygame'
# os.environ['KIVY_WINDOW'] = 'sdl2'
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# </ENVIRONMENT VARIABLES>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

import kivy
kivy.require("2.0.0")

from kivy.app import App
from kivy.config import Config
from kivy.core.window import Window
from kivy.graphics import Color, Rectangle
from kivy.properties import ColorProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget

import functools
import numpy as np
import string
import sys

from utils import debug_msg, err_msg, sys_msg
from utils import parse_arguments
from utils import WINDOW_SIZE

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# <KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Read the (local) configuration files and change stuff to our liking.
# NOTE: Changes require a restart to take effect
Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")
Config.set('kivy', 'exit_on_escape', 1)
Config.set('kivy', 'log_enable', 1)
Config.set('kivy', 'window_icon', "data/mier_347x437.jpg")
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 1000)
# Config.set('graphics', 'height', 480)
# Config.set('graphics', 'width', 800)
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'position', 'custom')  # auto|custom
Config.set('graphics', 'left', 100)         # ignored when 'position' == 'auto'
Config.set('graphics', 'top', 100)          # ignored when 'position' == 'auto'
Config.set('kivy', 'log_level', "warning")  # debug|info|warning|error|critical
Config.write()

# Config.set('modules', 'monitor', '')
# Config.set('modules', 'touchring', '')
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# </KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


class ButtonBG(Widget):
    def __init__(self):
        super(ButtonBG, self).__init__()
        with self.canvas.before:
            Color(1, 1, 1, 1)
            Rectangle(pos=self.pos, size=self.size)
        with self.canvas:
            Color(1, 1, 1, 0.3)
            Rectangle(pos=self.pos, size=self.size)
        self.background_color = (1, 1, 1, 1)


class NumberPadButton(Button):
    """Number pad buttons"""
    pass
    #def __init__(self, **kwargs):
    #    super(NumberPadButton, self).__init__(**kwargs)


class BoardButton(Button):
    """Sudoku board buttons"""
    pass


class SudokuBlock(GridLayout):
    """The sudoku board buttons are wrapped within 3 x 3 GridLayouts"""
    def __init__(self, **kwargs):
        super(SudokuBlock, self).__init__(**kwargs)


class RootWidget(GridLayout):
    """RootWidget: Sudoku board with a numerical keypad on the right"""
    # note = False
    the_board = ListProperty()
    active_number = NumericProperty()
    active_number_string = StringProperty()

    def __init__(self, board: np.ndarray = None, debug: bool = None) -> None:
        super(RootWidget, self).__init__()

        self.debug = debug
        self.board = board
        self.build_the_board()
        # self.add_gridbutton()

        if self.debug:
            print(self.board)

    def build_the_board(self):
        """Build the board widget tree"""
        # Add a 3 by 3 GridLayout widget
        self.sudokuboard = GridLayout(cols=3, rows=3,
                                      orientation="lr-tb",
                                      size_hint_x=3 / 8)
        # Add board buttons with text set to the corresponding
        # self.board[index] value. Also bind each button to the
        # 'update_boardbutton' function.
        for n in range(3):
            for m in range(3):
                sudoku_block = SudokuBlock(orientation='lr-tb')  # SudokuBlocks
                self.sudokuboard.add_widget(sudoku_block)
                for i in range(3):
                    for j in range(3):
                        index = (n * 3 + i, m * 3 + j)  # Index in the grand total GridLayout
                        board_button = BoardButton(disabled=False)  # BoardButton
                        # Bind the BoardButton to a function which updates the
                        # label text to the active number:
                        board_button.bind(on_release=functools.partial(self.update_board_button, index=index))

                        # If the number at position 'index' is set (i.e. is not zero),
                        # update the text of the corresponding BoardButton and disable it:
                        if self.board[index]:
                            board_button.text = str(self.board[index])
                            board_button.disabled = True
                        # Add the BoardButton to the SudokuBlock
                        sudoku_block.add_widget(board_button)
        # Add the finalised sudoku board (GridLayout) to the RootWidget
        self.add_widget(self.sudokuboard)

    # Update the BoardButton text with the active number
    def update_board_button(self, instance: BoardButton, index: tuple) -> None:
        if self.debug:
            print("index: ", index)
            print("instance.text (pre):", instance.text)
            print(f"self.board[{index}]:", self.board[index])
            print(f"self.ids.active_number.text:", self.ids.active_number.text)
            print(self.board)
        if self.ids.active_number.text:
            self.board[index] = int(self.ids.active_number.text)
            instance.text = str(self.ids.active_number.text)
            # print("active_number: ", self.ids.active_number.text)
        else:
            self.board[index] = 0
            instance.text = ""

        if self.debug:
            print("instance.text (post):", instance.text)

    # Quit the application (triggered by the Quit button)
    def do_quit(self, *args):
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)


class SudokuApp(App):

    def __init__(self, board: np.ndarray = np.zeros((9, 9), dtype=int), debug: bool = None) -> None:
        super(SudokuApp, self).__init__()
        self.debug = debug  # gets passed on to RootWidget
        self.board = board  # gets passed on to RootWidget
        self.kv_file = "kv/sudoku.kv"  # the kv file is in a separate directory

    def build(self):
        self.root = RootWidget(self.board, self.debug)
        return self.root

    def on_start(self):
        pass

    def on_stop(self):
        print("Bye bye!")


if __name__ == "__main__":
    # Parse and get command line arguments
    args = parse_arguments()
    debug = args.debug

    # Load the sudoku board file, if provided on the command line
    if args.filename:
        if debug:
            debug_msg("args.filename:", args.filename.name)
        try:
            board = np.loadtxt(args.filename.name, delimiter=",", dtype=int)
        except OSError as e:
            print(e)
        SudokuApp(board, debug=debug).run()
    else:
        SudokuApp(debug=debug).run()
