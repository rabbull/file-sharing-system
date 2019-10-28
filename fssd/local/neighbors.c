//
// Created by karl on 2019/10/28.
//

#include <fcntl.h>
#include <stdio.h>
#include <zconf.h>
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
        printf("%d %s %lu\n", n, buf, strlen(buf));
        if (n == EOF) {
            send(sock_fd, "$END", 4, 0);
            break;
        }
        send(sock_fd, buf, strlen(buf), 0);
    }
}
