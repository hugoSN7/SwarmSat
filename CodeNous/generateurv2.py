from array import array
from telnetlib import theNULL
import numpy as np
import projection

def generateur(donnee):
    fichier = open("trajectoire.wkt", 'w')
    x=donnee[0]
    y=donnee[1]

    #création d'un point de départ
    x_mean_start = np.array([np.mean(x.T[0]) for i in range(100)])
    y_mean_start = np.array([np.mean(y.T[0]) for i in range(100)])
    
    # ajout de ce point dans les matrices
    x = np.c_[x_mean_start,x]
    y = np.c_[y_mean_start,y]


    for i in range (0,100):
        fichier.write("LINESTRING (")
        for j in range(0,9999):
            fichier.write(str(x[i,j])+" "+str(y[i,j]))
            if (j<9999):
                fichier.write(", ")
        fichier.write(")\n")
    fichier.close()

generateur(projection.projection())