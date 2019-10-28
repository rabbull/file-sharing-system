//
// Created by karl on 2019/10/27.
//

#include "cliutils.h"

FILE* __output_stream = NULL;

void print_line(_s s) {
    print_string(s);
    print_char('\n');
}

void print_string(_s s) {
    if (__output_stream == NULL) {
        __output_stream = stdout;
    }
    fputs(s, __output_stream);
}

void print_char(_c c) {
    if (__output_stream == NULL) {
        __output_stream = stdout;
    }
    putc(c, __output_stream);
}

void print_unsigned_integer(unsigned long u) {
    static _c buf[45];
    sprintf(buf, "%lu", u);
    print_string(buf);
}

void print_integer(long long i) {
    static _c buf[45];
    sprintf(buf, "%lld", i);
    print_string(buf);
}
