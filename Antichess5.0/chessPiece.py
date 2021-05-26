class ChessPiece:
    captureMoves=[]
    legalMoves=[]

    def __init__(self,x,y,color,board,type):
        self.x=x
        self.y=y
        self.isWhite=color=='w'
        self.board=board
        self.type=type
        self.enpassant=-1
        self.alreadyMoved=False

        self.captureMoves=[]
        self.legalMoves=[]
    
    def changePosition(self,x,y,counter):
        a,b=x-self.x,y-self.y
        self.board[x][y]=self.board[self.x][self.y]
        self.board[self.x][self.y]=None
        self.x,self.y=x,y
        if not self.alreadyMoved:
            self.alreadyMoved=True
            if self.type=='pawn':
                self.enpassant=counter if b==2 else -1
        if type=='pawn':
            if self.isWhite:
                if self.y==0:
                    pass#promocja
            else:
                if self.y==7:
                    pass#promocja

        return a*60,b*60

    def figureMoving(self,capturing,isKing,list):
        x,y=self.x,self.y
        for i in range(4):
            l=[x[:] for x in list]
            while x+l[i][0]>=0 and x+l[i][0]<=7 and y+l[i][1]>=0 and y+l[i][1]<=7:
                if capturing and self.board[x+l[i][0]][y+l[i][1]]!=None and self.board[x+l[i][0]][y+l[i][1]].isWhite!=self.isWhite:
                    self.captureMoves.append((x+l[i][0],y+l[i][1]))
                    ChessPiece.captureMoves.append((x+l[i][0],y+l[i][1]))
                    break
                elif self.board[x+l[i][0]][y+l[i][1]]!=None and self.board[x+l[i][0]][y+l[i][1]].isWhite==self.isWhite:
                    break
                elif not capturing:
                    self.legalMoves.append((x+l[i][0],y+l[i][1]))
                    ChessPiece.legalMoves.append((x+l[i][0],y+l[i][1]))
                if isKing:
                    break
                l[i][0]+=list[i][0]
                l[i][1]+=list[i][1]