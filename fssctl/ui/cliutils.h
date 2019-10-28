//
// Created by karl on 2019/10/27.
//

#ifndef FFS_CLIUTILS_H
#define FFS_CLIUTILS_H

#include <stdio.h>
#include "../../types.h"

extern FILE* __output_stream;

void print_line(_s s);

void print_string(_s s);

void print_char(_c c);

void print_unsigned_integer(unsigned long u);

void print_integer(long long i);

#endif //FFS_CLIUTILS_H
