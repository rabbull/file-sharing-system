//
// Created by karl on 2019/10/27.
//

#include <stdio.h>
#include <pthread.h>
#include "../types.h"
#include "local/local.h"
#include "logger/logger.h"

int main(int argc, char **argv) {
    _i32 ret;
    logger_init("/home/karl/.fss/fssd.log");
    if (!logger_initialized()) {
        perror("Failed to initialize logger");
    }

    _b running = 1;
    pthread_t local_thread;
    pthread_create(&local_thread, 0, &local_main, &running);
    getchar();
    pthread_cancel(local_thread);
    pthread_join(local_thread, 0);
    return 0;
}
