from array import array
from cProfile import label
from dis import dis
from json import load
import networkx as nx
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import pandas as pd
import os.path

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
#trace le graphe de tous les satellites sur l'ensemble des points
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

#affiche les satellites à un instan donné
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

#calcule la distance entre 2 points à un instant t
def distance(i,j,t):
    return np.sqrt((x[i][t]-x[j][t])**2+(y[i][t]-y[j][t])**2+(z[i][t]-z[j][t])**2)





#trace affiche la trajectoire de l'ensemble dessatellites entre 2 instants (d et f)
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




#affiche le nombre de voisin d'un satellite pour les 3 valeurs de distance    
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
    

#affiche la distance entre i et j en fonction du temps
def graph_distance(i,j):
    axis_y=[]
    axis_x=range(np.shape(x)[1])
    for t in range(np.shape(x)[1]):
        axis_y.append(distance(i,j,t))
    plt.plot(axis_y)
    plt.show()
        




#fonction permettant de générer la matrice des distances entre les 100 satellites
# entre 0 et timemax
def graph_conectivity(debut, fin):
    distanceintersat = np.zeros((np.shape(x)[0],np.shape(x)[0],fin-debut))
    for i in range(np.shape(x)[0]):
        for j in range(np.shape(x)[0]):
            for t in range(debut, fin):
                distanceintersat[i][j][t]= distance(i,j,t)
    return distanceintersat


#permet de récupérer la liste des statellites qui reste en contact avec le satellite i dans un rayon donné 
def lien_always(sat_i, dist_transm_max):
    num_lien=list(range(np.shape(x)[0]))
    num_lien.remove(sat_i)
    for t in range(np.shape(x)[1]):
        for j in num_lien:
            if  distance(sat_i,j,t) > dist_transm_max :
                num_lien.remove(j)
            continue
    print("voisin de ",sat_i," :",num_lien);   
    return num_lien   
                
#permet de récupérer la liste des statellites qui est en contact avec le satellite i dans un rayon donné pendant un pourcentage donnée
def lien_pourcent(sat_i, dist_transm_max,pourcent):
    num_lien=[]
    for j in range(np.shape(x)[0]):
            if(j==sat_i) :
                continue
            count = 0
            for t in range(1792):
                if  distance(sat_i,j,t) < dist_transm_max :
                    count +=1
            if (count/1792>pourcent) :
                num_lien.append(j)
    return num_lien 


#renvoie la liste des clusters 
def cluster(distance):
    list_cluster =[]
    sat=list(range(np.shape(x)[0]-1))
    for i in sat : 
        list_proche_sat= lien_always(i,distance) #pour chaque satellite on récupère ses voisins
        for sat_tri in list_proche_sat : # puis on récupère les voisins des voisins et ainsi de suite
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

#renvoie la liste des temps ou les satellites i et j sont en contact pour une distance donnée
def contact_time(i,j,dist) :
    contacttime=[]
    debut,fin = False,False
    for t in range(1792):
        if  distance(i,j,t) > dist :
            if debut : ## on vient de sortir de la distance d'émission
                fin = True
                fin_t = t-1
            else : ## on attend un contact entre les 2 satellites
                continue
        elif not debut: ## on vient de rentrer en contact
            debut = True
            debut_t = t
        if (debut & fin) :
            debut,fin = False,False
            contacttime.append((debut_t,fin_t))
    return contacttime

# revoie si un satellite(sateliste éloigné) est en contact avec un cluster donné pour une distance et un instant donné 
def connection(clus,solotelite,dist,t):
    for sat in clus :
        if distance(sat,solotelite,t) < dist :
            return True
    return False

#affiche le graphe de contact d'un satellite avec les clusters (groupe) pour une distance donnée
def contact(groupe,distance,solotelite) :
    i=0
    y_axis=[]
    for t in range(np.shape(x)[1]):
        if connection(groupe,solotelite,distance,t) :
            y_axis.append(i+1)
        else :
            y_axis.append(0)
    plt.plot(y_axis)
    plt.xlabel("temps")
    plt.ylabel("numéro cluster")
    plt.title("contact du satelite {} avec les clusters".format(solotelite))
        
    plt.show()

#cherche les satellites qui reste en contact avec le cluster mais qui change de contact (satellite de périphérie)
def cluster_check(cluster,distance):
    fin = False
    while(not fin):
        fin = True
        for i in range(100):
            if i not in cluster[0]:
                boo = True
                for t in range(np.shape(x)[1]):
                    if not (connection(cluster[0],i,distance,t)):
                        boo = False
                        
                if boo:
                    cluster[0].append(i)
                    fin = False
        cluster[0].sort()
        print(cluster[0])
    return cluster

#récupère la liste des satellites qui sont en contact avec les satellites éloignés sour la forme (sat_loin,sat_contact,temps contact,debut contact,fin_contact)
def getlistepasseur(satloin,dist) :
    listpasseur=[]
    for i in satloin :
        listtemp = []
        for j in range(np.shape(x)[0]):
            listtemps = contact_time(i,j,dist)
            if (listtemps != []) :
                for interval in listtemps :
                    listtemp.append([i,j,interval[1]-interval[0],interval[0],interval[1]])
        listpasseur.append(listtemp)  
                    
                    
    return listpasseur


#renvoie les differents contacts entre les satellites pour un pourcentage de contact et une distance donnée
def getlistvoisin(dist,pourcent) :
        listvoisin = []
        for i in range(100):
            voisins = lien_pourcent(i, dist,pourcent)
            listvoisin.append(voisins)
        return listvoisin

#trace le graphe de contact des voisins proche à un pourcentage donnée
def tracerNetwork(listvoisin) :
    
    G = nx.Graph()
    for i in range(100):
        G.add_nodes_from(range(100))
    for i in range(100):
        for j in listvoisin[i] : 
            G.add_edge(i,j)
    return (G)
    
##renvoie un tableau qui permet de savoir quel satellite va etre en contact avec un satellite éloigné (routageloin[sat_loin][temps] renvoie le voisin de sat_loin s'il exsite sinon -1)
def getroutageexterne(satexterne,dist) :
    passeur = getlistepasseur(satexterne,dist)
    time = passeur
    i = 0

    for sat_loin in passeur : 
        
        time[i] = sorted(sat_loin,key=lambda sat_loin : sat_loin[2])
        time[i].reverse()
        i+=1
    routageloin = []
    for bestcontact in time :
        routage= [-1]*1792
        while bestcontact != [] :
            contacttemp=bestcontact[0]
            for i in range(contacttemp[3],contacttemp[4]) :
                routage[i] = contacttemp[1]
            bestcontact.pop(0)
            for autrecontact in bestcontact :
                if (autrecontact[3]>contacttemp[3] & autrecontact[4]<contacttemp[4]) :
                    bestcontact.remove(autrecontact)
                elif (autrecontact[3]>contacttemp[3]) :
                    autrecontact[3] = contacttemp[4] + 1
                elif (autrecontact[4]<contacttemp[4]) :
                    autrecontact[4] = contacttemp[3] - 1
        routageloin.append(routage)
    return routageloin
#affiche le routage entre sat_depart (appartenant au coeur) et sat_arrive à l'instant t et avec la distance dist pour le bon en dehors du cluster 
def routage_externe(sat_depart,sat_arrive,temps,dist) :
    satloin = [3, 36, 37, 53, 54, 86, 92]
    
    
    if(sat_arrive in satloin) :
        ind=satloin.index(sat_arrive)
        listroutage = getroutageexterne(satloin,dist)
        temps = temps % 1792
        sat_contact = listroutage[ind][temps]
        instantane = True
        while(sat_contact == -1 ) :
            temps +=1
            if (temps == 1792) :
                temps = 0
            sat_contact = listroutage[ind][temps]
            instantane = False
    
    # appel fonction cédric route entre sat_depart, sat_arrive à l'instant temps
    # rajouter un symbole si on attend
    cmd = "python3 ./findAPathInstant.py {} {} {} {} {}".format(sat_depart, sat_arrive, temps, instantane, sat_contact)
    os.system(cmd)
    
    
    
    
    # 40 km : cluster : [0, 1, 2, 5, 6, 7, 8, 9, 11, 12, 15, 16, 17, 18, 19, 22, 23, 24, 26, 27, 30, 31, 32, 33, 35, 38, 39, 40, 41, 42, 44, 45, 46, 48, 50, 51, 52, 55, 56, 57, 58, 59, 60, 62, 63, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 77, 78, 79, 80, 81, 84, 87, 88, 89, 90, 91, 94, 95, 97, 98]
    #         jamais  : 54
    #         contact : [3, 4, 10, 13, 14, 20, 21, 25, 28, 29, 34, 36, 37, 43, 47, 49, 53, 54, 61, 64, 76, 82, 83, 85, 86, 92, 93, 96, 99]

    # rejoins le cluster entre 40 et 60 :  [4, 10, 13, 14, 20, 21, 25, 28, 29, 34, 43, 47, 49, 61, 64, 76, 82, 83, 85, 93, 96, 99]

    # 60 km : cluster : [0, 1, 2, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 87, 88, 89, 90, 91, 93, 94, 95, 96, 97, 98, 99] 
    #         contact : [3, 36, 37, 53, 54, 86, 92]  

    #

    # seul      pour 20 km : 2,3,4,8,10,26,28,29,30,32,36,37,38,47,51,52,54,61,64,68,72,76,79,81,85,86,88,89,91,93,96,98


satloin = [3, 36, 37, 53, 54, 86, 92]
dist=60000
pourcent = 0.9


#routage_externe(1,92,1790,dist)

#print(getroutageexterne(satloin,dist))


#listvoisin = getlistvoisin(dist,pourcent)
#graph = tracerNetwork(listvoisin)
#nx.draw(graph,with_labels = True)
#plt.show()



a = cluster(dist)
clustv2=cluster_check(a,dist)[0]


b = [i for i in range(100)]
for j in clustv2:
        b.remove(j)
print(b)
for i in b :
    contact(clustv2,dist, i)
