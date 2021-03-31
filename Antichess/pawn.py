from chessPiece import ChessPiece

class Pawn(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)
    def findLegalMoves(self):
        self.captureMoves.clear()
        sign=-1 if self.isWhite else 1
        if self.x>0:
            move=(self.x-1,self.y+sign)
            if self.board.board[move[0]][move[1]]!=None and self.board.board[move[0]][move[1]].isWhite!=self.isWhite:
                self.game.captureMoves.append(move)
                self.captureMoves.append(move)
        if self.x<7:
            move=(self.x+1,self.y+sign)
            if self.board.board[move[0]][move[1]]!=None and self.board.board[move[0]][move[1]].isWhite!=self.isWhite:
                self.game.captureMoves.append(move)
                self.captureMoves.append(move)
    def findLegalMoves2(self):
        self.legalMoves.clear()
        sign=-1 if self.isWhite else 1
        d=0 if self.isWhite else 7
        if self.y!=d and self.board.board[self.x][self.y+sign]==None:
            self.legalMoves.append((self.x,self.y+sign))
            self.game.legalMoves.append((self.x,self.y+sign))
        if self.alreadyMoved==False and len(self.legalMoves)>0 and self.board.board[self.x][self.y+sign*2]==None:
            self.legalMoves.append((self.x,self.y+sign*2))
            self.game.legalMoves.append((self.x,self.y+sign*2))
