import sys
import os
sys.path.append(os.path.abspath(os.curdir))

import tkinter as tk
import pdb
from frontBoard_enum import *
from behindBoard import *


# def init_board():
	# board = []
	# for i in range(9):
		# column = []
		# for j in range(10):
			# column.append(NO_PIECE)
		# board.append(column)
	# for i in range(1, 8):
		# board[i][i]=i 
	# return board
	
def _get_row_column(x, y):
	x = int(x-horPadding)
	y = int(y-verPadding)
	row, column = int(x/gridLength), int(y/gridLength)
	if x%gridLength >= gridLength/2:
		row += 1
	if y%gridLength >= gridLength/2:
		column += 1
	return row, column
	
def _reverse_board(board):
	x_len = len(board)
	y_len = len(board[0])
	new_board = [[board[x][y] for x in range(x_len)] for y in range(y_len)]
	return new_board

def _board_change_side(board):
	x_len = len(board)
	y_len = len(board[0])
	new_board = [[board[x_len-x-1][y_len-y-1] for y in range(y_len)] for x in range(x_len)]
	return new_board
	
def _point_change_side(x_len, y_len, p):
	return x_len-p[0]-1, y_len-p[1]-1
	
def _reverse_point(p):
	return p[1], p[0]
	
def _get_piece_side(piece_type):
	if piece_type>0:
		return Side.RED
	else:
		return Side.BLUE

def _getBoardForWorstBehind(board, side):
	boardForWorstBehind = _reverse_board(board)
	if side == Side.RED:
		boardForWorstBehind = _board_change_side(boardForWorstBehind)
	return boardForWorstBehind

class FrontBoard(tk.Canvas):	
	def __init__(self, *args, onPieceMove, **keywords):
		super(FrontBoard, self).__init__(*args, **keywords)
		
		self.onceClicked = False
		self.board = _reverse_board(get_init_board())
		self.side = Side.BLUE
		self.runningSide = None
		self.onPieceMove = onPieceMove
		
		self.__draw_base_board()
		self.__draw_pieces()
		
		self.bind("<Button-1>", self.__onMouseLeftClicked)
		self.bind("<Button-3>", self.__onMouseRightClicked)
		
	def reset(self):
		self.board = _reverse_board(get_init_board())
		self.side = Side.BLUE
		self.runningSide = None
		self.__update_board()
		
	def move(self, sx, sy, ex, ey):
		self.__move(sx, sy , ex, ey)
		
	def setRunningSide(self, runningSide):
		self.runningSide = runningSide
	
	def setSide(self, side):
		if self.side == side:
			return
		self.reverseSide()
		
	def getSide(self):
		return self.side
		
	def isMyTurn(self):
		return self.side == self.runningSide
		
	def isGameOver(self):
		board = _getBoardForWorstBehind(self.board, self.side)
		judge = gameover(board)
		if judge == "continue":
			return False
		elif judge == "redwin":
			return Side.RED
		else:
			return Side.BLUE
		
		
	def reverseSide(self):
		if self.side == Side.RED:
			self.side = Side.BLUE
		else:
			self.side = Side.RED
		self.__change_side()
		
	def reverseRunningSide(self):
		if self.runningSide == Side.RED:
			self.runningSide = Side.BLUE
		elif self.runningSide == Side.BLUE:
			self.runningSide = Side.RED
		else:
			raise Exception("Not Runnning!")
		
	def __change_side(self):
		self.board = _board_change_side(self.board)
		self.__update_board()
		
	def __draw_base_board(self):
		#画横线
		for i in range(10):
			startPoint = horPadding, verPadding+i*gridLength
			endPoint = horEnd, verPadding+i*gridLength
			itemId = self.create_line(*startPoint, *endPoint)
			self.addtag_withtag("boardLine", itemId)
		
		#画竖线
		for i in range(9):
			startPoint = horPadding+i*gridLength, verPadding
			endPoint = horPadding+i*gridLength, verEnd
			itmeId = self.create_line(*startPoint, *endPoint)
			self.addtag_withtag("boardLine", itemId)
			
		#画将帅的九宫格
		leftSP = horPadding+3*gridLength, verPadding
		leftEP = horPadding+5*gridLength, verPadding+2*gridLength
		rightSP = horPadding+5*gridLength, verPadding
		rightEP = horPadding+3*gridLength, verPadding+2*gridLength
		self.create_line(*leftSP, *leftEP, tags="boardLine")
		self.create_line(*rightSP, *rightEP, tags="boardLine")
		
		leftSP = leftSP[0], leftSP[1]+7*gridLength
		leftEP = leftEP[0], leftEP[1]+7*gridLength
		rightSP = rightSP[0], rightSP[1]+7*gridLength
		rightEP = rightEP[0], rightEP[1]+7*gridLength
		self.create_line(*leftSP, *leftEP, tags="boardLine")
		self.create_line(*rightSP, *rightEP, tags="boardLine")
		
		#画楚河汉界
		topLeftSP = horPadding, verPadding+4*gridLength
		bottomRightSP = horEnd, verPadding+5*gridLength
		self.create_rectangle(*topLeftSP, *bottomRightSP, fill="white", tags="boardLine")
		
		text_x = horPadding+1.5*gridLength
		text_y = verPadding+4.5*gridLength
		textPos = {'楚':(text_x, text_y), '河':(text_x+gridLength, text_y),
					'汉':(text_x+4*gridLength, text_y), '界':(text_x+5*gridLength, text_y)}
		for word in textPos.keys():
			self.create_text(*textPos[word], text=word, tags="boardLine", anchor=tk.CENTER)
		
	
	
	def __draw_pieces(self):
		for x in range(9):
			for y in range(10):
				if self.board[x][y] != NO_PIECE:
					self.__draw_piece(self.board[x][y], x, y)
					
					
	def __draw_piece(self, piece_type, row, column):
		piece_color = "red" if piece_type>0 else "blue"
		piece_text = piecesText[piece_type]
		x = horPadding + row*gridLength
		y = verPadding + column*gridLength
		
		circleLT = x-pieceLength/2, y-pieceLength/2
		circleRB = x+pieceLength/2, y+pieceLength/2
		circleId = self.create_oval(*circleLT, *circleRB, outline="black", fill="white")
		textId = self.create_text(x, y, text=piece_text, anchor=tk.CENTER, fill=piece_color)
		
		self.addtag_withtag("piece", circleId)
		self.addtag_withtag("piece", textId)
		
	def __update_board(self):
		self.delete("piece")
		self.__draw_pieces()
		
	
	def __once_choose(self, row, column):
		x = horPadding + row*gridLength
		y = verPadding + column*gridLength
		
		leftTop = x-pieceLength/2, y-pieceLength/2
		rightTop = x+pieceLength/2, y-pieceLength/2
		rightBottom = x+pieceLength/2, y+pieceLength/2
		leftBottom = x-pieceLength/2, y+pieceLength/2
		
		lineId = self.create_line(*leftTop, *rightTop, *rightBottom, *leftBottom, *leftTop, fill="red")
		
		self.addtag_withtag("chosenLine", lineId)
		
		
	def __once_dischoose(self):
		self.delete("chosenLine")
		
		
	
	def __onMouseLeftClicked(self, event):
		if not(self.isMyTurn()):
			return
		if self.onceClicked:
			self.__onSecondClicked(event)
		else:
			self.__onOnceClicked(event)
			
			
	def __onMouseRightClicked(self, event):
		if not(self.isMyTurn()):
			return
		if self.onceClicked:
			self.__once_dischoose()
			self.chosenPiece = None
			self.onceClicked = False
	
	def __onOnceClicked(self, event):
		x, y = event.x, event.y
		row, column = _get_row_column(x, y)
		if self.board[row][column]==NO_PIECE:
			return
		if not(self.side == _get_piece_side(self.board[row][column])):
			return
		self.__once_choose(row, column)
		self.chosenPiece = (row, column)
		self.onceClicked = True
		
	def __onSecondClicked(self, event):
		x, y = event.x, event.y
		row, column = _get_row_column(x, y)
		cp = self.chosenPiece
		#这里之所以有这么多奇怪的代码，是为了封装与BehindBoard的接口的复杂逻辑……
		sp = cp
		ep = (row,column)
		if self.side == Side.RED:
			sp = _point_change_side(9, 10, sp)
			ep = _point_change_side(9, 10, ep)
		sp = _reverse_point(sp)
		ep = _reverse_point(ep)
		bb = behindBoard(sp, ep)
		
		boardForWorstBehind = _getBoardForWorstBehind(self.board, self.side)
			
		if bb.move(boardForWorstBehind):
			self.__move(*cp, row, column)
		else:
			return
			
		self.__once_dischoose()
		self.chosenPiece = None
		self.onPieceMove(*cp, row, column)#向上级发送消息
		self.onceClicked = False
		
	def __move(self, sx, sy, ex, ey):
		self.board[ex][ey] = self.board[sx][sy]
		self.board[sx][sy] = NO_PIECE
		self.__update_board()
		
		
		
		
		
		
		
		
		
		
		