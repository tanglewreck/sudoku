import re
from tkinter import *
from tkinter import ttk

# Root geometry
R_HEIGHT = 500
R_WIDTH = 500
R_X = 1000
R_Y = 0
ROOT_GEOMETRY = f"{R_WIDTH}x{R_HEIGHT}+{R_X}+{R_Y}"

def create_widgets(geometry=ROOT_GEOMETRY, debug=False):

    def root_configure( bg="white", geometry=ROOT_GEOMETRY):
        root.title("sudoku ftw")

        root.geometry(geometry)
        root.configure(background=bg)
        # root.update()
        if debug:
            print(f"({__name__}): root.winfo_geometry: {root.winfo_geometry()} ")

        for rc in range(11):
            root.rowconfigure(rc, weight=1)
            root.columnconfigure(rc, weight=1)
        # root.rowconfigure(9, weight=1)
        # root.columnconfigure(9, weight=1)

    def content_configure(borderwidth=10, padding=50):
        # ttk style:
        #   default class: TFrame
        #   possible widget states: active, disabled, focus, pressed, selected,
        #                           background, readonly, alternate, invalid
        content.configure(height=root.winfo_height() - 100)
        content.configure(width=root.winfo_width() - 100)
        if debug:
            print(f"({__name__}): content.winfo_geometry(): {content.winfo_geometry()}")
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


    def quit_frame_configure( bg="white"):
        quit_frame.configure(background=bg)
        quit_frame.configure(background="lightgray")
        quit_frame.configure(border=2)
        quit_frame.grid(column=10, row=10, columnspan=1, sticky=(E,W,S))
        quit_frame.update()

    def quit_button_configure( text="Quit"):
        quit_button.configure(text=text)
        quit_button.configure(padx=3, pady=3)
        quit_button.configure(command=root.destroy)
        quit_button.grid(column=10, row=10, sticky=(E))


#    def collision_counter_configure( text="Collisions:"):
#        collision_label = Label(master=root, text="Collisions:",
#                                     foreground="black", background="white")
#        collision_label.grid(column=0, row=1, sticky=W)
#
#        collision_counter.configure(text=text)
#        collision_counter.configure(textvariable=collisions)
#        collision_counter.configure(bg="white")
#        collision_counter.configure(foreground="black")
#        collision_counter.grid(column=1, row=1, sticky=(W))


    # <Decode geometry>
    regexp = r"^(\d+)x(\d+)\+(\d+)\+(\d+)$"
    try:
        (root_height,
         root_width,
         root_x,
         root_y) = re.search(regexp, geometry).groups()
    except AttributeError as e:
        print("Unable to decode geometry argument")
        sys.exit(1)

    # Is this needed?
    if root_height is None or root_width is None or root_x is None or root_y is None:
        print("Unable to decode argument geometry")
        sys.exit(1) 

    # Some debugging output:
    if debug:
        print(f"({__name__}) geometry (decoded): {root_height} x {root_width} + {root_x} + {root_y}")
    # </Decode geometry>

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

    # A list of lists of Sudoku number labels
    L = list()
    for i in range(9):
        l = list()
        for j in range(9):
            l.append(ttk.Label(content, text=f"{i+1}{j+1}"))
        L.append(l)

    # Place the numbers 
    for i in range(9):
        for j in range(9):
            L[i][j]['style'] = 'SudokuBoard.TLabel'
            L[i][j].grid(column=j, row=i, sticky=(E,N,W,S))

    # between_padding = (1, 1)
    # between_padding = (0, 0)
    # for child in content.winfo_children():
    #    child.grid_configure(padx=between_padding[0], pady=between_padding[1])


    # <Quit frame>
    quit_frame = Frame(root)
    quit_frame_configure()
    # </Quit frame>

    # <Quit button>
    quit_button = Button(root)
    quit_button_configure()
    # </Quit button>

    # Collision counter
    # collisions = IntVar()
    # collision_counter = Label(master=root) 
    # collision_counter_configure()

    return (root, content)


if __name__ == "__main__":
    (root, content) = create_widgets()
    root.mainloop()
