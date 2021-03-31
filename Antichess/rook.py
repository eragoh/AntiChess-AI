from chessPiece import ChessPiece

class Rook(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)
    def findLegalMoves(self):
        self.captureMoves.clear()
        self.rookMove(True,False)

    def findLegalMoves2(self):
        self.legalMoves.clear()
        self.rookMove(False,False)
