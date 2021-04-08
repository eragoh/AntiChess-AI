from chessPiece import ChessPiece

class Knight(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)


    def knightMoves(self,x,y,capturing):
        piece=self.board.board[x][y]
        if not capturing and piece==None:
            self.legalMoves.append((x,y))
            ChessPiece.legalMoves.append((x,y))
        elif capturing and piece!=None and piece.isWhite!=self.isWhite:
            self.captureMoves.append((x,y))
            ChessPiece.captureMoves.append((x,y))

    def findKnightMoves(self,capturing):
        self.captureMoves.clear()
        x,y=self.x,self.y
        if x-1>=0 and y-2>=0:
            self.knightMoves(x-1,y-2,capturing)
        if x+1<=7 and y-2>=0:
            self.knightMoves(x+1,y-2,capturing)
        if x-2>=0 and y-1>=0:
            self.knightMoves(x-2,y-1,capturing)
        if x+2<=7 and y-1>=0:
            self.knightMoves(x+2,y-1,capturing)
        if x-2>=0 and y+1<=7:
            self.knightMoves(x-2,y+1,capturing)
        if x+2<=7 and y+1<=7:
            self.knightMoves(x+2,y+1,capturing)
        if x-1>=0 and y+2<=7:
            self.knightMoves(x-1,y+2,capturing)
        if x+1<=7 and y+2<=7:
            self.knightMoves(x+1,y+2,capturing)
    
    def findCaptureMoves(self, moveNumber = -1):
        self.captureMoves.clear()
        self.findKnightMoves(True)

    def findLegalMoves(self):
        self.legalMoves.clear()
        self.findKnightMoves(False)