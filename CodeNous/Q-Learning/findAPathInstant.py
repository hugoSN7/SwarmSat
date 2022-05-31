from ctypes.wintypes import BOOLEAN
from SwarmNetwork import *
import random
import os.path
import sys
from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

if (len(sys.argv) != 6):
    print("How to execute the code: \n python3 findAPathInstant.py start end t instantane Id_Contact\n\n where start is from which sat we start, end the final sat destination and t the instant")
    exit()

if (int(sys.argv[1]) < 0 or int(sys.argv[1]) >= 100):
    print("start has to be between 0 and 99")
    exit()

if (int(sys.argv[2]) < 0 or int(sys.argv[2]) >= 100):
    print("end has to be between 0 and 99")
    exit()

if (int(sys.argv[3]) < 0 or int(sys.argv[3]) >= 10000):
    print("t has to be between 0 and 9999")
    exit()


if (sys.argv[4] == "True"):
    instantane = True
else:
    instantane = False

idContact = int(sys.argv[5])

print("Find a way from {} to {} at {}".format(sys.argv[1], sys.argv[2], sys.argv[3]))

swarmNetwork = SwarmNetwork(int(sys.argv[2]), int(sys.argv[3]))
swarmNetwork.setStart(int(sys.argv[1]))
print("SwarmNetwork:", swarmNetwork.getStart())
swarmNetwork.setStart(int(sys.argv[1]))
print("SwarmNetwork:", swarmNetwork.getStart())

nSat = 100
Q = np.zeros([nSat, nSat])
out = "q/to_{}/q_instant_{}.csv".format(int(sys.argv[2]), int(sys.argv[3]))
directory = "q/to_{}".format(int(sys.argv[1]))

if os.path.exists("q"):
    print("directory exist")
else:
    print("no directory")
    os.mkdir("q")

if os.path.exists(directory):
    print("directory exist")
else:
    print("no directory")
    os.mkdir(directory)

if os.path.isfile(out):
    print("Q already compute")
    with open(out) as file:
        Q = np.loadtxt(file, delimiter=",")
else:
    print("Q was never compute before")
    print("let's compute Q first")
    cmd = "python3 qlearningInstant.py {} {}".format(sys.argv[2], sys.argv[3])
    os.system(cmd)
    with open(out) as file:
        Q = np.loadtxt(file,delimiter=",")

couple = [swarmNetwork.getStart(), 0]
s = swarmNetwork.getStart()
couple = [s, 0]
states = [couple]
d = False
cnt = 0
while True:
    swarmNetwork.setPosition(s)
    if s == swarmNetwork.getEnd():
        break
    a = np.argmax(Q[s,:])
    distance = swarmNetwork.distance(a)
    couple = [a, distance]
    s = a
    states.append(couple)
    cnt += 1
    if cnt >= 100:
        break
    if d == True:
        break

swarmNetwork.displayPath(states)
if (instantane):
    swarmNetwork.display(states)
else:
    swarmNetwork.displayNotIstant(states, idContact)
