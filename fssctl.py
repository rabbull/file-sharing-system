#!/usr/bin/python3
import os
import shutil
import sys
import json
import argparse as ap
import socket

from download import FileClient


def get_local_socket():
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
    return local_socket


def fssctl_main():
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-c', '--config', action='store_true')
    group.add_argument('-s', '--search', action='store_true')

    args = parser.parse_args(sys.argv[1:2])
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[:2])
        sys.argv.remove(sys.argv[1])
    if args.config:
        config_main()
    elif args.search:
        search_main()
    else:
        parser.print_usage()
        exit(-1)


def config_main():
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-n', '--neighbor', action='store_true')
    group.add_argument('-r', '--repository', action='store_true')

    args = parser.parse_args(sys.argv[1:2])
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[:2])
        sys.argv.remove(sys.argv[1])

    if args.neighbor:
        neighbor_main()
    elif args.repository:
        repository_main()
    else:
        exit(-1)


def neighbor_main():
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true')
    group.add_argument('-a', '--add', metavar='ADDRESS')
    group.add_argument('-r', '--remove', metavar='ADDRESS')

    args = parser.parse_args(sys.argv[1:2])
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[:2])
        sys.argv.remove(sys.argv[1])

    command = ['$Neighbor']
    if args.list:
        command.append('List')
    elif args.add:
        command.append('Add')
        try:
            _, _ = args.add.split(':')
        except Exception:
            raise SyntaxError()
        command.append(args.add)
    elif args.remove:
        raise NotImplementedError()

    local_socket = get_local_socket()
    local_socket.send(' '.join(command).encode())
    response = local_socket.recv(1024)
    print(response)


def repository_main():
    parser = ap.ArgumentParser()
    group = parser.add_mutually_exclusive_group()
    group.add_argument('-l', '--list', action='store_true')
    group.add_argument('-a', '--add', metavar='PATH')
    group.add_argument('-r', '--remove', metavar='BASENAME')

    args = parser.parse_args(sys.argv[1:2])
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[:2])
        sys.argv.remove(sys.argv[1])

    command = ['$Repository']
    if args.list:
        command.append('List')
    elif args.add:
        command.append('Add')
        path = os.path.abspath(args.add)
        command.append(path)
    elif args.remove:
        raise NotImplementedError()
        # command.append('Remove')
        # command.append(args.remove)

    local_socket = get_local_socket()
    local_socket.send(' '.join(command).encode())
    response = local_socket.recv(1024).decode()
    print(response)


def search_main():
    parser = ap.ArgumentParser()
    parser.add_argument('filename', metavar='FILENAME')
    parser.add_argument('-t', '--timeout', metavar='SEC', type=float, default=3.0)
    parser.add_argument('-p', '--save-path', metavar='PATH', type=str, default='.')
    parser.add_argument('-y', '--yes', action='store_true')

    args = parser.parse_args()
    if len(sys.argv) > 1:
        sys.argv[0] = ' '.join(sys.argv[1])
        sys.argv.remove(sys.argv[1])

    filename = args.filename
    timeout = args.timeout
    default_savepath = args.save_path
    always_yes = args.yes

    local_socket = get_local_socket()
    local_socket.send(f'$Search {filename} {timeout}'.encode('utf-8'))
    local_socket.settimeout(timeout + 1)
    try:
        result_buffer = local_socket.recv(1024)
    except socket.timeout:
        print('search timeout. daemon can be daed.')
        return 0

    if result_buffer == b'timeout':
        print('no result found before timeout.')
        return 0

    result = json.loads(result_buffer)
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
            return 0
    else:
        remote_address = result['address']
        savepath = default_savepath
    savepath = os.path.abspath(savepath)
    print(f'downloading from {remote_address} to \'{savepath}\'..')
    client = FileClient(host_ip=remote_address[0], host_port=remote_address[1], save_path=savepath)
    client.run()


if __name__ == '__main__':
    fssctl_main()
