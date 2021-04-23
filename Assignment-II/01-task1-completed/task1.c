#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>
#include <omp.h>

/*
 * Use the models to calculate the times 
 *
 */
void main()
{

	// Define the variables
	int n;
	n=4;
	omp_set_num_threads(n);
	#pragma omp parallel
	{
		int X=omp_get_thread_num();
		printf("Hello World from Thread %d \n", X);

	}	
    
}
