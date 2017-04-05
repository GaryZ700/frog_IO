from numpy import linalg as LA
ndim = 3
class Molecule:
    def __init__(self, aumass, natoms, coord, vel, gradient, multigradient, nacv, statescoupled, surfacehopping, currenttime,\
                 timestep, activestate):
        INCOMPLETE

    def selectState(activestate, proba):
        INCOMPLETE

    def kenacv():
        
    
    def propagate():
        nacmat = np.zeros(nstates,nstates)
        nacl = np.zeros(nstates*(nstates+1)/2)
        b_matrix = np.zeros(nstates,nstates)
        c_matrix = np.zeros(nstates,nstates)
        c_matrix_temp = np.zeros(nstates,nstates)
        proba = np.zeros(nstates,nstates)
        pop = np.zero(nstates)
        minitimstp = timestep/2.0
        for iatoms in range(natoms):
            for idim in range(ndim):
                counter = 0
                for i in range(nstates):
                    for j in range(i,nstates):
                        nacl[counter] += nacv[counter][ndim*iatoms+idim]*vel[ndim*iatoms+idim]
                        counter++
        counter = 0
        for i in range(nstates):
            for j in range(i,nstates):
                nacmat[i][j] = nacl[counter]    
                nacmat[j][i] = -nacl[counter]    
                counter++

        ## Constructing Propagator
        b_matrix = 1.j * nacmat
        for i in range(nstates):
            b_matrix[i][i] += energies(i) - energies(0)
        w,vl = LA.eig(b_matrix) 
        for i in range(nstates):
            c_matrix[i][i] = np.exp(-1.j*w[i]*minitimstp)
        c_matrix_temp = np.dot(vl,c_matrix)
        c_matrix = np.dot(c_matrix_temp,vl.getH())
        # Midpoint	 
        densmat = io.iDensMat()
        densmat_temp = np.dot(c_matrix,densmat)
        densmat_mid = np.dot(densmat_temp,c_matrix.getH())
        for i in range(nstates):
            pop[i] = densmat_mid[i][i].real
        for i in range(nstates):
            for j in range(nstates):
                proba[i][j] = densmat_mid[i][j]*nacmat[i][[j]
                proba[i][j] = 2.*timestep*proba[i][j]/max(0.000001,pop[j])
        densmat_temp = np.dot(c_matrix,densmat_mid)
        densmat_new = np.dot(densmat_temp,c_matrix.getH())
        io.wDensMat(densmat_new)
        
        newstate = selectState(activestate,proba)
        return newstate
            
            
    def hopPossible(activestatenew)
        KEparallel = kenacv()
        if(KEparallel > energies(activestatenew)-energies(activestate)):
            return activestatenew
        return activestate

    def rescale():
        vt = np.dot(vel,nacv)
        tsqm = 0.0
        for iatoms in range(natoms):
            for idim in range(ndim):
                tsqm += nacv[ndim*iatoms+idim]*nacv[ndim*iatoms+idim]/aumass[iatoms]
        kepara = 0.5*vt*vt/tsqm
        deltae = energies(activestatenew)-energies(activestate)
        factorplus  = (-vt + np.sqrt(vt*vt + 2*deltae*tsqm))/tsqm
        for iatoms in range(natoms):
            for idim in range(ndim):
                vel[ndim*iatoms+idim]+= factorplus*nacv[ndim*iatoms+idim]/aumass[iatoms]
        
    def leapfrog():
        ndim = 3
        acc = gradient
        for iatoms in range(natoms):
            for idim in range(ndim):
                acc[ndim*iatoms+idim] /= aumass[iatoms]
        vel += acc*timestep
        coord += vel*timestep
        if(surfacehopping):
            activestatenew = propagate()
            activestatenew = hopPossible(activestatenew)
            if(activestate!=activestatenew):
                rescale()
                activestate = activestatenew

            
            
            

        
