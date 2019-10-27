cmake_minimum_required(VERSION 3.10)
project(fssctl)

add_executable(fssctl fssctl.c ui.c ui.h functions.h show_file_list.c show_neighbors.c query.c)
target_link_libraries(fssctl cliutils)
