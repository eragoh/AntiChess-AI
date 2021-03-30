class Board:
    def __init__(self):
        self.board=[None]
        self.board*=64
        self.whiteChecked=False
        self.blackChecked=False
    def decode(self,coordinates):#kod na pozycje
        return 8*(ord(coordinates[0])-65)+8-ord(coordinates[1])+48
    def encode(self,n):#pozycja na kod
        a,b=divmod(n,8)
        return chr(a+65)+chr(8-b+48)

b=Board()
print(b.encode(28))