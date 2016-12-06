from soundingBoard import SoundingBoard
import pdb

def noneFunc(msg, add):
    print("Receive:{}".format(msg))
localA = ("10.21.34.105", 23155)
localB = ("10.21.34.105", 23156)

sb = SoundingBoard(localA, noneFunc)
if sb.linkTo(localB):
    print("Link on")
else:
    print("Link fail")

sb.sendMsg("Hallo")

