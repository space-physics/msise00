cmake_minimum_required(VERSION 3.3)
project(msise00 Fortran)
enable_testing()

include (../cmake/compilers.cmake)
     
# ---

add_executable(msise00_driver nrlmsise00_sub.for msise00_driver.f90)
target_compile_options(msise00_driver PRIVATE ${FFLAGS})

add_executable(test_msise00 nrlmsise00_sub.for reference/nrlmsise00_driver.for)
target_compile_options(test_msise00 PRIVATE ${FFLAGS})
add_test(NAME MSISprint COMMAND test_msise00)

