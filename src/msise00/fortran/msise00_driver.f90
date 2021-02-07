program msis_driver

use, intrinsic:: iso_fortran_env, only: stderr=>error_unit
use msise00_python, only : gtd7, meters

implicit none

! ./msise00 172 8 0 0 60. -70. 150. 150. 4. 400

integer :: doy  ! day of year
real :: utsec ! UTC second of day
real :: alt_km  ! altitude [km]
real :: glat, glon ! geodetic latitude, longitude [deg]

real :: lst ! local solar time
real :: f107a
real :: f107
real :: Ap, Ap7(7)

real :: hour, minute, second

character(1000) :: argv

! output variables
real :: Density(9)
real :: Temperature(2)

! SW is as defined in NRL example
real, parameter :: SW(25)=[1.,1.,1.,1.,1.,1.,1.,1.,-1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]

call meters(.true.)

! --- command line input
if (command_argument_count() < 10) then
  write(stderr,*) 'need input parameters: DayOfYear hour minute second glat glon f107a f107 ap alt_km'
  stop 1
endif

call get_command_argument(1, argv)
read(argv,'(i3)') doy

call get_command_argument(2, argv)
read(argv,*) hour

call get_command_argument(3, argv)
read(argv,*) minute

call get_command_argument(4, argv)
read(argv,*) second

call get_command_argument(5, argv)
read(argv,*) glat

call get_command_argument(6, argv)
read(argv,*) glon

call get_command_argument(7, argv)
read(argv,*) f107a

call get_command_argument(8, argv)
read(argv,*) f107

call get_command_argument(9, argv)
read(argv,*) Ap
Ap7 = Ap

call get_command_argument(10, argv)
read(argv,*) alt_km


! --- execute program
utsec = hour*3600. + minute*60. + second

lst = utsec/3600. + glon/15.

CALL GTD7(doy, utsec, alt_km, glat, glon, lst, f107a, f107, Ap7, 48, Density, Temperature)

print '(9ES15.7)',Density
print '(2F9.2)',Temperature

end program
