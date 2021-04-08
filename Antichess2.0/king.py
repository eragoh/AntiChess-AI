from chessPiece import ChessPiece

class King(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)


    def findCaptureMoves(self, moveNumber = -1):
        self.captureMoves.clear()
        self.figureMoving(True,True,[[-1,-1],[1,-1],[-1,1],[1,1]])
        self.figureMoving(True,True,[[-1,0],[0,1],[1,0],[0,-1]])

    def findLegalMoves(self):
        self.legalMoves.clear()
        self.figureMoving(False,True,[[-1,-1],[1,-1],[-1,1],[1,1]])
        self.figureMoving(False,True,[[-1,0],[0,1],[1,0],[0,-1]])