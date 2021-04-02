cmake_minimum_required(VERSION 3.13...${CMAKE_VERSION})

if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE Release CACHE STRING "Debug or Release")
endif()

project(msise00 LANGUAGES Fortran)

include(CTest)

add_subdirectory(src/msise00)
