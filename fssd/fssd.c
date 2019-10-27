//
// Created by karl on 2019/10/27.
//

#include <zconf.h>
#include <stdio.h>
#include <pthread.h>
#include "../types.h"
#include "local/local.h"

int main(int argc, char **argv) {
    _i32 ret;

//    ret = daemon(1, 1);
//    if (ret < 0) {
//        perror("Failed to create daemon.");
//        return -1;
//    }

    _b running = 1;
    pthread_t local_thread;
    pthread_create(&local_thread, 0, &local_main, &running);
    getchar();
    pthread_cancel(local_thread);
    pthread_join(local_thread, 0);
    return 0;
}
