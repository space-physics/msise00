cmake_minimum_required(VERSION 3.13...${CMAKE_VERSION})

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()

project(msise00 LANGUAGES Fortran)

include(CTest)

if(CMAKE_Fortran_COMPILER_ID STREQUAL GNU)
  add_compile_options(-fmax-errors=3)
  set(old_flags -std=legacy)
endif()

add_library(msise00 OBJECT fortran/msise00_sub.f fortran/msise00_data.f)
target_compile_options(msise00 PRIVATE ${old_flags})
set_target_properties(msise00 PROPERTIES Fortran_MODULE_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}/include)
target_include_directories(msise00 INTERFACE ${CMAKE_CURRENT_BINARY_DIR}/include)

add_executable(msise00_driver fortran/msise00_driver.f90)
set_target_properties(msise00_driver PROPERTIES RUNTIME_OUTPUT_DIRECTORY ${PROJECT_SOURCE_DIR})
target_link_libraries(msise00_driver PRIVATE msise00)

add_test(NAME MSISdriver
  COMMAND $<TARGET_FILE:msise00_driver> 30 12 1 2 65 0 100 100 4 100)
set_tests_properties(MSISdriver PROPERTIES
  TIMEOUT 15
  PASS_REGULAR_EXPRESSION "1027.3.*187.8")
