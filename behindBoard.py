import pdb

def get_init_board():
	board = [[0 for i in range(9)] for i in range(10)]
	i=0
	for i in range(9):
		board[0][i] = 7-abs(i - 4)
		board[9][i] = -board[0][i]
	#炮
	board[2][1] = 2
	board[2][7] = 2
	board[7][1] = -2
	board[7][7] = -2
	#兵卒
	for i in range(0, 9, 2):
		board[3][i] = 1
		board[6][i] = -1
	return board
	
def gameover(board):
	isover = 0
	redwin = 0
	bluewin = 0
	for i in range(10):
		for j in range(9):
			if board[i][j] == 7:
				isover += 1
				redwin = 1
			if board[i][j] == -7:
				bluewin = 1
				isover += 1
	if isover == 2:
		return 'continue'
	if isover != 2 and redwin:
		return 'redwin'
	if isover != 2 and bluewin:
		return 'bluewin'

class behindBoard:
	dict = {	'帅': 7 , '仕':6,'相':5,'马':4,"车":3,"帅炮":2,"兵":1,"将":-7,"士":-6,"象":-5,"馬":-4,"車":-3,"将炮":-2,"卒":-1,'  ':0}
	def __init__(self,startPoint,endPoint):
		self.startPoint=startPoint
		self.endPoint=endPoint
	
	def move(self,board):
		if not board[self.endPoint[0]][self.endPoint[1]]*board[self.startPoint[0]][self.startPoint[1]]<=0:
			return False
		i=self.startPoint[0]
		j=self.startPoint[1]
		k=self.endPoint[0]
		l=self.endPoint[1]
		naxt=[]
		startNum=board[i][j]
		endNum=board[k][l]
		index=abs(startNum)
		nums=0
		if self.startPoint==self.endPoint:
			return 0
		if index == 7:
			next = [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]
			if (k not in (0, 1, 2, 7, 8, 9) )or (l not in (3, 4, 5)):
				return 0
			if (i>6 and k>6):
				if (k,l)not in next:
					return 0
				else:
					return 1
			elif (i<3 and k<3):
				if (k,l) not in	 next:
					return 0
				else:
					return 1
			else:
				if j == l:
					for k_try in range(min(i, k) + 1, max(i, k)):
						if board[k_try][l] != 0:
							nums += 1
					if (nums==0 and board[k][l]==-board[i][j]):
						return 1
					else:
						return 0
				else:
					return 0	

		if index == 6:
			next = [(i - 1, j - 1), (i + 1, j - 1), (i - 1, j + 1), (i + 1, j + 1)]
			if ((k,l) not in  next) or (k not in (0, 1, 2, 7, 8, 9) or l not in (3, 4, 5)) or (board[i][j] * board[k][l] > 0):
				return 0
			else:
				return 1

		if index == 5:
			next = [(i - 2, j - 2), (i + 2, j - 2), (i - 2, j + 2), (i + 2, j + 2)]
			if ((k,l) not in  next) or( (k - 4.5) * (i - 4.5) < 0 or k < 0 or k > 9 or l < 0 or l > 8 ) or (board[i][j] * board[k][l] > 0):
				return 0
			elif board[int((i + k) / 2)][int((j + l) / 2)] != 0:
				return 0
			else:
				return 1
		if index == 4:
			next = [(i - 2, j + 1), (i - 2, j - 1), (i - 1, j + 2), (i - 1, j - 2), (i + 2, j - 1), (i + 2, j + 1),(i + 1, j + 2), (i + 1, j - 2)]
			foot_i = int(i if abs(k - i) == 1 else (i + k) / 2)
			foot_j = int(j if abs(l - j) == 1 else (j + l) / 2)
			if(k < 0 or k > 9 or l < 0 or l > 8)or((k,l) not in	 next) or (board[i][j] * board[k][l] > 0):
				return 0
			elif board[foot_i][foot_j] != 0:
				return 0
			else:
				return 1
		#3：车 2：炮
		if index == 3 or index==2:
			nums=0
			if i==k:
				for	 l_try in  range(min(j, l) + 1,max(j, l)):
					if board[k][l_try] != 0:
						nums += 1
			if j==l:
				for	 k_try in  range(min(i,k) + 1,max(i,k)):
					if board[k_try][l] != 0:
						nums += 1
			if index == 3 and nums == 0:
				return 1
			elif (index == 2):
				if ((board[k][l] == 0 and nums == 0) or (board[k][l] != 0 and nums == 1)):
					return 1
			else:
				return 0
		if index == 1:
			if startNum * (i - 4.5) < 0:
				next = [(i + startNum, j)]
			else:
				next = [(i + startNum, j), (i, j - 1), (i, j + 1)]
			if (k < 0 or k > 9 or l < 0 or l > 8) or ((k,l) not in	next) or (board[i][j] * board[k][l] > 0):
				return 0
			else:
				return 1

