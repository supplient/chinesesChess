NO_PIECE = 0
PAWN = 1
CANNON = 2
ROOK = 3
KNIGHT = 4
MINISTER = 5
GUARD = 6
KING = 7

verPadding = 15
horPadding = 15
gridLength = 20
horEnd = horPadding + 8*gridLength
verEnd = verPadding + 9*gridLength

pieceLength = 20

piecesText = {0:'', 1:'兵', 2:'炮', 3:'车', 4:'马', 5:'相', 6:'仕', 7:'帅', 
					-1:'卒', -2:'炮', -3:'車', -4:'馬', -5:'象', -6:'士', -7:'将'}

from enhancedEnum import *
					
class Side(EnhancedEnum):
	RED = 0
	BLUE = 1