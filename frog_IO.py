#Written by Gary Zeri
import frag_finder as frag
import os
import sys
import json
import random


#import frag_finder 
#print("asdjfhaksjdhfkjashdkjfhskjdhfjksdhfkjashdjkfhaskjdhfjksdhfkj")


#import numpy as np

#init global vars########################################################################

atoms = []
masses = {'c':21894.2, 'h':1837.29, 'o':21894.2}


grad = []
energy = []
ex_energy = []
pos = []
vel = []

md = {}

sp = "    "

cutoff = 3.0

# f = file("control","r")


#Main Functions#############################################################################





#read data from file outside of control
#f = data file name
#returns last line data as string
def external_data(dtype,f):
    
    if(dtype == "energy"):  
        
        line = filter(None,os.popen("tail -n 2 "+f).read().split(" "))
         

        if(len(line) == 5):
            ex_energy.append(line[4].split("$end")[0])

        return line[1].strip(" ") + sp + line[2].strip(" ") + sp + line[3].strip(" ").split("$end")[0]
    
    elif(dtype == "grad"):
        
        line = filter(None,os.popen('tail -n ' + str(len(atoms)*2 + 1) + ' ' + f + ' | head -n ' + str(len(atoms))).read().split("\n"))
     
        for a in range(len(line)):
            
            holder = line[a].split(" ")
            holder = filter(None,holder)
                       
            grad.append(holder[0] + sp + holder[1] + sp + holder[2])
    
    elif(dtype == "coord"):
        
        f = file(f, 'r')
    
        for line in f:
            atom = line.split("    ")[len(line.split("    "))-1].strip("\n")
            
            tempPos = line.split("    ")

            if(atom.count("$") == 0):
                atoms.append(atom.strip(" "))
                pos.append(tempPos[0] + tempPos[1] + tempPos[2])



       
#reads data from inside of control file
def internal_data():
    
    return "Data inside control file"

#finds location of specified data, and retrives it
#dtype = type of data as string
def data(dtype): 
    
    line = os.popen(' grep -n ' + dtype + ' "control" ').read().split("   ")[1].split("\n")[0]
    
    if(line.count("file=") == 1):
        #if data in external file
        print("file")
        return external_data(dtype,line.split("file=")[1])
    else:
        #if data inside of control file
        print("not in file")
        return internal_data()

def init():
    
    master = {}
    
    master["Time Step"] = "Can not find time step"
    master["Surface Hopping"] = "surface"
    master["Coupled"] =  "coupled"

    with open("mdMaster.json","w") as out:
        json.dump(master,out)
       


#should be run after all datas
def log():
    
    Data = {}
    
    if(os.path.isfile("mdlog.json")):
        with open("mdlog.json","r") as f:
            Data = json.load(f)
    time = iTime()

    md["Time " + str(time)] = {} 
    
    md["Time " + str(time)]["Energy"] = data("energy").split("\n")[0]

    for atom in range(len(atoms)):

        md["Time " + str(time)][atoms[atom]] = {
            
            'Position': pos[atom],
            'Gradient': grad[atom],
            
            }

        Data.update(md)
        
    with open("mdlog.json","w") as out:
        json.dump(Data,out)

#End of main functions#####################################################################

#begining of io functions

def iAtoms():
    data("coord")
    aumass = []

    for atom in atoms:
        aumass.append(masses[atom])
    print(aumass)
    return aumass,atoms

def iCoord():
    data("coord")
    return pos,"None"

def iVel():
    return vel

def iActiveState():
    return "ActiveState"

def iGradient(activestate):
    data("grad")
    return grad

def iStateCoupled(statescoupled):
    return "coupled states"

def inacv(coupledstates):
    return "nacv"

def iMultiGradient(scoupled):
    return "multigradient"

def isSH():
    return "Surface hopping"

def iTime():
    return random.random()

def iTimestp():
    return "timestep"

def iFrag():
      
    with open("mdlog.json", "r") as f:
        data = json.load(f)

    frag.frag(atoms,data)

#end of io functions




#check if init should be run
if(not os.path.isfile("mdMaster.json")):
    init()




data("coord")
energy = data("energy")
data("grad")
#create log file
log()

#print(atoms)
#print(energy)
#print(grad)
#print(ex_energy)

print(iCoord())

iFrag()
