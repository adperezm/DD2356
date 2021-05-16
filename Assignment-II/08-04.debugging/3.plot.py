#!/usr/bin/python3

#-----------------------------------------------------------------------
#THIS SCRIPT PLOTS THE MEAN PROFILES
#-----------------------------------------------------------------------

#import modules
import numpy as np
import matplotlib.pyplot as plt
import subprocess
import sys


files=2

threads=np.zeros((16))
T=np.zeros((16))

for j in range(0,files):

    filename="v2.test"+str(j+1)+".output"
    with open(filename) as f:
        lines = f.readlines()

    count=0
    print(lines[20][15:25])
    for i in range(0,len(lines[:])):
        if lines[i][1:12]=="Solver took":
           #print(lines[i][1:12])
           #print(lines[i][7:18])
            T[count]= T[count] + float(lines[i][15:25])
            threads[count]=count+1
            #print(T[count])
            count+=1
T=T/files

print(T)

fig, ax=plt.subplots()
ax.plot(threads,T[0]/T,"ok", markersize=3, label="Experimental")
ax.plot(threads,threads,"-.k",label="Ideal")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Speedup")
ax.legend()

plt.show()

#fig.savefig("DFTW_Speedup_Plot.pdf", bbox_inches='tight')


