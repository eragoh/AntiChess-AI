from tkinter import Canvas
from tkinter import PhotoImage

class Canvas_object:
    def __init__(self,screen,x,y,w,h):
        self.x=x
        self.y=y
        self.width=w
        self.height=h
        self.Images={
            'wpawn':'images/whitepawn.png',
            'wknight':'images/whiteknight.png',
            'wbishop':'images/whitebishop.png',
            'wrook':'images/whiterook.png',
            'wqueen':'images/whitequeen.png',
            'wking':'images/whiteking.png',
            'bpawn':'images/blackpawn.png',
            'bknight':'images/blackknight.png',
            'bbishop':'images/blackbishop.png',
            'brook':'images/blackrook.png',
            'bqueen':'images/blackqueen.png',
            'bking':'images/blackking.png'
        }
        self.photoImages=[]
        self.imagesBoard=[]
        self.circles=[]
        for _ in range(8):
            self.imagesBoard.append([None for _ in range(8)])
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

    def setPieceImage(self,x,y,type,color):
        img=PhotoImage(file=self.Images[f'{"w" if color else "b"}{type}'])
        self.photoImages.append(img)
        self.imagesBoard[x][y]=self.canvas.create_image(x*60+32,y*60+34,image=img)
    
    def deleteImage(self,x,y):
        self.canvas.delete(self.imagesBoard[x][y])
    
    def drawCircles(self,piece,list):
        for cords in list:
            x,y=cords
            self.circles.append(self.canvas.create_oval(20+x*60,20+y*60,40+x*60,40+y*60,fill='red'))
    
    def deleteCircles(self):
        for circle in self.circles:
            self.canvas.delete(circle)
        self.circles.clear()

    def move(self,previous,nextPosition,position):
        self.imagesBoard[nextPosition[0]][nextPosition[1]]=self.imagesBoard[previous[0]][previous[1]]
        self.canvas.move(self.imagesBoard[previous[0]][previous[1]],position[0],position[1])
        self.imagesBoard[previous[0]][previous[1]]=None

    def clear(self):
        for i in range(8):
            for j in range(8):
                if self.imagesBoard[i][j]!=None:
                    self.deleteImage(i,j)
                    self.imagesBoard[i][j]=None