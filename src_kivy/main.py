#!/usr/bin/env python3

# KIVY_NO_ARGS = 1


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
from kivy.uix.button import Button
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

class CustomLabel(Label):
    def __init__(self, **kwargs):
        super(CustomLabel, self).__init__(**kwargs)
    # pass


class NumberPadButton(Button):
    def __init__(self, **kwargs):
        super(NumberPadButton, self).__init__(**kwargs)
    def update_active_number(self, number):
        SudokuWidgets().ids['active_number'].text = number



class BoardButton(Button):
    def __init__(self, **kwargs):
        super(BoardButton, self).__init__(**kwargs)


class SudokuWidgets(BoxLayout):
    """A widget tree that draws a sudoku board with a numerical keypad on the right"""

    def __init__(self, **kwargs):
        super(SudokuWidgets, self).__init__(**kwargs)
        ### grid_1 = GridLayout(cols=3, rows=3, size_hint_x=10)
        ### b1 = Button(text="f00")
        ### grid_1.add_widget(b1)
        ### self.add_widget(grid_1)

        # if debug:
        #    print("self.__class__.__name__ =", self.__class__.__name__)  # -> "Sudoku"

    def update_active_number(self, number):
        self.ids['active_number'].text = number

    def update_label_text(self, id, text):
        print("updating")
        self.ids[id].text = text
        for id in self.ids:
            print(id)

    def on_enter(self, *args):
        print('User pressed enter in', args)


    def on_focus(self, msg):
        print("got focus", msg)


    def do_quit(self, *args):
        print("See ya!", file=sys.stderr)
        raise SystemExit(0)


class SudokuApp(App):
    def build(self):
        return SudokuWidgets()
        # return Sudoku(cols=2, rows=3)


    def on_start(self):
        print("Starting up...")


    def on_resume(self):
        print("Resuming...")


    def on_stop(self):
        print("bye bye")


if __name__ == "__main__":
    args = parse_arguments()
    if args.filename:
        print(args.filename)
        print(type(args.filename))
        # Window.size = args.geometry
        #print("SIZE", args.geometry)
        Window.size = win_size
        # for k in args.geometry.split(","):
        #    print(int(k))
        # print(type(args.geometry))
    SudokuApp().run()
