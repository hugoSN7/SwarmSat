from SwarmNetwork import *
import random
import os.path
import sys
from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

if (len(sys.argv) != 3):
    print("How to execute the code: \n python3 qlearningInstant.py N t\n\n where N is the destination and t until which the instant")
    exit()

if (int(sys.argv[1]) < 0 or int(sys.argv[1]) >= 100):
    print("N has to be between 0 and 99")
    exit()

if (int(sys.argv[2]) < 1 or int(sys.argv[2]) >= 10000):
    print("t has to be between 1 and 9999")
    exit()

print("Compute of Q for sending to {} until {} instant".format(sys.argv[1], sys.argv[2]))

nSat = 100
Q = np.zeros([nSat, nSat])
end = int(sys.argv[1])
instant = int(sys.argv[2])
out = "q/to_{}_until_{}/q_until_{}.csv".format(end, instant, instant)
directory = "q/to_{}_until_{}".format(end, instant)

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


# Set learning parameters
lr = .99 #learning rate, c’est la vitesse d’apprentissage. Plus il est élevé, plus les nouvelles informations seront importantes par rapport aux anciennes.
gamma = .99 #facteur d’actualisation (gamma), entre 0 et 1. : détermine l’importance des récompenses futures.
num_episodes = 10000
swarmNetwork = SwarmNetwork(end)

for t in range(instant):
    print("t : {}".format(t))
    swarmNetwork.setInstant(t)
    print("instant {}".format(swarmNetwork.getInstant()))
    for i in range(num_episodes):
        s = swarmNetwork.reset()
        #print("start at ", swarmNetwork.getStart())
        couple = [swarmNetwork.getStart(), 0]
        actions = [couple]
        states = [couple]
        cumul_reward = 0
        d = False
        action_possible = False
        distance = 0
        while True:
            # on choisit une action aléatoire avec une certaine probabilité, qui décroit
            Q2 = Q[s,:] + np.random.randn(1, nSat)*(1. / (i +1))
            a = np.argmax(Q2)
            if (s == end):
                break
            s1, reward, d, distance, action_possible, _ = swarmNetwork.move(a)
            couple = [a, distance]
            # Fonction de mise à jour de la Q-table
            Q[s, a] = Q[s, a] + lr*(reward + gamma * np.max(Q[s1,:]) - Q[s, a])
            cumul_reward += reward
            s = s1
            actions.append(couple)
            if action_possible:
                states.append(couple)
            if d == True:
                if (distance < 0):
                    print("Echec à la {}-eme tentative avec {} actions tentées:".format(i, len(actions)))
                    #swarmNetwork.plot_tentative(actions, i)
                    #swarmNetwork.display(actions)
                break
        #if (i >= num_episodes - 100):
        #    #swarmNetwork.plot_instant(states, directory)
        #    swarmNetwork.displayPath(states)

#print("Q:")
#print(Q)
np.savetxt(out, Q, delimiter=",")
print("Compute of Q for sending to {} until {}\n".format(end, instant))
print("Number of Success: {}/{}".format(swarmNetwork.getSucess(), (num_episodes - 100) * instant))
