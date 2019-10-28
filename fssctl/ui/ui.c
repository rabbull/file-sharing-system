//
// Created by karl on 2019/10/27.
//

#include <stdlib.h>
#include "ui.h"
#include "cliutils.h"

void print_usage(FILE* fp) {
    FILE* os_bak = __output_stream;
    __output_stream = fp;

    print_line("Usage: fssctl [-h] [-n] [-l] [-q FILENAME [-c CHECKSUM]]");
    print_line("\t-h              Print this message and exit.");
    print_line("\t-q FILENAME     Query file with name as FILENAME from your neighbors.");
    print_line("\t-c CHECKSUM     [optional] Check the checksum of file while querying.");
    print_line("\t-n              Show your neighbors' ip address.");
    print_line("\t-l              Show local shared files.");

    __output_stream = os_bak;
}

void print_ignore_warning(int opt, FILE* fp) {
    FILE* os_bak = __output_stream;
    __output_stream = fp;

    print_string("[WW] for tag '");
    print_char(opt);
    print_line("' is selected, the others tags would be ignored.");

    __output_stream = os_bak;
}

void print_too_long_error(int opt, _u32 real, _u32 limit, FILE* fp) {
    FILE* os_bak = __output_stream;
    __output_stream = fp;

    print_string("[EE] Argument too long for option '-");
    print_char(opt);
    print_line("':");
    print_string("\tThe limit is ");
    print_unsigned_integer(limit);
    print_string(" but the real length is ");
    print_unsigned_integer(real);
    print_line(".");

    __output_stream = os_bak;
}
