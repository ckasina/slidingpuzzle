from tkinter import LabelFrame, messagebox, Label, Entry, Button, Frame, StringVar, filedialog, N, S, E, W

class tkWindow:
    def __init__(self, window, title, bgcolor, fgcolor, font, previousWindow=None, extras=None):
        self.title = title
        self.bgcolor = bgcolor
        self.fgcolor = fgcolor
        self.font = font
        self.previousWindow = previousWindow  # stores the previous window that was open in order to go back to it later
        self.extras = extras  # for any extra values to be passed by the statement creating this object
        self.window = window
        self.window.config(bg=bgcolor)  # sets background color
        self.window.title(title)
        self.window.resizable(False, False)  # stops window from being resized in both the x direction and the y directions
        # when the window is closed run the command 'returnToPreviousWindow'
        self.window.protocol("WM_DELETE_WINDOW", self.returnToPreviousWindow)

        self.createWindow()
        # self.iconPath = ""
        # self.window.iconbitmap(self.iconPath)  # sets icon
        self.syncColors()  # sets all the colors for the widgets based on the parameters
        self.window.mainloop()  # runs the window

    def createWindow(self): pass  # this is where all the widgets would be created

    def syncColors(self):  # sets the background and foreground color for all the widgets
        for widget in self.window.grid_slaves():
            if isinstance(widget, Frame) or isinstance(widget, LabelFrame):  # you can't set the background/foreground color of frames (you can for label frames though), but frames contain widgets...
                    for frameWidget in widget.grid_slaves():  # loop through the widgets inside the frame
                            frameWidget.config(bg=self.bgcolor, fg=self.fgcolor, font=self.font)

            if not isinstance(widget, Frame):
                    # if it's not a frame then just loop through the widgets normally
                    widget.config(bg=self.bgcolor, fg=self.fgcolor, font=self.font)

    def returnToPreviousWindow(self):
        if self.previousWindow is None:
            exit()
        else:
            self.window.destroy()
            self.previousWindow.__showWindow__()

    def __hideWindow__(self): self.window.withdraw()
    def __showWindow__(self): self.window.deiconify()