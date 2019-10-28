//
// Created by karl on 2019/10/27.
//

#include <sys/socket.h>
#include <sys/un.h>
#include <stdio.h>
#include "local.h"

void show_neighbors(FILE *fp) {
    init_socket_to_daemon("/home/karl/.fss/local.sock");
    _b buf[512] = "$N";

    connect_to_daemon();
    send_to_daemon(buf, sizeof(buf));

    int index = 0;
    do {
        int n = recv_from_daemon(buf, sizeof(buf));
        if (strncmp((char *) buf, "$END", n) == 0) {
            break;
        }
        fprintf(fp, "%s\n", buf);
    } while (1);
}
