#!/bin/bash -l 
# The -l above is required to get the full environment with modules

#SBATCH -A 2020-5-543
#SBATCH -J DD2356_PROJECT
#SBATCH -t 00:30:00
#SBATCH --nodes=8
#SBATCH -n 256

#SBATCH -e %J.error
#SBATCH -o %J.output
#SBATCH --mail-type=ALL
#SBATCH --mail-user=adperez@kth.se

ulimit -s unlimited
#------------------------------------------------------------

casename=turbPipe

module swap PrgEnv-cray PrgEnv-intel
module load allinea-forge/20.0.3


echo $casename        >  SESSION.NAME
echo `pwd`'/' >>  SESSION.NAME
rm -f ioinfo
mv $casename.log.$numproc $casename.log1.$numproc
mv $casename.sch $casename.sch1
./run2
sleep 3
