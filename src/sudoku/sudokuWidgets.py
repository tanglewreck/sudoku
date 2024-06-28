__doc__ = """Sudoku game widgets"""
__author__ = "Mikael Eriksson"
__version__ = "0.9.0"

import re

from tkinter import *
from tkinter import ttk

from utils import debug_msg, err_msg, sys_msg
from utils import ROOT_GEOMETRY

__all__ = ["SudokuWidgets"]

# class SudokuRoot():
#   pass
#
# class SudokuContent():
#   pass
#
# class SudokuQuit():
# """A frame containing the 'Quit' button"""
#   pass


class SudokuWidgets():
    """A class for creating and configuring the tkinter widgets used by the SudokuGUI class"""

    def __init__(self, geometry=ROOT_GEOMETRY, debug=False):
        self.debug = debug
        self.geometry = geometry
        print("geometry =", geometry)
        if not self.__validate_geometry__(geometry):
            err_msg(f"Invalid geometry")
            raise SystemExit(1)

        # <Root window>
        self.__root__(bg="white", geometry=self.geometry)
        # </Root window>

        
        # define ttk Styles
        self.content_style = self.__content_styles__(lf="helvetica", lfs=14, lw=4, lh=30, lpad=5, lbg="#efefef", theme='default')
        
        # <Content frame>
        self.__content__()
        # </Content frame>

        # <Quit frame>
        self.__quit_frame__()
        # </Quit frame>
        
        # <Quit button>
        self.__quit_button__()
        # </Quit button>

        # <Numerical keypad frame>
        self.__num_keypad_frame__()
        # </Numerical keypad frame>


    def __validate_geometry__(self, geometry, debug=False):
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


    def __root__(self, bg="white", geometry=ROOT_GEOMETRY):
        self.root = Tk()
        self.root.title("sudoku ftw")
        self.root.geometry(geometry)
        self.root.configure(background=bg)
        if self.debug:
            print(f"({__name__}): self.root.winfo_geometry: {self.root.winfo_geometry()} ")

        for rc in range(20):
            self.root.rowconfigure(rc, weight=1)
            self.root.columnconfigure(rc, weight=1)


    def __content_styles__(self, bg="white", lbg="white", lpad=7, lh=20, lw=3, lf="helvetica", lfs=18, theme='classic'):
        """Create and return a ttk.Style objecat for the content frame and its children"""
        self.content_style = ttk.Style()
        self.content_style.theme_use(theme)
        # Content frame style:
        self.content_style.configure('SudokuBoard.TFrame', background=bg, padding="20 20 20 20", relief="groove")
        # Label style:
        self.content_style.configure('SudokuBoard.TLabel', background=bg,
                                     foreground="black", font=f"{lf} {lfs}",
                                     anchor=(E,N,W,S), 
                                     padding=lpad, height=lh, width=lw
        )
                                     # anchor=(E,N,W,S), relief='groove',
        self.content_style.configure('SudokuBoard_numkey.TButton', background="#fefefe",
                                     padding=2, font=f"{lf} 12", anchor=(E,W))
        self.content_style.configure('SudokuBoard_boardbutton.TButton', background="#fafafa",
                                     padding=8, font=f"{lf} 12", anchor=(E,W),
                                     width=5, height=10)
        return self.content_style


    def __content__(self, borderwidth=1, padding="20 100 20 100"):
        # <Content frame>
        self.content = ttk.Frame(self.root)
        self.content['style'] = "SudokuBoard.TFrame"
        self.content.update()
        # ttk style:
        #   default class: TFrame
        #   possible widget states: active, disabled, focus, pressed, selected,
        #                           background, readonly, alternate, invalid
        self.content.configure(height=self.root.winfo_height() - 100)
        self.content.configure(width=self.root.winfo_width() - 100)
        if self.debug:
            print(f"({__name__}): self.content.winfo_geometry(): {self.content.winfo_geometry()}")
        self.content.configure(padding=padding)
        self.content.configure(borderwidth=borderwidth)
        self.content.grid(column=0, row=0, columnspan=10, rowspan=10, sticky=(N,E,W,S))
        self.content.update()


    def __quit_frame__(self, bg="white"):
        self.quit_frame = Frame(self.root)
        self.quit_frame.configure(background=bg)
        self.quit_frame.configure(background="lightgray")
        self.quit_frame.configure(border=2)
        self.quit_frame.grid(column=10, row=10, columnspan=1, sticky=(E,W,S))
        self.quit_frame.update()


    def __quit_button__(self, text="Quit"):
        self.quit_button = Button(self.root)
        self.quit_button.configure(text=text)
        self.quit_button.configure(padx=3, pady=3)
        self.quit_button.configure(command=self.root.destroy)
        self.quit_button.grid(column=10, row=10, sticky=(E))
        self.quit_button.update()


    def __num_keypad_frame__(self):
        """Maybe this should be moved to sudokuGUI.py in order to let the
        SudokuWidget class contain just the basic widgets, such as
        the content frame, etc.?"""

        self.num_keypad_frame = ttk.Frame(self.root)
        self.num_keypad_frame['style'] = 'SudokuBoard.TFrame'
        self.num_keypad_frame.grid(column=10, row=9, sticky=(E,N,W,S))

        self.current_number = IntVar()

        num_keypad_buttons = []
        for k in range(10):
            button_text = str((k+1) % 10)
            self.current_number.set(k)
            num_keypad_buttons.append(
                ttk.Button(self.num_keypad_frame,
                           text=str(button_text),
                           command=lambda k=k: self.current_number.set((k + 1) % 10),
                           padding=2
                           )
            )
        for k in range(10):
            r, c = divmod(k, 3)
            if self.debug:
                print("row, column =", r, c)
            if k == 9:
                num_keypad_buttons[k].grid(row=r, column=c+1, sticky=(E,N,W,S))
            else:
                num_keypad_buttons[k].grid(row=r, column=c, sticky=(E,N,W,S))
            num_keypad_buttons[k]['style'] = 'SudokuBoard_numkey.TButton'


        self.num_label = ttk.Label(self.num_keypad_frame,
                                   background="white", foreground="black",
                                   textvariable=self.current_number,
                                   width=5, padding=20, anchor="center", justify="center")
        self.num_label['style'] = "SudokuBoard.TLabel"
        self.num_label.grid(row=5, column=1)

        self.current_number.set(0)
        



    def mainloop(self):
        self.root.mainloop()


