from chessPiece import ChessPiece

class Bishop(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)


    def findCaptureMoves(self):
        self.captureMoves.clear()
        self.figureMoving(True,False,[[-1,-1],[1,-1],[-1,1],[1,1]])

    def findLegalMoves(self):
        self.legalMoves.clear()
        self.figureMoving(False,False,[[-1,-1],[1,-1],[-1,1],[1,1]])