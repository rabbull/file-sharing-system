//
// Created by karl on 2019/10/28.
//

#include "../types.h"

#ifndef FFS_LOCAL_H
#define FFS_LOCAL_H

void send_to_daemon(_b buf[], _u64 buf_size);

_u64 recv_from_daemon(_b buf[], _u64 buf_size);


void init_socket_to_daemon(_s path);

void connect_to_daemon();

#endif //FFS_LOCAL_H
