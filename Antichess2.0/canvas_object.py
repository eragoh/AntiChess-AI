from tkinter import Canvas
class Canvas_object:
    def __init__(self,screen,x,y,w,h):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.canvas=Canvas(screen,width=w,height=h)
        self.draw_board()
        self.canvas.place(x=x,y=y)  

    def draw_board(self):
        size=60    
        for i in range(8):
            x=size*i+1
            for j in range(8):
                if (i+j) % 2==0:
                    white=True
                else:
                    white=False
                y=size*j+1
                color='white' if white else 'black'
                self.canvas.create_rectangle(x,y,x+size+1,y+size+1,fill=color)              