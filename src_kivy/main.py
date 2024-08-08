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
from kivy.properties import ObjectProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

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
# Read the (local) configuration file, change stuff to our liking, then write it.
Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")
Config.set('kivy', 'exit_on_escape', 1)
Config.set('kivy', 'log_enable', 1)
Config.set('kivy', 'window_icon', "mier_347x437.jpg")
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'resizable', 1)
Config.set('graphics', 'position', 'auto')
Config.set('graphics', 'left', 500)         # ignored when 'position' == 'auto'
Config.set('graphics', 'top', 100)          # ignored when 'position' == 'auto'
# log_level := 'debug'|'info'|'warning'|'error'|'critical'
Config.set('kivy', 'log_level', "warning")
Config.write()
# Re-read the config (restart is needed to change the  window_icon):
# Config.read(f"{HOME}/Proj/sudoku/src_kivy/.kivy/config.ini")

# Config.set('modules', 'monitor', '')
# Config.set('modules', 'touchring', '')
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# </KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =


# The size of the root window can be set thus:
# Window.size = (1000, 600)
# or thus (using 'WINDOW_SIZE' set in utils.py):
# Window.size = WINDOW_SIZE


class NumberPadButton(Button):
    pass


class BoardButton(Button):
    pass


class SudokuBlock(GridLayout):
    """A 3x3 GridLayout with custom background colour"""
    pass


class SudokuBlockLight(SudokuBlock):
    """A lighter/brighter version of SudokuBlock"""
    pass


# RootWidget: The root of our widget tree: a sudoku board
#             with a numerical keypad on the right
class RootWidget(GridLayout):
    # note = False
    the_board = ListProperty()

    def __init__(self, board:np.ndarray=None, debug:bool=None) -> None:
        super(RootWidget, self).__init__()

        self.board = board

        # Add a 3 by 3 GridLayout widget 
        self.sudokuboard = GridLayout(cols=3, rows=3,
                                       orientation="lr-tb",
                                       size_hint_x=3/8)
        
        print(self.ids.active_number.text)

        # Add board buttons with text set to the corresponding
        # self.board[index] value. Also bind each button to the
        # 'update_boardbutton' function.
        self.blocks = list()
        self.board_buttons = list()


        # Add board buttons and match indices...
        for n in range(3):
            row_blocks = list()
            button_list = list()
            for m in range(3):
                block = SudokuBlock(orientation='lr-tb')
                row_blocks.append(block)
                self.sudokuboard.add_widget(block)
                print(f"(n, m) = ({n}, {m})")
                # Add buttons to the SudokuBlock.
                # Each button should have an index matching the (numpy) index
                # of self.board...
                for i in range(3):
                    for j in range(3):
                        index = (n * 3 + i, m * 3 + j)
                        button = BoardButton()
                        button_list.append(button)
                        # debug_msg(str(self.board[index]))
                        button.bind(on_release=functools.partial(self.update_boardbutton, index=index))
                        if self.board[index]:
                            button.text = str(self.board[index])
                        block.add_widget(button)
                    self.board_buttons.append(button_list)
            self.blocks.append(row_blocks)

        self.add_widget(self.sudokuboard)
        # print(self.blocks[0][0].children[0].text)
        print(len(self.board_buttons))
                

        if not self.board.all():
            pass
            # print(self.board)
            # self.populate_board()
            # self.the_board.append = list(self.board[0])
            # for r in self.board:
            #    self.the_board.append(list(r))
            # print(self.the_board[4][3])
            
    def populate_board(self):
        for k in range(9):
            for l in range(9):
                id = f"s{k}{l}"
                if self.board[k, l]:
                    # self.ids["s" + str(k) + str(l)].text = str(self.board[k,l])
                    # self.ids[id].text = str(self.board[k,l])
                    # self.ids[id].disabled = True
                    print(f"{self.board[k, l]} ", end="")
                else:
                    # self.ids["s" + str(k) + str(l)].text = ""
                    # self.ids[id].text = ""
                    print("0 ", end="")
            print()

    def do_quit(self, *args):
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)

    def update_boardbutton(self, instance, id=None, index=None):
        print("fubar")
        if self.ids.active_number.text:
            print("active_number: ", self.ids['active_number'].text)
            self.board[index] = int(self.ids['active_number'].text)
            instance.text = str(self.ids.active_number.text)
            print(str(self.ids.active_number.text))
        print("instance:", instance)
        print("instance.text:", instance.text)
        print(index)
        print(self.board[index])
        # print(self.ids.block11)
        # block11 = self.ids.block11
        # block11.add_widget(BoardButton(text='xx'))
        # block11.add_widget(BoardButton(text='xy'))
        # block11.add_widget(BoardButton(text='yy'))
        # block41 = SudokuBlock()
        # print(block41)
        # print(self.board[index])
        # self.ids['s05'].text = "99"
        # print(type(self))

    # def root_do_update(self, text):
        # Set the text of the Label:
        #                   <BoxLayoyt>
        #                   |      <AnchorLayoyt>
        #                   |      |
        # self.r00t= self.parent.parent
        # if text in string.digits:
        #     self.r00t.children[2].children[0].text = text
        # else:
        #    self.r00t.children[2].children[0].text = ""
        # print("root_do_update")




class SudokuApp(App):

    def __init__(self, board=np.zeros((9, 9), dtype=int), debug=None, **kwargs):
        super(SudokuApp, self).__init__(**kwargs)
        self.debug = debug # gets passed on to RootWidget in self.build() below
        self.board = board # gets passed on to RootWidget in self.build() below
        self.kv_file = "kv/sudoku.kv"

    def build(self):
        self.root = RootWidget(self.board, self.debug)
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
