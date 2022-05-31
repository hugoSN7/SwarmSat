import random
import os.path
import sys
from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

with open("../Traces.csv") as file:
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

    def distance_ij(self, i, j):
         t = self.instant
         return np.sqrt((x[i][t]-x[j][t])**2+(y[i][t]-y[j][t])**2+(z[i][t]-z[j][t])**2)

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

    def getInstant(self):
        return self.instant

    def setInstant(self, instant):
        self.instant = instant

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
        if (self.counter >= 60):
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
        cluster40 = [0, 1, 2, 5, 6, 7, 8, 9, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 30, 31, 32, 33, 35, 38, 39, 40, 41, 42, 44, 45, 46, 48, 50, 51, 52, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80, 81, 84, 87, 88, 89, 90, 91, 94, 95, 97, 98]
        cluster60 = [4, 10, 13, 14, 20, 21, 25, 28, 29, 34, 43, 47, 49, 61, 64, 76, 82, 83, 85, 93, 96, 99]
        contact = [3, 36, 37, 53, 54, 86, 92]
        t = self.instant
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        tx=np.transpose(x)
        ty=np.transpose(y)
        tz=np.transpose(z)
        for i in cluster40 :
            ax.scatter(tx[t][i], ty[t][i], tz[t][i], color = 'green')  # Tracé de la courbe 3D
        for i in cluster60 :
            ax.scatter(tx[t][i], ty[t][i], tz[t][i], color = 'orange')  # Tracé de la courbe 3D
        for i in contact :
            ax.scatter(tx[t][i], ty[t][i], tz[t][i], color = 'red')  # Tracé de la courbe 3D
        
        figName = "from_{}_to_{}_at_{}".format(self.start, self.end, t)
        plt.title("from {} to {} at {}".format(self.start, self.end, t))
        ax.scatter([tx[t][self.start]], [ty[t][self.start]], [tz[t][self.start]], color = 'red', marker='<', s = 100, label='start')
        ax.scatter([tx[t][self.end]], [ty[t][self.end]], [tz[t][self.end]], color = 'limegreen', marker='<', s = 100, label='end')
        for k in range(len(actions) - 1):
            d = self.distance_ij(actions[k][0], actions[k  + 1][0])
            if (d <= 20000):
                plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]],[ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'green', label='20km')
            elif (d <= 40000):
                 plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'orange', label='40km')
            elif (d <= 60000):
                plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'r', label='60km')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.tight_layout()
        plt.show()

    def displayNotIstant(self, actions, idContact):
        cluster40 = [0, 1, 2, 5, 6, 7, 8, 9, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 30, 31, 32, 33, 35, 38, 39, 40, 41, 42, 44, 45, 46, 48, 50, 51, 52, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80, 81, 84, 87, 88, 89, 90, 91, 94, 95, 97, 98]
        cluster60 = [4, 10, 13, 14, 20, 21, 25, 28, 29, 34, 43, 47, 49, 61, 64, 76, 82, 83, 85, 93, 96, 99]
        contact = [3, 36, 37, 53, 54, 86, 92]
        t = self.instant
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        tx=np.transpose(x)
        ty=np.transpose(y)
        tz=np.transpose(z)
        for i in cluster40 :
            ax.scatter(tx[t][i], ty[t][i], tz[t][i], color = 'green')  # Tracé de la courbe 3D
        for i in cluster60 :
            ax.scatter(tx[t][i], ty[t][i], tz[t][i], color = 'orange')  # Tracé de la courbe 3D
        for i in contact :
            ax.scatter(tx[t][i], ty[t][i], tz[t][i], color = 'red')  # Tracé de la courbe 3D
        
        figName = "from {} to {} by {} at {}".format(self.start, self.end, idContact, t)
        plt.title("from {} to {} by {} at {}".format(self.start, self.end, idContact, t))
        ax.scatter([tx[t][self.start]], [ty[t][self.start]], [tz[t][self.start]], color = 'red', marker='<', s = 100, label='start')
        ax.scatter([tx[t][self.end]], [ty[t][self.end]], [tz[t][self.end]], color = 'limegreen', marker='<', s = 100, label='end')
        ax.scatter([tx[t][idContact]], [ty[t][idContact]], [tz[t][idContact]], color = 'blue', marker='<', s = 100, label='sat contact')
        
        for k in range(len(actions) - 1):
            d = self.distance_ij(actions[k][0], actions[k  + 1][0])
            if (d <= 20000):
                plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]],[ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'green', label='20km')
            elif (d <= 40000):
                 plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'orange', label='40km')
            elif (d <= 60000):
                plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'r', label='60km')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.tight_layout()
        plt.show()

    def displayTotal(self, actions):
        t = self.instant
        fig = plt.figure()
        ax = fig.gca(projection='3d')
        tx=np.transpose(x)
        ty=np.transpose(y)
        tz=np.transpose(z)
        ax.scatter(tx[t], ty[t], tz[t])  # Tracé de la courbe 3D
        figName = "from_{}_to_{}".format(self.start, self.end)
        plt.title("from {} to {}".format(self.start, self.end))
        ax.scatter([tx[t][self.start]], [ty[t][self.start]], [tz[t][self.start]], color = 'r', marker='<', s = 100, label='start')
        ax.scatter([tx[t][self.end]], [ty[t][self.end]], [tz[t][self.end]], color = 'g', marker='<', s = 100, label='end')
        for k in range(len(actions) - 1):
            d = self.distance_ij(actions[k][0], actions[k  + 1][0])
            if (d <= 20000):
                plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]],[ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'green', label='20km')
            elif (d <= 40000):
                 plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'orange', label='40km')
            elif (d <= 60000):
                plt.plot([tx[t][actions[k][0]], tx[t][actions[k + 1][0]]], [ty[t][actions[k][0]], ty[t][actions[k + 1][0]]], [tz[t][actions[k][0]], tz[t][actions[k + 1][0]]], color = 'r', label='60km')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.legend()
        plt.tight_layout()
        plt.show()
