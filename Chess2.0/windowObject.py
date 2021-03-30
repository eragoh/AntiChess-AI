import tkinter 

class WindowObject:
    def __init__(self,title,size):
        self.screen=tkinter.Tk()
        self.screen.title(title)
        self.screen.geometry(size)