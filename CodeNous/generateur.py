from array import array
from telnetlib import theNULL
import numpy as np

with open("Traces.csv") as file:
    tab= np.loadtxt(file,delimiter=",")


fichier = open("trajectoire.wkt", 'w')
#fichier.close()

#with open("trajectoire.wkt") as file:
rows = len(tab)
cols = len(tab[0])

for i in range (0,rows-1, 3):
    fichier.write("LINESTRING (")
    for j in range(0,cols-1):
        fichier.write(str(tab[i,j])+" "+str(tab[i+2,j]))
        if (j<cols-1):
            fichier.write(", ")
    fichier.write(")\n\n")
fichier.close()



