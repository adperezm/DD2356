#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

/*
 * Use the models to calculate the times 
 *
 */
int main(int argc, char *argv[])
{
    
    double *nrows, *nnz, *mTime;
    double c,ct,bw;
    int    i;
    
    /* Clock Speed in Hz */
    c=3.9*pow(10,9);
    ct=1/c;
    
    
    nrows  = (double*)malloc(4*sizeof(double));
    nnz    = (double*)malloc(4*sizeof(double));
    mTime  = (double*)malloc(4*sizeof(double));
    
    nrows[1]=pow(10,2);
    nrows[2]=pow(10,4);
    nrows[3]=pow(10,6);
    nrows[4]=pow(10,8);
    
    /* Fill the models with the results */

    for (i=0; i<=4; i++) {
	nnz[i]   = 5*nrows[i];
	mTime[i] = nnz[i]*2*ct;	
    }
    
    bw=sizeof(double);
    
    printf("Given CLock Speed [Hz] = %f\n", c);
    printf("Modelled Time, nrows=%f, nnz=%f, T = %f\n", nrows[1], nnz[1], mTime[1]);
    printf("Modelled Time, nrows=%f, nnz=%f, T = %f\n", nrows[2], nnz[2], mTime[2]);
    printf("Modelled Time, nrows=%f, nnz=%f, T = %f\n", nrows[3], nnz[3], mTime[3]);
    printf("Modelled Time, nrows=%f, nnz=%f, T = %f\n", nrows[4], nnz[4], mTime[4]);
    free(nrows); free(nnz); free(mTime); 
    return 0;
}
