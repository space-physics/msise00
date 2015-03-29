module physics_constants

  use utils_constants

  public

  ! Basic physical constants of matter. The 10^-23 and 10^23 factors
  ! have been removed to ease calculations.

  ! Boltzman Constant - CODATA 2010
  real(8) , parameter :: boltzk = 1.380648813_r8
  ! Avogadro Constant - International Avogadro cohordination 2011
  real(8) , parameter :: navgdr = 6.0221407818_r8

  ! Gas constant in J/K/mol
  real(dp) , parameter :: rgasmol = boltzk*navgdr 

  ! Molecular weight of water
  real(dp) , parameter :: watmolwgt = 18.01528_r8 ! g/mol
  ! Mean dry air molecular weight
  real(dp) , parameter :: airmolwgt = 28.96443_r8 ! g/mol
  ! Ratio of mean molecular weight of water to that of dry air
  real(dp) , parameter :: wgtfrac = watmolwgt/airmolwgt

  ! Gas constant for dry air in J/K/kg
  real(dp) , parameter :: rgas = (rgasmol/airmolwgt)*d_1000
  ! Gas constant for water in J/K/kg
  real(dp) , parameter :: rwat = (rgasmol/watmolwgt)*d_1000

  ! 0 C in Kelvin
  real(dp) , parameter :: tzero = 273.16_r8

  ! Standard Gravity (m/sec**2) 3rd CGPM
  real(dp) , parameter :: egrav = 9.80665_r8

  ! Earth radius in meters
  real(8) , parameter :: earthrad = 6.371229D+06
  real(8) , parameter :: erkm = earthrad/d_1000
  ! Angular velocity of rotation of Earth
  real(8) , parameter :: eomeg = 7.2921159D-05
  real(8) , parameter :: eomeg2 = d_2*eomeg

  ! Hydrostatic coefficient
  real(8) , parameter :: gmr = egrav*airmolwgt/rgasmol

  ! Specific heat at constant pressure for dry air J/kg/K
  real(dp) , parameter :: cpd = 1005.46_r8
  ! Specific heat at constant pressure for moist air J/kg/K
  real(dp) , parameter :: cpv = 1869.46_r8
  ! Specific heat of water at 15 Celsius J/kg/K
  real(dp) , parameter :: cpw = 4186.95_r8
  ! Specific heat of water at 0 Celsius J/kg/K
  real(dp) , parameter :: cpw0 = 4218.0_r8

  ! Derived
  real(dp) , parameter :: rgovrw = rgas/rwat
  real(dp) , parameter :: rwovrg = rwat/rgas
  real(dp) , parameter :: rgovcp = rgas/cpd
  real(dp) , parameter :: rgovg  = rgas/egrav
  real(dp) , parameter :: govrg  = egrav/rgas
  
  real(dp) , parameter :: regrav = d_1/egrav
  real(dp) , parameter :: rrgas = d_1/rgas
  real(dp) , parameter :: rcpd = d_1/cpd

end module physics_constants
