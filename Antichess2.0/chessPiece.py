from tkinter import PhotoImage
import copy

class ChessPiece:
    captureMoves=[]
    legalMoves=[]
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        self.x,self.y=board.decode(coordinates)
        self.xx,self.yy=self.x*60+32,self.y*60+34
        self.image_path=img_path
        self.board=board
        self.canvas=canvas
        self.canvas_image=None
        self.isWhite=color=='w'
        self.game=game
        self.photo_image=PhotoImage(file=img_path)
        self.captureMoves=[]
        self.legalMoves=[]
        self.circles=[]
        self.alreadyMoved=False
        self.isPawn=False

    def drawCircles(self,list):
        for cords in list:
            x,y=cords
            self.circles.append(self.canvas.canvas.create_oval(20+x*60,20+y*60,40+x*60,40+y*60,fill='red'))
    def deleteCircles(self):
        for circle in self.circles:
            self.canvas.canvas.delete(circle)
        self.circles.clear()
    def changePosition(self,x,y):
        a,b=x-self.x,y-self.y
        self.board.board[x][y]=self.board.board[self.x][self.y]
        self.board.board[self.x][self.y]=None
        self.x,self.y=x,y
        self.xx,self.yy=x*60+32,y*60+34
        if not self.alreadyMoved:
            self.alreadyMoved=True
            if self.isPawn:
                self.enpassant=self.game.getCounter() if b==2 else -1
        if self.isPawn:
            if self.isWhite and self.y==0:
                self.game.pawnPromotion(self.x,self.y,'w')
            elif self.y==7:
                self.game.pawnPromotion(self.x,self.y,'b')
        return a*60,b*60
    
    def figureMoving(self,capturing,isKing,list):
        x,y=self.x,self.y
        for i in range(4):
            l=[x[:] for x in list]
            while x+l[i][0]>=0 and x+l[i][0]<=7 and y+l[i][1]>=0 and y+l[i][1]<=7:
                if capturing and self.board.board[x+l[i][0]][y+l[i][1]]!=None and self.board.board[x+l[i][0]][y+l[i][1]].isWhite!=self.isWhite:
                    self.captureMoves.append((x+l[i][0],y+l[i][1]))
                    ChessPiece.captureMoves.append((x+l[i][0],y+l[i][1]))
                    break
                elif self.board.board[x+l[i][0]][y+l[i][1]]!=None and self.board.board[x+l[i][0]][y+l[i][1]].isWhite==self.isWhite:
                    break
                elif not capturing:
                    self.legalMoves.append((x+l[i][0],y+l[i][1]))
                    ChessPiece.legalMoves.append((x+l[i][0],y+l[i][1]))
                if isKing:
                    break
                l[i][0]+=list[i][0]
                l[i][1]+=list[i][1]
