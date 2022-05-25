from array import array
from cProfile import label
from json import load
from statistics import mean
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

x_m = np.mean(x)
y_m = np.mean(y)
n = 100*10000
xy = np.zeros((100,10000))
for i in range(0,99):
    for j in range(0,9999):
        xy[i,j] = x[i,j]*y[i,j]
    
b = (n*np.sum(xy) - np.sum(x)*np.sum(y))/(n*np.sum(np.square(x)) + np.sum(np.square(y)))
a = y_m -x_m*b
print("\n b = "+str(b))
print("\n a = "+ str(a) )
angle = np.arctan(b)
print("\n b = "+str(angle)+ "\n\n")