from array import array
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D

with open("Traces.csv") as file:
    tab= np.loadtxt(file,delimiter=",")

print(np.size(tab[0]))
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

def vitesse(i,t):
    return 





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
    
    
    


    
    
def graph_distance(i,j):
    axis_y=[]
    axis_x=range(np.shape(x)[1])
    for t in range(np.shape(x)[1]):
        axis_y.append(distance(i,j,t))
    plt.plot(axis_y)
    plt.show()
        


#graph_distance(2,3)


#fonction permettant de générer la matrice des distances entre les 100 satellite
# entre 0 et timemax
def graph_conectivity():
    distanceintersat = np.zeros((np.shape(x)[0],np.shape(x)[0],np.shape(x)[1]))
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(x)[0]):
            for t in range(0, np.shape(x)[1]):
                distanceintersat[i][j][t]= distance(i,j,t)
    return distanceintersat

graph_conectivity()
