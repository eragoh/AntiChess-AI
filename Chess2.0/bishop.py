from chessPiece import ChessPiece

class Bishop(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)
    def findLegalMoves(self):
        self.legalMoves.clear()
        self.bishopMoving(True)
