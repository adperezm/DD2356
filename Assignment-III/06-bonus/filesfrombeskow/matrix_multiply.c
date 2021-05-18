#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <sys/time.h>
 
#define TRIALS 10 
#define MSIZE 2160

double matrix_a[MSIZE][MSIZE];
double matrix_b[MSIZE][MSIZE];
double matrix_c[MSIZE][MSIZE];
 
double mysecond(){
  struct timeval tp;
  struct timezone tzp;
  int i;

  i = gettimeofday(&tp,&tzp);
  return ( (double) tp.tv_sec + (double) tp.tv_usec * 1.e-6 );
}

int main(int argc, char* argv[]){
  
  double t1, t2;
  int i, j, k ;
  
  for (i = 0 ; i < MSIZE ; i++) {
    for (j = 0 ; j < MSIZE ; j++) {
      matrix_a[i][j] = (double) rand() / RAND_MAX;
      matrix_b[i][j] = (double) rand() / RAND_MAX;
      matrix_c[i][j] = 0.0;
    }
  }    
  
  t1 = mysecond();
  for (i = 0 ; i < MSIZE ; i++) {
    for (j = 0 ; j < MSIZE ; j++) {
      for (k = 0 ; k < MSIZE ; k++) {
        matrix_c[i][j] += matrix_a[i][k] * matrix_b[k][j];
      }
    }
  }
  t2 = mysecond();    
  
  double  ave = 0.0;
  for (i = 0 ; i < MSIZE ; i++) {
    for (j = 0 ; j < MSIZE ; j++) {
      ave += matrix_c[i][j]/(double)(MSIZE*MSIZE);
    }
  }
  printf("average = %8.6f \n", ave);     
  printf("Execution time = %f\n", (t2 - t1));
  /*
 	int row,columns;
 
 	printf("C\n"); 
 	
	for (row=0; row<MSIZE; row++)
	{
   	 for(columns=0; columns<MSIZE; columns++)
    	{
       	  printf("%f     ", matrix_c[row][columns]);
   	 }
    	printf("\n");
	}
*/
  return 0;
}
