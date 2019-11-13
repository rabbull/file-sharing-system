//
// Created by karl on 2019/10/27.
//

#ifndef FFS_LOCAL_H
#define FFS_LOCAL_H

struct local_main_args {
    _b* running;
    pthread_t* thread_id;
    _s sock_file_path;
};

void* local_main(void* _args);

#endif //FFS_LOCAL_H
