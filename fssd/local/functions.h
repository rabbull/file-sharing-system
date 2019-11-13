//
// Created by karl on 11/13/19.
//

#ifndef FFS_FUNCTIONS_H
#define FFS_FUNCTIONS_H

void send_neighbors(int sock_fd);

void send_file_list(int sock_fd);

void search_file_with_checksum(int fd);

void search_file(int fd);

#endif //FFS_FUNCTIONS_H
