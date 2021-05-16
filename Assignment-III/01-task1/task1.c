#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>
#include <mpi.h>

/*
 * On a laptop:
 * to compile this program use: mpicc task1.c 
 * to run this program use:     mpirun -n 4 ./a.out 
 *
 */
int main(int argc, char *argv[])
{

	// Define the variables
	int rank, size, provided;
	//rank=4;
	//printf("Hello World from rank %d \n", n);

	MPI_Init_thread(&argc,&argv,MPI_THREAD_SINGLE,&provided);
	MPI_Comm_size(MPI_COMM_WORLD,&size);
	MPI_Comm_rank(MPI_COMM_WORLD,&rank);
	
	printf("Hello World from rank %d out of %d \n", rank,size);
	
	MPI_Finalize();
	
	
	printf("=========================== \n");
	printf("It was compiled with mpicc \n")
	printf("It was run with mpirun -n <processes>... In beskow use srun instead.  \n")	
	printf("The most udes implementations are MPICH and OpenMPI  \n")
		
   return 0; 
}
