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

n = [500,1000,2000]
simple_exp = [0.52980230,2.10006979,8.25644889]
simple_err = [0.02822960,0.06553924,0.16628871]
simple_model_nomem=[0.12,0.46,1.85]
simple_model_simem=[0.43,1.70,6.81]

fig, ax=plt.subplots(figsize=(7,5))
ax.scatter(n,simple_exp,marker='x',c='black',label='Experimental (mean)')
ax.errorbar(n,simple_exp,yerr=simple_err, linestyle="None",label='Experimental (Std Dev)')
ax.scatter(n,simple_model_nomem,marker='o',color='black',label='Model (No memory)')
ax.scatter(n,simple_model_simem, marker='^',color='black',label='Model (Memory)')
ax.set_xlabel('Number of Particles')
ax.set_ylabel('Execution time [s]')
plt.ylim(0,9)
ax.legend()
plt.show()
fig.savefig("simple_Algorithm.pdf", bbox_inches='tight')



## Reduced

n = [500,1000,2000]
r_exp = [0.37923141,1.51495140,6.08869550]
r_err = [0.01182045,0.04719865,0.09882909]
r_model_nomem=[0.06423077,0.25666667,1.02615385]
r_model_simem=[0.31681296,1.26590972,5.06095466]

fig, ax=plt.subplots(figsize=(7,5))
ax.scatter(n,r_exp,marker='x',c='black',label='Experimental (mean)')
ax.errorbar(n,r_exp,yerr=simple_err, linestyle="None",label='Experimental (Std Dev)')
ax.scatter(n,r_model_nomem,marker='o',color='black',label='Model (No memory)')
ax.scatter(n,r_model_simem, marker='^',color='black',label='Model (Memory)')
ax.set_xlabel('Number of Particles')
ax.set_ylabel('Execution time [s]')
plt.ylim(0,9)
ax.legend()
plt.show()
fig.savefig("reduced_Algorithm.pdf", bbox_inches='tight')


## Comparison

fig, ax=plt.subplots(figsize=(7,5))
ax.scatter(n,simple_exp,marker='x',c='black',label='Experimental_Simple (mean)')
ax.scatter(n,r_exp,marker='^',c='black',label='Experimental_Reduced (mean)')
ax.errorbar(n,simple_exp,yerr=simple_err, linestyle="None",label='Experimental (Std Dev)')
ax.errorbar(n,r_exp,yerr=r_err, linestyle="None",label='Experimental (Std Dev)')
ax.set_xlabel('Number of Particles')
ax.set_ylabel('Execution time [s]')
plt.ylim(0,9)
ax.legend()
plt.show()
fig.savefig("reduced_vs_simple.pdf", bbox_inches='tight')


