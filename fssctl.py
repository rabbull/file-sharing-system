#!/usr/bin/python3
import os
import shutil
import sys
import json
import argparse as ap
import socket


def fssctl_main():
    command_parser = ap.ArgumentParser()
    group = command_parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--config', action='store_true')
    group.add_argument('-s', '--search', action='store_true')

    args = command_parser.parse_args(sys.argv[1:2])
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[:2])
        sys.argv.remove(sys.argv[1])
    if args.config:
        config_main()
    elif args.search:
        search_main()
    else:
        command_parser.print_usage()
        exit(-1)


def config_main():
    raise NotImplementedError()


def search_main():
    argparser = ap.ArgumentParser()
    argparser.add_argument('filename', metavar='FILENAME')
    argparser.add_argument('-t', '--timeout', metavar='SEC', type=float, default=3.0)
    argparser.add_argument('-p', '--save-path', metavar='PATH', type=str, default='.')
    argparser.add_argument('-y', '--yes', action='store_true')

    args = argparser.parse_args()
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[1])
        sys.argv.remove(sys.argv[1])

    filename = args.filename
    timeout = args.timeout
    default_savepath = args.save_path
    always_yes = args.yes

    local_socket = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    socket_path = '/tmp/fss.socket'
    try:
        local_socket.connect(socket_path)
    except FileNotFoundError:
        print(f'Daemon socket file not found at {socket_path}, check if daemon is running.')
        exit(-1)
    except ConnectionRefusedError:
        print(f'Connection to socket refused, check if daemon is running.')
        exit(-1)

    local_socket.send(f'$Search {filename} {timeout}'.encode('utf-8'))

    local_socket.settimeout(timeout + 1)
    try:
        result_buffer = local_socket.recv(1024)
    except socket.timeout:
        print('search timeout. daemon can be daed.')
        exit(0)

    print(result_buffer)
    if result_buffer == b'timeout':
        print('no result found before timeout.')
        exit(0)

    result = json.loads(result_buffer[4:])
    if not always_yes:
        remote_address = result['address']
        print(f'found at {remote_address[0]}:{remote_address[1]}')
        download = input('download? [y/N]: ')
        if download == 'y':
            savepath = input(f'save path [{default_savepath}]: ')
            if savepath == '':
                savepath = default_savepath
        else:
            print('aborted.')
            exit(0)
    else:
        savepath = default_savepath
    savepath = os.path.abspath(savepath)
    print(f'downloading to \'{savepath}\'..')



if __name__ == '__main__':
    fssctl_main()
