#!/bin/bash -l 
# The -l above is required to get the full environment with modules

#SBATCH -A 2020-5-543
#SBATCH -J adperez-turbpipe-1
#SBATCH -t 01:00:00
#SBATCH --nodes=1
#SBATCH -n 16
#SBATCH --ntasks-per-node=16

#SBATCH -e %J.error
#SBATCH -o %J.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=adperez@kth.se

ulimit -s unlimited
#------------------------------------------------------------

casename=turbPipe
numproc=16

module swap PrgEnv-cray PrgEnv-intel
module load allinea-forge/20.0.3


echo $casename        >  SESSION.NAME
echo `pwd`'/' >>  SESSION.NAME
rm -f ioinfo
mv $casename.log.$numproc $casename.log1.$numproc
mv $casename.sch $casename.sch1
map --profile srun -n $numproc ./nek5000 &> outputs2/ouput_process_16.out
sleep 3
rm -f SESSION.NAME
