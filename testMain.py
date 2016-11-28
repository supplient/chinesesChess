import sys
import os
sys.path.append(os.path.abspath(os.curdir))

from frontBoard import *
import tkinter as tk

root = tk.Tk()
fb = FrontBoard(root, bg="white")
fb.pack()
root.mainloop()