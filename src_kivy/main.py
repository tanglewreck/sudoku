#!/usr/bin/env python3

# KIVY_NO_ARGS = 1

import kivy
kivy.require("2.0.0")

from kivy.config import Config 

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput

from  utils import debug_msg, err_msg, sys_msg
from  utils import parse_arguments
from  utils import WINDOW_SIZE

import sys

# Config.set('modules', 'monitor', '')
# Config.set('modules', 'touchring', '')

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


class BoardButton(Button):
    def __init__(self, **kwargs):
        super(BoardButton, self).__init__(**kwargs)


class SudokuWidgets(BoxLayout):


    def __init__(self, **kwargs):
        super(SudokuWidgets, self).__init__(**kwargs)
        # print("self.kv_file =", self.kv_file)
        # print("self.__class__.__name__ =", self.__class__.__name__)  # -> "Sudoku"

        # self.cols = 2
        # self.rows = 2
        # self.row_force_default = True
        # self.row_default_height = 1000
#
#        username_label = Label(text='Username')
#        self.add_widget(username_label)
#
#        self.username = TextInput(multiline=False)
#        self.add_widget(self.username)
#
#        password_label = Label(text='Password')
#        self.add_widget(password_label)
#
#        self.password = TextInput(password=True, multiline=False)
#        self.add_widget(self.password)

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
