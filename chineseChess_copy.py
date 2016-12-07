import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from soundingBoard import SoundingBoard
from frontBoard import FrontBoard
from enhancedEnum import EnhancedEnum
import tkinter as tk
import socket

NET_HEAD = "@_@"
USER_HEAD = "%"

class CCState(EnhancedEnum):
	NONE = 0
	PLAYING = 1
	WAIT_FOR_GAME_START = 2

def _headIs(s, head):
	if len(s)<len(head):
		return False
	if s[0:len(head)] == head:
		return True
	else:
		return False

def _isNetMsg(msg):
	return _headIs(msg, NET_HEAD)
		
def _isUserMsg(msg):
	return _headIs(msg, USER_HEAD)

#user <->  chineseChess <-> rival
#响应网络消息的槽用onExampleFunc的形式
#响应用户消息的槽用exampleFunc的形式
#画图用的槽用draw_example_func的形式
	
class ChineseChess(tk.Toplevel):
	def __init__(self, *args, **keys):
		#初始化窗体自身
		super(ChineseChess, self).__init__(args, keys)
		#初始化棋盘
		self.board = FrontBoard(self)
		#初始化传声筒
		ip = socket.gethostbyname(socket.gethostname())
		port = 21565#todo:如何获取空闲port?
		self.sound = SoundingBoard((ip,port), self.__onMsgRecv, self.__onLinkAsk)
		#初始化状态量
		self.state = CCState.NONE
		
	def __onMsgRecv(self, msg, add):
		if _isNetMsg(msg):
			self.__onNetMsg(msg[len(NET_HEAD):], add)
		elif _isUserMsg(msg):
			self.__onUserMsg(msg[len(USER_HEAD):], add)
		else:
			raise Exception("Cannot process such msg")
			
	def __onNetMsg(self, msg, add):
		if msg == "gamestart":
			
		elif msg == "yes":
			self.__
		
	def __onUserMsg(self, msg, add):
		if _headIs(msg, "link"):
			_, ip, port = msg.split(' ')
			port = int(port)
			self.sound.linkTo((ip, port))
			
		elif msg == "gamestart":
			self.__sendMsgToRival("gamestart")
			self.state = CCState.WAIT_FOR_GAME_START
			
		elif msg == 
		
	def __onLinkAsk(self, add):
		pass
		
	def __sendMsgToRival(self, msg):
		msg = NET_HEAD + msg
		self.sound.sendMsg(msg)
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		