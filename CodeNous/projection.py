from array import array
from cProfile import label
from json import load
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd

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

def plotall():
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for j in range(np.shape(x)[0]-1):
        ax.plot(x[j], y[j], z[j], label='Courbe')  # Tracé de la courbe 3D
    plt.title("Courbe des satellites")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_xlim3d(np.min(x), np.max(x))
    ax.set_ylim3d(np.min(y), np.max(y))
    ax.set_zlim3d(np.min(z), np.max(z))
    plt.tight_layout()
    plt.show()

plotall()
