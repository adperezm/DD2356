#!/usr/bin/python3

#-----------------------------------------------------------------------
#THIS SCRIPT PLOTS THE MEAN PROFILES
#-----------------------------------------------------------------------

#import modules
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys
from  scipy.optimize import curve_fit

#System information
#core speed in beskow
c=2.3e9
#beskow bandwidth from stream: 
mem_band=6913e6/2
sizeofdouble=8 #bytes

# Case information
n=8
nel=2835
#nel=256

npmax=256 #number of processes

s=0.7e-6
bandwidth=7.34e9
r=1/bandwidth


npr=np.zeros((npmax))
t=np.zeros((npmax))

for i in range(0,npmax):
    npr[i]=i+1


    # Communication info
    ## Assume that on a process, each element needs to comunicate one face. That means that it is n*n data values.
    msg_size=(n*n)*sizeofdouble #For ONE element
    # Time of one message
    #t1message=s+r*msg_size
    t1message=(s+r*msg_size*nel/npr[i])

    ## Total number of messages PER DDS CALL depend then on the number of elements
    dds_msg_num=npr[i]
    dds_msg_t=t1message*dds_msg_num
    #print(dds_msg_t)

    # MXM Values retrieved from deville. They make sense.
    ## Values for ONE call to the function.
    ### Operation count
    mxm_opc=2*n*n*n #(sum and mult)
    ### Memory acceses
    mxm_mem=(n+n)*n*sizeofdouble

    n6=6
    mxm6_opc=2*n6*n6*n6 #(sum and mult)
    ### Memory acceses
    mxm6_mem=(n6+n6)*n6*sizeofdouble


    # Axhelm operation
    axhelm_opc=(mxm_opc+n*mxm_opc+mxm_opc)*2*(nel/npr[i])
    axhelm_mem=(mxm_mem+n*mxm_mem+mxm_mem)*2*(nel/npr[i])


    #hsmgsolve
    localsolve_opc=2*(mxm_opc+n*mxm_opc+mxm_opc)*(nel/npr[i])
    localsolve_mem=2*(mxm_mem+n*mxm_mem+mxm_mem)*(nel/npr[i])
    localsolve_msg=2*dds_msg_t

    swa_opc=2*(mxm6_opc+n6*mxm6_opc+mxm6_opc)*(nel/npr[i])
    swa_mem=2*(mxm6_mem+n*mxm6_mem+mxm6_mem)*(nel/npr[i])
    swa_msg=2*dds_msg_t
    
    hsmgsolve_opc=localsolve_opc+swa_opc
    hsmgsolve_mem=localsolve_mem+swa_mem
    hsmgsolve_msg=localsolve_msg+swa_msg
    
    
    #CDABDTP
    opdiv_opc=3*3*(mxm_opc+n*mxm_opc+mxm_opc)*(nel/npr[i])
    opdiv_mem=3*3*(mxm_mem+n*mxm_mem+mxm_mem)*(nel/npr[i])

    opgrad_opc=3*(mxm6_opc+n6*mxm6_opc+mxm6_opc)*(nel/npr[i])
    opgrad_mem=3*(mxm6_mem+n6*mxm6_mem+mxm6_mem)*(nel/npr[i])

    cda_opc=opdiv_opc+opgrad_opc
    cda_mem=opdiv_mem+opgrad_mem

    #CG 
    maxcg=5 # Hard set in nek
    cg_opc=axhelm_opc*maxcg
    cg_mem=axhelm_mem*maxcg
    cg_msg=dds_msg_t*maxcg
    cg_t=cg_opc/c+cg_mem/mem_band+cg_msg
    #cg_t=cg_msg

    #GMres
    iter=5
    gmres_opc=(hsmgsolve_opc+cda_opc)*iter
    gmres_mem=(hsmgsolve_mem+cda_mem)*iter
    gmres_msg=hsmgsolve_msg*iter
    gmres_t=gmres_opc/c+gmres_mem/mem_band+gmres_msg

#print('cg_time= ',repr(cg_t))
    t[i]=(cg_t*3+gmres_t) #COG IS CALLED 3 TIMES PER TIME STEP BY OPHINV
    #t[i]=(cg_msg*3+gmres_msg)/(cg_t*3+gmres_t) #COG IS CALLED 3 TIMES PER TIME STEP BY OPHINV
    #t[i]=hsmgsolve_msg-cg_msg #COG IS CALLED 3 TIMES PER TIME STEP BY OPHINV

fig, ax = plt.subplots()    
ax.plot(npr,t,"-b", markersize=1, label="Model")
ax.set_xlabel("# Processes")
ax.set_ylabel("Execution Time [s]")
ax.legend()
plt.show()

sys.exit(00)

# Communication info

## Assume that on a process, each element needs to comunicate one face. That means that it is n*n data values.
msg_size=(n*n)*sizeofdouble #For ONE element

# Time of one message
t1message=s+r*msg_size


## Total number of messages PER DDS CALL depend then on the number of elements
dds_msgnum=nel/np


# TO DO... NUMBER OF CALLS TO MXM AND DDS PER TIME STEP. THAT WAY WE DO OUR THING CHECK IN MAP TOMORROW


sys.exit(0)

## Operations info


#number of operations (This is only counted once because each process does in paralell)
n_ops=iterations*(lsize*lsize*lsize*(2)) #For each operation in matmul there is one sum and one multiplication

T_op=n_ops/c


#memory acceses (This is only counted once because each process does in paralell)

#beskow bandwidth from stream: 
mem_band=6913e6/2

# Atemp and B are loaded lsize^3 while C is loaded and written lsize^2 since it is kept in register when iterating over

n_data=iterations*(lsize*lsize*lsize*(2))*sizeofdouble+iterations*(lsize*lsize*(1))*sizeofdouble
	
#Sum the value of copying the temporal matrices
n_data=n_data+iterations*(lsize*lsize*(2))*sizeofdouble*2
T_mem=n_data/mem_band





#=========================================================== MODEL


size1=np.zeros(10)
T_tot=np.zeros(10)

count=0
for i in [9,16,25,36,64,81,100,144,225,256]:

	#Number of mpi ranks
	size1[count]=i
	size=size1[count]
	#Size of one side of the cartesian grid
	procgrid=np.sqrt(size)

	#Problem information
	msize=2160
	sizeofdouble=8
	lsize=msize/np.sqrt(size)
	iterations=np.sqrt(size)

	## Communication info

	#Network information
	s=0.7e-6
	bandwidth=7.34e9
	r=1/bandwidth

	# Size of a regular message
	n=(lsize*lsize)*sizeofdouble
	# Time of one message
	t1message=s+r*n

	# Get how many messages in total
	Nm=iterations*(procgrid*(procgrid-1) + size) # iterations * (Messages broadcasted + messages during roll up)

	T_comm=Nm*t1message;


	## Operations info

	#core speed in beskow
	c=2.3e9

	#number of operations (This is only counted once because each process does in paralell)
	n_ops=iterations*(lsize*lsize*lsize*(2)) #For each operation in matmul there is one sum and one multiplication

	T_op=n_ops/c


	#memory acceses (This is only counted once because each process does in paralell)

	#beskow bandwidth from stream: 
	mem_band=6913e6/2

	# Atemp and B are loaded lsize^3 while C is loaded and written lsize^2 since it is kept in register when iterating over
	
	n_data=iterations*(lsize*lsize*lsize*(2))*sizeofdouble+iterations*(lsize*lsize*(1))*sizeofdouble
	
	#Sum the value of copying the temporal matrices
	n_data=n_data+iterations*(lsize*lsize*(2))*sizeofdouble*2
	T_mem=n_data/mem_band


	T_tot[count]=T_comm+T_op+T_mem

	print((T_mem+T_op)/T_tot[count])	
	count=count+1
	
	## Print
	#print('communication time:',T_comm)
	#print('operations time:',T_op)
	#print('memory access time:',T_mem)
	#print('Total time:',T_tot)

ax.plot(size1,T_tot,"-ob", markersize=3, label="Model")


ax.set_xlabel("# Processes")
ax.set_ylabel("Execution Time [s]")

ax.legend()
plt.show()



fig.savefig("ex6-plot1.pdf", bbox_inches='tight')


