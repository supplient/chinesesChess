import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from enhancedEnum import EnhancedEnum
from threading import Thread
import socket, select
import time
import logging
from logging import debug, info

# logger = logging.getLogger("soundingBoard")
# fh = logging.FileHandler("sb.log")
# fh.setLevel(logging.DEBUG)
# formatter = logging.Formatter("%(levelname)s %(process)d %(threadName)s : %(message)s")
# fh.setFormatter(formatter)
# logger.addHandler(fh)
# debug = logger.debug
# info = logger.info


#交互信息约定：
# @_@link
# @_@yes
# @_@no

class SBState(EnhancedEnum):
	LISTEN = 0
	WAIT_FOR_LINK = 1
	SEND = 2
	
class Msg(EnhancedEnum):
	ASK_LINK_MSG = "@_@link"
	YES_MSG = "@_@yes"
	NO_MSG = "@_@no"
	

class SoundingBoard:
	'''
	Description:这是一个传声筒，它同时只能做收、听、处理消息中的一件事情
	Constructor:
		address		——	(ip, port)：这个传声筒所绑定到的(ip, 端口)
		on_msg_recv	——	void f(msg, add)：当这个传声筒接收到一般消息时所调用的函数
		on_link_ask	——	bool f(add):当这个传声筒接收到请求消息时所调用的函数
	Methods:
		bool linkTo(target)[block]：若成功连接到target,则返回True,否则False
		bool isLinked()
		void sendMsg(msg)[block]:发送msg给所连接的对象，若无，则扔出异常
		
	Todo:
		1.reLink
	'''
	def __init__(self, address, on_msg_recv, on_link_ask):
		self.target = None
		self.on_msg_recv = on_msg_recv
		self.on_link_ask = on_link_ask
		self.state = SBState.LISTEN
		self.address = address
		#初始化套接字（UDP）
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(address)
		#初始化线程
		self.listenThread = Thread(target=self.__listen)
		#开始线程
		self.listenThread.start()
		
	def getMyAdd(self):
		return self.address
		
	def getTargetAdd(self):
		return self.target
		
	def linkTo(self, target):
		info("开始请求连接, address为{}".format(self.address))
		self.state = SBState.SEND
		time.sleep(0.1)#等待监听线程停止
		self.target = target
		s = self.sock
		s.sendto(str(Msg.ASK_LINK_MSG).encode("utf-8"), target)
		self.state = SBState.WAIT_FOR_LINK
		info("target为{}, 等待连接回复...".format(target))
		ans, add = self.__listenForLink()#需要排除其它ip的访问
		info("收到连接回复  {}".format(ans))
		self.state = SBState.LISTEN
		#重启监听线程
		self.__restartListen()
		return str(ans) == str(Msg.YES_MSG)
		
	def isLinked(self):
		return not(self.target==None)
		
		
	def sendMsg(self, msg):
		info("发送消息  {}".format(msg))
		if self.target == None:
			error("请求发送消息时，未连接")
			raise Exception("Have not link someone")
		self.state = SBState.SEND
		s = self.sock
		s.sendto(msg.encode("utf-8"), self.target)
		self.state = SBState.LISTEN
		#重启监听线程
		self.__restartListen()
		info("发送消息成功")
		
	def __listen(self):
		info("进入__listen线程,address为{}".format(self.address))
		s = self.sock
		info("进入监听循环")
		while self.state == SBState.LISTEN:
			rs, [], [] = select.select([s], [], [], 0.01)
			if s in rs:
				msg, add = s.recvfrom(8192)
				msg = msg.decode("utf-8")
				info("监听到数据  {}".format(msg))
				if str(msg) == str(Msg.ASK_LINK_MSG):
					info("监听到连接请求 {}".format(msg))
					if self.on_link_ask(add):
						info("接受连接请求")
						#建立连接
						self.target = add
						self.sock.sendto(str(Msg.YES_MSG).encode("utf-8"), add)
					else:
						info("拒绝连接请求")
						#拒绝请求
						self.sock.sendto(str(Msg.NO_MSG).encode("utf-8"), add)
				else:
					info("监听到一般数据 {}".format(msg))
					self.on_msg_recv(msg, add)
		info("结束__listen线程")
		
	def __listenForLink(self):
		time.sleep(0.1)#为了进行自机自连
		s = self.sock
		msg, add = s.recvfrom(8192)#等待2000ms)
		return msg.decode(), add
		
	def __restartListen(self):
		#重启监听线程
		self.listenThread = Thread(target=self.__listen)
		self.listenThread.start()
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		
		