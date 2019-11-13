//
// Created by karl on 11/13/19.
//

#include <stdio.h>
#include <stdbool.h>

#include "../logger/logger.h"

void *remote_main(void *_args) {
    struct remote_main_args *args = (struct remote_main_args *) _args;
    const _u32 buf_size = 1024;
    _c buf[buf_size];
    if (!logger_initialized()) {
        fprintf(stderr, "waiting for logger to be initialized.. ");
        while (!logger_initialized());
        fprintf(stderr, "done.");
    }

    return NULL;
}
