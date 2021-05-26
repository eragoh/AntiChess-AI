#include <Python.h>
#include<vector>

int DEPTH=6;
#define WHITE false
#define BLACK true
#define DEFAULT_POSITION_DATA -50
#define PAWN 1
#define KING 2
#define KNIGHT 3
#define BISHOP 4
#define ROOK 5
#define QUEEN 9
#define CAPTURE 1
#define MOVE 2

struct Piece {
	unsigned char value;  //kolor*10+value
	unsigned char number; //numer 0-31
	char enpassant;

	Piece(unsigned char value, unsigned char number,char enpassant=-1) {
		this->value = value;
		this->number = number;
		this->enpassant=enpassant;
	}
};

class TreeNode {
public:
	int data = DEFAULT_POSITION_DATA;
};

class Leaf : public TreeNode {
public:
	Leaf(Piece* p, bool color, char whiteAmount, char blackAmount) {
		if (p != NULL) {
			if (color == WHITE && whiteAmount == p->value) {
				data = -10000;
			}
			else if (color == BLACK && blackAmount == p->value % 10) {
				data = 10000;
			}
		}
		if (data == DEFAULT_POSITION_DATA) {
			data = int(whiteAmount) - int(blackAmount);
		}
	}
};

class SuperNode : public TreeNode {
protected:
	bool continueBuilding = true;
	Piece*** board;
	char* pieces;
public:
	SuperNode(Piece*** b, char* p, bool color, unsigned int counter, char whiteAmount, char blackAmount, char depth) {
		pieces = new char[32];
		for (int i = 0; i < 32; i++) {
			pieces[i] = p[i];
		}
		board = new Piece * *[8];
		for (int i = 0; i < 8; i++) {
			board[i] = new Piece * [8];
			for (int j = 0; j < 8; j++) {
				board[i][j] = b[i][j] == NULL ? NULL : new Piece(b[i][j]->value, b[i][j]->number,b[i][j]->enpassant);
			}
		}
	}
	void buildTree(unsigned int counter, bool color, char whiteAmount, char blackAmount, char depth) {
		bool capturedPiece = false;
		int turn = color == WHITE ? 0 : 16;
		for (int i = turn; i < turn + 16 && continueBuilding; i++) {
			bool b = captureMove(pieces[i], counter, whiteAmount, blackAmount, depth, color); //ruch figura
			if (!capturedPiece) {
				capturedPiece = b;
			}
		}
		if (!capturedPiece) {
			bool moved = false;
			int turn2 = color == WHITE ? 0 : 16;
			for (int i = turn; i < turn + 16 && continueBuilding; i++) {
				bool b = legalMove(pieces[i], counter, whiteAmount, blackAmount, depth, color); //ruch figur
				if (!moved) {
					moved = b;
				}
			}
			if (!moved) {
				if (color == WHITE)
					data = -10000;
				else
					data = 10000;
			}
		}
		for (int i = 0; i < 8; i++) {
			delete[] board[i];
		}
		delete[] board;
		delete[] pieces;
		board = NULL;
		pieces = NULL;
	}
	bool legalMove(char figure, int counter, char whiteAmount, char blackAmount, char depth, bool color) {
		if (figure == -1) {
			return false;
		}
		char bishopTab[4][2] = { {-1,-1},{1,-1},{-1,1},{1,1} };
		char rookTab[4][2] = { {-1,0},{0,1},{1,0},{0,-1} };
		bool b = false;
		switch (board[figure / 10][figure % 10]->value % 10) {
		case PAWN:
			if (pawnMoving(figure, counter, whiteAmount, blackAmount, depth, color) == MOVE) {
				return true;
			}
			break;
		case KING:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, false, bishopTab) == MOVE) {
				b = true;
			}
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, false, rookTab) == MOVE) {
				b = true;
			}
			break;
		case KNIGHT:
			if (knightMoving(figure, counter, whiteAmount, blackAmount, depth, false, color) == MOVE) {
				return true;
			}
			break;
		case BISHOP:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, false, bishopTab) == MOVE) {
				b = true;
			}
			break;

		case ROOK:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, false, rookTab) == MOVE) {
				b = true;
			}
			break;

		case QUEEN:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, false, bishopTab) == MOVE) {
				b = true;
			}
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, false, rookTab) == MOVE) {
				b = true;
			}
			break;

		}
		return b;
	}
	bool captureMove(char figure, int counter, char whiteAmount, char blackAmount, char depth, bool color) {
		if (figure == -1) {
			return false;
		}
		char bishopTab[4][2] = { {-1,-1},{1,-1},{-1,1},{1,1} };
		char rookTab[4][2] = { {-1,0},{0,1},{1,0},{0,-1} };
		bool b = false;
		switch (board[figure / 10][figure % 10]->value % 10) {
		case PAWN:
			if (pawnCapturing(figure, counter, whiteAmount, blackAmount, depth, color) == CAPTURE) {
				return true;
			}
			break;
		case KING:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, true, bishopTab) == CAPTURE) {
				b = true;
			}
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, true, rookTab) == CAPTURE) {
				b = true;
			}
			break;
		case KNIGHT:
			if (knightMoving(figure, counter, whiteAmount, blackAmount, depth, true, color) == CAPTURE) {
				return true;
			}
			break;
		case BISHOP:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, true, bishopTab) == CAPTURE) {
				b = true;
			}
			break;

		case ROOK:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, true, rookTab) == CAPTURE) {
				b = true;
			}
			break;

		case QUEEN:
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, true, bishopTab) == CAPTURE) {
				b = true;
			}
			if (figureMoving(figure, counter, whiteAmount, blackAmount, depth, color, true, rookTab) == CAPTURE) {
				b = true;
			}
			break;

		}
		return b;
	}
	char pawnMoving(char figure, int counter, char whiteAmount, char blackAmount, char depth, bool color) {
		char x = figure / 10, y = figure % 10;
		char sign = color == WHITE ? -1 : 1, d = color == WHITE ? 0 : 7;
		if (y != d && board[x][y + sign] == NULL && continueBuilding) {
			addNode(counter, whiteAmount, blackAmount, color, depth, 10 * x + y + sign, figure);
			if (y != d - sign && board[x][y]->enpassant == -1 && board[x][y + 2 * sign] == NULL && continueBuilding) {
                if((color==WHITE && y==1) || (color==BLACK && y==6)){
                    addNode(counter, whiteAmount, blackAmount, color, depth, 10 * x + y + 2 * sign, figure);
                }
			}
			return MOVE;
		}
		return 0;
	}
	char pawnCapturing(char figure, int counter, char whiteAmount, char blackAmount, char depth, bool color) {
		char b = 0;
		char x = figure / 10, y = figure % 10;
		char sign = color == WHITE ? -1 : 1, d = color == WHITE ? 0 : 7;
		if (x > 0 && y != d && board[x - 1][y + sign] != NULL && board[x - 1][y + sign]->value / 10 != board[figure / 10][figure % 10]->value / 10 && continueBuilding) {
			addNode(counter, whiteAmount, blackAmount, color, depth, 10 * (x - 1) + y + sign, figure);
			b = CAPTURE;
		}
		if (x < 7 && y != d && board[x + 1][y + sign] != NULL && board[x + 1][y + sign]->value / 10 != board[figure / 10][figure % 10]->value / 10 && continueBuilding) {
			addNode(counter, whiteAmount, blackAmount, color, depth, 10 * (x + 1) + y + sign, figure);
			b = CAPTURE;
		}
		bool b2 = false;
		if (color == WHITE && y == 3) {
			b2 = true;
		}
		else if (color == BLACK && y == 4) {
			b2 = true;
		}
		if (b2) {
			if (x - 1 >= 0 && board[x - 1][y] != NULL && board[x - 1][y]->value % 10 == PAWN && board[x - 1][y]->enpassant == counter && continueBuilding) {
				addNode(counter, whiteAmount, blackAmount, color, depth, 10 * (x - 1) + y + sign, figure, 10 * (x - 1) + y);
				b = CAPTURE;

			}
			if (x + 1 <= 7 && board[x + 1][y] != NULL && board[x + 1][y]->value % 10 == PAWN && board[x + 1][y]->enpassant == counter && continueBuilding) {
				addNode(counter, whiteAmount, blackAmount, color, depth, 10 * (x + 1) + y + sign, figure, 10 * (x + 1) + y);
				b = CAPTURE;
			}
		}
		return b;
	}
	char figureMoving(char figure, int counter, char whiteAmount, char blackAmount, char depth, bool color, bool capturing, char tab[4][2]) {
		char b = 0;
		char x = figure / 10, y = figure % 10;
		char tab2[4][2];
		for (int i = 0; i < 4; i++) {
			for (int k = 0; k < 4; k++) {
				for (int j = 0; j < 2; j++) {
					tab2[i][j] = tab[i][j];
				}
			}
			while (b != CAPTURE && x + tab2[i][0] >= 0 && x + tab2[i][0] <= 7 && y + tab2[i][1] >= 0 && y + tab2[i][1] <= 7 && continueBuilding) {
				if (capturing && board[x + tab2[i][0]][y + tab2[i][1]] != NULL && board[x + tab2[i][0]][y + tab2[i][1]]->value / 10 != board[figure / 10][figure % 10]->value / 10) {
					addNode(counter, whiteAmount, blackAmount, color, depth, (x + tab2[i][0]) * 10 + y + tab2[i][1], figure);
					b = CAPTURE;
				}
				else if (board[x + tab2[i][0]][y + tab2[i][1]] != NULL && board[x + tab2[i][0]][y + tab2[i][1]]->value / 10 == board[figure / 10][figure % 10]->value / 10) {
					break;
				}
				else if (!capturing) {
					b = MOVE;
					addNode(counter, whiteAmount, blackAmount, color, depth, (x + tab2[i][0]) * 10 + y + tab2[i][1], figure);
				}
				if (board[figure / 10][figure % 10]->value % 10 == KING) {
					break;
				}
				tab2[i][0] += tab[i][0];
				tab2[i][1] += tab[i][1];
			}
		}
		return b;
	}
	char knightsMoves(char x, char y, char figure, int counter, char whiteAmount, char blackAmount, char depth, bool capturing, bool color) {
		char b = 0;
		if (capturing && board[x][y] != NULL && board[x][y]->value / 10 != board[figure / 10][figure % 10]->value / 10) {
			addNode(counter, whiteAmount, blackAmount, color, depth, x * 10 + y, figure);
			b = CAPTURE;
		}
		else if (!capturing && board[x][y] == NULL) {
			addNode(counter, whiteAmount, blackAmount, color, depth, x * 10 + y, figure);
			b = MOVE;
		}
		return b;
	}
	char knightMoving(char figure, int counter, char whiteAmount, char blackAmount, char depth, bool capturing, bool color) {
		char b = 0;
		char c=0;
		char x = figure / 10, y = figure % 10;
		if (x - 1 >= 0 && y - 2 >= 0 && continueBuilding) {
			b = knightsMoves(x - 1, y - 2, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x + 1 <= 7 && y - 2 >= 0 && continueBuilding) {
			b = knightsMoves(x + 1, y - 2, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x - 2 >= 0 && y - 1 >= 0 && continueBuilding) {
			b = knightsMoves(x - 2, y - 1, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x + 2 <= 7 && y - 1 >= 0 && continueBuilding) {
			b = knightsMoves(x + 2, y - 1, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x - 2 >= 0 && y + 1 <= 7 && continueBuilding) {
			b = knightsMoves(x - 2, y + 1, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x + 2 <= 7 && y + 1 <= 7 && continueBuilding) {
			b = knightsMoves(x + 2, y + 1, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x - 1 >= 0 && y + 2 <= 7 && continueBuilding) {
			b = knightsMoves(x - 1, y + 2, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		if (x + 1 <= 7 && y + 2 <= 7 && continueBuilding) {
			b = knightsMoves(x + 1, y + 2, figure, counter, whiteAmount, blackAmount, depth, capturing, color);
			if(b==CAPTURE){
                c=1;
			}
		}
		return c;
	}

	virtual void addNode(int counter, char whiteAmount, char blackAmount, bool color, char depth, char destination, char figureToMove, char enpassantMove = -1) = 0;
};

class Node : public SuperNode {

public:
	TreeNode* father = NULL;
	Node(Piece*** b, char* p, bool color, unsigned int counter, char destination, char figureToMove, char whiteAmount, char blackAmount, char depth, TreeNode* father, char enpassantMove = -1)
		:SuperNode(b, p, color, counter, whiteAmount, blackAmount, depth) {
		this->father = father;
		char x, y;
		if (enpassantMove == -1) {
			x = destination / 10;
			y = destination % 10;
		}
		else {
			x = enpassantMove / 10;
			y = enpassantMove % 10;
		}
		if (board[x][y] != NULL) {
			pieces[board[x][y]->number] = -1;
			if (color == WHITE) {
				whiteAmount -= board[x][y]->value;
				if (whiteAmount == 0) {
					data = -10000;
				}
			}
			else {
				blackAmount -= board[x][y]->value % 10;
				if (blackAmount == 0) {
					data = 10000;
				}
			}
			if (board[x][y] != NULL) {
				delete board[x][y];
			}
		}
		if (data == DEFAULT_POSITION_DATA) {
			board[destination / 10][destination % 10] = board[figureToMove / 10][figureToMove % 10];
			board[figureToMove / 10][figureToMove % 10] = NULL;
			pieces[board[destination / 10][destination % 10]->number] = destination;
			if (board[destination / 10][destination % 10]->enpassant == -1) {
				board[destination / 10][destination % 10]->enpassant = counter;
			}
			buildTree(counter, color, whiteAmount, blackAmount, depth);
			if (color == WHITE && data > father->data) {
				father->data = data;
			}
			else if (color == BLACK && data < father->data) {
				father->data = data;
            }
		}
        if (father->data == DEFAULT_POSITION_DATA) {
            father->data = data;
        }
	}
	void addNode(int counter, char whiteAmount, char blackAmount, bool color, char depth, char destination, char figureToMove, char enpassantMove = -1) {
		int d;
		if (depth == 1) {
			char x, y;
			if (enpassantMove == -1) {
				x = destination / 10;
				y = destination % 10;
			}
			else {
				x = enpassantMove / 10;
				y = enpassantMove % 10;
			}
			Leaf* leaf;
			if (color == WHITE && y == 0 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				leaf = new Leaf(board[x][y], !color, whiteAmount + 8, blackAmount);
			}
			else if (color == BLACK && y == 7 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				leaf = new Leaf(board[x][y], !color, whiteAmount, blackAmount + 8);
			}
			else
			{
				leaf = new Leaf(board[x][y], !color, whiteAmount, blackAmount);
			}
			d = leaf->data;
            delete leaf;
		}
		else {
			Node* node;
			char y = destination % 10;
			if (color == WHITE && y == 0 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				//leaf = new Leaf(board[x][y], !color, whiteAmount + 8, blackAmount);
				board[figureToMove / 10][figureToMove % 10]->value = QUEEN;
				node = new Node(board, pieces, !color, counter + 1, destination, figureToMove, whiteAmount + 8, blackAmount, depth - 1, this, enpassantMove);
				board[figureToMove / 10][figureToMove % 10]->value = PAWN;
			}
			else if (color == BLACK && y == 7 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				//leaf = new Leaf(board[x][y], !color, whiteAmount, blackAmount + 8);
				board[figureToMove / 10][figureToMove % 10]->value = QUEEN + 10;
				node = new Node(board, pieces, !color, counter + 1, destination, figureToMove, whiteAmount, blackAmount + 8, depth - 1, this, enpassantMove);
				board[figureToMove / 10][figureToMove % 10]->value = PAWN + 10;
			}
			else
			{
				node = new Node(board, pieces, !color, counter + 1, destination, figureToMove, whiteAmount, blackAmount, depth - 1, this, enpassantMove);
			}
			d = node->data;
			delete node;
		}

		if(depth==1 && data==DEFAULT_POSITION_DATA){
            data=d;
		}

		if (color == WHITE && d < data) {
			data = d;
		}
		else if (color == BLACK && d > data) {
			data = d;
		}
		if (color == WHITE && data < father->data) {
			continueBuilding = false;
		}
		else if (color == BLACK && data > father->data) {
			continueBuilding = false;
		}
	}
};

class Root : public SuperNode {
public:
	int index = 0;
	std::vector<int> returnValue;
public:
	Root(Piece*** b, char* p, bool color, char whiteAmount, char blackAmount) :SuperNode(b, p, color, 0, whiteAmount, blackAmount, DEPTH) {
		buildTree(0, color, whiteAmount, blackAmount, DEPTH);
	}

	void addNode(int counter, char whiteAmount, char blackAmount, bool color, char depth, char destination, char figureToMove, char enpassantMove = -1) {
		int d;
		returnValue.push_back(100 * (int)(destination)+(int)(figureToMove));
		if (depth == 1) {
			Leaf* leaf;
			char y = destination % 10;
			if (color == WHITE && y == 0 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				leaf = new Leaf(board[destination / 10][destination % 10], !color, whiteAmount + 8, blackAmount);
			}
			else if (color == BLACK && y == 7 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				leaf = new Leaf(board[destination / 10][destination % 10], !color, whiteAmount, blackAmount + 8);
			}
			else
			{
				leaf = new Leaf(board[destination / 10][destination % 10], !color, whiteAmount, blackAmount);
			}
			d = leaf->data;
			delete leaf;
		}
		else {
			Node* node;
			char y = destination % 10;
			if (color == WHITE && y == 0 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				//leaf = new Leaf(board[x][y], !color, whiteAmount + 8, blackAmount);
				board[figureToMove / 10][figureToMove % 10]->value = QUEEN;
				node = new Node(board, pieces, !color, counter + 1, destination, figureToMove, whiteAmount + 8, blackAmount, depth - 1, this, enpassantMove);
				board[figureToMove / 10][figureToMove % 10]->value = PAWN;
			}
			else if (color == BLACK && y == 7 && board[figureToMove / 10][figureToMove % 10]->value % 10 == PAWN)
			{
				//leaf = new Leaf(board[x][y], !color, whiteAmount, blackAmount + 8);
				board[figureToMove / 10][figureToMove % 10]->value = QUEEN + 10;
				node = new Node(board, pieces, !color, counter + 1, destination, figureToMove, whiteAmount, blackAmount + 8, depth - 1, this, enpassantMove);
				board[figureToMove / 10][figureToMove % 10]->value = PAWN + 10;
			}
			else
			{
				node = new Node(board, pieces, !color, counter + 1, destination, figureToMove, whiteAmount, blackAmount, depth - 1, this, enpassantMove);
			}
			d = node->data;
			delete node;
		}

        if((d==-10000 && color==WHITE) || (d==10000 && color==BLACK)){
            index=index=returnValue.size()-1;
        }
        
		if (color == WHITE && d <= data) {
			data = d;
			index=returnValue.size()-1;
		}
		else if(color == BLACK && d >= data) {
			data = d;
			index=returnValue.size()-1;
		}
	}
};

bool setChess(Piece ***tab,char p[32],char *fen,char &w,char &b){
    int row=0,column=0;
    int white=0,black=16;
    w=0;
    b=0;
    for(int i=0;fen[i]!='\0';i++){
        switch(fen[i]){
        case 'R':
            tab[column][row]=new Piece(5,white);
            p[white]=10*column+row;
            white++;
            column++;
            w+=5;
            break;
        case 'r':
            tab[column][row]=new Piece(15,black);
            p[black]=10*column+row;
            black++;
            column++;
            b+=5;
            break;
        case 'N':
            tab[column][row]=new Piece(3,white);
            p[white]=10*column+row;
            white++;
            column++;
            w+=3;
            break;
        case 'n':
            tab[column][row]=new Piece(13,black);
            p[black]=10*column+row;
            black++;
            column++;
            b+=3;
            break;
        case 'B':
            tab[column][row]=new Piece(4,white);
            p[white]=10*column+row;
            white++;
            column++;
            w+=4;
            break;
        case 'b':
            tab[column][row]=new Piece(14,black);
            p[black]=10*column+row;
            black++;
            column++;
            b+=4;
            break;
        case 'Q':
            tab[column][row]=new Piece(9,white);
            p[white]=10*column+row;
            white++;
            column++;
            w+=9;
            break;
        case 'q':
            tab[column][row]=new Piece(19,black);
            p[black]=10*column+row;
            black++;
            column++;
            b+=9;
            break;
        case 'K':
            tab[column][row]=new Piece(2,white);
            p[white]=10*column+row;
            white++;
            column++;
            w+=2;
            break;
        case 'k':
            tab[column][row]=new Piece(12,black);
            p[black]=10*column+row;
            black++;
            column++;
            b+=2;
            break;
        case 'P':
            tab[column][row]=new Piece(1,white);
            p[white]=10*column+row;
            white++;
            column++;
            w++;
            break;
        case 'p':
            tab[column][row]=new Piece(11,black);
            p[black]=10*column+row;
            black++;
            column++;
            b++;
            break;
        case '/':
            row++;
            column=0;
            break;
        default:
            if(fen[i]>='1' && fen[i]<='9'){
                int maximum=int(fen[i])-48;
                for(int i=0;i<maximum;i++){
                    tab[column][row]=NULL;
                    column++;
                }
            }else if(fen[i]==' '){
                for(int i=white;i<16;i++){
                    p[i]=-1;
                }
                for(int i=black;i<32;i++){
                    p[i]=-1;
                }
                return fen[i+1]=='w' ? WHITE:BLACK;
            }
            break;
        }
    }
}

int getMove(char *fen){
    Piece*** tab;
	tab = new Piece * *[8];
	for (int i = 0; i < 8; i++) {
		tab[i] = new Piece * [8];
	}
	char p[32];
	char whiteAmount, blackAmount;
    bool color=setChess(tab,p,fen,whiteAmount,blackAmount);
    Root* root = new Root(tab, p, color, whiteAmount, blackAmount);
    int value=root->returnValue[root->index];
    delete root;
    return value;
}


static PyObject* antichessAI_get(PyObject* self,PyObject *args){
	char *msg;
	int sts=0;

	if(!PyArg_ParseTuple(args,"s",&msg)){
        return NULL;
    }

	sts=getMove(msg);
	return Py_BuildValue("i",sts);
}

static PyObject* antichessAI_getD(PyObject* self,PyObject *args){
	char *msg;
	int d=0;
	int sts=0;

	if(!PyArg_ParseTuple(args,"si",&msg,&d)){
        return NULL;
    }
	DEPTH=d;
	sts=getMove(msg);
	return Py_BuildValue("i",sts);
}

static PyMethodDef antichessAI_methods[]={
	{"get",antichessAI_get,METH_VARARGS,"Get best move // Antichess"},
	{"getD",antichessAI_getD,METH_VARARGS,"Get best move with given depth // Antichess"},
	{NULL,NULL,0,NULL}
};

static struct PyModuleDef AntichessAI={
	PyModuleDef_HEAD_INIT,
	"antichessAI",
	NULL,
	-1,
	antichessAI_methods
};

PyMODINIT_FUNC PyInit_antichessAI(void){
	return PyModule_Create(&AntichessAI);
}