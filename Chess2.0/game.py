from windowObject import WindowObject
from canvasObject import CanvasObject
from board import Board
from pawn import Pawn
from bishop import Bishop
from knight import Knight
from rook import Rook
from queen import Queen

class Game:
    def __init__(self):
        self.leftButtonPressed=False
        self.previousPosition=-1
        self.screen=WindowObject("Szachy",'1000x600')
        self.canvas=CanvasObject(self.screen.screen,50,50,600,500)
        self.board=Board()
        self.whitePieces=[]
        self.blackPieces=[]
        self.addPiece(Pawn('C2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Bishop('D3','images/blackbishop.png',self.board,self.canvas,'b',self))
        self.addPiece(Rook('B6','images/whiterook.png',self.board,self.canvas,'w',self))
        self.addPiece(Queen('A6','images/whitequeen.png',self.board,self.canvas,'w',self))
        self.addPiece(Knight('E5','images/whiteknight.png',self.board,self.canvas,'w',self))
        self.addPiece(Knight('C4','images/blackknight.png',self.board,self.canvas,'b',self))
        self.addPiece(Knight('F6','images/blackknight.png',self.board,self.canvas,'b',self))
        self.canvas.canvas.bind("<Button-1>",self.move)

        for p in self.whitePieces:
            p.canvas_image=self.canvas.canvas.create_image(p.x,p.y,image=p.photo_image)
            self.board.board[p.position]=p
        for p in self.blackPieces:
            p.canvas_image=self.canvas.canvas.create_image(p.x,p.y,image=p.photo_image)
            self.board.board[p.position]=p

        self.screen.screen.mainloop()
    def addPiece(self,piece):
        if piece.color=='w':
            self.whitePieces.append(piece)
        else:
            self.blackPieces.append(piece)
    def move(self,event):
        x,y=event.x//60,event.y//60
        p=self.board.board[8*x+y]
        if self.leftButtonPressed:
            self.leftButtonPressed=False
            p2=self.board.board[self.previousPosition]
            if p2.isLegalMove(8*x+y):
                try:
                    self.canvas.canvas.delete(p.canvas_image)
                    if p.color=='w':
                        self.whitePieces.remove(p)
                    else:
                        self.blackPieces.remove(p)
                    del p
                except:
                    print("None")
                a,b=p2.changePosition(x,y)
                self.canvas.canvas.move(p2.canvas_image,a,b)
            p2.deleteCircles()
        else:
            try:
                p.findLegalMoves()
                p.drawCircles()
                self.previousPosition=p.position
                self.leftButtonPressed=True
            except:
                pass
