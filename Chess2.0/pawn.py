from chessPiece import ChessPiece

class Pawn(ChessPiece):
    def __init__(self,coordinates,img_path,board,canvas,color,game):
        super().__init__(coordinates,img_path,board,canvas,color,game)  
    def findLegalMoves(self):
        self.legalMoves.clear()
        sign=-1 if self.color=='w' else 1
        move=self.position+sign
        if not self.alreadyMoved:
            if self.checkMove(move) and self.board.board[move]==None:
                move+=sign
                if self.checkMove(move) and self.board.board[move]==None:
                    self.legalMoves.append(move)
                move-=sign
        if self.checkMove(move) and self.board.board[move]==None:
            self.legalMoves.append(move)
        
        if self.position//8!=0 and self.position%8!=0 and self.board.board[self.position-9]!=None and self.board.board[self.position-9].color!=self.color:
            self.legalMoves.append(self.position-9)
        if self.position//8!=7 and self.position%8!=0 and self.board.board[self.position+7]!=None and self.board.board[self.position+7].color!=self.color:
            self.legalMoves.append(self.position+7)
    def checkMove(self,move):
        return move//8==self.position//8
