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


files=5

threads=np.zeros((16))
T=np.zeros((16))

for j in range(0,files):

    filename="v2_big.test"+str(j+1)+".output"
    with open(filename) as f:
        lines = f.readlines()

    count=0
    #print(lines[20][15:25])
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



## Do a fit of the data
def funtofit06(x,a,b,c,d):
    return a*x**3+b*x**2+c*x+d
popt06,pcov06=curve_fit(funtofit06,threads,T[0]/T)
arrff06=np.linspace(1,16,100)


fig, ax=plt.subplots()
ax.plot(threads,T[0]/T,"ok", markersize=3)
ax.plot(threads,threads,"-.k",label="Ideal")
ax.plot(arrff06,funtofit06(arrff06,popt06[0],popt06[1],popt06[2],popt06[3]),'-k', label="Experimental (Fitted)")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Speedup")
ax.legend()
plt.show()

fig.savefig("v2_big_plot.pdf", bbox_inches='tight')


