#!/usr/bin/env python3

import datetime
import functools
import kivy
import solver
import subprocess
import time
from utils import debug_msg, err_msg, sys_msg, parse_arguments

from kivy.app import App
from kivy.clock import Clock
from kivy.config import Config
from kivy.graphics import Color, Rectangle
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import StringProperty
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout

from kivy.uix.label import Label
from kivy.metrics import dp

kivy.require("2.0.0")


class RootWidget(GridLayout):
    # dt means delta-time
    def __init__(self, *args, **kwargs): 
        super().__init__()




class TimeApp(App):
    def my_callback(self, dt):
        now = str(datetime.datetime.now())
        self.l.text = now


    def __init__(self, *args, **kwargs):
        super().__init__()
        # call my_callback every * seconds
        Clock.schedule_interval(self.my_callback, 0.01)

    def build(self):
        """Build the widget tree"""
        self.root = RootWidget()
        self.root.cols = 1
        self.root.rows = 1
        self.root.padding = 0
        # self.root.size_hint = (None, None)
        self.root.size_hint = (1.0, 1.0)
        self.root.size_hint = (1.0, 0.5)
        # self.root.padding = 10, 0, 10, 0
        # self.root.height = 300

        self.l = Label(text="foo text")
        self.l.halign = 'center'
        self.l.valign = 'center'
        # self.l.size_hint = (None, 100.0)
        # self.l.size_hint = (None, None)
        # self.l.pos_hint = (0.5, 0)
        # self.l.size_hint_x = 0.5
        # self.l.size = self.l.texture_size
        # self.l.text_size = (None, 100)
        # self.l.font_size = self.root.width / 2
        # self.l.font_size = self.root.height
        self.l.font_size = self.root.width / 2
        # self.l.font_size = '32sp'
        # self.l.width = self.l.texture_size[0] + dp(10)
        # self.l.height = self.l.texture_size[1] + dp(2)
        self.root.add_widget(self.l)
        return self.root

if __name__ == "__main__":
    TimeApp().run()
    
