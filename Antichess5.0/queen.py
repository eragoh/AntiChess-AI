from chessPiece import ChessPiece

class Queen(ChessPiece):
    def __init__(self,x,y,color,board):
        super().__init__(x,y,color,board,'queen')


    def findCaptureMoves(self, moveNumber = -1):
        self.captureMoves.clear()
        self.figureMoving(True,False,[[-1,-1],[1,-1],[-1,1],[1,1]])
        self.figureMoving(True,False,[[-1,0],[0,1],[1,0],[0,-1]])

    def findLegalMoves(self):
        self.legalMoves.clear()
        self.figureMoving(False,False,[[-1,-1],[1,-1],[-1,1],[1,1]])
        self.figureMoving(False,False,[[-1,0],[0,1],[1,0],[0,-1]])