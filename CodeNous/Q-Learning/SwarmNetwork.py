import random
import os.path
import sys
from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

with open("Traces.csv") as file:
    tab= np.loadtxt(file,delimiter=",")


i=0
x=np.zeros((100,10000))
y=np.zeros((100,10000))
z=np.zeros((100,10000))
while i<np.shape(tab)[0]:
    x[i//3]=tab[i]
    y[i//3]=tab[i+1]
    z[i//3]=tab[i+2]
    i+=3
#Class SwarmNetwork qui manipule l'essaim de nano satelite pour l'apprentissage
class SwarmNetwork:

    # l'action est de se rendre à un autre satelite
    ACTIONS = [x for x in range(100)]

    num_actions = len(ACTIONS)

    def __init__(self, end, instant, alea=False):
        self.nSat = 100
        self.end = end
        self.instant = instant
        self.alea = alea
        self.generate_swarm()
        self.start = 0
        self.success = 0
        self.counter = 0

    def _position_to_id(self, a):
        return a

    def _id_to_position(self, id):
        return (id % self.nSat, id // self.nSat)

    def generate_swarm(self):
        cases = [s for s in range(self.nSat) ]
        start = random.choice(cases)

        self.start = start
        self.position = start

        if not self.alea:
            self.start = start
        return self._get_state()

    def reset(self):
        if not self.alea:
            self.counter = 0
            self.start = (self.start + 1) % 100
            self.position = self.start
            return self._get_state()
        else:
            return self.generate_swarm()

    def _get_state(self):
        return self._position_to_id(self.position)

    def distance(self, j):
        i = self.position
        t = self.instant
        return np.sqrt((x[i][t]-x[j][t])**2+(y[i][t]-y[j][t])**2+(z[i][t]-z[j][t])**2)

    def setPosition(self, position):
        self.position = position

    def getCounter(self):
        return self.counter

    def setStart(self, start):
        self.start = start

    def getStart(self):
        return self.start

    def getEnd(self):
        return self.end

    def getSucess(self):
        return self.success

    def move(self, action):
        """
        takes an action parameter
        :param action : the id of an action
        :return (state_id, reward, is_final, distance, possible_action, actions)
        """
        if action not in self.ACTIONS:
            raise Exception("Invalid action")

        new_s = action;

        #eviter de boucler à l'infini
        if (self.counter >= 100):
            return self._get_state(), -1000, True, -1, False, self.ACTIONS

        distance = self.distance(new_s)
        #print("\npack at", self.position, "next sat", new_s)
        #print("distance:", d/1000)
        #print("counter:", self.counter)

        #le satelite n'est autre que lui même
        if (self.position == new_s):
            #print("c'est moi")
            self.counter += 1
            return self._get_state(), -1000, False, distance, False, self.ACTIONS
        #le satelite est à plus de 60km
        if (distance > 60000):
            #print("sat hors de portee")
            self.counter += 1
            return self._get_state(), -1000, False, distance, False, self.ACTIONS
        #le satelite est à moins de 20km
        elif (distance <= 20000):
            #print("sat à moins de 20km")
            self.position = new_s
            #la destination finale est atteinte
            if (self.end == new_s):
                self.success += 1
                #print("paquet reçu\n")
                return self._get_state(), 60, True, distance, True, self.ACTIONS
            return self._get_state(), -20, False, distance, True, self.ACTIONS
        #le satelite est à moins de 40km
        elif (distance <= 40000):
            #print("sat à moins de 40km")
            self.position = new_s
            #la destination finale est atteinte
            if (self.end == new_s):
                self.success += 1
                #print("paquet reçu\n")
                return self._get_state(), 40, True, distance, True, self.ACTIONS
            return self._get_state(), -40, False, distance, True, self.ACTIONS
        #le satelite est à moins de 60km
        elif (distance <= 60000):
            #print("sat à moins de 60km")
            self.position = new_s
            #la destination finale est atteinte
            if (self.end == new_s):
                self.success += 1
                #print("paquet reçu\n")
                return self._get_state(), 20, True, distance, True, self.ACTIONS
            return self._get_state(), -60, False, distance, True, self.ACTIONS
        else:
            self.position = new_s
            self.counter += 1
            return self._get_state(), 0, False, distance, False, self.ACTIONS

    def displayPath(self, actions):
        output = ""
        for j in range(len(actions)):
            if j == 0:
                output += str(actions[j][0]) + " --"
            elif j == (len(actions) - 1):
                output += "(" + str(actions[j][1] / 1000) + "km)--> " + str(actions[j][0])
            else:
                output +=  "(" + str(actions[j][1] / 1000) + "km)--> " + str(actions[j][0]) + " --"
        print(output, "\n")

    def plot_instant(self, actions, where):
        t = self.instant
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        tx=np.transpose(x)
        ty=np.transpose(y)
        tz=np.transpose(z)
        ax.scatter(tx[t], ty[t], tz[t])  # Tracé de la courbe 3D
        figName = "from_{}_to_{}_at_{}".format(self.start, self.end, t)
        plt.title("from {} to {} at {}".format(self.start, self.end, t))
        ax.scatter([tx[t][self.start]], [ty[t][self.start]], [tz[t][self.start]], color = 'r', marker='<', s = 100, label='start')
        ax.scatter([tx[t][self.end]], [ty[t][self.end]], [tz[t][self.end]], color = 'g', marker='<', s = 100, label='end')
        for k in range(len(actions) - 1):
            plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'r')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.tight_layout()
        plt.show()
        #where += "/" + figName
        #fig.savefig(where)

    def plot_tentative(self, actions, num_tentative):
        t = self.instant
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        tx=np.transpose(x)
        ty=np.transpose(y)
        tz=np.transpose(z)
        ax.scatter(tx[t], ty[t], tz[t])  # Tracé de la courbe 3D
        figName = "from_{}_to_{}_at_{}".format(self.start, self.end, t)
        plt.title("from {} to {} at {}".format(self.start, self.end, t))
        for k in range(len(actions) - 1):
            ax.scatter(tx[t][actions[k][0]], ty[t][actions[k][0]], tz[t][actions[k][0]], color = 'r', marker='<', s = 100)
        ax.scatter([tx[t][self.start]], [ty[t][self.start]], [tz[t][self.start]], color = 'blue', marker='<', s = 100, label='start')
        ax.scatter([tx[t][self.end]], [ty[t][self.end]], [tz[t][self.end]], color = 'g', marker='<', s = 100, label='end')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.tight_layout()
        plt.show()

    def display(self, actions):
        t = self.instant
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        tx=np.transpose(x)
        ty=np.transpose(y)
        tz=np.transpose(z)
        ax.scatter(tx[t], ty[t], tz[t])  # Tracé de la courbe 3D
        figName = "from_{}_to_{}_at_{}".format(self.start, self.end, t)
        plt.title("from {} to {} at {}".format(self.start, self.end, t))
        ax.scatter([tx[t][self.start]], [ty[t][self.start]], [tz[t][self.start]], color = 'r', marker='<', s = 100, label='start')
        ax.scatter([tx[t][self.end]], [ty[t][self.end]], [tz[t][self.end]], color = 'g', marker='<', s = 100, label='end')
        for k in range(len(actions) - 1):
            plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'r')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.tight_layout()
        plt.show()
