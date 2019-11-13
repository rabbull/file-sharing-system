//
// Created by karl on 2019/10/27.
//

#include "../types.h"
#include "ui/ui.h"
#include "connection.h"

void search(_s filename, _s checksum, _u64 buf_size) {
    printf("%s", filename);
    if (checksum) {
        printf(" %s", checksum);
    }
    printf("\n");

    init_socket_to_daemon("/home/karl/.fss/local.sock");
    connect_to_daemon();

    _s command;
    if (checksum) {
        command = "$C";
    } else {
        command = "$S";
    }

    send_to_daemon((_b *) command, 2);

    send_to_daemon((_b *) filename, buf_size);
    if (checksum) {
        send_to_daemon((_b *) checksum, buf_size);
    }
}
