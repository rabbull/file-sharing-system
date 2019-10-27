cmake_minimum_required(VERSION 3.10)
project(ffs C)

set(CMAKE_C_STANDARD 11)

add_subdirectory(fssctl)
add_subdirectory(fssd)
add_subdirectory(cliutils)
