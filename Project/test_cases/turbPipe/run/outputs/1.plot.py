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

tt=np.zeros((11))
npp=np.zeros((11))
nps=[4, 8, 16, 32, 64, 96, 128, 160, 192, 224, 256]



i=2
for i in range(0,11):
    filename="ouput_process_"+repr(nps[i])+".out"
    with open(filename) as f:
        lines = f.readlines()

    A=lines[-4][0:18]
    npp[i]=int(nps[i])
    tt[i]=float(lines[-4][35:46])
    print(A+" for "+repr(npp[i])+" procesess = "+repr(tt[i]))


fig, ax=plt.subplots()
ax.plot(npp,tt,"-ok", markersize=3)

ax.set_xlabel("# Processes")
ax.set_ylabel("Execution time per time step [s]")
#plt.yscale('log')

plt.show()

fig.savefig("scaling_turbPipe.png", bbox_inches='tight')


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
ax.plot(npp,permpi,"-ok", markersize=3, label='Communication')
#ax.plot(np,perrest,"-ok", markersize=3)

ax.set_xlabel("# Processes")
ax.set_ylabel("Total execution time [%]")
#plt.yscale('log')
plt.legend()
plt.show()
fig.savefig("communication_turbPipe.png", bbox_inches='tight')

fig, ax=plt.subplots()
ax.plot(npp,permx8,"-ok", markersize=3, label='mxf8')
ax.plot(npp,permx6,"-.ok", markersize=3, label='mxf6')
ax.plot(npp,perwaitall,"-ob", markersize=3, label='MPI_Waitall')
ax.plot(npp,permreduce,"-.ob", markersize=3, label='MPI_allreduce')
ax.plot(npp,perisend,"--ob", markersize=3, label='MPI_Isend')
ax.plot(npp,perirecieve,":ob", markersize=3, label='MPI_Irecv')

ax.set_xlabel("# Processes")
ax.set_ylabel("Total execution time [%]")
#plt.yscale('log')
plt.legend()
plt.show()
fig.savefig("used_functions_turbPipe.png", bbox_inches='tight')


#=========================================================== MODEL

#System information
#core speed in beskow
c=2.3e9
#beskow bandwidth from stream: 
mem_band=6913e6/2
sizeofdouble=8 #bytes

# Case information
nel=2835
npmax=256 #number of processes

# Network information
s=0.7e-6
bandwidth=7.34e9
r=1/bandwidth

# Declare variables
npr=np.zeros((npmax))
t=np.zeros((npmax))
tcomm=np.zeros((npmax))

for i in range(0,npmax):
    npr[i]=i+1

    # dds
    n=8
    ## Message size
    msg_size=(n*n)*sizeofdouble
    ## Time for one message
    t1message=(s+r*msg_size*nel/npr[i])
    ## Total number of messages PER DDS CALL depend then on the number of elements
    dds_msg_num=npr[i]*4 # Assuming that each process has 4 neighbours (Max would be 6)
    dds_msg_t=t1message*dds_msg_num

    # mxm8
    n=8
    ## When calculating in x and z:
    ### Operation count
    mxmxz_opc=2*n*n*n**2 #(sum and mult)
    ### Memory acceses
    mxmxz_mem=(n+n**2)*1*sizeofdouble #where it says 1 it should be n.But we use the unrolled version
    ## When calculating for y
    ### Operation count
    mxmy_opc=2*n*n*n #(sum and mult)
    ### Memory acceses
    mxmy_mem=(n+n)*1*sizeofdouble 

    # mxm6
    n6=6
    ## When calculating in x and z:
    mxm6xz_opc=2*n6*n6*n6**2 #(sum and mult)
    ### Memory acceses
    mxm6xz_mem=(n6+n6**2)*1*sizeofdouble
    ## When calculating in y:
    mxm6y_opc=2*n6*n6*n6 #(sum and mult)
    ### Memory acceses
    mxm6y_mem=(n6+n6)*1*sizeofdouble

    #ophinv =======================================================

    # Axhelm operation
    axhelm_opc=2*(mxmxz_opc+n*mxmy_opc+mxmxz_opc)*(nel/npr[i])
    axhelm_mem=2*(mxmxz_mem+n*mxmy_mem+mxmxz_mem)*(nel/npr[i])
    
    # CG 
    maxcg=5 
    cg_opc=axhelm_opc*maxcg
    cg_mem=axhelm_mem*maxcg
    cg_msg=dds_msg_t*maxcg
    cg_t=cg_opc/c+cg_mem/mem_band+cg_msg
    
    # h_solve
    hsolve_t=cg_t

    #ophinv
    ophinv_t=3*hsolve_t


    #incompr =======================================================
    
    #HSMGSOLVE

    #tensr3
    tensr3_opc=(mxmxz_opc+n*mxmy_opc+mxmxz_opc)*(nel/npr[i])
    tensr3_mem=(mxmxz_mem+n*mxmy_mem+mxmxz_mem)*(nel/npr[i])
    
    #fastdm1
    fastdm1_opc=2*tensr3_opc
    fastdm1_mem=2*tensr3_mem

    #local_solves
    localsolve_opc=fastdm1_opc
    localsolve_mem=fastdm1_mem
    localsolve_msg=2*dds_msg_t
    
    #hsmg_tnsr3d
    hsmg_tnsr3d_opc=(mxm6xz_opc+n6*mxm6y_opc+mxm6xz_opc)*(nel/npr[i])
    hsmg_tnsr3d_mem=(mxm6xz_mem+n6*mxm6y_mem+mxm6xz_mem)*(nel/npr[i])

    #hsmg_fdm
    hsmg_fdm_opc=2*hsmg_tnsr3d_opc
    hsmg_fdm_mem=2*hsmg_tnsr3d_mem

    #hsmg_schwarz
    swa_opc=hsmg_fdm_opc
    swa_mem=hsmg_fdm_mem
    swa_msg=3*dds_msg_t
   
    #hsmgsolve
    hsmgsolve_opc=localsolve_opc+swa_opc
    hsmgsolve_mem=localsolve_mem+swa_mem
    hsmgsolve_msg=localsolve_msg+swa_msg
    
    
    #CDABDTP
    
    #multd
    multd_opc=2.6*(mxm6xz_opc+n6*mxm6y_opc+mxm6xz_opc)*(nel/npr[i])
    multd_mem=2.6*(mxm6xz_mem+n6*mxm6y_mem+mxm6xz_mem)*(nel/npr[i])

    #opdiv
    opdiv_opc=3*multd_opc
    opdiv_mem=3*multd_mem

    #cdtp
    cdtp_opc=3*(mxm6xz_opc+n6*mxm6y_opc+mxm6xz_opc)*(nel/npr[i])
    cdtp_mem=3*(mxm6xz_mem+n6*mxm6y_mem+mxm6xz_mem)*(nel/npr[i])

    #opgradt
    opgrad_opc=3*cdtp_opc
    opgrad_mem=3*cdtp_mem

    #cdabtp
    cda_opc=opdiv_opc+opgrad_opc
    cda_mem=opdiv_mem+opgrad_mem

    #GMres
    iter=15
    gmres_opc=(hsmgsolve_opc+cda_opc)*iter
    gmres_mem=(hsmgsolve_mem+cda_mem)*iter
    gmres_msg=hsmgsolve_msg*iter
    gmres_t=gmres_opc/c+gmres_mem/mem_band+gmres_msg

    #incompr
    incompr_t=gmres_t


    t[i]=(ophinv_t+incompr_t)
    tcomm[i]=(cg_msg*3+gmres_msg)/t[i] #COG IS CALLED 3 TIMES PER TIME STEP BY OPHINV
    

fig, ax = plt.subplots()    
#ax.plot(npr,t[0]/npr,"--r", markersize=1, label="Ideal")
ax.plot(npr,t,"-b", markersize=1, label="model")
ax.plot(npp,tt,"-ok", markersize=3, label="Experiment")
ax.set_xlabel("# Processes")
ax.set_ylabel("Execution Time per time step [s]")
#plt.yscale('log')
#plt.xscale('log')
ax.legend()
plt.show()
fig.savefig("mod_vs_exp.png", bbox_inches='tight')

fig, ax = plt.subplots()    
ax.plot(npr,tcomm*100,"-b", markersize=1, label="Model comms")
ax.plot(npp,permpi,"-ok", markersize=3, label="Experiment comms")
ax.set_xlabel("# Processes")
ax.set_ylabel("Total execution Time [%]")
ax.legend()
plt.show()
fig.savefig("mod_vs_exp_comm.png", bbox_inches='tight')
