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
    int i,size,nc,padsize;
    int mt;
    
    // define variables
    double *x;
    double serial_sum_x,omp_sum_x,serial_el,omp_el,omp_crit_sum_x,omp_crit_el;
    double omp_loc_sum_x,omp_loc_el,omp_loc_padded_sum_x,omp_loc_padded_el;
    double sum_val,t1,t2;
    double *local_sum;
    double *local_sum_padded;
    
    
    
    
    
    //omp terms
    nc=4; // number of threads
    omp_set_num_threads(n);
    mt=omp_get_max_threads();
    
     
    // Allocate space
    size=pow(10,7);
    padsize=32;
    x  = (double*)malloc(size*sizeof(double));
    local_sum  = (double*)malloc(mt*sizeof(double));
    local_sum_padded  = (double*)malloc(mt*padsize*sizeof(double));
    
    
    
    printf("mt= %d \n",mt );
    
    
    // Check openmp is working
	
    #pragma omp parallel
    {
    	int X=omp_get_thread_num();
  	printf("Thread %d is active \n", X);
    }
    
    
    // Initialize the vector
    for (size_t i = 0; i < size; i++) {
      x[i] = rand() / (double)(RAND_MAX);
    }
    
    for (i = 0; i < mt*padsize; i++) {
      local_sum[i] = 0;
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
    //#pragma omp paralell for reduction(+:sum_val)
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
    
    
    
    
    //Calculate the parallel sum with local 
    sum_val = 0.0;

    t1=omp_get_wtime();
    #pragma omp parallel shared(local_sum)
    {
      int id=omp_get_thread_num(); //IMPORTANT! declare id inside the paralell region, 
                                   //so each thread has a copy, otherwise it is also shared.
      local_sum[id]=0;
      #pragma omp for
        for (i = 0; i < size; i++) {
          local_sum[id] += x[i];
        }
     }
      // sum the local values in serial
    for (i = 0; i < mt; i++) {
      sum_val += local_sum[i];
    }
    t2=omp_get_wtime();
    omp_loc_sum_x=sum_val;
    omp_loc_el=t2-t1;
    
    
    //Calculate the parallel sum with local and padding
    sum_val = 0.0;

    t1=omp_get_wtime();
    #pragma omp parallel shared(local_sum)
    {
      int id=omp_get_thread_num(); //IMPORTANT! declare id inside the paralell region, 
                                   //so each thread has a copy, otherwise it is also shared.
      local_sum_padded[id*padsize]=0;
      #pragma omp for
        for (i = 0; i < size; i++) {
          local_sum_padded[id*padsize] += x[i];
        }
     }
      // sum the local values in serial
    for (i = 0; i < mt*padsize; i=i+padsize) {
      sum_val += local_sum_padded[i];
    }
    t2=omp_get_wtime();
    omp_loc_padded_sum_x=sum_val;
    omp_loc_padded_el=t2-t1;







    printf("serial sum= %f, time= %f \n", serial_sum_x, serial_el);
    printf("omp sum= %f, time= %f \n", omp_sum_x,omp_el);
    printf("omp sum with critical region = %f, time= %f \n", omp_crit_sum_x,omp_crit_el);
    printf("omp sum with local sum = %f, time= %f \n", omp_loc_sum_x,omp_loc_el);
    printf("omp sum with local padded sum = %f, time= %f \n", omp_loc_padded_sum_x,omp_loc_padded_el);
    return 0;
}
