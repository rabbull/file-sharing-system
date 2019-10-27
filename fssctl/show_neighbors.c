//
// Created by karl on 2019/10/27.
//

#include <sys/socket.h>
#include <sys/un.h>
#include <zconf.h>
#include "ui.h"

void show_neighbors() {
    int fd = socket(AF_UNIX, SOCK_DGRAM, 0);
    _b msg[] = "Hello bitch!\n";

    struct sockaddr_un daemon_addr;
    socklen_t daemon_addr_len = sizeof(daemon_addr);
    daemon_addr.sun_family = AF_UNIX;
    strcpy(daemon_addr.sun_path, "/home/karl/.fss/local.sock");

    sendto(fd, msg, sizeof(msg), 0, (struct sockaddr *) &daemon_addr, daemon_addr_len);
}
