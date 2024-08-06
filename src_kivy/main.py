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
HOME = os.environ['HOME']

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
from kivy.properties import ColorProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import numpy as np
import sys

from utils import debug_msg, err_msg, sys_msg
from utils import parse_arguments
from utils import WINDOW_SIZE

# Read the (local) configuration file, change stuff to our liking, then write it.
Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")
Config.set('kivy', 'exit_on_escape', 1)
Config.set('kivy', 'log_enable', 1)
Config.set('kivy', 'window_icon', "mier_347x437.jpg")
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'auto')
Config.set('graphics', 'left', 500)         # ignored when 'position' == 'auto'
Config.set('graphics', 'top', 100)          # ignored when 'position' == 'auto'
# log_level := 'debug'|'info'|'warning'|'error'|'critical'
Config.set('kivy', 'log_level', "warning")
Config.write()
# Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")

# Config.set('modules', 'monitor', '')
# Config.set('modules', 'touchring', '')


# The size of the root window can be set thus:
# Window.size = (1000, 600)
# or thus (using 'WINDOW_SIZE' set in utils.py):
# Window.size = WINDOW_SIZE


class NumberPadButton(Button):
    def __init__(self, **kwargs):
        super(NumberPadButton, self).__init__(**kwargs)


class BoardButton(Button):
    def __init__(self, **kwargs):
        super(BoardButton, self).__init__(**kwargs)
    nn = StringProperty("1")
    pass
#    def __init__(self, **kwargs):
#        super(BoardButton, self).__init__(**kwargs)
#     def update_block_button(self, text):
#         #
#         # This is butt ugly! Gotta find a cleaner, neater, better way of
#         # updating the blockbutton text!
#         #
#         #           <SudokuBlock>
#         #                |      <GridLayout>
#         #                |      |      <RootWidget>
#         #                |      |      |      <BoxLayout>
#         #                |      |      |      |           <Label>
#         #                |      |      |      |           |
#         self.text = self.parent.parent.parent.children[0].children[1].text # the text property of the Label widget (i.e. active_number)


class SudokuBlock(GridLayout):
    """A 3x3 GridLayout with custom background colour"""
    pass


class SudokuBlockLight(SudokuBlock):
    """A lighter/brighter version of SudokuBlock"""
    pass


# RootWidget: The root of our widget tree: a sudoku board
#             with a numerical keypad on the right
class RootWidget(BoxLayout):
    nnn = StringProperty("2")
    lll = ListProperty()

    Active_Number = StringProperty("spam")
    print(Active_Number)
    N = NumericProperty(100)
    print(N)
    #if N:
    #    print("100 xyz")
    #    print(N)

    def __init__(self, board=None,
                 debug=None, **kwargs):
        super(RootWidget, self).__init__(**kwargs)
        self.board = board
        if not self.board.all():
            sys_msg("non-zero b")
            print(board)
            for i in range(9):
                self.lll.append(list(self.board[i]))
            for i in range(9):
                for j in range(9):
                    print(self.lll[i][j], end="")
                print()
            # print(" ".join(self.lll[0]))
            # self.lll = self.board
            #self.lll = "apa"
            l = list()
            self.ids['s11'].text = str(self.board[0][0])
            self.ids['s12'].text = str(self.board[0][1])
            self.ids['s13'].text = str(self.board[0][2])
            for k in range(9):
                for l in range(9):
                    id = f"s{k}{l}"
                    if self.board[k,l]:
                        # self.ids["s" + str(k) + str(l)].text = str(self.board[k,l])
                        self.ids[id].text = str(self.board[k,l])
                        self.ids[id].disabled = True
                    else:
                        # self.ids["s" + str(k) + str(l)].text = ""
                        self.ids[id].text = ""


            
        # pass
    def f_s11(self, n):
        n = int(n)
        print(n + 1)
        # print(self.thenumber.text)
        # self.s11 = self.thenumber.text
        self.s11x.text = str(n + 1)
        print(self.block11.text)
        print(self.ids['s12'].text)

    def do_quit(self, *args):
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)

    def foo(self):
        print("fubar")
        print(type(self))


class SudokuApp(App):

    def __init__(self, board=np.zeros((9, 9), dtype=int), debug=None, **kwargs):
        super(SudokuApp, self).__init__(**kwargs)
        self.debug = debug # gets passed on to RootWidget in self.build() below
        self.board = board # gets passed on to RootWidget in self.build() below
        #if not self.board.all():
        #    print("The board:")
        #    print(self.board)
        #else:
        #    print(self.board)
        #
        # Which .kv file to use:
        #
        # self.kv_directory = "/Users/mier/Proj/sudoku/src_kivy/kv/"
        # self.kv_file = "/Users/mier/Proj/sudoku/sudoku.kv"
        # self.kv_file = "/Users/mier/Proj/sudoku/src_kivy/sudoku.kv"
        self.kv_file = "kv/sudoku.kv"

    def build(self):
        self.root = RootWidget(self.board, self.debug)
        # self.icon = 'mier_347x437.jpg' # Use our own window icon
        return self.root

    def on_start(self):
        print("Hello : ) ")

    def on_stop(self):
        print("Bye bye!")


if __name__ == "__main__":
    args = parse_arguments()
    if args.filename:
        if args.debug:
            sys_msg("args.filename:", args.filename.name)
            print(type(args.filename))
        try:
            board = np.loadtxt(args.filename.name, delimiter=",", dtype=int)
        except OSError as e:
            print(e)
        SudokuApp(board, debug=args.debug).run()
    else:
        SudokuApp(debug=args.debug).run()
