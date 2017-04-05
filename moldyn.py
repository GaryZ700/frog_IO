import sys
import io
import numpy as np


errortext = ''


aumass, natoms= io.iAtoms()
coord, errortext = io.iCoord()
vel, errortext  = io.iVel()
activestate = io.iActiveState()
gradient, errortext = io.iGradient(activestate)
statescoupled = io.iStatesCoupled()
nacv, errortext = io.inacv(statescoupled)
multigradient = io.iMultiGradient(statescoupled)
surfacehopping = io.isSH()
currenttime = io.iTime()
timestep = io.iTimstp()

molecule  = MS.Molecule(aumass,natoms,coord,vel,gradient,multigradient,nacv,statescoupled,surfacehopping,\
                        currenttime,timestep,activestate) 

molecule.leapfrog()

io.wmdlog(molecule)
