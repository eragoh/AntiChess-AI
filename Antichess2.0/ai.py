from chessPiece import ChessPiece
from copy import deepcopy

class Node:
    def __init__(self, white, black, color, move, figure, counter, depth):
        myslniki='-'*(3-depth)
        print(f'{myslniki} {figure} -> {move}')
        self.board = []
        for _ in range(8):
            self.board.append([None for _ in range(8)])
        for elem in white:
            self.board[elem.x][elem.y]=elem
        for elem in black:
            self.board[elem.x][elem.y]=elem
        self.value = None
        self.white = white
        self.black = black
        self.color = color
        self.children = []
        if move:
            piece = self.board[figure[0]][figure[1]]
            if self.board[move[0]][move[1]] != None:
                attacked_piece = self.board[move[0]][move[1]]
                if color == 'b':
                    white.remove(attacked_piece)
                    if not white:
                        self.value = 10000 if color == 'w' else -10000
                else:
                    black.remove(attacked_piece)
                    if not black:
                        self.value = 10000 if color == 'w' else -10000
                del attacked_piece
            piece.x, piece.y = move[0], move[1]
        ChessPiece.captureMoves.clear()
        ChessPiece.legalMoves.clear()
        if depth > 0:
            for piece in (white if color == 'w' else black):
                piece.findCaptureMoves(counter)
                if piece.captureMoves:
                    for mov in piece.captureMoves:
                        w, b = deepcopy(white), deepcopy(black)
                        self.children.append(Node(w, b, 'w' if color == 'b' else 'b', mov, (piece.x, piece.y), counter+1, depth-1))

            if not ChessPiece.captureMoves:
                for piece in (white if color == 'w' else black):
                    piece.findLegalMoves()
                    if piece.legalMoves:
                        for mov in piece.legalMoves:
                            w, b = deepcopy(white), deepcopy(black)
                            self.children.append(Node(w, b, 'w' if color == 'b' else 'b', mov, (piece.x, piece.y), counter+1, depth-1))
                if not ChessPiece.legalMoves:
                    self.value = 10000 if color == 'w' else -10000






class AI:
    def __init__(self,game):
        self.game = game
        w, b = deepcopy(game.whitePieces), deepcopy(game.blackPieces)
        self.root = Node(w, b, 'w', None, None, game.counter, 3)
        #zawsze AI jest czarne