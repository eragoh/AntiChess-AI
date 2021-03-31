from window_object import Window_object
from canvas_object import Canvas_object
from board import Board
from pawn import Pawn
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King

from tkinter import PhotoImage

class Game:
    def __init__(self):
        self.leftButtonPressed=False
        self.previousPosition=(-1,-1)

        self.screen=Window_object('Szachy','1000x600')
        self.canvas=Canvas_object(self.screen.screen,50,50,600,500)
        self.board=Board()
        self.circles=[]
        self.captureMoves=[]
        self.legalMoves=[]
        self.capture=False
        self.whitesMove=True
        self.whitePieces=[]
        self.blackPieces=[]
        self.canvas.canvas.bind("<Button-1>",self.move)

        self.addPiece(Pawn('A2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('B2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('C2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('D2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('E2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('F2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('G2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('H2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Rook('H3','images/whiterook.png',self.board,self.canvas,'w',self))
        self.addPiece(King('H4','images/whiteking.png',self.board,self.canvas,'w',self))

        self.addPiece(Pawn('A7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('B7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('C7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('D7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('E7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('F7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('G7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('H7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Queen('G6','images/blackqueen.png',self.board,self.canvas,'b',self))
        self.addPiece(Bishop('H8','images/blackbishop.png',self.board,self.canvas,'b',self))

        for p in self.whitePieces:
            p.canvas_image=self.canvas.canvas.create_image(p.xx,p.yy,image=p.photo_image)
            self.board.board[p.x][p.y]=p
        for p in self.blackPieces:
            p.canvas_image=self.canvas.canvas.create_image(p.xx,p.yy,image=p.photo_image)
            self.board.board[p.x][p.y]=p
        self.screen.screen.mainloop()

    def findLegalMoves(self):
        self.captureMoves.clear()
        if self.whitesMove:
            for p in self.whitePieces:
                p.findLegalMoves()
        else:
            for p in self.blackPieces:
                p.findLegalMoves()
        self.drawCircles(self.captureMoves)
        return len(self.captureMoves)>0
    def findLegalMoves2(self):
        self.legalMoves.clear()
        if self.whitesMove:
            for p in self.whitePieces:
                p.findLegalMoves2()
                if len(self.legalMoves)>0:
                    return True
        else:
            for p in self.whitePieces:
                p.findLegalMoves2()
                if len(self.legalMoves)>0:
                    return True
        return False
        
    def isLegalMove(self,cords,list):
        if cords in list:
            return True
        return False
    def addPiece(self,piece):
        if piece.isWhite:
            self.whitePieces.append(piece)
        else:
            self.blackPieces.append(piece)
    def drawCircles(self,list):
        for cords in list:
            x,y=cords
            self.circles.append(self.canvas.canvas.create_oval(20+x*60,20+y*60,40+x*60,40+y*60,fill='red'))
    def deleteCircles(self,list):
        for circle in list:
            self.canvas.canvas.delete(circle)
        list.clear()

    def move(self,event):
        x,y=event.x//60,event.y//60
        if x>7 or y>7:
            return
        p=self.board.board[x][y]
        if self.leftButtonPressed:
            self.leftButtonPressed=False
            p2=self.board.board[self.previousPosition[0]][self.previousPosition[1]]
            if p2!=None and p!=p2 and self.isLegalMove((x,y),p2.legalMoves) or (self.isLegalMove((x,y),self.captureMoves) and self.isLegalMove((x,y),p2.captureMoves)):
                if len(self.captureMoves)>0:
                    self.legalMoves.clear()
                try:
                    self.canvas.canvas.delete(p.canvas_image)
                    if p.isWhite:
                        self.whitePieces.remove(p)
                        if len(self.whitePieces)==0:
                            print("White won the game")
                            self.screen.screen.quit()
                    else:
                        self.blackPieces.remove(p)
                        if len(self.blackPieces)==0:
                            print("Black won the game")
                            self.screen.screen.quit()
                    del p
                except:
                    pass
                a,b=p2.changePosition(x,y)
                self.canvas.canvas.move(p2.canvas_image,a,b)
                self.board.printBoard()
                print(len(self.whitePieces))
                print(len(self.blackPieces))
                self.whitesMove=not self.whitesMove
            if self.capture:
                self.deleteCircles(self.circles)
            else:
                self.deleteCircles(p2.circles)
        else:
            if self.findLegalMoves():
                self.capture=True
                self.previousPosition=(x,y)
                self.leftButtonPressed=True
            else:
                self.capture=False
                try:
                    if(p.isWhite==self.whitesMove):
                        p.findLegalMoves2()
                        if len(p.legalMoves)==0:
                            if not self.findLegalMoves2():
                                print(f'{"white" if self.whitesMove else "black"} won the game')
                        p.drawCircles()
                        self.previousPosition=(x,y)
                        self.leftButtonPressed=True
                except:
                    pass
        