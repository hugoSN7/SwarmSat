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

def plot_instant(t):
    fig = plt.figure()
    ax = fig.gca(projection='3d')
    tx=np.transpose(x)
    ty=np.transpose(y)
    tz=np.transpose(z)
    
    ax.scatter(tx[t], ty[t], tz[t])  # Tracé de la courbe 3D
    plt.title("Emplacement des satellites")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    plt.tight_layout()
    plt.show()

def distance(i,j,t):
    return np.sqrt((x[i][t]-x[j][t])**2+(y[i][t]-y[j][t])**2+(z[i][t]-z[j][t])**2)






def plot_shortanim(d,f): 
    fig = plt.figure()
    ax = fig.gca(projection='3d')

    for j in range(np.shape(x)[0]-1):
        ax.plot(x[j][d:f], y[j][d:f], z[j][d:f], label='Courbe')  # Tracé de la courbe 3D
    plt.title("Courbe des satellites")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    
    plt.tight_layout()
    plt.show()



def func(num, dataSet, line):
        # NOTE: there is no .set_data() for 3 dim data...
    line.set_data(dataSet[0:2, :num])    
    line.set_3d_properties(dataSet[2, :num])    
    return line


def plotanim():    
    # THE DATA POINTS
    #t = np.arange(0,20,0.2) # This would be the z-axis ('t' means time here)
    #x = np.cos(t)-1
    #y = 1/2*(np.cos(2*t)-1)
    
    
    # GET SOME MATPLOTLIB OBJECTS
    fig = plt.figure()
    ax = Axes3D(fig)
    # AXES PROPERTIES]
    # ax.set_xlim3d([limit0, limit1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Trajectoire des satellites')
    for j in range(2):
    # NOTE: Can't pass empty arrays into 3d version of plot()
        dataSet = np.array([x[j], y[j], z[j]])
        numDataPoints = len(x[j])
        line = plt.plot(dataSet[0], dataSet[1], dataSet[2], lw=2)[0] # For line plot
    
    
    
    # Creating the Animation object
        line_ani = animation.FuncAnimation(fig, func, frames=100, fargs=(dataSet,line), interval=50, blit=False)
        plt.show()
    

    


    
def voisin(i):
    
    y_20=[]
    y_40=[]
    y_60=[]
    for t in range(np.shape(x)[1]-1):
        v_20=0
        v_40=0
        v_60=0
        for j in range(np.shape(x)[0]-1):
            if (distance(i,j,t)<20000):
                v_20+=1
            if (distance(i,j,t)<40000):
                v_40+=1
            if (distance(i,j,t)<60000):
                v_60+=1
     
        y_20.append(v_20) 
        y_40.append(v_40) 
        y_60.append(v_60)        
    plt.plot(y_20)
    plt.plot(y_40)
    plt.plot(y_60)
    plt.show()
    
    
def graph_distance(i,j):
    axis_y=[]
    axis_x=range(np.shape(x)[1])
    for t in range(np.shape(x)[1]):
        axis_y.append(distance(i,j,t))
    plt.plot(axis_y)
    plt.show()
        

#graph_distance(2,3)


#fonction permettant de générer la matrice des distances entre les 100 satellites
# entre 0 et timemax
def graph_conectivity(debut, fin):
    distanceintersat = np.zeros((np.shape(x)[0],np.shape(x)[0],fin-debut))
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(x)[0]):
            for t in range(debut, fin):
                distanceintersat[i][j][t]= distance(i,j,t)
    return distanceintersat


# savegarde la matrice distance en .csv
def save_graph_distance():
    a = graph_conectivity(0, 10000)
    np.save("Distance_entre_sat", a)
    

def import_distance():
    return np.load("Distance_entre_sat.npy")




#permet de récupérer la liste des statellites qui reste en contact avec le satellite i dans un rayon donné 
def lien_always(sat_i, dist_transm_max):
    num_lien=list(range(np.shape(x)[0]))
    num_lien.remove(sat_i)
    for t in range(np.shape(x)[1]):
        for j in num_lien:
            if  distance(sat_i,j,t) > dist_transm_max :
                num_lien.remove(j)
    print("voisin constent de ",sat_i," :",num_lien);   
    return num_lien   
                
                


#renvoie la liste des clusters 
def cluster(distance):
    list_cluster =[]
    sat=list(range(np.shape(x)[0]-1))
    for i in sat :
        list_proche_sat= lien_always(i,distance)
        for sat_tri in list_proche_sat :
            sat.remove(sat_tri)
            oui=lien_always(sat_tri,distance)
            for new_sat in oui :
                if new_sat not in list_proche_sat and new_sat != i :
                    list_proche_sat.append(new_sat)
        list_proche_sat.append(i)
        list_proche_sat.sort()
        if np.size(list_proche_sat)!=1 :
            list_cluster.append(list_proche_sat)
    return list_cluster


# revoie si un satellite(soloteliste) est en contact avec u cluster donné pour une distance et un instant donnée 
def connection(clus,solotelite,dist,t):
    for sat in clus :
        if distance(sat,solotelite,t) < dist :
            return True
    return False

#affiche le graphe de contact d'un satelite avec les clusters (groupe) pour une distance donnée
def oui(groupe,distance,solotelite) :
    nb=len(groupe)
    for i in range(nb):
        y_axis=[]
        for t in range(np.shape(x)[1]):
            if connection(groupe[i],solotelite,distance,t) :
                y_axis.append(i+1)
            else :
                y_axis.append(0)
        plt.plot(y_axis)
        plt.xlabel("temps")
        plt.ylabel("numéro cluster")
        plt.title("contact du satelite {} avec les clusters".format(solotelite))
        
    plt.show()




a = cluster(60000)
b = [i for i in range(100)]
for i in a:
    for j in i:
        b.remove(j)
for i in b :
    oui(a,60000, i)
