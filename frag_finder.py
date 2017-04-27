#Written by Gary Zeri
import networkx as nx
from collections import Counter

fragments = []
cutoff = 3.0

#get X coords from data of atom with grad & pos

def dist(X1,X2):
    return ((X1[0]-X2[0])**2 + (X1[1]-X2[1])**2 + (X1[2]-X2[2])**2)**0.5

def is_num(test):
    try:
        float(test)
        return True
    except ValueError:
        return False

def getX(data):
    
    coord = []

    strX = data["Position"].split(" ")

    for i in strX:
        if (is_num(i)):
            coord.append(float(i))

    return coord


def createGraph(longX,atoms,cutoff):
    G = nx.Graph()
    for i in range(len(atoms)):
        G.add_node(i)
    for i in range(len(atoms)):
        for j in range(i+1,len(atoms)):
            if(dist(longX[i],longX[j])<cutoff):
                G.add_edge(i,j)
    return G


def frag(atoms,data):
    fragments = []
    #print(len(data))

#This is where the main loop of reading the coordinates begin:
    for time in data:
       X = []
       for atom in atoms:
           X.append(getX(data[time][atom]))
       
       G = createGraph(X,atoms,cutoff)

       H = [list(yy) for yy in nx.connected_components(G)]

    ha1 = []
    for h1 in H:
        ha2 = []
        for h2 in h1:
            ha2.append(atoms[h2])
        ha1.append(ha2)
    fragments = fragments + [str([list(Hh) for Hh in ha1])]
        
    print(Counter(fragments)) 


         #   for a in range(0,len(atoms)):
          #      X.append(list(getx(s,atoms,struct_size,m,a)))
            #G = createGraph(X,atoms,cutoff)
            #H is the list of subgraphs
            #H = [list(yy) for yy in nx.connected_components(G)]

#Written by Saswata 
#   print loc, H
#   ha1/2 are for converting it into atoms (so that degenerate ones are
#   taken into the same class. (In case that was not clear: atom number 3 and 4
#   are both Hydrogens. So, if the atoms are not distinguishable, except their
#   identity in atom number, then the fragments may not be distinguished.

