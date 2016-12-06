import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from enhancedEnum import EnhancedEnum
from threading import Thread
import socket, select
import time
import logging
from logging import debug, info, warning

logging.basicConfig(level=logging.DEBUG, 
		format="%(levelname)s %(process)d %(threadName)s : %(message)s",
		filename="sb.log", filemode='w')


#交互信息约定：
# @_@link
# @_@yes
# @_@no

class State(EnhancedEnum):
	LISTEN = 0
	WAIT_FOR_LINK = 1
	SEND = 2
	
class Msg(EnhancedEnum):
	ASK_LINK_MSG = "@_@link"
	YES_MSG = "@_@yes"
	NO_MSG = "@_@no"
	

class SoundingBoard:
	
	def __init__(self, address, on_msg_recv):
		self.target = None
		self.on_msg_recv = on_msg_recv
		self.state = State.LISTEN
		self.address = address
		#初始化套接字（UDP）
		self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		self.sock.bind(address)
		#初始化线程
		self.listenThread = Thread(target=self.__listen)
		#开始线程
		self.listenThread.start()
		
	def __listen(self):
		info("进入__listen线程,address为{}".format(self.address))
		s = self.sock
		info("进入监听循环")
		while self.state == State.LISTEN:
			rs, [], [] = select.select([s], [], [], 0.01)
			if s in rs:
				msg, add = s.recvfrom(8192)
				msg = msg.decode("utf-8")
				info("监听到数据  {}".format(msg))
				if str(msg) == str(Msg.ASK_LINK_MSG):
					info("监听到连接请求 {}".format(msg))
					if self.target == None:
						info("接受连接请求")
						#建立连接
						self.target = add
						self.sock.sendto(str(Msg.YES_MSG).encode("utf-8"), add)
					else:
						info("拒绝连接请求")
						#如果已有连接， 忽视
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
	
	def linkTo(self, target):
		info("开始请求连接, address为{}".format(self.address))
		self.state = State.SEND
		time.sleep(0.1)#等待监听线程停止
		self.target = target
		s = self.sock
		s.sendto(str(Msg.ASK_LINK_MSG).encode("utf-8"), target)
		self.state = State.WAIT_FOR_LINK
		info("target为{}, 等待连接回复...".format(target))
		ans, add = self.__listenForLink()#需要排除其它ip的访问
		info("收到连接回复  {}".format(ans))
		self.state = State.LISTEN
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
		self.state = State.SEND
		s = self.sock
		s.sendto(msg.encode("utf-8"), self.target)
		self.state = State.LISTEN
		#重启监听线程
		self.__restartListen()
		info("发送消息成功")