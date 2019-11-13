//
// Created by karl on 11/13/19.
//

#ifndef FFS_REMOTE_H
#define FFS_REMOTE_H

#include <pthread.h>
#include "../../types.h"

struct remote_main_args {
    _b* running;
    pthread_t *thread_id;
};

void* remote_main(void* args);

#endif //FFS_REMOTE_H
