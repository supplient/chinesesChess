from soundingBoard import SoundingBoard
import pdb


def noneFunc(msg, add):
    print("Receive:{}".format(msg))
    sb.sendMsg("World")
localA = ("10.21.34.105", 23155)
localB = ("10.21.34.105", 23156)

sb = SoundingBoard(localB, noneFunc)
while not(sb.isLinked()):
    pass
print("Link on")
