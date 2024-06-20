"""Sudoku game widgets"""

import re

from tkinter import *
from tkinter import ttk

from utils import debug_msg, err_msg, sys_msg
from utils import ROOT_GEOMETRY

__all__ = ["create_widgets", "validate_geometry", "SudokuWidgets"]


class SudokuWidgets():
    def __init__(self, sudoku_game=None, geometry=ROOT_GEOMETRY, debug=False):
        self.debug = debug
        self.root = Tk()
        self.content = ttk.Frame(self.root)
        self.board = sudoku_game
        self.geometry = geometry
        if not self.validate_geometry(geometry):
            err_msg(f"Invalid geometry")
            raise SystemExit(1)
        self.root_configure(bg="white", geometry=self.geometry)
        

    def root_configure(self, bg="white", geometry=ROOT_GEOMETRY):
        self.root.title("sudoku ftw")
        self.root.geometry(geometry)
        self.root.configure(background=bg)
        if self.debug:
            print(f"({__name__}): self.root.winfo_geometry: {self.root.winfo_geometry()} ")

        for rc in range(11):
            self.root.rowconfigure(rc, weight=1)
            self.root.columnconfigure(rc, weight=1)


    def mainloop(self):
        self.root.mainloop()


    def validate_geometry(self, geometry, debug=False):
        regexp = r"^(\d+)x(\d+)\+(\d+)\+(\d+)$"
        try:
            if match := re.search(regexp, geometry):
                if debug:
                    sys_msg(f"geometry (decoded): {match.groups()}")
                return True
            else:
                err_msg(f"geometry format error: {geometry}")
        except AttributeError as e:
            err_msg("Unable to decode geometry")
            return False
        except re.error as e:
            err_msg(e)
            return False




def validate_geometry(geometry, debug=False):
    regexp = r"^(\d+)x(\d+)\+(\d+)\+(\d+)$"
    try:
        if match := re.search(regexp, geometry):
            if debug:
                sys_msg(f"geometry (decoded): {match.groups()}")
            return True
        else:
            err_msg(f"geometry format error: {geometry}")
    except AttributeError as e:
        err_msg("Unable to decode geometry")
        return False
    except re.error as e:
        err_msg(e)
        return False


def create_widgets(geometry=ROOT_GEOMETRY, debug=False):

    def root_configure(bg="white", geometry=ROOT_GEOMETRY):
        root.title("sudoku ftw")
        root.geometry(geometry)
        root.configure(background=bg)
        if debug:
            print(f"({__name__}): root.winfo_geometry: {root.winfo_geometry()} ")

        for rc in range(11):
            root.rowconfigure(rc, weight=1)
            root.columnconfigure(rc, weight=1)


    def content_configure(borderwidth=10, padding=50):
        # ttk style:
        #   default class: TFrame
        #   possible widget states: active, disabled, focus, pressed, selected,
        #                           background, readonly, alternate, invalid
        content.configure(height=root.winfo_height() - 100)
        content.configure(width=root.winfo_width() - 100)
        if debug:
            debug_msg(f"content.winfo_geometry(): {content.winfo_geometry()}")
        content.configure(padding=padding)
        content.configure(borderwidth=borderwidth)
        content.grid(column=0, row=0, columnspan=10, rowspan=10, sticky=(N,E,W,S))
        content.update()


    def configure_content_styles(cbg="white", lbg="white", lpad=7, lh=20, lw=3, lf="helvetica", lfs=18, theme='classic'):
        content_style = ttk.Style()
        content_style.theme_use(theme)
    
        # Content frame style:
        content_style.configure('SudokuBoard.TFrame',
                                background=cbg,
                                relief="groove"
        )
    
        # Label style:
        content_style.configure('SudokuBoard.TLabel',
                                background=lbg,
                                foreground="black",
                                font=f"{lf} {lfs}",
                                anchor=(E,N,W,S),
                                relief='groove',
                                padding=lpad,
                                height=lh,
                                width=lw
        )
        return content_style


    def quit_frame_configure(bg="white"):
        quit_frame.configure(background=bg)
        quit_frame.configure(background="lightgray")
        quit_frame.configure(border=2)
        quit_frame.grid(column=10, row=10, columnspan=1, sticky=(E,W,S))
        quit_frame.update()


    def quit_button_configure(text="Quit"):
        quit_button.configure(text=text)
        quit_button.configure(padx=3, pady=3)
        quit_button.configure(command=root.destroy)
        quit_button.grid(column=10, row=10, sticky=(E))


    # <Decode geometry>
    if not validate_geometry(geometry, debug=debug):
        err_msg(f"Invalid geometry: {geometry}")
        raise SystemExit(1)


    # <Root window>
    root = Tk()
    root_configure(geometry=geometry)
    # </Root window>

    # <Content frame>
    content = ttk.Frame(root)
    content_configure(borderwidth=1, padding="20 100 20 100")

    content_style = configure_content_styles(cbg="white",
                                             lf="helvetica", lfs=14,
                                             lw=4,lh=30, lpad=5, lbg="#efefef",
                                             theme='default')

    content['style'] = "SudokuBoard.TFrame"
    content.update()
    # </Content frame>

    # <Quit frame>
    quit_frame = Frame(root)
    quit_frame_configure()
    # </Quit frame>

    # <Quit button>
    quit_button = Button(root)
    quit_button_configure()
    # </Quit button>

    return (root, content)


if __name__ == "__main__":
    print(__doc__)
