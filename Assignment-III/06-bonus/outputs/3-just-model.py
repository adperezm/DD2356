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

size1=np.zeros(10)
T_tot=np.zeros(10)

count=0
for i in [9,16,25,36,64,81,100,144,225,256]:

	#Number of mpi ranks
	size1[count]=i
	size=size1[count]
	
	procgrid=np.sqrt(size)

	#Problem information
	msize=2160
	sizeofdouble=8
	lsize=msize/np.sqrt(size)
	iterations=np.sqrt(size)

	#print(lsize)


	## Communication info

	#Network information
	s=0.7e-6
	bandwidth=7.34e9
	r=1/bandwidth

	#print(r)
	# Size of a regular message
	n=(lsize*lsize)*sizeofdouble
	# Time of one message
	t1message=s+r*n

	# Get how many messages in total
	Nm=iterations*(procgrid*(procgrid-1) + size) # iterations * (Messages broadcasted + messages during roll up)

	T_comm=Nm*t1message;

	#print('communication time:',T_comm)


	## Operations info

	#core speed in beskow
	c=2.3e9

	#number of operations (This is only counted once because each process does in paralell)
	n_ops=iterations*(lsize*lsize*lsize*(2)) #For each operation in matmul there is one sum and one multiplication

	T_op=n_ops/c


	#memory acceses

	#beskow bandwidth from stream copy/2
	mem_band=6913e6/2

	n_loads=iterations*(lsize*lsize*lsize*(4))

	T_mem=n_loads/mem_band

	#print('operations time:',T_mem)




	T_tot[count]=T_comm+T_op+T_mem
	#print('Total time:',T_tot)
	
	
	count=count+1


fig, ax=plt.subplots()
ax.plot(size1,T_tot,"-ok", markersize=3)


ax.set_xlabel("# Processes")
ax.set_ylabel("Execution Time [s]")


plt.show()

sys.exit("stop")



