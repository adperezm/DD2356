! Set the number of entries in the array size of "inputs" array
! Then enter that many entries through terminal
! Remeber to create the blank text file "data.txt" in the directory before executing this code
! That is where the output will be saved
! This code gives you standard deviation and prints out to data.txt in required format

PROGRAM standard_dev
IMPLICIT NONE
INTEGER :: i,threads
REAL :: temp_in,mean,dev,dev_sum,std_dev
REAL, DIMENSION(1:5) :: inputs

DO i=1, SIZE(inputs)
    WRITE(*,*) "Enter input"
    READ(*,*) temp_in
    inputs(i)=temp_in
END DO
mean = SUM(inputs)/SIZE(inputs)
WRITE(*,*) "Mean=",mean

dev_sum= 0.0
DO i=1,SIZE(inputs)
    dev =(inputs(i)-mean)**2
    dev_sum = dev_sum + dev
END DO
std_dev = SQRT(dev_sum/SIZE(inputs))

WRITE(*,*) "Std dev=",std_dev
WRITE(*,*) "Enter No. of threads used"
READ(*,*) threads

WRITE(*,*) "Writing data to data.txt file"
OPEN(12,file="data.txt",status="old",position="append",action="write")
WRITE(12,*) threads,mean,std_dev
End PROGRAM
