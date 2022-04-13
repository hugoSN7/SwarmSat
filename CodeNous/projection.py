from array import array
from cProfile import label
from json import load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
from mgen import rotation_around_axis

# Determie l'angle des données par rapport au plan XZ via régression linéaire
def determinerAngle(x,y):
    x_m = np.mean(x)
    y_m = np.mean(y)
    n = 100*10000
    xy = np.zeros((100,10000))
    for i in range(0,99):
        for j in range(0,9999):
            xy[i,j] = x[i,j]*y[i,j]
        
    b = (n*np.sum(xy) - np.sum(x)*np.sum(y))/(n*np.sum(np.square(x)) + np.sum(np.square(y)))
    a = y_m -x_m*b
    """ print("\n b = "+str(b))
    print("\n a = "+ str(a)) """
    angle = np.arctan(b)

    return angle

# Affiche en 3D
def plotall(x,y,z):
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for j in range(np.shape(x)[0]-1):
        ax.plot(x[j], y[j], z[j], label='Courbe')  # Tracé de la courbe 3D
    plt.title("Courbe des satellites")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim3d(np.min(x), np.max(x))
    ax.set_ylim3d(np.min(x), np.max(x))
    ax.set_zlim3d(np.min(z), np.max(z))
    plt.tight_layout()
    plt.show()

# Affiche en 2D
def plotPartiel(coordonnees):
    fig = plt.figure()
    x = coordonnees[0]
    z = coordonnees[1]

    for j in range(np.shape(x)[0]-1):
        plt.plot(x[j], z[j], label='Courbe')  # Tracé de la courbe 2D
    plt.title("Courbe des satellites")
    plt.xlabel('X')
    plt.ylabel('Z')
    plt.show()

# Effectue une rotation des données pour les mettre sur le plan XZ
def reformater(x,y,z):
    rot = rotation_around_axis([0, 0, 1], -determinerAngle(x,y))

    for k in range(np.shape(x)[0]):
        [x[k],y[k],z[k]] = rot.dot([x[k],y[k],z[k]])
    coord = [x,z]

    return coord
# MAIN
# On récupères les données
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

#Avant rotation
#plotAll(x,y,z)

#Après rotation
newDonnees = reformater(x,y,z)
plotPartiel(newDonnees)