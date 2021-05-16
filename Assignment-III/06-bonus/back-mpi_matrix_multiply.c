#include <stdlib.h>
#include <stdio.h>
#include <math.h>
#include <mpi.h>
#include <stdbool.h>

/*
	The work done here was acomplished thanks to examples seen from 
	www.rookiehpc.com
	
	Possible places where bugs can be found:
		Where the broadcast is made. If two rolls are done, then probable mistakes
		
	In laptop compile with:
	mpicc mpi_matrix_multiply.c -lm
	to debug, use:
	mpicc -DDEBUG mpi_matrix_multiply.c -lm
*/
 
#define TRIALS 10 
#define MSIZE 1024

// Define original matrix
double matrix_a[MSIZE][MSIZE];
double matrix_b[MSIZE][MSIZE];
double matrix_c[MSIZE][MSIZE];

// Create a function to allocate 2d arrays
double **alloc_2d_array(int rows, int cols) {
  int i;
  double *data = (double *)malloc(rows*cols*sizeof(double));
  double **array= (double **)malloc(rows*sizeof(double*));
  for (i=0; i<rows; i++)
    array[i] = &(data[cols*i]);

  return array;
}

int main(int argc, char* argv[]){
  
    //Variables for MPI initialization
    int rank, size, provided;
    
    int i, j, k ;
    int rankprint=0;
    
    for (i = 0 ; i < MSIZE ; i++) {
      for (j = 0 ; j < MSIZE ; j++) {
        matrix_a[i][j] = (double) rand() / RAND_MAX;
        matrix_b[i][j] = (double) rand() / RAND_MAX;
        matrix_c[i][j] = 0.0;
      }
    } 
    
    // =====================Set Up Communications============================
        
    //Initialize mpi
    MPI_Init_thread(&argc, &argv, MPI_THREAD_SINGLE, &provided);

    //Variables for the timer
    double start_time, stop_time, elapsed_time;
    start_time = MPI_Wtime();

    //Call useful functions
    MPI_Comm_size(MPI_COMM_WORLD, &size);
    MPI_Comm_rank(MPI_COMM_WORLD, &rank);
    
    // Ask MPI to decompose our processes in a 2D cartesian grid
    int dims[2] = {0, 0}; // 0 means that there is no restriction. MPI will fit all the ranks as best as it can
    MPI_Dims_create(size, 2, dims);
 
    // Make both dimensions periodic
    int periods[2] = {true, true}; // Periodic dimensions are neighbours.
    
    // Let MPI assign arbitrary ranks if it deems it necessary
    int reorder = false; // Reorder to better maach arquitecture. DONT USE FOR THIS IMPLEMENTATION
 
    // Create a communicator given the 2D torus topology.
    MPI_Comm cartesian_communicator;
    MPI_Cart_create(MPI_COMM_WORLD, 2, dims, periods, reorder, &cartesian_communicator);
 
    // My rank in the cartesian communicator communicator
    int cart_rank;
    MPI_Comm_rank(cartesian_communicator, &cart_rank);
 
    // Get my coordinates in the cartesian communicator
    int cart_coords[2];
    MPI_Cart_coords(cartesian_communicator, cart_rank, 2, cart_coords);
 
#ifdef DEBUG
    
    if (rank==rankprint){
    printf("============================================\n");
    //Print my location in the 2D torus.
    printf("[MPI process %d] I am located at (%d, %d).\n", cart_rank, cart_coords[0],cart_coords[1]);
    printf("============================================\n");
    }
#endif  
    
    // Find the neighbours of each rank
    // Declare neighbours	
    enum DIRECTIONS {DOWN, UP, LEFT, RIGHT};
    char* neighbours_names[4] = {"down", "up", "left", "right"};
    int neighbours_ranks[4];
 
    // shift tells us our up and down neighbours
    MPI_Cart_shift(cartesian_communicator, 0, 1, &neighbours_ranks[UP], &neighbours_ranks[DOWN]);
 
    // shift tells us our left and right neighbours
    MPI_Cart_shift(cartesian_communicator, 1, 1, &neighbours_ranks[LEFT], &neighbours_ranks[RIGHT]);

#ifdef DEBUG
    if (rank==rankprint){
    printf("============================================\n");
    //Print some information regarding the neighbours.
      for(int i = 0; i < 4; i++)
      {
          if(neighbours_ranks[i] == MPI_PROC_NULL)
              printf("[MPI process %d] I have no %s neighbour.\n", cart_rank, neighbours_names[i]);
          else
              printf("[MPI process %d] I have a %s neighbour: process %d.\n", cart_rank, neighbours_names[i], neighbours_ranks[i]);
      }
    printf("============================================\n");
    }
#endif  
    
    // Partition the 2D cartesian topology along the first dimension, by preserving the second dimension
    int remain_dims[2] = {false, true};
    MPI_Comm subgrid_communicator;
    MPI_Cart_sub(cartesian_communicator, remain_dims, &subgrid_communicator);
  
    // My rank in the subgrid communicator
    int sub_rank;
    MPI_Comm_rank(subgrid_communicator, &sub_rank);
    
#ifdef DEBUG
    if (rank==rankprint){
    printf("============================================\n");
    printf("My original rank is %d, but I am rank %d in the subgrid \n",rank,sub_rank);
    printf("============================================\n");
    }
#endif 	    
 
    // ===================== Implement the Algorithm ========================
 
    //Create local matrices to divide
    int Lsize=MSIZE/sqrt(size);
    // How many rows and columns in each tile
    int r = Lsize;
    int c = Lsize;
    // Allocate space for the tiles and comm buffers 
    double **A, **Atemp, **B, **Btemp, **C;
    A= alloc_2d_array(Lsize, Lsize);
    Atemp= alloc_2d_array(Lsize, Lsize);
    B= alloc_2d_array(Lsize, Lsize);
    Btemp= alloc_2d_array(Lsize, Lsize);
    C= alloc_2d_array(Lsize, Lsize);
    
    // Perform the domain decomposition - Copy entries from the global to local. 
    for (i = 0; i <  r; i++)
      for (j = 0; j < c; j++)
        A[i][j] = matrix_a[i+cart_coords[0]*Lsize][j+cart_coords[1]*Lsize]; //
        
    for (i = 0; i <  r; i++)
      for (j = 0; j < c; j++)
        B[i][j] = matrix_b[i+cart_coords[0]*Lsize][j+cart_coords[1]*Lsize]; // 
        
    for (i = 0; i <  r; i++)
      for (j = 0; j < c; j++)
        C[i][j] = matrix_c[i+cart_coords[0]*Lsize][j+cart_coords[1]*Lsize]; // 
        
  	
  	//Follow the Fox algorithm
       int totaliterations=sqrt(size);
       for (int it=0;it<totaliterations;it++){
      
       // First copy A before broadcasting. So you dont overwrite it. 
       for (i = 0; i <  r; i++)
         for (j = 0; j < c; j++)
           Atemp[i][j] = A[i][j]; //
        
       // broadcast the diagonal+it      	
	int broadcast_root=cart_coords[0]+it;
  	//If the entry is over number of horizontal tiles (squareroot(size))-1 since the rank start at 0. Then start from 0.
  	if (broadcast_root>(int)sqrt(size)-1){
  	broadcast_root=cart_coords[0]+it-(int)sqrt(size);
  	}
  	//Perform the broadcast
  	MPI_Bcast(&Atemp[0][0], Lsize*Lsize, MPI_DOUBLE, broadcast_root, subgrid_communicator);

	//Do the matrix multiply for the tile
  	for (i = 0 ; i < Lsize ; i++) {
    	  for (j = 0 ; j < Lsize ; j++) {
      	    for (k = 0 ; k < Lsize ; k++) {
              C[i][j] += Atemp[i][k] * B[k][j];
      	    }
    	  }
  	}
  	
  	//Now Roll B.
  	//send B up recieve down
    	MPI_Sendrecv(&B[0][0], Lsize*Lsize, MPI_DOUBLE, neighbours_ranks[UP], 0, &Btemp[0][0], Lsize*Lsize, MPI_DOUBLE, neighbours_ranks[DOWN], MPI_ANY_TAG, MPI_COMM_WORLD,MPI_STATUS_IGNORE);
   	
  	//Update the recieved value in preparation from the next iteration
	for (i = 0; i <  r; i++)
         for (j = 0; j < c; j++)
           B[i][j] = Btemp[i][j]; 
  	}
  	
  	
  	
  // ===================== Print and validate results ========================

  
  //Calculate a global average of each tile
  double  ave = 0.0;
  for (i = 0 ; i < Lsize ; i++) {
    for (j = 0 ; j < Lsize ; j++) {
      ave += C[i][j]/(double)(MSIZE*MSIZE);
    }
  }
  
  //Communicate the results and perform reduction
  double reduction_result = 0;
  int root_rank=rankprint;
  MPI_Reduce(&ave, &reduction_result, 1, MPI_DOUBLE, MPI_SUM, root_rank, MPI_COMM_WORLD);
  
  int row, columns;
  //Pint the matrix
  if (rank==rankprint){
  	
  printf("average = %8.6f \n", reduction_result);
  
       /*
 
 	printf("a\n"); 
 	
	for (row=0; row<MSIZE; row++)
	{
   	 for(columns=0; columns<MSIZE; columns++)
    	{
       	  printf("%f     ", matrix_a[row][columns]);
   	 }
    	printf("\n");
	}
	
	printf("b\n");
	
	for (row=0; row<MSIZE; row++)
	{
   	 for(columns=0; columns<MSIZE; columns++)
    	{
       	  printf("%f     ", matrix_b[row][columns]);
   	 }
    	printf("\n");
	}
	

	printf("B\n");

	for (row=0; row<Lsize; row++)
	{
    		for(columns=0; columns<Lsize; columns++)
    		{
       	 	 printf("%f     ", B[row][columns]);
    		}
    	printf("\n");
	}
	
	*/
	/*
	printf("C\n");
	
	for (row=0; row<Lsize; row++)
	{
    		for(columns=0; columns<Lsize; columns++)
    		{
       	 	 printf("%f     ", C[row][columns]);
    		}
    	printf("\n");
	}
	*/
	stop_time = MPI_Wtime();
	elapsed_time = stop_time - start_time;
    	
    	printf("It took %f seconds\n", elapsed_time);


  }
  
  //double  ave = 0.0;
  //for (i = 0 ; i < MSIZE ; i++) {
  //  for (j = 0 ; j < MSIZE ; j++) {
  //    ave += matrix_c[i][j]/(double)(MSIZE*MSIZE);
  //  }
  //}
  //printf("Sum = %8.6f \n", ave);     
  //printf("time = %f\n", (t2 - t1));7
  
  //if(rank==0){
  //printf("Sum = %8.6f \n", matrix_a[0][1]);
  //}
  
      MPI_Finalize();

  return 0;
}
