from chessPiece import ChessPiece

class Knight(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)  
    def knightMoves(self,x,y):
        piece=self.board.board[x*8+y]
        if piece==None or piece.color!=self.color:
            self.legalMoves.append(x*8+y)
    def findLegalMoves(self):
        self.legalMoves.clear()
        x,y=divmod(self.position,8)
        if x-1>=0 and y-2>=0:
            self.knightMoves(x-1,y-2)
        if x+1<=7 and y-2>=0:
            self.knightMoves(x+1,y-2)
        if x-2>=0 and y-1>=0:
            self.knightMoves(x-2,y-1)
        if x+2<=7 and y-1>=0:
            self.knightMoves(x+2,y-1)
        if x-2>=0 and y+1<=7:
            self.knightMoves(x-2,y+1)
        if x+2<=7 and y+1<=7:
            self.knightMoves(x+2,y+1)
        if x-1>=0 and y+2<=7:
            self.knightMoves(x-1,y+2)
        if x+1<=7 and y+2<=7:
            self.knightMoves(x+1,y+2)