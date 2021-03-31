from chessPiece import ChessPiece

class Queen(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)
    def findLegalMoves(self):
        self.captureMoves.clear()
        self.bishopMove(True,False)
        self.rookMove(True,False)

    def findLegalMoves2(self):
        self.legalMoves.clear()
        self.bishopMove(False,False)
        self.rookMove(False,False)
