#!/bin/bash -l 
# The -l above is required to get the full environment with modules


casename=turbPipe
numproc=64
echo $casename        >  SESSION.NAME
echo `pwd`'/' >>  SESSION.NAME

