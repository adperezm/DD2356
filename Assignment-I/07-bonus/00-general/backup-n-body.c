#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>


int main(int argc, char *argv[])
{
  
  
  //------------------ Variable declaration---------------------------------//
    
  #define DIM 2
  typedef double vect_t[DIM];
 
  // Define parameters
  int n,X,Y,q,k,step,n_steps;
  double G,delta_t;
  double x_diff, y_diff, dist, dist_cubed;
  
  // Define vectors
  double *masses,*force_qk;
  
  // Define continous memory arrays
  vect_t *forces, *pos, *vel;
  
  //---------------------     Allocation   ---------------------------------//
    
  // Assign constant values
  n=2;
  X=0;
  Y=1;
  G=6.67408*pow(10,-11);
  delta_t=0.05;
  n_steps=1;
  
  // Allocate space
  masses  = (double*)malloc(n*sizeof(double));
  force_qk = (double*)malloc(2*sizeof(double));
  forces = malloc(n*sizeof(vect_t));
  pos    = malloc(n*sizeof(vect_t));
  vel    = malloc(n*sizeof(vect_t));
  
  //---------------------   Initialization ---------------------------------//
  
  
  //Pos of first particle (Me)
  pos[0][X]=0;
  pos[0][Y]=6371*1000;
  masses[0]=90;
  
  //Pos of second particle (Earth)
  pos[1][X]=0;
  pos[1][Y]=0;
  masses[1]=5.972*pow(10,24);
  
  //---------------------   Solver ---------------------------------//
  
  for (step = 1; step <= n_steps; step++) {
    // Compute total force on each q
    // Option 1
    for (q = 0; q < n; q++) { 
      for (k = 0; k < n; k++)  {
        if ( k!=q ) {
          x_diff = pos[q][X] - pos[k][X]; 
          y_diff = pos[q][Y] - pos[k][Y]; 
          dist = sqrt(x_diff*x_diff+y_diff*y_diff); 
          dist_cubed = dist*dist*dist; 
          forces[q][X] -= G*masses[q]*masses[k]/dist_cubed * x_diff; 
          forces[q][Y] -= G*masses[q]*masses[k]/dist_cubed * y_diff; 
        }
      }
      printf("Info on particle =%d\n", q+1); 
      printf("Force in x= %f N, force in y= %f N\n", forces[q][X], forces[q][Y]);  
    }
  
   
    // Option 2
    for (q = 0; q < n; q++) {
    forces[q][X]=0;
    forces[q][Y]=0;
    } 
    for (q = 0; q < n; q++) { 
      for (k = 0; k < n; k++)  {
        if ( k>q ) {
          x_diff = pos[q][X] - pos[k][X]; 
          y_diff = pos[q][Y] - pos[k][Y]; 
          dist = sqrt(x_diff*x_diff + y_diff*y_diff); 
          dist_cubed = dist*dist*dist; 
          force_qk[X] = -G*masses[q]*masses[k]/dist_cubed * x_diff; // The signs here where the opposite
          force_qk[Y] = -G*masses[q]*masses[k]/dist_cubed * y_diff; // The signs here where the opposite
          forces[q][X] += force_qk[X];  
          forces[q][Y] += force_qk[Y];  
          forces[k][X] -= force_qk[X];  
          forces[k][Y] -= force_qk[Y];  
        }
      }
      printf("Info on particle =%d\n", q+1); 
      printf("Force in x= %f N, force in y= %f N\n", forces[q][X], forces[q][Y]);  
    }
  
    // Compute the position
    for (q = 0; q < n; q++) {
      vel[q][X] += delta_t/masses[q]*forces[q][X]; 
      vel[q][Y] += delta_t/masses[q]*forces[q][Y];
      pos[q][X] += delta_t*vel[q][X]; 
      pos[q][Y] += delta_t*vel[q][Y]; 
    
      if (step==n_steps){
      printf("Particle =%d after time= %f s \n", q+1, n_steps*delta_t);
      printf("pos in x= %f m , pos in y= %f m\n", pos[q][X], pos[q][Y]);
      
      }
    
    }
  }
  
   
  
  
    return 0;
}



