class Board:
    def __init__(self):
        self.board=[]
        for _ in range(8):
            self.board.append([None for _ in range(8)])
    def decode(self,coordinates):
        return ord(coordinates[0])-65,8-ord(coordinates[1])+48
    def encode(self,x,y):
        return chr(x+65)+chr(8-y+48)
    def printBoard(self):
        for j in range(8):
            for i in range(8):
                if self.board[i][j]==None:
                    print(0,end=' ')
                elif self.board[i][j].isWhite:
                    print('w',end=' ')
                else:
                    print('b',end=' ')
            print()
