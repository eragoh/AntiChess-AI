from window_object import Window_object
from canvas_object import Canvas_object
from board import Board
from tkinter import Button, Entry, messagebox

import antichessAI

from chessPiece import ChessPiece
from pawn import Pawn
from bishop import Bishop
from knight import Knight
from rook import Rook
from queen import Queen
from king import King

class Game():
    def __init__(self):
        self.screen=Window_object('Antichess','800x600')
        self.canvas=Canvas_object(self.screen.screen,50,50,600,500)
        self.board=Board()
        self.whitePieces=[]
        self.blackPieces=[]

        self.fenEntry=Entry(self.screen.screen)
        self.canvas.canvas.create_window(600,140,window=self.fenEntry)
        button=Button(self.screen.screen,text="Wczytaj fen",command=self.p)
        self.canvas.canvas.create_window(600,170,window=button)

        #biale
        self.setBoard("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")

        self.leftButtonPressed=False
        #self.whitesTurn=True
        self.capturing=False
        self.counter=0
        self.previousPosition=(-1,-1)

        self.canvas.canvas.bind('<Button-1>',self.move)
        self.screen.screen.mainloop()
    
    def setBoard(self,fen):
        row,column=0,0
        for character in fen:
            if character=='R':
                self.addPiece(Rook(column,row,'w',self.board.board))
                column+=1
            elif character=='r':
                self.addPiece(Rook(column,row,'b',self.board.board))
                column+=1
            elif character=='N':
                self.addPiece(Knight(column,row,'w',self.board.board))
                column+=1
            elif character=='n':
                self.addPiece(Knight(column,row,'b',self.board.board))
                column+=1
            elif character=='B':
                self.addPiece(Bishop(column,row,'w',self.board.board))
                column+=1
            elif character=='b':
                self.addPiece(Bishop(column,row,'b',self.board.board))
                column+=1
            elif character=='P':
                self.addPiece(Pawn(column,row,'w',self.board.board))
                column+=1
            elif character=='p':
                self.addPiece(Pawn(column,row,'b',self.board.board))
                column+=1
            elif character=='K':
                self.addPiece(King(column,row,'w',self.board.board))
                column+=1
            elif character=='k':
                self.addPiece(King(column,row,'b',self.board.board))
                column+=1
            elif character=='Q':
                self.addPiece(Queen(column,row,'w',self.board.board))
                column+=1
            elif character=='q':
                self.addPiece(Queen(column,row,'b',self.board.board))
                column+=1
            elif character=='/':
                column=0
                row+=1
            else:
                if character>='1' and character<='9':
                    column+=int(character)
                elif character==' ':
                    i=fen.index(character)+1
                    self.whitesTurn = True if fen[i]=='w' else False
                    return
             
    def addPiece(self,piece):
        self.whitePieces.append(piece) if piece.isWhite else self.blackPieces.append(piece)
        self.canvas.setPieceImage(piece.x,piece.y,piece.type,piece.isWhite)      
        self.board.board[piece.x][piece.y]=piece

    def move(self,event):
        self.canvas.deleteCircles()
        x,y=event.x//60,event.y//60
        if x>7 or y>7 or x<0 or y<0:
            return
        piece=self.board.board[x][y]
        if self.leftButtonPressed:
            self.leftButtonPressed=False
            piece2=self.board.board[self.previousPosition[0]][self.previousPosition[1]]
            if self.capturing and piece==None:
                piece=self.board.board[x][3 if self.whitesTurn else 4]
                self.board.board[x][3 if self.whitesTurn else 4]=None
                self.canvas.deleteImage(x,3 if self.whitesTurn else 4)
            if self.capturing and (x,y) in piece2.captureMoves:
                self.canvas.deleteImage(x,y)
                if piece.isWhite:
                    self.whitePieces.remove(piece)
                    if not self.whitePieces:
                        messagebox.showinfo("Game over!", "White won the game")
                        self.screen.screen.quit()
                else:
                    self.blackPieces.remove(piece)
                    if not self.blackPieces:
                        print('Black won the game')
                        messagebox.showinfo("Game over!", "Black won the game")
                        self.screen.screen.quit()
                del piece
                self.moving(x,y,piece2)
                self.AIMove()
            elif not self.capturing and (x,y) in piece2.legalMoves:
                self.moving(x,y,piece2)
                self.AIMove()
            self.board.printBoard()
            print(len(self.whitePieces))
            print(len(self.blackPieces))
            print()
        else:
            self.capturing=False
            if piece!=None and piece.isWhite==self.whitesTurn:
                piece.findCaptureMoves(self.counter)

                # Ewentualnie programowanie dynamiczne, na początku sprawdzać już wszystkie ruchy zamiast po każdym kliknięciu

                if not piece.captureMoves:
                    ChessPiece.captureMoves.clear() 
                    for p in (self.whitePieces if self.whitesTurn else self.blackPieces):
                        p.findCaptureMoves(self.counter)
                    if not ChessPiece.captureMoves:
                        piece.findLegalMoves()
                        if not piece.legalMoves:
                            ChessPiece.legalMoves.clear()
                            for p in (self.whitePieces if self.whitesTurn else self.blackPieces):
                                p.findLegalMoves()
                            if not ChessPiece.legalMoves:
                                print(f'{"white" if self.whitesTurn else "black"} won the game')
                                msb = messagebox.showinfo("Game over!", f'{"white" if self.whitesTurn else "black"} won the game')
                                self.screen.screen.quit()
                        else:
                            self.leftButtonPressed=True
                            self.previousPosition=(x,y)
                            self.canvas.drawCircles(piece,piece.legalMoves)
                else:
                    self.leftButtonPressed=True
                    self.capturing=True
                    self.previousPosition=(x,y)
                    self.canvas.drawCircles(piece,piece.captureMoves)

    def moving(self,x,y,piece):
        self.whitesTurn=not self.whitesTurn
        self.counter+=1
        xx,yy=piece.x,piece.y
        if piece.type == "pawn":
            if piece.isWhite and y == 0:
                self.canvas.deleteImage(x, y)
                self.canvas.deleteImage(xx, yy)
                self.whitePieces.remove(piece)
                self.addPiece(Queen(xx, yy, 'w', self.board.board))
            if not piece.isWhite and y == 7:
                self.canvas.deleteImage(x, y)
                self.canvas.deleteImage(xx, yy)
                self.blackPieces.remove(piece)
                self.addPiece(Queen(xx, yy, 'b', self.board.board))
            piece = self.board.board[xx][yy]
        a,b=piece.changePosition(x,y,self.counter)
        self.canvas.move((xx,yy),(piece.x,piece.y),(a,b))
        self.canvas.canvas.update()

    def AIMove(self):
        message=self.board.fen(f'{"w" if self.whitesTurn else "b"} - - 0 0')
        message=antichessAI.get(message)
        x=int(message//1000)
        y=int(message%1000//100)
        x2=int(message%100/10)
        y2=int(message%10)
        piece2=self.board.board[x2][y2]
        piece=self.board.board[x][y]
        print(piece)
        print(piece2)
        print(x,y)
        print(x2,y2)
        if piece!=None:
            self.canvas.deleteImage(x,y)
            if piece.isWhite:
                self.whitePieces.remove(piece)
                if not self.whitePieces:
                    print('White won the game')
                    msb = messagebox.showinfo("Game over!", "White won the game!")

                    self.screen.screen.quit()
            else:
                self.blackPieces.remove(piece)
                if not self.blackPieces:
                    print('Black won the game')
                    msb = messagebox.showinfo("Game over!", "Black won the game!")
                    self.screen.screen.quit()
            del piece
        
        self.moving(x,y,piece2)
    def p(self):
        self.clear()
        fen=self.fenEntry.get()
        self.setBoard(fen)

    def clear(self):
        self.canvas.clear()
        self.whitePieces.clear()
        self.blackPieces.clear()
        self.leftButtonPressed=False
        self.capturing=False
        self.counter=0
        self.previousPosition=(-1,-1)
        del self.board
        self.board=Board()