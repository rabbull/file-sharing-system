//
// Created by karl on 2019/10/27.
//

#ifndef FFS_UI_H
#define FFS_UI_H

#include <stdio.h>
#include "../types.h"

void print_usage(FILE* fp);

void print_ignore_warning(int opt, FILE* fp);

void print_too_long_error(int opt, _u32 real, _u32 limit, FILE* fp);

void print_neighbors(_s neighbor_path);

void print_filelist(_s filelist_path);

#endif //FFS_UI_H
