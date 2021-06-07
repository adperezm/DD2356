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
dp=15
t=np.zeros((dp))
np=np.zeros((dp))
nps=[1, 2, 4, 8, 12, 16, 24, 32, 64, 96, 128, 160, 192, 224, 256]



i=2
for i in range(0,dp):
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
fig.savefig("scaling_eddy_uv.png", bbox_inches='tight')


