import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from enhancedEnum import EnhancedEnum
from frontBoard_enum import *
from net_enum import *
from errors import *

from soundingBoard import SoundingBoard
from frontBoard import FrontBoard
from queueHourglass import QueueHourglass
from Shell import Shell

from threading import Thread
from queue import Queue
import socket

import tkinter as tk

import random
import logging
from logging import debug, info

logging.basicConfig(format="%(asctime)s %(process)d %(threadName)s : %(message)s",
			level=logging.DEBUG)

# logger = logging.getLogger("chineseChess")
# sh = logging.StreamHandler()
# sh.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(levelname)s %(process)d %(threadName)s : %(message)s")
# sh.setFormatter(formatter)
# logger.addHandler(sh)
# debug = logger.debug
# info = logger.info


QUEUE_SIZE = 8192


def _headIs(s, head):
	if len(s)<len(head):
		return False
	if s[0:len(head)] == head:
		return True
	else:
		return False
		
def _isSystemMsg(msg):
	if msg == USER_HEAD+"help":
		return True
	return False

def _isNetMsg(msg):
	return _headIs(msg, NET_HEAD)
		
def _isUserMsg(msg):
	return _headIs(msg, USER_HEAD)

def _isNetChatMsg(msg):
	return _headIs(msg, NET_CHAT_HEAD)
	
#辅助函数	
def _pushFunc(queue, signal):
	queue.put(signal, block=1)
	
def _point_change_side(x_len, y_len, p):
	return x_len-p[0]-1, y_len-p[1]-1
	
def _cleanUserMsg(msg):
	return msg.strip()
	
def _meta_print(*args, **keywords):
    s = ""
    sep = ' '
    if "sep" in keywords.keys():
        sep = keywords["sep"]

    first = True
    for i in args:
        if first:
            s+= str(i)
            first = False
            continue
        s += sep + str(i)
        
    end = '\n'
    if "end" in keywords.keys():
        end = keywords["end"]
    return s+end
	
#我的ip  10.21.34.105
#A号端口 23155
#B号端口 23156
#%link 10.21.34.105 23156
	
class ChineseChess(tk.Toplevel):
	def __init__(self, *args, port, **keys):
		info("开始初始化Chinese Chess")
		#初始化窗体自身
		super(ChineseChess, self).__init__(args, keys)
		#初始化棋盘
		self.board = FrontBoard(self, onPieceMove=self.__onPieceMove)
		self.board.grid(row=0, column=0)
		#初始化终端
		self.shell = Shell(self, on_user_msg_recv=self.__onUserMsgRecv)
		self.shell.grid(row=0, column=1)
		#初始化传声筒
		ip = socket.gethostbyname(socket.gethostname())
		port = port#todo:如何获取空闲port?
		self.sound = SoundingBoard((ip,port), self.__onMsgRecv, self.__onLinkAsk)
		#初始化临时量
		self.myRand = 0
		#初始化队列沙漏&主消息队列
		self.hourglass = QueueHourglass()
		self.mainQueue = Queue(QUEUE_SIZE)
		self.hourglass.append(self.mainQueue)
		#运行主消息处理线程
		self.mainThread = Thread(target=self.__mainSignalProcess)
		self.mainThread.start()
		info("初始化Chinese Chess结束")
		#显示初始信息
		self.__print("Your address is {}".format(self.sound.getMyAdd()))
		self.__print("Press %help for help")
		
		
	def __onPieceMove(self, sx, sy, ex, ey):
		msg = "{}p {} {} {} {}".format(USER_HEAD, sx, sy, ex, ey)
		add = self.sound.getMyAdd()
		self.hourglass.pushSignal(_pushFunc, (msg,add))
		
	def __onUserMsgRecv(self, msg):
		msg = _cleanUserMsg(msg)
		debug("收到用户消息 {}".format(msg))
		add = self.sound.getMyAdd()
		self.hourglass.pushSignal(_pushFunc, (msg,add))
		
	def __onMsgRecv(self, msg, add):
		info("接收到{}的消息 {}".format(add, msg))
		self.hourglass.pushSignal(_pushFunc, (msg,add))
		
		
	def __mainSignalProcess(self):
		while True:
			msg, add = self.mainQueue.get(1)
			info("开始处理{}的消息 {}".format(add, msg))
			try:
				if _isNetMsg(msg):
					self.__onNetMsg(msg[len(NET_HEAD):], add)
				elif _isUserMsg(msg):
					self.__onUserMsg(msg[len(USER_HEAD):], add)
				elif _isNetChatMsg(msg):
					self.__onNetChatMsg(msg[len(NET_CHAT_HEAD):])
				else:
					self.__onUserChatMsg(msg)
			except UnknownCmdError:
				self.__print("unknown command")
			except NotLinked:
				self.__print("has not linked someone")
			
	def __onNetMsg(self, msg, add):
		if msg == "start":
			self.__print("{} want to start the game, do you?".format(add))
			if self.__askUserWhether(self.sound.getMyAdd()):
				self.__sendMsgToRival("yes")
				self.__determineFirst()
			else:
				self.__sendMsgToRival("no")
				
		elif _headIs(msg, "rand"):
			_, rivalRand = msg.split(' ')#space
			rivalRand = int(rivalRand)
			if self.myRand < rivalRand:#小的后下
				info("我后下")
				self.board.setSide(Side.BLUE)
				self.__gameStart()
			elif self.myRand > rivalRand:
				info("我先下")
				self.board.setSide(Side.RED)
				self.__gameStart()
			else:
				info("重新决先")
				self.myRand = random.randint(0, 100)
				self.__sendMsgToRival("rand {}".format(self.myRand))				
			
		elif _headIs(msg, "p"):
			_, sx, sy, ex, ey = msg.split(' ')#space
			sx, sy, ex, ey = (int(x) for x in [sx, sy, ex, ey])
			sx, sy = _point_change_side(9, 10, (sx, sy))
			ex, ey = _point_change_side(9, 10, (ex, ey))
			self.__print("Rival move from {} to {}".format((sx,sy), (ex,ey)))
			self.__move(sx, sy, ex, ey)
			self.board.reverseRunningSide()
			if self.board.isGameOver():
				self.__gameOver(self.board.isGameOver())
		else:
			raise UnknownNetCmdError
				
				
	def __onUserMsg(self, msg, add):
		if _headIs(msg, "link"):
			_, ip, port = msg.split(' ')
			port = int(port)
			self.sound.linkTo((ip,port))
			
		elif msg == "start":
			self.__print("Waiting for rival's answer.....")
			self.__sendMsgToRival("start")
			if self.__askRivalWhether(self.sound.getTargetAdd()):
				self.__print("Agreed! Game start!")
				self.__determineFirst()
			else:
				self.__print("Refused...")
				
		elif _headIs(msg, "p"):
			_, sx, sy, ex, ey = msg.split(' ')
			self.__print("You move from {} to {}".format((sx,sy), (ex,ey)))
			self.__sendMsgToRival(msg)
			self.board.reverseRunningSide()
			if self.board.isGameOver():
				self.__gameOver(self.board.isGameOver())
			
		elif msg == "help":
			self.__showHelp()
			
		else:
			raise UnknownUserCmdError
			
	def __onUserChatMsg(self, msg):
		self.__sendChatMsgToRival(msg)
		
	def __onNetChatMsg(self, msg):
		self.__print("Rival: ", msg)
			
	def __move(self, sx, sy, ex, ey):
		self.board.move(sx, sy, ex, ey)
	
		
	def __onLinkAsk(self, add):
		self.__print("{} want to link with you, do you?".format(add))
		if self.__askUserWhether(self.sound.getMyAdd()):
			self.__print("Link success")
			return True
		else:
			self.__print("Link fail")
			return False
		
	def __sendMsgToRival(self, msg):
		msg = NET_HEAD + msg
		if not self.sound.isLinked():
			raise NotLinked
		self.sound.sendMsg(msg)
	
	def __sendChatMsgToRival(self, msg):
		msg = NET_CHAT_HEAD + msg
		if not self.sound.isLinked():
			raise NotLinked
		self.sound.sendMsg(msg)
		
	def __print(self, *args, **keywords):
		msg = _meta_print(*args, *keywords)
		info("请求绘制 {}".format(msg))
		#终端绘制
		self.shell.Shell_print(msg)
	
	def __determineFirst(self):
		info("游戏开始前的决先")
		self.myRand = random.randint(0, 100)
		self.__sendMsgToRival("rand {}".format(self.myRand))
		
	def __gameStart(self):
		info("游戏开始")
		self.board.setRunningSide(Side.RED)
		
	def __gameOver(self, winSide):
		info("游戏结束")
		self.board.setRunningSide(None)
		if winSide == self.board.getSide():
			info("我赢了")
			self.__print("You win!")
		else:
			info("我输了")
			self.__print("You lose...")
		self.board.reset()
		
	def __showHelp(self):
		help = '''
%link [ip] [port]
%yes
%no
%start
		'''
		self.__print(help)
		
	#次消息队列函数	[block]
	def __askWhether(self, old_add, MSG_HEAD):
		info("开始询问whether")
		tempQueue = Queue(QUEUE_SIZE)
		self.hourglass.append(tempQueue)
		res = None
		YES_MSG = MSG_HEAD + "yes"
		NO_MSG = MSG_HEAD + "no"
		while True:
			ans, new_add = tempQueue.get(1)
			debug("YES_MSG:{}  ans:{}  ans==YES_MSG:{}".format(YES_MSG, ans, ans==YES_MSG))
			
			if not(new_add == old_add):
				debug("不是我要问的人")
				if _isSystemMsg(ans):
					self.hourglass.leak(tempQueue, (ans, old_add), _pushFunc)
				continue
			if not(ans == YES_MSG or ans == NO_MSG):
				debug("不是我要的答案")
				if _isSystemMsg(ans):
					self.hourglass.leak(tempQueue, (ans, old_add), _pushFunc)
				continue
				
			if ans == YES_MSG:
				debug("被同意")
				res = True
				break
			else:
				debug("不被同意")
				res = False
				break
		self.hourglass.pop()
		return res
	
	def __askRivalWhether(self, rival_add):
		debug("对手whether")
		return self.__askWhether(rival_add, NET_HEAD)
		
	def __askUserWhether(self, user_add):
		debug("用户whether")
		return self.__askWhether(user_add, USER_HEAD)
		
	def __askUserSomething(self, user_add):
		tempQueue = Queue(QUEUE_SIZE)
		self.hourglass.append(tempQueue)
		res = None
		while True:
			ans, new_add = tempQueue.get(1)
			
			if not(new_add == user_add):
				self.hourglass.leak(tempQueue, (msg, user_add), _pushFunc)
				continue
				
			res = ans
			break
		self.hourglass.pop()
		return res
		
	
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		