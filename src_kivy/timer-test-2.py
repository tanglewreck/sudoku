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

kivy.require("2.0.0")


class RootWidget(GridLayout):
    # dt means delta-time
    def __init__(self, *args, **kwargs): 
        super().__init__()




class TimeApp(App):
    def my_callback(self, dt):
        now = str(datetime.datetime.now())
        self.root.text = now


    def __init__(self, *args, **kwargs):
        super().__init__()
        # call my_callback every * seconds
        Clock.schedule_interval(self.my_callback, 1.0)

    def build(self):
        """Build the widget tree"""
        self.root = Label(text="foo text")
        self.root.halign = 'center'
        # self.root.valign = 'center'
        self.root.valign = 'top'
        # self.root.text_size = (None, 10)
        # self.root.text_size = self.root.size
        # error: self.root.font_size = self.root.height, self.root.width
        self.root.font_size = self.root.width * 0.75
        # self.root.font_size = '64sp'
        self.root.size = self.root.texture_size
        # self.root.size = self.root.texture_size
        # self.root.add_widget(self.root)
        return self.root

if __name__ == "__main__":
    TimeApp().run()
    
