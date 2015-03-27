module utils_spline

  use utils_constants

  private

  public :: splini , spline , splint

  contains

!    
!  Calculate 2nd derivatives of cubic spline interp function
!  Adapted from numerical recipes by press et al
!    
    subroutine spline(x,y,yp1,ypn,y2)
      implicit none
!    
      integer , parameter :: nmax = 100
!    
      ! Arrays of tabulated function in ascending order by x with y = f(x)
      real(dp) , dimension(:) , intent(in)  :: x , y
      ! Specified derivatives at x(1) and x(n)
      ! Values > 1E30 signals second derivative zero
      real(dp) , intent(in) :: yp1 , ypn
      ! Output array of second derivatives
      real(dp) , dimension(:) , intent(out) :: y2
!    
      integer :: n , i , k
      real(dp) :: p , qn , sig , un
      real(dp) , dimension(nmax) :: u

      n = size(x,1)
      if ( yp1 > 0.99E30_r8 ) then
        y2(1) = d_0
        u(1) = d_0
      else
        y2(1) = -d_half
        u(1) = (d_3/(x(2)-x(1)))*((y(2)-y(1))/(x(2)-x(1))-yp1)
      end if
      do i = 2 , n - 1
        sig = (x(i)-x(i-1))/(x(i+1)-x(i-1))
        p = sig*y2(i-1) + d_2
        y2(i) = (sig-d_1)/p
        u(i) = (d_6*((y(i+1)-y(i))/(x(i+1)-x(i))- &
                     (y(i)-y(i-1))/(x(i)-x(i-1))) / &
                     (x(i+1)-x(i-1))-sig*u(i-1))/p
      end do
      if ( ypn > .99E30_r8 ) then
        qn = d_0
        un = d_0
      else
        qn = d_half
        un = (d_3/(x(n)-x(n-1)))*(ypn-(y(n)-y(n-1))/(x(n)-x(n-1)))
      end if
      y2(n) = (un-qn*u(n-1))/(qn*y2(n-1)+d_1)
      do k = n - 1 , 1 , -1
        y2(k) = y2(k)*y2(k+1) + u(k)
      end do
    end subroutine spline
!
!   Integrate cubic spline function from xa(1) to x
!
    subroutine splini(xa,ya,y2a,x,yi)
      implicit none
!
      ! Arrays of tabulated function in ascending order by xa with ya = f(xa)
      real(dp) , dimension(:) , intent(in) :: xa , ya
      ! Array of second derivatives
      real(dp) , dimension(:) , intent(in) :: y2a
      ! Ascissa endpoint of integration
      real(dp) , intent(in) :: x
      ! Output value
      real(dp) , intent(out) :: yi
!
      real(dp) :: a , a2 , b , b2 , h , xx
      integer :: n , khi , klo
!
      n = size(xa,1)
      yi = d_0
      klo = 1
      khi = 2
      do while ( x > xa(klo) .and. khi <= n )
        xx = x
        if ( khi<n ) xx = dmin1(x,xa(khi))
        h = xa(khi) - xa(klo)
        a = (xa(khi)-xx)/h
        b = (xx-xa(klo))/h
        a2 = a*a
        b2 = b*b
        yi = yi + ((d_1-a2)*ya(klo)/d_2+b2*ya(khi)/d_2+ &
                   ((-(d_1+a2*a2)/d_4+a2/d_2)*y2a(klo)+ &
                   (b2*b2/d_4-b2/d_2)*y2a(khi))*h*h/d_6)*h
        klo = klo + 1
        khi = khi + 1
      end do
    end subroutine splini
!
!   Calculate cubic spline interp value
!   Adapted from numerical recipes by press et al.
!
    subroutine splint(xa,ya,y2a,x,y)
      implicit none
!
      ! Arrays of tabulated function values in ascending xa order
      real(dp) , dimension(:) , intent(in) :: xa , ya
      ! Arrays of second derivatives 
      real(dp) , dimension(:) , intent(in) :: y2a
      ! Abscissa of interpolation
      real(dp) , intent(in) :: x
      ! Output value
      real(dp) , intent(out) :: y
!
      real(dp) :: a , b , h
      integer :: n , k , khi , klo
!
      n = size(xa,1)
      klo = 1
      khi = n
      do while ( khi-klo > 1 )
        k = (khi+klo)/2
        if ( xa(k)>x ) then
          khi = k
        else
          klo = k
        end if
      end do
      h = xa(khi) - xa(klo)
      if ( h==0 ) then
        y = 1.0E-30_r8
        return
      end if
      a = (xa(khi)-x)/h
      b = (x-xa(klo))/h
      y = a*ya(klo) + b*ya(khi) + ((a*a*a-a)*y2a(klo) + &
                                   (b*b*b-b)*y2a(khi))*h*h/d_6
    end subroutine splint

end module utils_spline
