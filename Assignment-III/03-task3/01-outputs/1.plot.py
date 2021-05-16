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


filename="intra-two.out"
with open(filename) as f:
    lines = f.readlines()
    size=np.zeros(len(lines))
    T=np.zeros(len(lines))


for i in range(0,len(lines[:])):
    T[i]= float(lines[i][13:31])
    size[i]=float(lines[i][0:10])
    
p=np.polyfit(size,T,1)
interp=np.linspace(0,max(size),100)
print(p)
print("For intra node communications:")
print("Latency="+repr(p[1]/0.000001)+" ms")
print("bandwidth="+repr(1/p[0]/1000000000)+" GB/s")

print("========")

fig, ax=plt.subplots()
ax.plot(size,T,"ok", markersize=3)
ax.plot(interp,interp*p[0]+p[1],"--k", markersize=3)


filename="inter-two.out"
with open(filename) as f:
    lines = f.readlines()
    size=np.zeros(len(lines))
    T=np.zeros(len(lines))


for i in range(0,len(lines[:])):
    T[i]= float(lines[i][13:31])
    size[i]=float(lines[i][0:10])
    
h=0

p=np.polyfit(size,T,1)
interp=np.linspace(0,max(size),100)
print(p)
print("For inter node communications:")
print("Latency="+repr(p[1]/0.000001)+" ms")
print("bandwidth="+repr(1/p[0]/1000000000)+" GB/s")

ax.plot(size,T,"ob", markersize=3)
ax.plot(interp,interp*p[0]+p[1],"--b", markersize=3)



plt.show()


fig.savefig("plot.pdf", bbox_inches='tight')


