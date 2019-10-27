//
// Created by karl on 2019/10/27.
//

#include <zconf.h>
#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <fcntl.h>
#include "logger.h"

_ab __init_flag = 0;
int __output_fd = -1;
pthread_mutex_t __mutex = {0};

void initialize(_s log_path) {
    if (__init_flag) {
        return;
    }
    pthread_mutex_init(&__mutex, 0);
    __output_fd = open(log_path, O_WRONLY | O_APPEND | O_CREAT, 0777);
    if (__output_fd < 0) {
        return;
    }
    __init_flag = 1;
}

_ab initialized() {
    return __init_flag;
}

void put_line(_s record) {
    write(__output_fd, record, strlen(record));
}
