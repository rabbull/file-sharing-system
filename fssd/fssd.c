//
// Created by karl on 2019/10/27.
//

#include <stdio.h>
#include <string.h>
#include <pthread.h>
#include <stdlib.h>
#include "../types.h"
#include "local/local.h"
#include "logger/logger.h"

int main(int argc, char **argv) {
    _s user_home = getenv("HOME");
    if (user_home == NULL) {
        fprintf(stderr, "Failed to get user home directory from env.");
    }
    _c log_path[1024] = {0};
    sprintf(log_path, "%s/.fss/fssd.log", user_home);
    logger_init(log_path);
    if (!logger_initialized()) {
        perror("Failed to initialize logger");
    }

    _b running = 0;
    pthread_t local_thread;
    struct local_main_args local_main_args;
    local_main_args.running = &running;
    local_main_args.thread_id = &local_thread;
    _c sock_file_path[1024];
    sprintf(sock_file_path, "%s/.fss/local.sock", user_home);
    local_main_args.sock_file_path = sock_file_path;
    pthread_create(&local_thread, 0, &local_main, &local_main_args);
    running = 1;
    getchar();
    pthread_cancel(local_thread);
    pthread_join(local_thread, 0);
    return 0;
}
