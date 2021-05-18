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


#Print Experimental data

filename="paralell.out"
with open(filename) as f:
    lines = f.readlines()

T=np.zeros(10)
pro=np.zeros(10)

count1=0
count2=0
for i in range(0,len(lines[:])):
    if (lines[i][8:23]=="execution time:"):
        T[count1]= float(lines[i][24:32])
        
        count1=count1+1
     
    if (lines[i][0:24]=="Number of MPI Processes:"):
        pro[count2]= float(lines[i][25:len(lines[i])])
        count2=count2+1

fig, ax=plt.subplots()
ax.plot(pro,T,"-ok", markersize=3, label="Experimental")




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


fig.savefig("ex6-plot5.pdf", bbox_inches='tight')


