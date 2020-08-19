cmake_minimum_required(VERSION 3.12)
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()
project(msise00
LANGUAGES Fortran)
enable_testing()

add_executable(msise00_driver fortran/nrlmsise00_sub.for fortran/msise00_driver.f90)
set_target_properties(msise00_driver PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})

add_test(NAME MSISdriver
  COMMAND $<TARGET_FILE:msise00_driver> 30 12 1 2 65 0 100 100 4 100)
set_tests_properties(MSISdriver PROPERTIES TIMEOUT 15)
