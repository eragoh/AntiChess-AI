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
    def fen(self,color):
        fenNotation=''
        for i in range(8):
            fenNotation+='/'
            n=0
            for j in range(8):
                if self.board[j][i]==None:
                    n+=1
                else:
                    if n!=0:
                        fenNotation+=str(n)
                        n=0
                    if self.board[j][i].type=='king':
                        fenNotation+='K' if self.board[j][i].isWhite else 'k'
                    elif self.board[j][i].type=='queen':
                        fenNotation+='Q' if self.board[j][i].isWhite else 'q'
                    elif self.board[j][i].type=='rook':
                        fenNotation+='R' if self.board[j][i].isWhite else 'r'
                    elif self.board[j][i].type=='bishop':
                        fenNotation+='B' if self.board[j][i].isWhite else 'b'            
                    elif self.board[j][i].type=='knight':
                        fenNotation+='N' if self.board[j][i].isWhite else 'n'
                    elif self.board[j][i].type=='pawn':
                        fenNotation+='P' if self.board[j][i].isWhite else 'p'  
            if n!=0:
                fenNotation+=str(n)
        fenNotation=fenNotation[1:]
        fenNotation+=' '
        fenNotation+=color
        return fenNotation