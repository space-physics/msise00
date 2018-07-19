cmake_minimum_required(VERSION 3.3)
project(msise00 Fortran)
enable_testing()

if(CMAKE_BUILD_TYPE STREQUAL Debug)
  add_compile_options(-g -O0)
else()
  add_compile_options(-O3)
endif()

if(${CMAKE_Fortran_COMPILER_ID} STREQUAL GNU)
  list(APPEND FFLAGS -mtune=native -ffpe-trap=invalid,zero,overflow -fbacktrace
       -Wall)
  # -fdefault-real-8 -fno-align-commons)
elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Intel)

elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL PGI)
  list(APPEND FFLAGS -Mallocatable=03)
elseif(${CMAKE_Fortran_COMPILER_ID} STREQUAL Flang)
  list(APPEND FFLAGS -Mallocatable=03)
  link_libraries(-static-flang-libs)
endif()
     
# ---
add_executable(test_msise00 nrlmsise00_sub.for nrlmsise00_driver.for nrlmsise00_driver.for)
target_compile_options(test_msise00 PRIVATE ${FFLAGS})

add_test(NAME MSISprint COMMAND test_msise00)
