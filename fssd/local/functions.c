//
// Created by karl on 2019/10/28.
//

#include <stdio.h>
#include <sys/socket.h>
#include <string.h>
#include "../../types.h"

void send_neighbors(int sock_fd) {
    FILE *fp = fopen("/home/karl/.fss/neighbors", "r");
    if (fp == NULL) {
        perror("Failed to read neighbors file");
        return;
    }
    _c buf[512];
    int n;
    while (1) {
        n = fscanf(fp, "%s", buf);
        if (n == EOF) {
            send(sock_fd, "$END", 4, 0);
            break;
        }
        if (buf[0] == '#') {
            continue;
        }
        send(sock_fd, buf, strlen(buf), 0);
    }
}

#include <ctype.h>
#include <stdlib.h>
#include <assert.h>

//inline _i64 size_to_long(_c *size_str) {
//    _u64 len = strlen(size_str);
//
//    for (_u64 i = 0; i < len; ++i) {
//        if (!isalnum(size_str[i])) {
//            return -1;
//        }
//    }
//
//    _u64 size = strtol(size_str, NULL, 10);
//    _c unit = 0;
//    if (isdigit(size_str[len - 1])) {
//        return size;
//    } else {
//        unit = tolower(size_str[len - 1]);
//    }
//    switch(unit) {
//        case 't':
//            size <<= 10u;
//        case 'g':
//            size <<= 10u;
//        case 'm':
//            size <<= 10u;
//        case 'k':
//            size <<= 10u;
//            break;
//        default:
//            return -2;
//    }
//    return size;
//}

void send_file_list(int sock_fd) {
    FILE *fp = fopen("/home/karl/.fss/file_list", "r");
    if (fp == NULL) {
        perror("Failed to read file_list");
        return;
    }
    _c buf[512];
    while (1) {
        bzero(buf, 512);
        if (fgets(buf, 512, fp) == NULL) {
            break;
        }
        if (buf[0] == '#') {
            continue;
        }  // comment allowed

        _c *p = NULL, *checksum = NULL;

        _c *delim = " ";
        strtok(buf, delim);
        p = strtok(NULL, delim);
        if (p == NULL) {
            perror("Syntax error in file /home/karl/.fss/file_list");
            return;
        }

        checksum = p;

        p = strtok(NULL, delim);

        printf("%s\n%s\n%s\n", buf, checksum, p);

        send(sock_fd, buf, strlen(buf), 0);
        send(sock_fd, checksum, strlen(checksum), 0);
        send(sock_fd, p, strlen(p), 0);
    }
    send(sock_fd, "$END", 4, 0);
}
