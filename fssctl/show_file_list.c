//
// Created by karl on 2019/10/27.
//

#include "ui/ui.h"
#include "connection.h"
#include <string.h>

void show_file_list(FILE *fp) {
    init_socket_to_daemon("/home/karl/.fss/local.sock");
    _b size[20];
    _b checksum[17];
    _b buf[512] = "$L";
    _b *path = buf;

    connect_to_daemon();
    send_to_daemon(buf, sizeof(buf));

    int index = 0;
    do {
        int n = recv_from_daemon(size, sizeof(size));
        if (strncmp((char *) size, "$END", n) == 0) {
            break;
        }
        recv_from_daemon(checksum, sizeof(checksum));
        recv_from_daemon(path, sizeof(buf));
        fprintf(fp, "%s %s %s\n", size, checksum, path);
    } while (1);
}
