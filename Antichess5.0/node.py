from chessPiece import ChessPiece
from copy import deepcopy

class Node:
    def __init__(self,white,black,color,counter,move,figure,depth):
        board=[]
        for _ in range(8):
            board.append([None for _ in range(8)])
        for element in white:
            board[element.x][element.y]=element
        for element in black:
            board[element.x][element.y]=element

        self.value=None
        self.children=[]

        if move:
            piece=board[figure[0]][figure[1]]
            if board[move[0]][move[1]]!=None:
                attackedPiece=board[move[0]][move[1]]
                if color=='b':
                    white.remove(attackedPiece)
                    if not white:
                        self.value=-10000
                else:
                    black.remove(attackedPiece)
                    if not black:
                        self.value=10000
                piece.x,piece.y=move[0],move[1]
                piece.alreadyMoved=True
        

        if depth>0:
            ChessPiece.captureMoves.clear()
            for piece in (white if color=='w' else black):
                piece.findCaptureMoves(counter)
                if piece.captureMoves:
                    for mov in piece.captureMoves:
                        w,b=deepcopy(white),deepcopy(black)
                        self.children.append(Node(w,b,'w' if color=='b' else 'b',counter+1,mov,(piece.x,piece.y),depth-1))

            if not ChessPiece.captureMoves:
                ChessPiece.legalMoves.clear()
                for piece in (white if color=='w' else black):
                    piece.findLegalMoves()
                    if piece.legalMoves:
                        for mov in piece.legalMoves:
                            if depth==3:
                                print('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx')
                            w,b=deepcopy(white),deepcopy(black)
                            self.children.append(Node(w,b,'w' if color=='b' else 'b',counter+1,mov,(piece.x,piece.y),depth-1))
                
                if not ChessPiece.legalMoves:
                    self.value=10000 if color == 'w' else -10000