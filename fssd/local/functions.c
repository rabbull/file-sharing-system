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

void search_file_with_checksum(int fd) {
    _b filename[1024];
    recv(fd, filename, 1024, 0);
    _b checksum[1024];
    recv(fd, checksum, 1024, 0);
    puts((_s) filename);
    puts((_s) checksum);
}

void search_file(int fd) {
    _b filename[1024];
    recv(fd, filename, 1024, 0);
    puts((_s) filename);
}
