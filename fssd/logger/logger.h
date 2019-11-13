//
// Created by karl on 2019/10/27.
//

#ifndef FFS_LOGGER_H
#define FFS_LOGGER_H

#include "../../types.h"

_b logger_initialized();

void logger_init(_s log_path);

void add_information(_s format, ...);

void add_warning(_s format, ...);

void add_error(_s format, ...);

#endif //FFS_LOGGER_H
