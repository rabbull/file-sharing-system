//
// Created by karl on 2019/10/27.
//

#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include <errno.h>
#include <unistd.h>
#include "../../types.h"


static _i32 init_local_socket(_s path);

void send_neighbors(int sock_fd);

void send_file_list(int sock_fd);

void query_file_with_checksum(int fd);

void query_file_without_checksum(int fd);

void *local_main(void *running) {
    int fd;

    fd = init_local_socket("/home/karl/.fss/local.sock");
    if (fd < 0) {
        return NULL;
    }
    while (*(_b *) running) {
        struct sockaddr_un client_addr;
        socklen_t client_addr_len = sizeof(client_addr);
        static const _u32 buf_size = 1024;
        _c buf[buf_size];
        memset(buf, 0, buf_size);

        int new_fd = accept(fd, (struct sockaddr *) &client_addr, &client_addr_len);
        printf("connected.\n");

        sleep(1);
        recv(new_fd, buf, buf_size, 0);
        printf("recv: %s\n", buf);
        if (strcmp(buf, "$N") == 0) {
            send_neighbors(new_fd);
        } else if (strcmp(buf, "$L") == 0) {
            send_file_list(new_fd);
        } else if (strcmp(buf, "$C") == 0) {
            query_file_with_checksum(new_fd);
        } else if (strcmp(buf, "$Q") == 0) {
            query_file_without_checksum(new_fd);
        }
    }
    return NULL;
}

_i32 init_local_socket(_s path) {
    int fd, ret;
    struct sockaddr_un addr;

    fd = socket(AF_UNIX, SOCK_SEQPACKET, 0);
    if (fd < 0) {
        perror("Failed to create socket");
        return -1;
    }

    addr.sun_family = AF_UNIX;
    strcpy(addr.sun_path, path);
    retry:
    ret = bind(fd, (struct sockaddr *) &addr, sizeof(struct sockaddr_un));
    if (ret < 0) {
        perror("Failed to bind socket with address");
        if (errno == 98) {  // socket address already in use
            fprintf(stderr, "Trying to release socket file.. ");
            ret = remove(path);
            if (ret < 0) {
                perror("Failed");
                return -1;
            }
            fprintf(stderr, "Done.\n");
            goto retry;
        }
        return -1;
    }
    listen(fd, 16);
    return fd;
}
