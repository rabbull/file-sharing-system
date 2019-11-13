cmake_minimum_required(VERSION 3.10)
project(fssd)

add_subdirectory(local)
add_subdirectory(logger)
add_subdirectory(remote)

add_executable(fssd fssd.c)
target_link_libraries(fssd pthread local logger remote)
