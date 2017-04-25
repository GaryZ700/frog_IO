#Written by Gary Zeri

import networkx as nx
from collections import Counter


cutoff = 3.0

def test():
    print("hi")
    return 0

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
#This is where the main loop of reading the coordinates begin:
    for m in range(0,0):
#struct loop
        for s in range(0,int(struct[m])):
            X = [] 


            for a in range(0,len(atoms)):
                X.append(list(getx(s,atoms,struct_size,m,a)))
            G = createGraph(X,atoms,cutoff)
            #H is the list of subgraphs
            H = [list(yy) for yy in nx.connected_components(G)]

#Written by Saswata 
#   print loc, H
#   ha1/2 are for converting it into atoms (so that degenerate ones are
#   taken into the same class. (In case that was not clear: atom number 3 and 4
#   are both Hydrogens. So, if the atoms are not distinguishable, except their
#   identity in atom number, then the fragments may not be distinguished.
    return 0

