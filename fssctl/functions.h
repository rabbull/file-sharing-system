//
// Created by karl on 2019/10/27.
//

#ifndef FFS_FUNCTIONS_H
#define FFS_FUNCTIONS_H

#include "../types.h"

void show_file_list(FILE *fp);

void show_neighbors(FILE *fp);

void search(_s filename, _s checksum, _u64 buf_size);

#endif //FFS_FUNCTIONS_H
