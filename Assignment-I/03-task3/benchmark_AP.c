#define N 50000
#include <stdio.h>
#include <sys/time.h>

double mysecond();

int main(){
  int i, j, repeat;
  double t1, t2, totaltime; // timers                                                         
  double a[N], b[N], c[N]; // arrays  
                                             
  // init arrays                                                                   
  for (i = 0; i < N; i++){
    a[i] = 47.0;
    b[i] = 3.1415;
  }
  
  // Run a loop to avoid cold start
  for(i = 0; i < N; i++)
    c[i] = a[i]*b[i];


  // Repeat the loop some times to avoid granularity
  // Report the total time divided by the nomber of iterations 
  totaltime=0;
  repeat=10;

  for (j=0;j<repeat;j++)
  {
          // measure performance                                                           
          t1 = mysecond();
          for(i = 0; i < N; i++)
            c[i] = a[i]*b[i];
          t2 = mysecond();
  	  printf("Execution time iteration %d: %11.8f s\n", j+1, (t2 - t1));
	  // Acumulate elapsed time
	  totaltime+=(t2-t1);
  }

  printf("Average: %11.8f \n", totaltime/(float)repeat);
  // Use the c variable to trick the compiler
  printf("Array value: %11.8f s \n", c[1]);

  return 0;
}

// function with timer                                                             
double mysecond(){
  struct timeval tp;
  struct timezone tzp;
  int i;

  i = gettimeofday(&tp,&tzp);
  return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
}
