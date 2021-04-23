#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>
#include <omp.h>

/*
 * Use the models to calculate the times 
 *
 */


int main(int argc, char *argv[])
{
    // define integers
    int i,size,n;
    
    // define variables
    double *x;
    double serial_sum_x,omp_sum_x,serial_el,omp_el,omp_crit_sum_x,omp_crit_el;
    double sum_val,t1,t2;
     
    // Allocate space
    size=100000000;
    n=4; // number of threads
    x  = (double*)malloc(size*sizeof(double));
    
    
    // Check openmp is working
	omp_set_num_threads(n);
	#pragma omp parallel
	{
		int X=omp_get_thread_num();
		printf("Thread %d is active \n", X);
	}
    
    
    // Initialize the vector
    for (size_t i = 0; i < size; i++) {
      x[i] = rand() / (double)(RAND_MAX);
    }
    
    //Calculate the serial sum
    sum_val = 0.0;
    t1=omp_get_wtime();
    for (i = 0; i < size; i++) {
      sum_val += x[i];
    }
    t2=omp_get_wtime();

    serial_sum_x=sum_val;
    serial_el=t2-t1;
    
    
    //Calculate the parallel sum 
    sum_val = 0.0;

    t1=omp_get_wtime();
    #pragma omp parallel for
    for (i = 0; i < size; i++) {
      sum_val += x[i];
    }
    t2=omp_get_wtime();
    omp_sum_x=sum_val;
    omp_el=t2-t1;
    
    //Calculate the parallel sum with critical 
    sum_val = 0.0;

    t1=omp_get_wtime();
    #pragma omp parallel for
    for (i = 0; i < size; i++) {
      #pragma omp critical
      {
      sum_val += x[i];
      }
    }
    t2=omp_get_wtime();
    omp_crit_sum_x=sum_val;
    omp_crit_el=t2-t1;
    
    

       printf("serial sum= %f, time= %f \n", serial_sum_x, serial_el);
       printf("omp sum= %f, time= %f \n", omp_sum_x,omp_el);
       printf("omp sum with critical region = %f, time= %f \n", omp_crit_sum_x,omp_crit_el);
    return 0;
}
