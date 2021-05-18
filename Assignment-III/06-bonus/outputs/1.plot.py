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


#Read information


filename="paralell.out"
with open(filename) as f:
    lines = f.readlines()
    #size=np.zeros(len(lines))
    #T=np.zeros(len(lines))

A=lines[25][8:23]
print(A)

A=lines[25][24:32]
print(A)


A=lines[1][0:24]
print(A)

A=lines[1][25:len(lines[1])]
print(A)


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
ax.plot(pro,T,"-ok", markersize=3)


ax.set_xlabel("# Processes")
ax.set_ylabel("Execution Time [s]")


plt.show()


fig.savefig("ex6-plot1.pdf", bbox_inches='tight')


