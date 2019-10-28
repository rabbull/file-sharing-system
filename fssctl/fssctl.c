//
// Created by karl on 2019/10/27.
//

#include <stdio.h>
#include <stdlib.h>
#include <getopt.h>
#include <string.h>
#include "../types.h"
#include "ui/ui.h"
#include "functions.h"


int main(int argc, char **argv) {
    static const _u32 buf_size = 1024;
    _i32 opt;
    _c filename[buf_size];
    _b checksum_specified = 0;
    _c checksum[buf_size];
    _u32 len;

    memset(filename, 0, buf_size);
    memset(checksum, 0, buf_size);

    if (argc < 2) {
        print_usage(stderr);
        exit(-1);
    }

    while (1) {
        opt = getopt(argc, argv, "hq:c:ln");
        if (opt < 0) break;

        switch (opt) {
            case 'h':
                print_usage(stdout);
                break;

            case 'q':
                len = strlen(optarg);
                if (len >= buf_size) {
                    print_too_long_error(opt, len, buf_size, stderr);
                    exit(-1);
                }
                strcpy(filename, optarg);
                break;

            case 'c':
                len = strlen(optarg);
                if (len >= buf_size) {
                    print_too_long_error(opt, len, buf_size, stderr);
                    exit(-1);
                }
                strcpy(checksum, optarg);
                checksum_specified = 1;
                break;

            case 'l':
                if (argc > 2) {
                    print_ignore_warning(opt, stderr);
                }
                show_file_list();
                exit(0);

            case 'n':
                if (argc > 2) {
                    print_ignore_warning(opt, stderr);
                }
                show_neighbors(stdout);
                exit(0);

            case '?':
            default:
                print_usage(stderr);
                exit(-1);
        }
    }

    query(filename, checksum_specified, checksum);
    return 0;
}
