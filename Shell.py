import tkinter as tk
from tkinter import END, VERTICAL
from logging import info, debug

Shell_enter=[]
vs='vs'
class Shell(tk.Frame):
	def __init__(self, *args, on_user_msg_recv, **keywords):
		super(Shell, self).__init__(*args, *keywords)
		self.on_user_msg_recv=on_user_msg_recv
		self.redScore = 0
		self.blueScore = 0
		'''
		Create Top
		'''
		self.Shell_top = tk.Frame(self)
		# self.Shell_top_redscore = tk.Text(self.Shell_top, width=10, height=3, bg="red")
		# self.Shell_top_redscore.grid(row=0, column=0)
		# self.Shell_top_redscore.insert(END, "{}".format(self.redScore))
		# self.Shell_top_redscore.configure(state='disabled')

		# self.Shell_top_vs = tk.Text(self.Shell_top, width=5, height=3)
		# self.Shell_top_vs.grid(row=0, column=1)
		# self.Shell_top_vs.insert(END, "\n  {}".format(vs))
		# self.Shell_top_vs.configure(state='disabled')

		# self.Shell_top_bluescore = tk.Text(self.Shell_top, width=10, height=3, bg="blue")
		# self.Shell_top_bluescore.grid(row=0, column=2)
		# self.Shell_top_bluescore.insert(END, "{}".format(self.blueScore))
		# self.Shell_top_bluescore.configure(state='disabled')


		self.Shell_top_record = tk.Text(self.Shell_top, width=26, height=12, state='disabled')
		self.Shell_top_record.grid(row=0, column=0,columnspan=4)
		self.Shell_top_scroll = tk.Scrollbar(self.Shell_top, orient=VERTICAL,command=self.Shell_top_record.yview)
		self.Shell_top_record['yscrollcommand'] = self.Shell_top_scroll.set
		self.Shell_top_scroll.grid(row=0, column=0, sticky='s' + 'w' + 'e' + 'n',columnspan=4)
		self.Shell_top.grid(row=0, column=0, sticky='WESN')


		'''
		Create Shell_bottom
		'''
		self.Shell_bottom = tk.Frame(self)
		self.Shell_bottom.grid(row=1, column=0, sticky='WESN')
		self.Shell_bottom_sendbox = tk.Text(self.Shell_bottom, width=21, height=1)
		self.Shell_bottom_sendbox.grid(row=0, column=0)
		self.Shell_bottom_sendbox.bind("<KeyPress>", self.__onKeyPress)

		'''
		Create Buttons
		'''
		self.Shell_buttons = tk.Frame(self.Shell_bottom)
		self.Shell_buttons.grid(row=0, column=1)

		self.Shell_bottom_send = tk.Button(self.Shell_buttons, text='Send', command=self.send)
		self.Shell_bottom_send.grid(row=0, column=0, sticky='WE')
	
	def __onKeyPress(self, event):
		if event.keysym in {"KP_Enter", "Return"}:
			self.send()
			
	# def __updateScore(self):
		# debug("更新绘制成绩")
		# self.Shell_top_redscore.configure(state="normal")
		# self.Shell_top_bluescore.configure(state="normal")
		# self.Shell_top_redscore.delete(0.0, END)
		# self.Shell_top_redscore.insert(END, str(self.redScore))
		# self.Shell_top_bluescore.delete(0.0, END)
		# self.Shell_top_bluescore.insert(END, str(self.blueScore))
		# self.Shell_top_redscore.configure(state="disabled")
		# self.Shell_top_bluescore.configure(state="disabled")
	
	def send(self):
		"""
		receive the text content and add it to the record
		"""
		self.Shell_top_record.configure(state='normal')
		msg = self.Shell_bottom_sendbox.get(0.0, END)
		self.on_user_msg_recv(msg)
		self.Shell_top_record.insert(END, "{}".format(msg))
		Shell_enter.append(msg)
		self.Shell_bottom_sendbox.delete(0.0, END)
		self.Shell_top_record.configure(state='disabled')
		self.Shell_top_record.see(END)
	def Shell_print(self,msg, color="black"):
		self.Shell_top_record.configure(state='normal')
		self.Shell_top_record.insert(END, "{}".format(msg))
		self.Shell_top_record.configure(state='disabled')
		self.Shell_top_record.see(END)

	# def setScore(self, side, score):
		# if side=="red":
			# self.redScore=score
		# elif side=="blue":
			# self.blueScore=score
		# else:
			# raise Exception("shell unknown side name")
		# self.__updateScore()
	
	# def plusScore(self, side):
		# if side=="red":
			# score=self.redScore+1
		# elif side=="blue":
			# score=self.blueScore+1
		# else:
			# raise Exception("shell unknown side name")
		# debug("new_score={}".format(score))
		# self.setScore(side, score)
