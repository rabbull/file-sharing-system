//
// Created by karl on 2019/10/27.
//

#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include "logger.h"

static _ab __init_flag = 0;
static int __output_fd = -1;
static pthread_mutex_t __mutex = {0};

typedef enum {
    INFO,
    WARN,
    ERROR
} record_t;

static void put_line(record_t type, _s message, _u64 message_len);

static _u32 get_time_str(_s buf, _u32 buf_size);

void logger_init(_s log_path) {
    if (__init_flag) {
        return;
    }
    pthread_mutex_init(&__mutex, 0);
    __output_fd = open(log_path, O_WRONLY | O_APPEND | O_CREAT, 0b110110110);
    if (__output_fd < 0) {
        perror("Failed to open log file");
        return;
    }
    __init_flag = 1;
}

_b logger_initialized() {
    return (_b) __init_flag;
}

_u32 get_time_str(_s buf, _u32 buf_size) {
    // "yyyy-mm-dd DDD hh:mm:ss "
    time_t tt;
    struct tm *tm;
    _u32 len = 0;
    time(&tt);
    tm = localtime(&tt);
    len = strftime(buf, buf_size, "%Y-%m-%d %a %T ", tm);
    return len;
}

void put_line(record_t type, _s message, _u64 message_len) {
    pthread_mutex_lock(&__mutex);
    // write tag
    static _s tags[3] = {"[II] ", "[WW] ", "[EE] "};
    write(__output_fd, tags[type], strlen(message));

    // write time
    _c time_buf[32];
    int time_len;
    time_len = get_time_str(time_buf, 32);
    write(__output_fd, time_buf, time_len);

    // wirte message
    write(__output_fd, message, message_len);

    // write '\n'
    write(__output_fd, "\n", 1);
    pthread_mutex_unlock(&__mutex);
}

void add_information(_s message, _i64 message_len) {
    if (message_len <= 0) {
        put_line(INFO, message, strlen(message));
    } else {
        put_line(INFO, message, message_len);
    }
}

void add_warning(_s message, _i64 message_len) {
    if (message_len <= 0) {
        put_line(WARN, message, strlen(message));
    } else {
        put_line(WARN, message, message_len);
    }
}

void add_error(_s message, _i64 message_len) {
    if (message_len <= 0) {
        put_line(ERROR, message, strlen(message));
    } else {
        put_line(ERROR, message, message_len);
    }
}
