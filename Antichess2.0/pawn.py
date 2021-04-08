from chessPiece import ChessPiece

class Pawn(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)
        self.isPawn=True
        self.enpassant=-1

    def findCaptureMoves(self, moveNumber = -1):
        self.captureMoves.clear()
        sign=-1 if self.isWhite else 1
        if self.x>0:
            move=(self.x-1,self.y+sign)
            if self.board.board[move[0]][move[1]]!=None and self.board.board[move[0]][move[1]].isWhite!=self.isWhite:
                ChessPiece.captureMoves.append(move)
                self.captureMoves.append(move)
        if self.x<7:
            move=(self.x+1,self.y+sign)
            if self.board.board[move[0]][move[1]]!=None and self.board.board[move[0]][move[1]].isWhite!=self.isWhite:
                ChessPiece.captureMoves.append(move)
                self.captureMoves.append(move)
        if self.y==3.5+0.5*sign:
            if self.x-1>=0 and self.board.board[self.x-1][self.y]!=None and self.board.board[self.x-1][self.y].isPawn \
                    and self.board.board[self.x-1][self.y].enpassant+1==(self.game.counter if moveNumber == -1 else moveNumber):
                ChessPiece.captureMoves.append((self.x-1,self.y+sign))
                self.captureMoves.append((self.x-1,self.y+sign))                  
            if self.x+1<=7 and self.board.board[self.x+1][self.y]!=None and self.board.board[self.x+1][self.y].isPawn \
                    and self.board.board[self.x+1][self.y].enpassant+1==(self.game.counter if moveNumber == -1 else moveNumber):
                ChessPiece.captureMoves.append((self.x+1,self.y+sign))
                self.captureMoves.append((self.x+1,self.y+sign)) 

    def findLegalMoves(self):
        self.legalMoves.clear()
        sign=-1 if self.isWhite else 1
        d=0 if self.isWhite else 7
        if self.y!=d and self.board.board[self.x][self.y+sign]==None:
            self.legalMoves.append((self.x,self.y+sign))
            ChessPiece.legalMoves.append((self.x,self.y+sign))
        if self.alreadyMoved==False and len(self.legalMoves)>0 and self.board.board[self.x][self.y+sign*2]==None:
            self.legalMoves.append((self.x,self.y+sign*2))
            ChessPiece.legalMoves.append((self.x,self.y+sign*2))