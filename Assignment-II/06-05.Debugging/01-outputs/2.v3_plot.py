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

#Read information

threads=np.zeros((16))
T=np.zeros((16))

for j in range(0,files):

    filename="v3.test"+str(j+1)+".output"
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
T1=T/files


threads=np.zeros((16))
T=np.zeros((16))

for j in range(0,files):

    filename="v3_big.test"+str(j+1)+".output"
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
T2=T/files




## Do a fit of the data
def funtofit06(x,a,b,c,d):
    return a*x**3+b*x**2+c*x+d
popt06,pcov06=curve_fit(funtofit06,threads,T1[0]/T1)
arrff06=np.linspace(1,16,100)

## Do a fit of the data
def funtofit06(x,a,b,c,d):
    return a*x**3+b*x**2+c*x+d
popt062,pcov062=curve_fit(funtofit06,threads,T2[0]/T2)
arrff062=np.linspace(1,16,100)




fig, ax=plt.subplots()
ax.plot(threads,T1[0]/T1,"or", markersize=3)
ax.plot(threads,T2[0]/T2,"ob", markersize=3)
ax.plot(threads,threads,"-.k",label="Ideal")
ax.plot(arrff06,funtofit06(arrff06,popt06[0],popt06[1],popt06[2],popt06[3]),'-r', label="Experimental n=m=1000")
ax.plot(arrff062,funtofit06(arrff062,popt062[0],popt062[1],popt062[2],popt062[3]),'-b', label="Experimental n=m=2000")
ax.set_xlabel("Number of Threads")
ax.set_ylabel("Speedup")
ax.legend()
plt.show()

fig.savefig("v3_plot.pdf", bbox_inches='tight')


