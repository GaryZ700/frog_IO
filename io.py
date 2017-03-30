import os
#import numpy as np

#init global vars########################################################################

atoms = []

grad = []
energy = []
ex_energy = []

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
            if(atom.count("$") == 0):
                atoms.append(atom.strip(" "))
       
#reads data from inside of control file
def internal_data():
    
    return 0

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



#End of main functions#####################################################################



data("coord")
energy = data("energy")
data("grad")


print(atoms)
print(energy)
print(grad)
print(ex_energy)


