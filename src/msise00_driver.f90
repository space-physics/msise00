program msise00

implicit none

real :: iyd=172  ! day of year
real :: utsec=29000. ! UTC second of day
real :: alt_km=400.  ! altitude [km]
real :: glat = 60. ! geodetic latitude [deg]
real :: glon = -70. ! geodetic longitude [deg]

real :: lst ! local solar time
real :: f107a = 150.
real :: f107 = 150
real :: ap = 4.

! output variables
real :: Density(9)
real :: Temperature(2)

! SW is as defined in NRL example
real, parameter :: SW(25)=[1.,1.,1.,1.,1.,1.,1.,1.,-1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.,1.]


lst = utsec/3600. + glon/15.


CALL GTD7(iyd, utsec, alt_km, glat, glon, lst, f107a, f107, ap,48, Density, Temperature)

print *,Density
print *,Temperature

end program
