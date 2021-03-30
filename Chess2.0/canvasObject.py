from tkinter import Canvas

class CanvasObject:
    def __init__(self,screen,x,y,width,height):
        self.x=x
        self.y=y
        self.width=width
        self.height=height
        self.canvas=Canvas(screen,width=width,height=height)
        self.canvas.place(x=x,y=y)
        self.drawBoard()
    def drawBoard(self):
        size=60
        for i in range(8):
            x=size*i+1
            for j in range(8):
                if (i+j)%2==0:
                    white=True
                else:
                    white=False
                y=size*j+1
                color='white' if white else 'black'
                self.canvas.create_rectangle(x,y,x+size+1,y+size+1,fill=color)