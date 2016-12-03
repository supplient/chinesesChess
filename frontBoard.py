import sys
import os
sys.path.append(os.path.abspath(os.curdir))

import tkinter as tk
import pdb
from frontBoard_enum import *
from behindBoard import *

verPadding = 15
horPadding = 15
gridLength = 20
horEnd = horPadding + 8*gridLength
verEnd = verPadding + 9*gridLength

pieceLength = 20

piecesText = {0:'', 1:'兵', 2:'炮', 3:'车', 4:'马', 5:'相', 6:'仕', 7:'帅', 
					-1:'卒', -2:'炮', -3:'車', -4:'馬', -5:'象', -6:'士', -7:'将'}

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
	
def _reverse_point(p):
	return p[1], p[0]

class FrontBoard(tk.Canvas):	
	def __init__(self, *args, **keywords):
		super(FrontBoard, self).__init__(*args, **keywords)
		
		self.onceClicked = False
		self.board = _reverse_board(get_init_board())
		
		self.__draw_base_board()
		self.__draw_pieces()
		
		self.bind("<Button-1>", self.__onMouseLeftClicked)
		self.bind("<Button-3>", self.__onMouseRightClicked)
		
		
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
		piece_text = piecesText[piece_type]
		x = horPadding + row*gridLength
		y = verPadding + column*gridLength
		
		circleLT = x-pieceLength/2, y-pieceLength/2
		circleRB = x+pieceLength/2, y+pieceLength/2
		circleId = self.create_oval(*circleLT, *circleRB, outline="black", fill="white")
		textId = self.create_text(x, y, text=piece_text, anchor=tk.CENTER)
		
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
		if self.onceClicked:
			self.__onSecondClicked(event)
		else:
			self.__onOnceClicked(event)
			
			
	def __onMouseRightClicked(self, event):
		if self.onceClicked:
			self.__once_dischoose()
			self.chosenPiece = None
			self.onceClicked = False
	
	def __onOnceClicked(self, event):
		x, y = event.x, event.y
		row, column = _get_row_column(x, y)
		if self.board[row][column]==NO_PIECE:
			return
		self.__once_choose(row, column)
		self.chosenPiece = (row, column)
		self.onceClicked = True
		
	def __onSecondClicked(self, event):
		x, y = event.x, event.y
		row, column = _get_row_column(x, y)
		cp = self.chosenPiece
		
		# self.board[cp[0]][cp[1]], self.board[row][column] = NO_PIECE, self.board[cp[0]][cp[1]]
		bb = behindBoard(_reverse_point(cp), _reverse_point((row, column)))
		# pdb.set_trace()
		if bb.move(_reverse_board(self.board)):
			self.board[row][column] = self.board[cp[0]][cp[1]]
			self.board[cp[0]][cp[1]] = NO_PIECE
		else:
			return
		self.__once_dischoose()
		self.chosenPiece = None
		self.__update_board()
		self.onceClicked = False
		
		
		
		
		
		
		
		
		
		
		