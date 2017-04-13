program testgtd7
  use utils_constants
  use physics_msis
  implicit none
!
  real(dp) , dimension(15) :: alt , ap , f107 , f107a , ut , xlat ,     &
                        & xlong , xlst
  real(dp) , dimension(7) :: aph
  real(dp) , dimension(9,16) :: d
  integer :: i , j
  integer , dimension(15) :: iday
  real(dp) , dimension(25) :: sw
  real(dp) , dimension(2,16) :: t
!
!     TEST DRIVER FOR GTD7 (ATMOSPHERIC MODEL)
  data iday/172 , 81 , 13*172/
  data ut/29000. , 29000. , 75000. , 12*29000./
  data alt/400. , 400. , 1000. , 100. , 6*400. , 0 , 10. , 30. ,    &
     & 50. , 70./
  data xlat/4*60. , 0. , 10*60./
  data xlong/5* - 70. , 0. , 9* - 70./
  data xlst/6*16. , 4. , 8*16./
  data f107a/7*150. , 70. , 7*150./
  data f107/8*150. , 180. , 6*150./
  data ap/9*4. , 40. , 5*4./
  data aph/7*100./ , sw/8*1. , -1. , 16*1./
  do i = 1 , 15
    call gtd7(iday(i),ut(i),alt(i),xlat(i),xlong(i),xlst(i),f107a(i)&
            & ,f107(i),ap(i),48,d(:,i),t(:,i))
    write (6,99001) (d(j,i),j=1,9) , t(1,i) , t(2,i) , &
         TLB,S,DB04,DB16,DB28,DB32,DB40,DB48,DB01,ZA,T0,Z0, &
         XG0,RL,DD,DB14
  end do
  call tselec(sw)
  i = 16
  call gtd7(iday(1),ut(1),alt(1),xlat(1),xlong(1),xlst(1),f107a(1), &
          & f107(1),aph,48,d(:,i),t(:,i))
  write (6,99001) (d(j,i),j=1,9) , t(1,i) , t(2,i) , &
         TLB,S,DB04,DB16,DB28,DB32,DB40,DB48,DB01,ZA,T0,Z0, &
         XG0,RL,DD,DB14
  call gtd7(iday(1),ut(1),alt(4),xlat(1),xlong(1),xlst(1),f107a(1), &
          & f107(1),aph,48,d(:,i),t(:,i))
  write (6,99001) (d(j,i),j=1,9) , t(1,i) , t(2,i) , &
         TLB,S,DB04,DB16,DB28,DB32,DB40,DB48,DB01,ZA,T0,Z0, &
         XG0,RL,DD,DB14
  write (6,99022) chname , isdate , istime
  write (6,99002) (iday(i),i=1,5)
  write (6,99003) (ut(i),i=1,5)
  write (6,99004) (alt(i),i=1,5)
  write (6,99005) (xlat(i),i=1,5)
  write (6,99006) (xlong(i),i=1,5)
  write (6,99007) (xlst(i),i=1,5)
  write (6,99008) (f107a(i),i=1,5)
  write (6,99009) (f107(i),i=1,5)
  write (6,99010) (ap(i),i=1,5)
  write (6,99011) (t(1,i),i=1,5)
  write (6,99012) (t(2,i),i=1,5)
  write (6,99013) (d(1,i),i=1,5)
  write (6,99014) (d(2,i),i=1,5)
  write (6,99015) (d(3,i),i=1,5)
  write (6,99016) (d(4,i),i=1,5)
  write (6,99017) (d(5,i),i=1,5)
  write (6,99018) (d(7,i),i=1,5)
  write (6,99019) (d(8,i),i=1,5)
  write (6,99020) (d(9,i),i=1,5)
  write (6,99021) (d(6,i),i=1,5)
  write (6,99002) (iday(i),i=6,10)
  write (6,99003) (ut(i),i=6,10)
  write (6,99004) (alt(i),i=6,10)
  write (6,99005) (xlat(i),i=6,10)
  write (6,99006) (xlong(i),i=6,10)
  write (6,99007) (xlst(i),i=6,10)
  write (6,99008) (f107a(i),i=6,10)
  write (6,99009) (f107(i),i=6,10)
  write (6,99010) (ap(i),i=6,10)
  write (6,99011) (t(1,i),i=6,10)
  write (6,99012) (t(2,i),i=6,10)
  write (6,99013) (d(1,i),i=6,10)
  write (6,99014) (d(2,i),i=6,10)
  write (6,99015) (d(3,i),i=6,10)
  write (6,99016) (d(4,i),i=6,10)
  write (6,99017) (d(5,i),i=6,10)
  write (6,99018) (d(7,i),i=6,10)
  write (6,99019) (d(8,i),i=6,10)
  write (6,99020) (d(9,i),i=6,10)
  write (6,99021) (d(6,i),i=6,10)
  write (6,99002) (iday(i),i=11,15)
  write (6,99003) (ut(i),i=11,15)
  write (6,99004) (alt(i),i=11,15)
  write (6,99005) (xlat(i),i=11,15)
  write (6,99006) (xlong(i),i=11,15)
  write (6,99007) (xlst(i),i=11,15)
  write (6,99008) (f107a(i),i=11,15)
  write (6,99009) (f107(i),i=11,15)
  write (6,99010) (ap(i),i=11,15)
  write (6,99011) (t(1,i),i=11,15)
  write (6,99012) (t(2,i),i=11,15)
  write (6,99013) (d(1,i),i=11,15)
  write (6,99014) (d(2,i),i=11,15)
  write (6,99015) (d(3,i),i=11,15)
  write (6,99016) (d(4,i),i=11,15)
  write (6,99017) (d(5,i),i=11,15)
  write (6,99018) (d(7,i),i=11,15)
  write (6,99019) (d(8,i),i=11,15)
  write (6,99020) (d(9,i),i=11,15)
  write (6,99021) (d(6,i),i=11,15)
99001 format (1x,1P8e9.2/4x,1pe9.2,2E10.3/4x,8E9.2/4x,8E9.2/)
99002 format (//' DAY  ',5I12)
99003 format (' UT   ',5F12.0)
99004 format (' ALT  ',5F12.0)
99005 format (' LAT  ',5F12.0)
99006 format (' LONG ',5F12.0)
99007 format (' LST  ',5F12.0)
99008 format (' F107A',5F12.0)
99009 format (' F107 ',5F12.0)
99010 format (' AP   ',5F12.0)
99011 format (/' TINF ',5F12.2)
99012 format (' TG   ',5F12.2)
99013 format (' HE   ',1P5e12.3)
99014 format (' O    ',1P5e12.3)
99015 format (' N2   ',1P5e12.3)
99016 format (' O2   ',1P5e12.3)
99017 format (' AR   ',1P5e12.3)
99018 format (' H    ',1P5e12.3)
99019 format (' N    ',1P5e12.3)
99020 format (' ANM O',1P5e12.3)
99021 format (' RHO  ',1P5e12.3)
99022 format (1x,2A4,2x,3A4,2x,2A4)
end program testgtd7
