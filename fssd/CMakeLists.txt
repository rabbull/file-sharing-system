cmake_minimum_required(VERSION 3.10)
project(fssd)

add_subdirectory(local)
add_subdirectory(logger)

add_executable(fssd fssd.c remote/remote.c remote/functions.c remote/remote.h)
target_link_libraries(fssd pthread local logger)
