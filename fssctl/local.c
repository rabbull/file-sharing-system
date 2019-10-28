//
// Created by karl on 2019/10/28.
//

#include <sys/un.h>
#include <sys/socket.h>
#include <stdio.h>
#include <fcntl.h>
#include "local.h"

static int sock_fd;
static struct sockaddr_un daemon_addr;
static socklen_t daemon_addr_len;

void init_socket_to_daemon(_s path) {
    sock_fd = socket(AF_UNIX, SOCK_SEQPACKET, 0);
    if (sock_fd < 0) {
        perror("Failed to create socket");
        return;
    }
    daemon_addr.sun_family = AF_UNIX;
    strcpy(daemon_addr.sun_path, path);
    daemon_addr_len = sizeof(daemon_addr);
}

void connect_to_daemon() {
    int ret;
    ret = connect(sock_fd, (const struct sockaddr *) &daemon_addr, daemon_addr_len);
    if (ret < 0) {
        perror("Failed to connect to daemon");
    }
}

void send_to_daemon(_b buf[], _u64 buf_size) {
    if (sock_fd == -1) {
        return;
    }
    send(sock_fd, buf, buf_size, 0);
}

_u64 recv_from_daemon(_b buf[], _u64 buf_size) {
    if (sock_fd == -1) {
        return 0;
    }
    return recv(sock_fd, buf, buf_size, 0);
}
