from array import array
from telnetlib import theNULL
import numpy as np
import projection

def generateur(donnee):
    fichier = open("trajectoire.wkt", 'w')
    x=donnee[0]
    y=donnee[1]

    for i in range (0,99):
        fichier.write("LINESTRING (")
        for j in range(0,9999):
            fichier.write(str(x[i,j])+" "+str(y[i,j]))
            if (j<9999):
                fichier.write(", ")
        fichier.write(")\n")
    fichier.close()

generateur(projection.projection())