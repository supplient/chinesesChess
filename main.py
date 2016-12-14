import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from chineseChess import ChineseChess
import tkinter as tk

port = int(input("选择一个端口:"))

root = tk.Tk()
cc = ChineseChess(port=port)
cc.mainloop()
