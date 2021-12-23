import tkinter
import tkinter.font as tk_font
from tkinter import BooleanVar, LabelFrame, Radiobutton, StringVar, IntVar
from tkinter import Label, Entry, Button, Checkbutton, OptionMenu
from tkinter import filedialog, colorchooser, messagebox
from tkinter import N, S, E, W
from tkTemplate import tkWindow
from gameWindow import gameWindow
from os.path import isfile


class configWindow(tkWindow):
    def createWindow(self):
        # Frames
        self.sizeFrame = LabelFrame(self.window, text="Puzzle Size")
        self.formatFrame = LabelFrame(self.window, text="Puzzle Format")

        # Variables
        self.rowsVar = IntVar(self.window, 3)
        self.colsVar = IntVar(self.window, 3)
        self.imageStringVar = StringVar(self.window)
        self.fontVar = StringVar(self.window)
        self.gridVar = IntVar(self.window, 0)
        self.gridVar.trace('w', self.gridVarChanged)
        self.colourImageVar = IntVar(self.window, 0)
        self.colourImageVar.trace('w', self.colourImageVarChanged)
        self.showNumVar = BooleanVar(self.window, True)
        self.showNumVar.trace('w', self.showNumVarChanged)
        self.tileColor = (0, 0, 255)
        self.tileColorVar = StringVar(self.window, str(self.tileColor))

        # Labels
        self.rowsLabel = Label(self.sizeFrame, text="Rows:")
        self.colsLabel = Label(self.sizeFrame, text="Columns:")
        self.fontLabel = Label(self.formatFrame, text="Font:")
        self.colourLabel = Label(self.formatFrame, text="Tile Colour:")
        self.actualColourLabel = Label(self.formatFrame, textvariable=self.tileColorVar)
        self.imageLabel = Label(self.formatFrame, text="Image path:")

        # Entries
        self.imageEntry = Entry(self.formatFrame, textvariable=self.imageStringVar)

        # Buttons
        self.chooseColorButton = Button(self.formatFrame, text="Choose colour", command=self.choosecolor)
        self.browseButton = Button(self.formatFrame, text="Browse ...", command=self.browse)
        self.playButton = Button(self.window, text="Play", command=self.play)

        # Radiobutton
        self.threeRadio = Radiobutton(self.sizeFrame, text="3x3", variable=self.gridVar, value=0)
        self.fourRadio = Radiobutton(self.sizeFrame, text="4x4", variable=self.gridVar, value=1)
        self.fiveRadio = Radiobutton(self.sizeFrame, text="5x5", variable=self.gridVar, value=2)
        self.customRadio = Radiobutton(self.sizeFrame, text="Custom", variable=self.gridVar, value=3)

        self.colorRadio = Radiobutton(self.formatFrame, text="Colour", variable=self.colourImageVar, value=0)
        self.imageRadio = Radiobutton(self.formatFrame, text="Image", variable=self.colourImageVar, value=1)

        # Checkbutton
        self.showNumCheck = Checkbutton(self.formatFrame, text="Show numbers", variable=self.showNumVar)
        
        # Option Menu
        fonts = tk_font.families()
        self.fontVar.set("Comic Sans MS")
        self.fontMenu = OptionMenu(self.formatFrame, self.fontVar, *fonts)
        self.rowsMenu = OptionMenu(self.sizeFrame, self.rowsVar, *[i for i in range(2, 10)])
        self.colsMenu = OptionMenu(self.sizeFrame, self.colsVar, *[i for i in range(2, 10)])
        self.rowsMenu.config(state="disabled")
        self.colsMenu.config(state="disabled")

        # Widget positions
        sizeRowZero = [self.threeRadio, self.fourRadio, self.fiveRadio, self.customRadio]
        for i in range(len(sizeRowZero)):
            sizeRowZero[i].grid(row=0, column=i, padx=13)

        sizeRowOne = [self.rowsLabel, self.rowsMenu, self.colsLabel, self.colsMenu]
        for i in range(len(sizeRowOne)):
            sizeRowOne[i].grid(row=1, column=i, padx=13)

        self.colorRadio.grid(row=0, column=0)
        self.imageRadio.grid(row=0, column=1)
        self.showNumCheck.grid(row=0, column=2)
        self.showNumCheck.config(state="disabled")

        self.fontLabel.grid(row=1, column=0)
        self.fontMenu.grid(row=1, column=1)
        self.colourLabel.grid(row=2, column=0)
        self.actualColourLabel.grid(row=2, column=1)
        self.chooseColorButton.grid(row=2, column=2)

        self.imageLabel.grid(row=2, column=0)
        self.imageEntry.grid(row=2, column=1, columnspan=2)
        self.browseButton.grid(row=2, column=3, sticky=W+E)
        
        self.imageLabel.grid_remove()
        self.imageEntry.grid_remove()
        self.browseButton.grid_remove()

        self.formatFrame.grid(row=0, column=0, pady=10)
        self.sizeFrame.grid(row=1, column=0, pady=10)

        self.playButton.grid(row=2, column=0, sticky=W+E)

    def play(self):
        if self.colourImageVar.get() == 1 and not isfile(self.imageStringVar.get()):
            messagebox.showerror(self.title, "The image file does not exist!")

        elif self.colourImageVar.get() == 1:
            self.__hideWindow__()
            _ = gameWindow(self.title, int(self.rowsVar.get()), int(self.colsVar.get()), self.showNumVar.get(), 
            True, self, [self.fontVar.get(), self.imageStringVar.get()])

        elif self.colourImageVar.get() == 0:
            self.__hideWindow__()
            _ = gameWindow(self.title, int(self.rowsVar.get()), int(self.colsVar.get()), self.showNumVar.get(), 
            False, self, [self.fontVar.get(), self.tileColor])
    
    def browse(self):
        filetypes = (("BMP Files", "*.bmp"), ("PNG Files", "*.png"), 
        ("JPG Files", "*.jpg *.jpeg"), ("All Files", "*.*"))
        filename = filedialog.askopenfilename(title="Open sliding puzzle picture file", filetypes=filetypes)
        self.imageStringVar.set(filename)

    def choosecolor(self):
        colorCode = colorchooser.askcolor(title="Choose tile colour")
        if colorCode[0] != None:
            self.tileColor = tuple(int(i) for i in colorCode[0])
            self.tileColorVar.set(str(self.tileColor))

    def colourImageVarChanged(self, *args, **kwargs):
        if self.colourImageVar.get() == 0: #colour
            self.imageLabel.grid_remove()
            self.imageEntry.grid_remove()
            self.browseButton.grid_remove()

            self.showNumVar.set(True)
            self.showNumCheck.config(state="disabled")

            self.colourLabel.grid()
            self.actualColourLabel.grid()
            self.chooseColorButton.grid()

            self.syncColors()

        elif self.colourImageVar.get() == 1: #image
            self.colourLabel.grid_remove()
            self.actualColourLabel.grid_remove()
            self.chooseColorButton.grid_remove()
            self.showNumCheck.config(state="normal")

            self.imageLabel.grid()
            self.imageEntry.grid()
            self.browseButton.grid()
            self.syncColors()


    def gridVarChanged(self, *args, **kwargs):
        if self.gridVar.get() == 3: # custom
            self.rowsMenu.config(state="normal")
            self.colsMenu.config(state="normal")

        elif self.gridVar.get() < 3: # not custom
            self.rowsMenu.config(state="disabled")
            self.colsMenu.config(state="disabled")
            self.rowsVar.set(self.gridVar.get()+3)
            self.colsVar.set(self.gridVar.get()+3)

    def showNumVarChanged(self, *args, **kwargs):
        if self.showNumVar.get():
            self.fontMenu.config(state="normal")

        else:
            self.fontMenu.config(state="disabled")
