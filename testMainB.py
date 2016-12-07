import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from chineseChess import ChineseChess
import tkinter as tk

root = tk.Tk()
cc = ChineseChess(port=23156)
cc.mainloop()
