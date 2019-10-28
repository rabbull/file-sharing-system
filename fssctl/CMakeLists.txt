cmake_minimum_required(VERSION 3.10)
project(fssctl)

add_subdirectory(ui)

add_executable(fssctl fssctl.c functions.h show_file_list.c show_neighbors.c query.c local.c local.h)
target_link_libraries(fssctl ui)
