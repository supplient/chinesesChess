import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from soundingBoard import SoundingBoard
from frontBoard import FrontBoard
import tkinter as tk
import socket

class ChineseChess(tk.Toplevel):
	def __init__(self, *args, **keys):
		#初始化窗体自身
		super(ChineseChess, self).__init__(args, keys)
		#初始化棋盘
		self.board = FrontBoard(self)
		#初始化传声筒
		ip = socket.gethostbyname(socket.gethostname())
		port = 21565#todo:如何获取空闲port?
		self.sound = SoundingBoard((ip,port), self.__onMsgRecv)
		
	def __onMsgRecv(self, msg, add):
		pass