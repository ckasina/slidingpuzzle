import tkinter
from configWindow import configWindow


TITLE = "Sliding Puzzle"
BGCOLOR = "#16B9DE"
FGCOLOR = "black"
FONT = ("Helvetica", 16, "bold")
root = tkinter.Tk()
mainInterface = configWindow(root, TITLE, BGCOLOR, FGCOLOR, FONT)
