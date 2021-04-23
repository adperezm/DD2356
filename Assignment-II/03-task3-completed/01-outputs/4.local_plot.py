#!/usr/bin/python3

#-----------------------------------------------------------------------
#THIS SCRIPT PLOTS THE MEAN PROFILES
#-----------------------------------------------------------------------

#import modules
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys


##Simple

filename="4.local.output"
with open(filename) as f:
    lines = f.readlines()

threads=np.zeros((32))
T=np.zeros((32))
count=0
#print(lines[20][0:4])
for i in range(0,len(lines[:])):
    if lines[i][0:4]=="Mean":
        #print(lines[i][0:4])
        #print(lines[i][7:18])
        T[count]= float(lines[i][7:18])
        threads[count]=count+1
        #print(T[count])
        count+=1

fig, ax=plt.subplots()
ax.plot(threads,T,"-k", markersize=3, label="Experimental")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Execution time [s]")
#ax.legend()

plt.show()

fig.savefig("4.local_Plot.pdf", bbox_inches='tight')


