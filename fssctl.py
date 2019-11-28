import os
import sys
import json
import argparse as ap
import socket

from daemon_config import DaemonConfig


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

    args = argparser.parse_args()
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[1])
        sys.argv.remove(sys.argv[1])

    filename = args.filename
    timeout = args.timeout

    local_socket = socket.socket(socket.AF_UNIX, socket.SOCK_SEQPACKET)
    socket_path = 'test/communicator.socket'
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


if __name__ == '__main__':
    fssctl_main()
