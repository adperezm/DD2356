#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <math.h>

double mysecond();

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
  double *masses,*force_qk,*t_e;
  
  // Define continous memory arrays
  vect_t *forces, *pos, *old_pos, *vel;
  
  // Define parameters for the timer
  int j,repeat,prt;
  double t1,t2,totaltime,mean,std_dev;
  
  //---------------------     Allocation   ---------------------------------//
  
  // Set the timer
  prt=0;
  repeat=10;
  totaltime=0;
  
    
  // Assign constant values
  n=500;
  X=0;
  Y=1;
  G=6.67408*pow(10,-11);
  delta_t=0.05;
  n_steps=100;
  
  // Allocate space
  masses  = (double*)malloc(n*sizeof(double));
  force_qk = (double*)malloc(2*sizeof(double));
  forces = malloc(n*sizeof(vect_t));
  pos    = malloc(n*sizeof(vect_t));
  old_pos    = malloc(n*sizeof(vect_t));
  vel    = malloc(n*sizeof(vect_t));
  t_e = (double*)malloc(repeat*sizeof(double));
  
  //---------------------   Initialization ---------------------------------//
  
  /*
  //Pos of first particle (Me)
  pos[0][X]=0;
  pos[0][Y]=6371*1000;
  old_pos[0][X]=0;
  old_pos[0][Y]=6371*1000;
  masses[0]=90;
  
  //Pos of second particle (Earth)
  pos[1][X]=0;
  pos[1][Y]=0;
  old_pos[1][X]=0;
  old_pos[1][Y]=0;
  masses[1]=5.972*pow(10,24);
  */
  
  
  for (q=0;q<n;q++) {
	pos[q][X] = (rand() / (double)(RAND_MAX)) * 2 - 1;
	pos[q][Y] = (rand() / (double)(RAND_MAX)) * 2 - 1;

	old_pos[q][X] = pos[q][X];
	old_pos[q][Y] = pos[q][Y];

	vel[q][X] = (rand() / (double)(RAND_MAX)) * 2 - 1;
	vel[q][Y] = (rand() / (double)(RAND_MAX)) * 2 - 1;

	masses[q] = fabs((rand() / (double)(RAND_MAX)) * 2 - 1);
  }

  
  //------------ Run without timer to avoid cold start ---------------------//
  
  for (step = 1; step <= n_steps; step++) {
      // Option 1
      // Compute total force on each q
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
      //printf("Info on particle =%d\n", q+1); 
      //printf("Force in x= %f N, force in y= %f N\n", forces[q][X], forces[q][Y]);  
      }   
   
      // Option 2
      // Make the forces 0
      for (q = 0; q < n; q++) {
        forces[q][X]=0;
        forces[q][Y]=0;
      } 
      // Compute total force on each q
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
        //printf("Info on particle =%d\n", q+1); 
        //printf("Force in x= %f N, force in y= %f N\n", forces[q][X], forces[q][Y]);  
      }
  
      // Compute the position
      for (q = 0; q < n; q++) {
        vel[q][X] += delta_t/masses[q]*forces[q][X]; 
        vel[q][Y] += delta_t/masses[q]*forces[q][Y];
        pos[q][X] += delta_t*vel[q][X]; 
        pos[q][Y] += delta_t*vel[q][Y]; 
    
        if (step==n_steps && j==0 && prt==1){
        printf("Particle =%d after time= %f s \n", q+1, n_steps*delta_t);
        printf("initial pos in x= %f m , initial pos in y= %f m\n", old_pos[q][X], old_pos[q][Y]);
        printf("pos in x= %f m , pos in y= %f m\n", pos[q][X], pos[q][Y]);
        }
    
      }
    }
  
  
  //---------------   Start the outer timer loop ---------------------------//
   
  j=0;
  for (j=0;j<repeat;j++)
  {
    t1 = mysecond();
  
    //---------------------   Solver ---------------------------------//
  
    for (step = 1; step <= n_steps; step++) {
      // Option 1
      // Compute total force on each q
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
      //printf("Info on particle =%d\n", q+1); 
      //printf("Force in x= %f N, force in y= %f N\n", forces[q][X], forces[q][Y]);  
      }   
   
      // Option 2
      // Make the forces 0
      for (q = 0; q < n; q++) {
        forces[q][X]=0;
        forces[q][Y]=0;
      } 
      // Compute total force on each q
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
        //printf("Info on particle =%d\n", q+1); 
        //printf("Force in x= %f N, force in y= %f N\n", forces[q][X], forces[q][Y]);  
      }
  
      // Compute the position
      for (q = 0; q < n; q++) {
        vel[q][X] += delta_t/masses[q]*forces[q][X]; 
        vel[q][Y] += delta_t/masses[q]*forces[q][Y];
        pos[q][X] += delta_t*vel[q][X]; 
        pos[q][Y] += delta_t*vel[q][Y]; 
    
        if (step==n_steps && j==0 && prt==1){
        printf("Particle =%d after time= %f s \n", q+1, n_steps*delta_t);
        printf("initial pos in x= %f m , initial pos in y= %f m\n", old_pos[q][X], old_pos[q][Y]);
        printf("pos in x= %f m , pos in y= %f m\n", pos[q][X], pos[q][Y]);
        }
    
      }
    }
    
    // Capture execution time
    t2 = mysecond();
    t_e[j]=t2-t1;
    // Acumulate elapsed time
    totaltime+=t_e[j];
  }
  
  // Calculate the mean
  mean=totaltime/(float)repeat;
  
  for (j=0;j<repeat;j++) {
  printf("Execution time iteration %d: %11.8f s\n", j+1, t_e[j]);
  std_dev += sqrt(pow(t_e[j]-mean,2)/repeat);
  }
  printf("Mean: %11.8f \n", mean);
  printf("Std deviation: %11.8f \n", std_dev);
  
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


