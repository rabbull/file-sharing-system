cmake_minimum_required(VERSION 3.10)
project(ui)

add_library(ui SHARED cliutils.c ui.c)
