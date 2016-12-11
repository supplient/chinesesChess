from Shell import Shell
import tkinter as tk
import pdb

def noneFunc(msg):
	pass

root = tk.Tk()
pdb.set_trace()
shell = Shell(root, on_user_msg_recv=noneFunc)
shell.grid(row=0, column=0)
root.mainloop()
