from tkinter import PhotoImage

class ChessPiece:
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        self.color=color
        self.position=board.decode(coordinates)
        self.x,self.y=divmod(self.position,8)
        self.x,self.y=self.x*60+32,self.y*60+34
        self.board=board
        self.game=game
        self.image_path=img_path
        self.photo_image=PhotoImage(file=img_path)
        self.canvas_image=None
        self.canvas=canvas
        self.isKing=False
        self.alreadyMoved=False
        self.legalMoves=[]
        self.circles=[]
    def isLegalMove(self,n):
        return n in self.legalMoves
    def changePosition(self,x,y):
        a,b=divmod(self.position,8)
        a,b=60*(x-a),60*(y-b)
        self.board.board[8*x+y]=self.board.board[self.position]
        self.board.board[self.position]=None
        self.position=8*x+y
        self.x,self.y=x*60+32,y*60+34
        if not self.alreadyMoved:
            self.alreadyMoved=True
        return a,b
    def drawCircles(self):
        for pos in self.legalMoves:
            x,y=divmod(pos,8)
            self.circles.append(self.canvas.canvas.create_oval(20+x*60,20+y*60,40+x*60,40+y*60,fill='red'))
    def deleteCircles(self):
        for circle in self.circles:
            self.canvas.canvas.delete(circle)
        self.circles.clear()
    def findLegalMovesFromPosition(self,n,directions,addition,append):
        if n%8!=directions[0] and n//8!=directions[1]:
            if self.board.board[n+addition]==None:
                if append:
                    self.legalMoves.append(n+addition)
                self.findLegalMovesFromPosition(n+addition,directions,addition,append)
            elif self.board.board[n+addition].color!=self.color:
                if append:
                    self.legalMoves.append(n+addition)
    def rookMoving(self,append):
        self.findLegalMovesFromPosition(self.position,(0,-1),-1,append)
        self.findLegalMovesFromPosition(self.position,(7,-1),1,append)
        self.findLegalMovesFromPosition(self.position,(-1,0),-8,append)
        self.findLegalMovesFromPosition(self.position,(-1,7),8,append)
    def bishopMoving(self,append):
        self.findLegalMovesFromPosition(self.position,(0,0),-9,append)
        self.findLegalMovesFromPosition(self.position,(7,0),-7,append)
        self.findLegalMovesFromPosition(self.position,(0,7),7,append)
        self.findLegalMovesFromPosition(self.position,(7,7),9,append)