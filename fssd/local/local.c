//
// Created by karl on 2019/10/27.
//

#include <stdlib.h>
#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include "../../types.h"

_i32 init_socket(_s path);

void *local_main(void *running) {
    int fd;

    fd = init_socket("/home/karl/.fss/local.sock");
    if (fd < 0) {
        return NULL;
    }
    while (*(_b *) running) {
        struct sockaddr_un client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        static const _u32 buf_size = 1024;
        _b buf[buf_size];
        memset(buf, 0, buf_size);
        recvfrom(fd, buf, buf_size, 0, (struct sockaddr *) &client_addr, &client_addr_len);
        printf("%s", buf);
    }
    return NULL;
}

_i32 init_socket(_s path) {
    int fd, ret;
    struct sockaddr_un addr;

    fd = socket(AF_UNIX, SOCK_DGRAM, 0);
    if (fd < 0) {
        perror("Failed to create socket");
        return -1;
    }

    addr.sun_family = AF_UNIX;
    strcpy(addr.sun_path, path);
    ret = bind(fd, (struct sockaddr *) &addr, sizeof(struct sockaddr_un));
    if (ret < 0) {
        perror("Failed to bind socket with address");
        return -1;
    }
    return fd;
}