from chessPiece import ChessPiece

class King(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)
    def findLegalMoves(self):
        self.captureMoves.clear()
        self.bishopMove(True,True)
        self.rookMove(True,True)

    def findLegalMoves2(self):
        self.legalMoves.clear()
        self.bishopMove(False,True)
        self.rookMove(False,True)
