from window_object import Window_object
from canvas_object import Canvas_object
from board import Board
from chessPiece import ChessPiece
from pawn import Pawn
from bishop import Bishop
from rook import Rook
from queen import Queen
from king import King
from knight import Knight

class Game:
    def __init__(self):
        self.screen=Window_object('Antichess','1000x600')
        self.canvas=Canvas_object(self.screen.screen,50,50,600,500)
        self.board=Board()
        self.whitePieces=[]
        self.blackPieces=[]

        #biale
        self.addPiece(Pawn('A2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('B2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('C2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('D2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('E2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('F2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('G2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Pawn('H2','images/whitepawn.png',self.board,self.canvas,'w',self))
        self.addPiece(Knight('B1','images/whiteknight.png',self.board,self.canvas,'w',self))
        self.addPiece(Knight('G1','images/whiteknight.png',self.board,self.canvas,'w',self))
        self.addPiece(Bishop('C1','images/whitebishop.png',self.board,self.canvas,'w',self))
        self.addPiece(Bishop('F1','images/whitebishop.png',self.board,self.canvas,'w',self))
        self.addPiece(Rook('A1','images/whiterook.png',self.board,self.canvas,'w',self))
        self.addPiece(Rook('H1','images/whiterook.png',self.board,self.canvas,'w',self))
        self.addPiece(Queen('D1','images/whitequeen.png',self.board,self.canvas,'w',self))
        self.addPiece(King('E1','images/whiteking.png',self.board,self.canvas,'w',self))

        #czarne
        self.addPiece(Pawn('A7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('B7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('C7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('D7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('E7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('F7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('G7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Pawn('H7','images/blackpawn.png',self.board,self.canvas,'b',self))
        self.addPiece(Knight('B8','images/blackknight.png',self.board,self.canvas,'b',self))
        self.addPiece(Knight('G8','images/blackknight.png',self.board,self.canvas,'b',self))
        self.addPiece(Bishop('C8','images/blackbishop.png',self.board,self.canvas,'b',self))
        self.addPiece(Bishop('F8','images/blackbishop.png',self.board,self.canvas,'b',self))
        self.addPiece(Rook('A8','images/blackrook.png',self.board,self.canvas,'b',self))
        self.addPiece(Rook('H8','images/blackrook.png',self.board,self.canvas,'b',self))
        self.addPiece(Queen('D8','images/blackqueen.png',self.board,self.canvas,'b',self))
        self.addPiece(King('E8','images/blackking.png',self.board,self.canvas,'b',self))

        self.canvas.canvas.bind('<Button-1>',self.move)

        self.leftButtonPressed=False
        self.whitesTurn=True
        self.capturing=False
        self.previousPosition=(-1,-1)


        self.screen.screen.mainloop()


    def addPiece(self,piece):
        if piece.isWhite:
            self.whitePieces.append(piece)
        else:
            self.blackPieces.append(piece)
        piece.canvas_image=self.canvas.canvas.create_image(piece.xx,piece.yy,image=piece.photo_image)
        self.board.board[piece.x][piece.y]=piece
    def pawnPromotion(self,x,y,color):
        piece=self.board.board[x][y]
        if piece.isWhite:
            self.whitePieces.remove(piece)
        else:
            self.blackPieces.remove(piece)
        self.canvas.canvas.delete(piece.canvas_image)
        del piece
        img='white' if color=='w' else 'black'
        self.addPiece(Queen(self.board.encode(x,y),f'images/{img}queen.png',self.board,self.canvas,color,self))
   
    def moving(self,x,y,piece):
        a,b=piece.changePosition(x,y)
        self.canvas.canvas.move(piece.canvas_image,a,b)
        self.whitesTurn=not self.whitesTurn

    def move(self,event):
        x,y=event.x//60,event.y//60
        if x>7 or y>7 or x<0 or y<0:
            return
        square=self.board.board[x][y]
        if self.leftButtonPressed:
            self.leftButtonPressed=False
            square2=self.board.board[self.previousPosition[0]][self.previousPosition[1]]
            if self.capturing and (x,y) in square2.captureMoves:
                self.canvas.canvas.delete(square.canvas_image)
                if square.isWhite:
                    self.whitePieces.remove(square)
                    if not self.whitePieces:
                        print('White won the game')
                        self.screen.screen.quit()
                else:
                    self.blackPieces.remove(square)
                    if not self.blackPieces:
                        print('Black won the game')
                        self.screen.screen.quit()
                del square
                self.moving(x,y,square2)
            elif not self.capturing and (x,y) in square2.legalMoves:
                self.moving(x,y,square2)
            square2.deleteCircles()
        else:
            self.capturing=False
            if square!=None and square.isWhite==self.whitesTurn:
                square.findCaptureMoves()
                if not square.captureMoves:
                    ChessPiece.captureMoves.clear() 
                    if self.whitesTurn:
                        for p in self.whitePieces:
                            p.findCaptureMoves()
                    else:
                        for p in self.blackPieces:
                            p.findCaptureMoves()
                    if not ChessPiece.captureMoves:
                        square.findLegalMoves()
                        if not square.legalMoves:
                            ChessPiece.legalMoves.clear() 
                            if self.whitesTurn:
                                for p in self.whitePieces:
                                    p.findLegalMoves()
                            else:
                                for p in self.blackPieces:
                                    p.findLegalMoves() 
                            if not ChessPiece.legalMoves:
                                print(f'{"white" if self.whitesTurn else "black"} won the game')
                                self.screen.screen.quit()
                        else:
                            self.leftButtonPressed=True
                            self.previousPosition=(x,y)
                            square.drawCircles(square.legalMoves)
                else:
                    self.leftButtonPressed=True
                    self.capturing=True
                    self.previousPosition=(x,y)
                    square.drawCircles(square.captureMoves)
