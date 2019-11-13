//
// Created by karl on 2019/10/27.
//

#include <string.h>
#include <stdlib.h>
#include <pthread.h>
#include <fcntl.h>
#include <stdio.h>
#include <unistd.h>
#include <stdarg.h>
#include "logger.h"

static _ab __init_flag = 0;
static FILE* __output_fp = NULL;
static pthread_mutex_t __mutex = {0};

typedef enum {
    INFO,
    WARN,
    ERROR
} record_t;

static void __put_line(record_t type, _s format);

static _u32 __get_time_str(_s buf, _u32 buf_size);

void logger_init(_s log_path) {
    if (__init_flag) {
        return;
    }
    pthread_mutex_init(&__mutex, 0);
    __output_fp = fopen(log_path, "a+");
    if (__output_fp == NULL) {
        perror("Failed to open log file");
        return;
    }
    __init_flag = 1;
}

_b logger_initialized() {
    return (_b) __init_flag;
}

_u32 __get_time_str(_s buf, _u32 buf_size) {
    // "yyyy-mm-dd DDD hh:mm:ss "
    time_t tt;
    struct tm *tm;
    _u32 len = 0;
    time(&tt);
    tm = localtime(&tt);
    len = strftime(buf, buf_size, "%Y-%m-%d %a %T ", tm);
    return len;
}

void __put_line(record_t type, _s format) {
    pthread_mutex_lock(&__mutex);
    // write tag
    static _s tags[3] = {"[II] ", "[WW] ", "[EE] "};
    fputs(tags[type], __output_fp);

    // write time
    _c time_buf[32];
    __get_time_str(time_buf, 32);
    fputs(time_buf, __output_fp);

    // wirte format
    fputs(format, __output_fp);

    // write '\n'
    fputs("\n", __output_fp);
    fflush(__output_fp);
    pthread_mutex_unlock(&__mutex);
}

void add_information(_s format, ...) {
    static _c buf[1024] = {0};
    va_list args;
    va_start(args, format);
    vsprintf(buf, format, args);
    __put_line(INFO, buf);
    va_end(args);
}

void add_warning(_s format, ...) {
    static _c buf[1024] = {0};
    va_list args;
    va_start(args, format);
    vsprintf(buf, format, args);
    __put_line(WARN, buf);
    va_end(args);
}

void add_error(_s format, ...) {
    static _c buf[1024] = {0};
    va_list args;
    va_start(args, format);
    vsprintf(buf, format, args);
    __put_line(ERROR, buf);
    va_end(args);
}
