cmake_minimum_required(VERSION 3.3)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(msise00 Fortran)
enable_testing()

add_executable(msise00_driver fortran/nrlmsise00_sub.for fortran/msise00_driver.f90)
target_compile_options(msise00_driver PRIVATE ${FFLAGS})

add_test(NAME MSISdriver
  COMMAND test_msise00 30 12 1 2 65 0 100 100 4 100)
set_tests_properties(MSISdriver PROPERTIES TIMEOUT 15)