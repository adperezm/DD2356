c-----------------------------------------------------------------------
      subroutine exact(uu,vv,xx,yy,n,time,visc,u0,v0)
c
c     This routine creates initial conditions for an exact solution
c     to the Navier-Stokes equations based on the paper of Walsh,
c     with an additional translational velocity (u0,v0).
c     
c     The computational domain is [0,2pi]^2 with doubly-periodic 
c     boundary conditions.
c
c
      include 'SIZE'
      include 'INPUT'
c
      real uu(n),vv(n),xx(n),yy(n)
c
      real cpsi(2,5), a(2,5)
      save cpsi     , a

c     data a / .4,.45 , .4,.2 , -.2,-.1 , .2,.05, -.09,-.1 / ! See eddy.m
c     data cpsi / 0,65 , 16,63 , 25,60 , 33,56 , 39,52 /     ! See squares.f
c     data cpsi / 0,85 , 13,84 , 36,77 , 40,75 , 51,68 /


c     This data from Walsh's Figure 1 [1]:

      data a / -.2,-.2, .25,0.,   0,0  ,  0,0  ,  0,0  /
      data cpsi / 0, 5 ,  3, 4 ,  0,0  ,  0,0  ,  0,0  /

      one   = 1.
      pi    = 4.*atan(one)

      aa    = cpsi(2,1)**2
      arg   = -visc*time*aa  ! domain is [0:2pi]
      e     = exp(arg)
c
c     ux = psi_y,  uy = -psi_x
c
      do i=1,n
         x = xx(i) - u0*time
         y = yy(i) - v0*time

         sx = sin(cpsi(2,1)*x)
         cx = cos(cpsi(2,1)*x)
         sy = sin(cpsi(2,1)*y)
         cy = cos(cpsi(2,1)*y)
         u  =  a(1,1)*cpsi(2,1)*cy 
         v  =  a(2,1)*cpsi(2,1)*sx

         do k=2,5
            s1x = sin(cpsi(1,k)*x)
            c1x = cos(cpsi(1,k)*x)
            s2x = sin(cpsi(2,k)*x)
            c2x = cos(cpsi(2,k)*x)

            s1y = sin(cpsi(1,k)*y)
            c1y = cos(cpsi(1,k)*y)
            s2y = sin(cpsi(2,k)*y)
            c2y = cos(cpsi(2,k)*y)
            
            c1  = cpsi(1,k)
            c2  = cpsi(2,k)

            if (k.eq.2) u = u + a(1,k)*s1x*c2y*c2
            if (k.eq.2) v = v - a(1,k)*c1x*s2y*c1
            if (k.eq.2) u = u - a(2,k)*s2x*c1y*c1
            if (k.eq.2) v = v + a(2,k)*c2x*s1y*c2

            if (k.eq.3) u = u - a(1,k)*s1x*c2y*c2
            if (k.eq.3) v = v + a(1,k)*c1x*s2y*c1
            if (k.eq.3) u = u - a(2,k)*c2x*c1y*c1
            if (k.eq.3) v = v - a(2,k)*s2x*s1y*c2

            if (k.eq.4) u = u + a(1,k)*c1x*c2y*c2
            if (k.eq.4) v = v + a(1,k)*s1x*s2y*c1
            if (k.eq.4) u = u + a(2,k)*c2x*c1y*c1
            if (k.eq.4) v = v + a(2,k)*s2x*s1y*c2

            if (k.eq.5) u = u - a(1,k)*s1x*c2y*c2
            if (k.eq.5) v = v + a(1,k)*c1x*s2y*c1
            if (k.eq.5) u = u - a(2,k)*s2x*c1y*c1
            if (k.eq.5) v = v + a(2,k)*c2x*s1y*c2
         enddo
         uu(i) = u*e + u0
         vv(i) = v*e + v0
      enddo

      return
      end
c-----------------------------------------------------------------------
      subroutine exactp(pe,x2,y2,n2,time,visc,u0,v0)

c     This routine, complementary to the exact routine above, returns
c     the exact pressure, given the pressure counterpart to the
c     arguments for the exact routine i.e., xx -> x2, yy -> y2, n -> n2
c
c     Brandon E. Merrill, Yulia T. Peet, Paul F. Fischer, and
c     James W. Lottes. "A Spectrally Accurate Method for Overlapping
c     Grid Solution of Incompressible Navier-Stokes Equations." Journal
c     of Computational Physics 307 (2016), 60--93.

      real x2(n2),y2(n2),pe(n2)

      e = exp(-50*time*visc)

      do i=1,n2
         x = x2(i) - u0*time
         y = y2(i) - v0*time

         pe(i) = (1.0/64.0)*e*(16*cos(6*x) + 8*cos(8*x-4*y)
     $         - 32*cos(2*(x-2*y)) + 9*cos(8*y) - 8*cos(4*(2*x+y))
     $         + 32*cos(2*(x+2*y)) - 4*sin(3*(x-3*y)) + 32*sin(5*(x-y))
     $         + 36*sin(3*x-y) - 32*sin(5*(x+y)) + 36*sin(3*x+y)
     $         - 4*sin(3*(x+3*y)))
      enddo

      call ortho(pe)

      return
      end
c-----------------------------------------------------------------------
      subroutine uservp (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
C
      udiff =0.
      utrans=0.
      return
      end
c-----------------------------------------------------------------------
      subroutine userf  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
C
      ffx = 0.0
      ffy = 0.0
      ffz = 0.0
      return
      end
c-----------------------------------------------------------------------
      subroutine userq  (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
C
      qvol   = 0.0
      source = 0.0
      return
      end
c-----------------------------------------------------------------------
      subroutine userchk
      include 'SIZE'  
      include 'TOTAL' 
c
      common /exacu/ ue(lx1,ly1,lz1,lelt),ve(lx1,ly1,lz1,lelt)
      common /exacp/ pe(lx2,ly2,lz2,lelt)
      common /exacd/ ud(lx1,ly1,lz1,lelt),vd(lx1,ly1,lz1,lelt)
     $              ,pd(lx2,ly2,lz2,lelt)

      ifield = 1  ! for outpost

      n    = nx1*ny1*nz1*nelv
      n2   = nx2*ny2*nz2*nelv
      visc = param(2)
      u0   = param(96)
      v0   = param(97)

      call exact  (ue,ve,xm1,ym1,n,time,visc,u0,v0)
      call exactp (pe,xm2,ym2,n2,time,visc,u0,v0)

      if (istep.eq.0) call outpost(ue,ve,vx,pe,t,'   ')

      call sub3   (ud,ue,vx,n)
      call sub3   (vd,ve,vy,n)
      call sub3   (pd,pe,pr,n2)

      if (istep.eq.nsteps) call outpost(ud,vd,vx,pd,t,'err')

      umx = glamax(vx,n)
      vmx = glamax(vy,n)
      pmx = glamax(pr,n2)
      uex = glamax(ue,n)
      vex = glamax(ve,n)
      pex = glamax(pe,n2)
      udx = glamax(ud,n)
      vdx = glamax(vd,n)
      pdx = glamax(pd,n2)

      if (nid.eq.0) then
         write(6,11) istep,time,udx,umx,uex,u0,'  X err'
         write(6,11) istep,time,vdx,vmx,vex,v0,'  Y err'
         write(6,12) istep,time,pdx,pmx,pex,'                P err'
   11    format(i5,1p5e14.6,a7)
   12    format(i5,1p4e14.6,a21)
      endif

      if (istep.le.5) then        !  Reset velocity & pressure to eliminate
         call copy (vx,ue,n)      !  start-up contributions to
         call copy (vy,ve,n)      !  temporal-accuracy behavior.
         call copy (pr,pe,n2)
      endif

      return
      end
c-----------------------------------------------------------------------
      subroutine userbc (ix,iy,iz,iside,ieg)
c     NOTE ::: This subroutine MAY NOT be called by every process
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'
      ux=0.0
      uy=0.0
      uz=0.0
      temp=0.0
      return
      end
c-----------------------------------------------------------------------
      subroutine useric (ix,iy,iz,ieg)
      include 'SIZE'
      include 'TOTAL'
      include 'NEKUSE'

      common /exacu/ ue(lx1,ly1,lz1,lelt),ve(lx1,ly1,lz1,lelt)
      common /exacp/ pe(lx2,ly2,lz2,lelt)
      common /exacd/ ud(lx1,ly1,lz1,lelt),vd(lx1,ly1,lz1,lelt)
     $              ,pd(lx2,ly2,lz2,lelt)

      integer icalld
      save    icalld
      data    icalld  /0/

      n = nx1*ny1*nz1*nelv
      if (icalld.eq.0) then
         icalld = icalld + 1
         time = 0.
         u0   = param(96)
         v0   = param(97)
         call exact (ue,ve,xm1,ym1,n,time,visc,u0,v0)
      endif

      ie = gllel(ieg)
      ux=ue(ix,iy,iz,ie)
      uy=ve(ix,iy,iz,ie)
      uz=0.0
      temp=0

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat
      include 'SIZE'
      include 'TOTAL'
      integer e

      one   = 1.
      twopi = 8.*atan(one)

      do e=1,nelv   !  Rescale mesh to [0,2pi]^2
      do i=1,4      !  Assumes original domain in .rea file on [0,1]
         xc(i,e) = twopi*xc(i,e)
         yc(i,e) = twopi*yc(i,e)
      enddo 
      enddo 

c     param(66) = 4
c     param(67) = 4

      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat2
      return
      end
c-----------------------------------------------------------------------
      subroutine usrdat3
      return
      end
c-----------------------------------------------------------------------

c automatically added by makenek
      subroutine usrdat0() 

      return
      end

c automatically added by makenek
      subroutine usrsetvert(glo_num,nel,nx,ny,nz) ! to modify glo_num
      integer*8 glo_num(1)

      return
      end

c automatically added by makenek
      subroutine userqtl

      call userqtl_scig

      return
      end
