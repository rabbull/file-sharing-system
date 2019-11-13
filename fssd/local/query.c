//
// Created by karl on 11/13/19.
//

#include <stdio.h>
#include <unistd.h>
#include "../../types.h"


void query_file_with_checksum(int fd) {
    _b filename[1024];
    read(fd, filename, 1024);
    _b checksum[1024];
    read(fd, checksum, 1024);
    puts((_s) filename);
    puts((_s) checksum);
}

void query_file_without_checksum(int fd) {
    _b filename[1024];
    read(fd, filename, 1024);
    puts((_s) filename);
}
