from array import array
from telnetlib import theNULL
import numpy as np
import csv

with open("Test.csv") as file:
    tab= np.loadtxt(file,delimiter=",")

fichier = open("/home/ternardin/Documents/2A/SwarmSat/the-one-1.6.0/data/Ltrajectoire.wkt", 'w')


#fichier.close()

#with open("Ltrajectoire.wkt") as file:
rows = len(tab)
cols = len(tab[0])

for i in range (0,rows-1, 3):
    fichier.write("LINESTRING (")
    for j in range(0,cols-1):
        fichier.write(str(tab[i,j])+" "+str(tab[i+2,j]))
        if (j<cols-2):
            fichier.write(", ")
    fichier.write(")\n\n")
fichier.close()





