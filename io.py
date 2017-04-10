import os
import json
#import numpy as np

#init global vars########################################################################

atoms = []

grad = []
energy = []
ex_energy = []
pos = []
vel = []

md = {}

sp = "    "


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

    md["Time Step"] = "Can not find time step"
    md["Surface Hopping"] = "surface"
    md["Coupled"] =  "coupled"

    with open("mdMaster.json","w") as out:
        json.dump(md,out)


#should be run after all datas
def log():
    md["Time "] = {} 
    
    md["Time "]["Energy"] = data("energy").split("\n")[0]

    for atom in range(len(atoms)):

        md["Time "][atoms[atom]] = {
            
            'Position': pos[atom],
            'Gradient': grad[atom],
            
            }
        
    with open("mdlog.json","w") as out:
        json.dump(md,out)

#End of main functions#####################################################################

#begining of io functions

def iAtoms():
    data("coord")
    return "atomsMasses",atoms

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

def iMultiGradient(statescoupled):
    return "multigradient"

def isSH():
    return "Surface hopping"

def iTime():
    return "time"

def iTimestp():
    return "timestep"


#end of io functions




#check if init should be run
if(not os.path.isfile("mdMaster.json")):
    init()




data("coord")
energy = data("energy")
data("grad")
#create log file
log()

print(atoms)
print(energy)
print(grad)
print(ex_energy)



