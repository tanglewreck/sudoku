#!/usr/bin/env python3

# ----------------------------------------
# setup_kivy_config.py –
# ----------------------------------------
'''
Create a local kivy config file

'''

__version__ = "2024-08-23"

import os
# NOTE: KIVY_HOME must be set *before* kivy is imported
os.environ['KIVY_HOME'] = f"{os.getcwd()}/.kivy"
# Make kivy ignore command-line arguments 
os.environ['KIVY_NO_ARGS'] = 'yes'

import kivy
from kivy.config import Config
kivy.require("2.0.0")

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# <KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# Read the (local) configuration files and change stuff to our liking.
# NOTE: Changes require a restart to take effect
# NOTE: This code might probaly better be moved to its own file,
#     which can be run when needed (+TODO-list)
Config.read(f"{os.environ['HOME']}/Proj/sudoku/src_kivy/.kivy/config.ini")
Config.set('kivy', 'exit_on_escape', 1)
Config.set('kivy', 'log_enable', 1)
Config.set('kivy', 'window_icon', "data/mier_347x437.jpg")
Config.set('graphics', 'fullscreen', 0)
Config.set('graphics', 'height', 600)
Config.set('graphics', 'width', 1000)
Config.set('graphics', 'resizable', 0)
Config.set('graphics', 'position', 'custom')  # auto|custom
Config.set('graphics', 'left', 100)         # ignored when 'position' == 'auto'
Config.set('graphics', 'top', 100)          # ignored when 'position' == 'auto'
Config.set('kivy', 'log_level', "warning")  # debug|info|warning|error|critical
Config.write()

# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =
# </KIVY CONFIG>
# = = = = = = = = = = = = = = = = = = = = = = = = = = = = = = =

