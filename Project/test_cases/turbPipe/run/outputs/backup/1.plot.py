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


#Performance Plot

t=np.zeros((11))
np=np.zeros((11))
nps=[4, 8, 16, 32, 64, 96, 128, 160, 192, 224, 256]



i=2
for i in range(0,11):
    filename="ouput_process_"+repr(nps[i])+".out"
    with open(filename) as f:
        lines = f.readlines()

    A=lines[-4][0:18]
    np[i]=int(nps[i])
    t[i]=float(lines[-4][35:46])
    print(A+" for "+repr(np[i])+" procesess = "+repr(t[i]))


fig, ax=plt.subplots()
ax.plot(np,t,"-ok", markersize=3)

ax.set_xlabel("# Processes")
ax.set_ylabel("Execution time per time step [s]")
#plt.yscale('log')

plt.show()



# MPI Time analysis

permpi=[10.6, 18.4,24.6,45.8,61.6,70.3,74.2,79.3,79.6,83.9,84.5]
perrest=[100-10.6, 100-18.4,100-24.6,100-45.8,100-61.6,100-70.3,100-74.2,100-79.3,100-79.6,100-83.9,100-84.5]

perwaitall=[7.8, 12.1,12.1,22.2,29.6,44.7,31.4,33,43.9,28.5,22.1]
permreduce=[1.6, 3.8, 5.9,11.6,15.5,12.7,19.6,19.8,15.6,22.2,25.3]

perrecieve=[0.5, 1.2, 2.5,4.6,4.1,6.6,9,9.1,8.6,10.7,14]
perisend=[0.3, 0.7, 2.4,3.9,6.4,3.1,7.6,9.2,5.8,11.7,11.2]
perirecieve=[0,0,0,3,5.3,2.6,5.9,7.4,4.9,10.1,9.9]

permx8=[23.3, 22.9, 21.6,15.8,11.2,7.1,7.3,5.6,4.5,4.3,4.2]
permx6=[10.5, 9.9, 10.4,7.2,5.2,3.4,3.6,2.7,2.1,2,2]

 
fig, ax=plt.subplots()
ax.plot(np,permpi,"-ob", markersize=3, label='Communication')
#ax.plot(np,perrest,"-ok", markersize=3)

ax.set_xlabel("# Processes")
ax.set_ylabel("Total execution time [%]")
#plt.yscale('log')
plt.legend()
plt.show()


fig, ax=plt.subplots()
ax.plot(np,permx8,"-ok", markersize=3, label='mxf8')
ax.plot(np,permx6,"-.ok", markersize=3, label='mxf6')
ax.plot(np,perwaitall,"-ob", markersize=3, label='MPI_Waitall')
ax.plot(np,permreduce,"-.ob", markersize=3, label='MPI_allreduce')
ax.plot(np,perisend,"--ob", markersize=3, label='MPI_Isend')
ax.plot(np,perirecieve,":ob", markersize=3, label='MPI_Irecv')

ax.set_xlabel("# Processes")
ax.set_ylabel("Total execution time [%]")
#plt.yscale('log')
plt.legend()
plt.show()


sys.exit(0)
#System information
#core speed in beskow
c=2.3e9
#beskow bandwidth from stream: 
mem_band=6913e6/2

#Operation count needed for 


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


