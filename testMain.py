import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from frontBoard import *
import tkinter as tk
from frontBoard_enum import *

rs = Side.BLUE

def crs():
	global rs
	if rs == Side.BLUE:
		rs = Side.RED
	else:
		rs = Side.BLUE
	fb.setRunningSide(rs)

root = tk.Tk()
fb = FrontBoard(root, bg="white")
fb.pack()
tk.Button(root, text="changeSide", command=fb.reverseSide).pack()
tk.Button(root, text="changeRunningSide", command=crs).pack()
root.mainloop()
