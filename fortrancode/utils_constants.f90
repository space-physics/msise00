module utils_constants

  public

  ! Kind helpers
  integer , parameter :: dp = kind(1.0D0)
  integer , parameter :: sp = kind(1.0)
  integer , parameter :: r8 = kind(1.0D0)
  integer , parameter :: r4 = kind(1.0)
  integer , parameter :: shortint = 2
  integer , parameter :: normint = 4
  integer , parameter :: longint = 8

  ! Numbers 1-10
  real(dp) , parameter :: d_0 = 0.0_r8
  real(dp) , parameter :: d_1 = 1.0_r8
  real(dp) , parameter :: d_2 = 2.0_r8
  real(dp) , parameter :: d_3 = 3.0_r8
  real(dp) , parameter :: d_4 = 4.0_r8
  real(dp) , parameter :: d_5 = 5.0_r8
  real(dp) , parameter :: d_6 = 6.0_r8
  real(dp) , parameter :: d_7 = 7.0_r8
  real(dp) , parameter :: d_8 = 8.0_r8
  real(dp) , parameter :: d_9 = 9.0_r8
  real(dp) , parameter :: d_10 = 10.0_r8
  real(dp) , parameter :: d_16 = 16.0_r8
  real(dp) , parameter :: d_32 = 32.0_r8

  ! Simple Fractions
  real(dp) , parameter :: d_half = d_1/d_2

  real(dp) , parameter :: d_1q2 = d_1/d_2
  real(dp) , parameter :: d_3q2 = d_3/d_2
  real(dp) , parameter :: d_5q2 = d_5/d_2
  real(dp) , parameter :: d_7q2 = d_7/d_2
  real(dp) , parameter :: d_9q2 = d_9/d_2
  real(dp) , parameter :: d_1q3 = d_1/d_3
  real(dp) , parameter :: d_2q3 = d_2/d_3
  real(dp) , parameter :: d_4q3 = d_4/d_3
  real(dp) , parameter :: d_5q3 = d_5/d_3
  real(dp) , parameter :: d_1q4 = d_1/d_4
  real(dp) , parameter :: d_3q4 = d_3/d_4
  real(dp) , parameter :: d_5q4 = d_5/d_4
  real(dp) , parameter :: d_7q4 = d_7/d_4
  real(dp) , parameter :: d_1q5 = d_1/d_5
  real(dp) , parameter :: d_2q5 = d_2/d_5
  real(dp) , parameter :: d_3q5 = d_3/d_5
  real(dp) , parameter :: d_4q5 = d_4/d_5
  real(dp) , parameter :: d_6q5 = d_6/d_5
  real(dp) , parameter :: d_7q5 = d_7/d_5

  ! 100 and 1000 and their inverse
  real(dp) , parameter :: d_100 = 100.0_r8
  real(dp) , parameter :: d_1000 = 1000.0_r8
  real(dp) , parameter :: d_r100 = 0.01_r8
  real(dp) , parameter :: d_r1000 = 0.001_r8

  ! Power of 10
  real(dp) , parameter :: d_10E1  = 10.0_r8
  real(dp) , parameter :: d_10E2  = 100.0_r8
  real(dp) , parameter :: d_10E3  = 1000.0_r8
  real(dp) , parameter :: d_10E4  = 10000.0_r8
  real(dp) , parameter :: d_10E5  = 100000.0_r8
  real(dp) , parameter :: d_10E6  = 1000000.0_r8
  real(dp) , parameter :: d_10E7  = 10000000.0_r8
  real(dp) , parameter :: d_10E8  = 100000000.0_r8
  real(dp) , parameter :: d_10E9  = 1000000000.0_r8
  real(dp) , parameter :: d_10E10 = 10000000000.0_r8
  real(dp) , parameter :: d_10E11 = 100000000000.0_r8
  real(dp) , parameter :: d_10E12 = 1000000000000.0_r8
  real(dp) , parameter :: d_10E13 = 10000000000000.0_r8
  real(dp) , parameter :: d_10EM1  = 0.1_r8
  real(dp) , parameter :: d_10EM2  = 0.01_r8
  real(dp) , parameter :: d_10EM3  = 0.001_r8
  real(dp) , parameter :: d_10EM4  = 0.0001_r8
  real(dp) , parameter :: d_10EM5  = 0.00001_r8
  real(dp) , parameter :: d_10EM6  = 0.000001_r8
  real(dp) , parameter :: d_10EM7  = 0.0000001_r8
  real(dp) , parameter :: d_10EM8  = 0.00000001_r8
  real(dp) , parameter :: d_10EM9  = 0.000000001_r8
  real(dp) , parameter :: d_10EM10 = 0.0000000001_r8
  real(dp) , parameter :: d_10EM11 = 0.00000000001_r8
  real(dp) , parameter :: d_10EM12 = 0.000000000001_r8
  real(dp) , parameter :: d_10EM13 = 0.0000000000001_r8

  ! Time related constants
  real(dp) , parameter :: d_seconds_per_hour = 3600.0_r8
  real(sp) , parameter :: s_seconds_per_hour = 3600.0
  integer  , parameter :: i_seconds_per_hour = 3600

  real(dp) , parameter :: d_seconds_per_minute = 60.0_r8
  real(sp) , parameter :: s_seconds_per_minute = 60.0
  integer  , parameter :: i_seconds_per_minute = 60

  real(dp) , parameter :: d_minutes_per_hour = 60.0_r8
  real(sp) , parameter :: s_minutes_per_hour = 60.0
  integer  , parameter :: i_minutes_per_hour = 60

  real(dp) , parameter :: d_hours_per_day = 24.0_r8
  real(sp) , parameter :: s_hours_per_day = 24.0
  integer  , parameter :: i_hours_per_day = 24

  real(dp) , parameter :: d_minutes_per_day = 1440.0_r8
  real(sp) , parameter :: s_minutes_per_day = 1440.0
  integer  , parameter :: i_minutes_per_day = 1440

  real(dp) , parameter :: d_seconds_per_day = 86400.0_r8
  real(sp) , parameter :: s_seconds_per_day = 86400.0
  integer  , parameter :: i_seconds_per_day = 86400

  real(dp) , parameter :: d_months_per_year = 12.0_r8
  real(sp) , parameter :: s_months_per_year = 12.0
  integer  , parameter :: i_months_per_year = 12

  ! Degrees helpers
  real(dp) , parameter :: d_000 = 0.0D0
  real(dp) , parameter :: d_045 = 45.0D0
  real(dp) , parameter :: d_090 = 90.0D0
  real(dp) , parameter :: d_180 = 180.0D0
  real(dp) , parameter :: d_360 = 360.0D0

  ! Trigonometric
  real(dp) , parameter :: mathpi  = 3.1415926535897932384626433832795029_r8
  real(dp) , parameter :: invpi   = d_1/mathpi
  real(dp) , parameter :: twopi   = d_2*mathpi
  real(dp) , parameter :: halfpi  = d_1q2*mathpi
  real(dp) , parameter :: deg2rad = mathpi/d_180
  real(dp) , parameter :: rad2deg = d_180/mathpi

  integer , parameter :: maxpath = 256

end module utils_constants
