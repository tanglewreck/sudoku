#!/usr/bin/env python3

# KIVY_NO_ARGS = 1


# KIVY_HOME environment variable
import os
os.environ['KIVY_HOME'] = "./.kivy"  # Use local .kivy directory (for config, logs, etc.)

# 
from kivy.config import Config
# Read the configuration file and then change stuff to our liking
Config.read("/Users/mier/Proj/sudoku/src_kivy/.kivy/config.ini")  # 
Config.set('kivy', 'exit_on_escape', 1)                           # set to 0 to disable exit on escape
Config.set('kivy', 'log_enable', 1)                               # set to 0 to disable logging
Config.set('kivy', 'log_level', "warning")                        # possible values: 'debug', 'info', 'warning', 'error', 'critical'
Config.set('graphics', 'fullscreen', 0)                           #
Config.set('graphics', 'height', 600)                             #
Config.set('graphics', 'width', 1000)                             #
Config.set('graphics', 'resizable', 0)                            # set to 1 to enable 
Config.set('graphics', 'position', 'auto')                        # or 'custom'
Config.set('graphics', 'left', 500)                               # ignored when 'position' is set to 'auto'
Config.set('graphics', 'top', 100)                                # ignored when 'position' is set to 'auto'
Config.write()                                                    # save configuration for future reference

# Config.set('modules', 'monitor', '')
# Config.set('modules', 'touchring', '')

import kivy
kivy.require("2.0.0")


from kivy.app import App
from kivy.core.window import Window
from kivy.properties import ColorProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

import numpy as np

from  utils import debug_msg, err_msg, sys_msg
from  utils import parse_arguments
from  utils import WINDOW_SIZE

import sys

# class Sudoku(GridLayout):
# Window.size = (1000, 600)
# Window.size = WINDOW_SIZE


Active_Number = StringProperty("spam")
print("A_N:", str(Active_Number))
N = NumericProperty()
N = 100
# print(N)

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
    # pass


class NumberPadButton(Button):
    def __init__(self, **kwargs):
        super(NumberPadButton, self).__init__(**kwargs)


class BoardButton(Button):
    def __init__(self, **kwargs):
        super(BoardButton, self).__init__(**kwargs)
        # This seems to be ignored:
        # self.kv_file = "kv/boardbutton.kv"

#     Moved the .kv-file:
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
        

# class BoardButtonTest(BoardButton):
#    def __init__(self, **kwargs):
#        super(BoardButtonTest, self).__init__(**kwargs)


class SudokuBlock(GridLayout):
    """A 3x3 GridLayout with custom background colour"""
    pass

class SudokuBlockLight(SudokuBlock):
    """A lighter/brighter version of SudokuBlock"""
    pass


class RootWidget(BoxLayout):
    """A widget tree that draws a sudoku board with a numerical keypad on the right"""

    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

    def do_quit(self, *args):
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)

    # def on_enter(self, *args):
    #     print('User pressed enter in', args)

    # def on_focus(self, msg):
    #    print("got focus", msg)


class SudokuApp(App):
    def __init__(self, **kwargs):
        super(SudokuApp, self).__init__(**kwargs)
        # self.kv_directory = "/Users/mier/Proj/sudoku/src_kivy/kv/"
        # self.kv_file = "/Users/mier/Proj/sudoku/sudoku.kv"
        # self.kv_file = "/Users/mier/Proj/sudoku/src_kivy/sudoku.kv"
        self.kv_file = "kv/sudoku.kv"

    def build(self):
        self.root = RootWidget()
        self.icon = 'mier_347x437.jpg'
        return self.root

    def on_start(self):
        print("Starting up...")

    def on_resume(self):
        print("Resuming...")

    def on_stop(self):
        print("Bye bye!")


if __name__ == "__main__":
    args = parse_arguments()
    if args.filename:
        print(args.filename)
        print(type(args.filename))

    SudokuApp().run()
