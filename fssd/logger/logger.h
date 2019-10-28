//
// Created by karl on 2019/10/27.
//

#ifndef FFS_LOGGER_H
#define FFS_LOGGER_H

#include "../../types.h"

_b logger_initialized();

void logger_init(_s log_path);

void add_information(_s message, _i64 message_len);

void add_warning(_s message, _i64 message_len);

void add_error(_s message, _i64 message_len);

#endif //FFS_LOGGER_H
