from SwarmNetwork import *
import random
import os.path
import sys
from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

if (len(sys.argv) != 4):
    print("How to execute the code: \n python3 findAPath.py start end t\n\n where start is from which sat we start, end the final sat destination and it sends at t")
    exit()

start = int(sys.argv[1])
end = int(sys.argv[2])
instantStart = int(sys.argv[3])

if (int(sys.argv[1]) < 0 or int(sys.argv[1]) >= 100):
    print("start has to be between 0 and 99")
    exit()

if (int(sys.argv[2]) < 0 or int(sys.argv[2]) >= 100):
    print("end has to be between 0 and 99")
    exit()

if (int(sys.argv[3]) < 0 or int(sys.argv[3]) >= 10000):
    print("t has to be between 0 and 9999")
    exit()

print("Find a way from {} to {}".format(sys.argv[1], sys.argv[2]))

swarmNetwork = SwarmNetwork(end, 0)
swarmNetwork.setStart(start)
swarmNetwork.setInstant(instantStart)
print("SwarmNetwork:", swarmNetwork.getStart())

nSat = 100
Q = np.zeros([nSat, nSat])
out = "q/to_{}/q_to_{}.csv".format(end, end)
directory = "q/to_{}".format(end)

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
    cmd = "python3 qlearning.py {} {}".format(sys.argv[2], 10)
    os.system(cmd)
    with open(out) as file:
        Q = np.loadtxt(file,delimiter=",")

couple = [swarmNetwork.getStart(), 0]
s = swarmNetwork.getStart()
couple = [s, 0]
states = [couple]
#nb de fois où le paquet est en arret
wait = 0
waitList = []
#nb de passage à l'instant d'après
instant = 0
d = False
cnt = 0
oldAction = -1
while True:
    swarmNetwork.setPosition(s)
    if s == swarmNetwork.getEnd():
        break
    a = np.argmax(Q[s,:])
    #on retente d'envoyer le paquet au meme satellite
    if (a == oldAction):
        wait += 1
        situation = [oldAction, distance, instant]
        waitList.append(situation)
    #tirer un nb aleatoire pour passer ou non à l'instant d'apres, si la distance reste valide on passe a l'etat d'apres sinon on attend que l'on passe a l'instant d'apres
    if (random.randint(1,2) == 2):
        instant += 1
        swarmNetwork.setInstant(instant)
    distance = swarmNetwork.distance(a)
    if (distance <= 60000):
        couple = [a, distance]
        s = a
        oldAction = a
        states.append(couple)
        cnt += 1
        if cnt >= 100:
            break
        if d == True:
            break
print("paquet delivers with wait {}".format(instant))
print("difficult situation \n", waitList)
swarmNetwork.displayPath(states)
swarmNetwork.displayTotal(states)

